"""用标准库演示能力路由和持久化动作账本，不调用模型或外部业务。

本模块只验证应用控制逻辑，全部型号、地区与成本均为虚构配置。
真实模型能力应经过接口验收，不能从此处的能力名称推断。
动作账本也不是完整生产运行时：它不实现用户鉴权、任务租约或队列。
外部写服务必须支持同一操作键的幂等执行和可查询回执。
业务动作已经发出而结果未知时，先核对实际结果，不能盲目重试。
所有身份与审批输入应来自可信服务，不能直接使用模型提供的值。
演示把模型选择和动作执行拆开：切换模型不会产生新的业务动作。
账本保存的成功状态只表示一个动作完成，不代表整个客户问题解决。
执行者拿到领取权后应使用已保存的参数，不再让模型修改请求。
SQLite 文件需要应用自身的访问控制，表中租户字段不是鉴权机制。
数据库事务只保护本地记录，不能回滚另一服务已经发生的写入。
"""

import hashlib
import json
import sqlite3
from dataclasses import dataclass
from pathlib import Path
from tempfile import TemporaryDirectory


@dataclass(frozen=True)
class ModelProfile:
    """保存已经验收的模型部署快照，不把供应商品牌当成能力证明。

    name 是应用内唯一部署名称，应关联精确模型与接口版本。
    capabilities 用于必要能力的集合判断，例如文本、工具和图片。
    region 是经过确认的数据处理区域，不能由输入消息自行指定。
    cost_units 是整个请求的非负估计成本，不是供应商实际价格。
    本例不估计 token，也不评测质量，调用方应先筛选质量合格部署。
    同一供应商的两个区域应作为不同部署记录，以便独立判断健康。
    能力验收应覆盖模型、API 和 SDK 组合，而不是仅测试返回文本。
    请求成本超过估计时，上层仍需要总费用限制和停止条件。
    """

    name: str
    capabilities: frozenset[str]
    region: str
    cost_units: int

    def __post_init__(self):
        """在配置边界拒绝空身份、错误成本与不可变能力清单之外的输入。

        布尔值在 Python 中也是整数，但不应作为预算或费用。
        拒绝可变集合，避免一次执行中途出现配置内容被修改的情况。
        对真实能力的核验仍属于部署流程，此处只检查配置类型。
        frozen 约束字段赋值，frozenset 同时避免集合内容被原地修改。
        零费用允许用于模拟部署，但不暗示真实服务免费。
        """
        if not self.name or not self.region:
            raise ValueError("model identity and region required")
        if not isinstance(self.capabilities, frozenset):
            raise ValueError("immutable capabilities required")
        if type(self.cost_units) is not int or self.cost_units < 0:
            raise ValueError("nonnegative integer cost required")


def select_model(profiles, required, allowed_regions, budget_units, healthy_names):
    """先检查能力、区域、预算和健康，再选择估计成本最低的合格部署。

    required 和 allowed_regions 来自任务契约及可信数据策略。
    healthy_names 是调用方提供的健康快照，应在真实系统中设置有效期。
    本例不把模型置信度当成质量评分，也不尝试放宽必要能力。
    同名部署会导致故障或能力记录混淆，因此明确拒绝重复名称。
    没有合格候选时抛出错误，调用方只能选择合法替代流程。
    一次过滤使用同一能力快照，不能在选择中途更换健康结果。
    健康仅说明当前服务可调用，不证明它能满足任务质量要求。
    预算覆盖整个候选请求，后续工具与重试费用由上层单独计入。
    """
    if type(budget_units) is not int or budget_units < 0:
        raise ValueError("nonnegative integer budget required")
    profiles = list(profiles)
    if len({profile.name for profile in profiles}) != len(profiles):
        raise ValueError("duplicate deployment name")
    # 将允许集合固定一次，避免生成器被候选遍历消耗后出现不同结果。
    required = frozenset(required)
    allowed_regions = frozenset(allowed_regions)
    healthy_names = frozenset(healthy_names)
    # 过滤条件是同时满足，健康的纯文本模型不能替代工具模型。
    candidates = [profile for profile in profiles
                  if required <= profile.capabilities
                  and profile.region in allowed_regions
                  and profile.name in healthy_names
                  and profile.cost_units <= budget_units]
    if not candidates:
        raise ValueError("no compatible model")
    # 用名称打破费用相同时的平局，使本地实验的选择可复现。
    return min(candidates, key=lambda profile: (profile.cost_units, profile.name))


def action_fingerprint(tool, arguments):
    """对确定工具与参数生成稳定指纹，用于比较同一动作的意图。

    参数只接受 JSON 对象；键顺序不影响指纹，数值变化则影响指纹。
    禁止非标准 JSON 的 NaN 与 Infinity，防止跨系统解释不一致。
    字符串编码采用 UTF-8，指纹不能作为身份认证或数字签名。
    生产还应在指纹中绑定必要的策略版本和业务资源版本。
    相同指纹只表示序列化意图一致，不说明审批人真的批准过它。
    本地排序不是跨语言的规范化 JSON 标准，跨服务需约定编码。
    若数字或默认字段在业务上等价，应先经 schema 校验与归一化。
    """
    if not isinstance(tool, str) or not tool or not isinstance(arguments, dict):
        raise ValueError("tool and argument object required")
    encoded = json.dumps({"tool": tool, "arguments": arguments},
                         sort_keys=True, ensure_ascii=False, allow_nan=False,
                         separators=(",", ":"))
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()


class ActionLedger:
    """把业务动作与模型对话分开持久化，保留参数、审批和回执。

    主键由可信租户、业务问题和动作标识组成，不能使用新 Run 去重。
    pending 只有在审批有效时可以原子领取为 executing。
    executing 超时后可标记 unknown，该状态不能重新领取。
    真实外部结果经业务服务独立核验后，以回执登记为 succeeded。
    多进程原子领取不等于跨服务恰好执行一次，仍需外部幂等。
    action_id 在同一 Case 内稳定，不能在每次网络重试时重新生成。
    参数变化需要新动作和新批准，原动作的事实仍需保留。
    本例没有确定失败或取消状态，不能据此实现完整工单生命周期。
    结果未知的记录应交给对账流程，执行 worker 不自行清空它。
    真实系统还需记录事件时间与执行者，以判断故障和移交责任。
    """

    def __init__(self, path):
        """打开 SQLite 持久化账本，独立连接可竞争同一动作。

        五秒锁等待仅用于本地示例，不是生产性能或超时建议。
        表内限制可用状态，避免未经约定的状态被直接写入。
        路径来自应用配置，不能允许模型选择任意数据库文件。
        连接绑定当前线程，竞争测试由各线程创建自己的连接。
        with connection 提交或回滚事务，但不会自动关闭连接。
        主键约束在数据库中实施，独立进程不依赖共享内存去重。
        """
        self.connection = sqlite3.connect(path, timeout=5)
        self.connection.row_factory = sqlite3.Row
        with self.connection:
            # 参数、批准和回执放在同一动作行中，便于检查状态前提。
            # CHECK 只限制状态名称，转换规则还要由以下条件更新实施。
            self.connection.execute(
                "CREATE TABLE IF NOT EXISTS actions ("
                "tenant TEXT NOT NULL, case_id TEXT NOT NULL, action_id TEXT NOT NULL, "
                "tool TEXT NOT NULL, arguments TEXT NOT NULL, fingerprint TEXT NOT NULL, "
                "state TEXT NOT NULL CHECK(state IN ('pending','executing','unknown','succeeded')), "
                "approval TEXT, expires_at INTEGER, receipt TEXT, "
                "PRIMARY KEY (tenant, case_id, action_id))")

    def close(self):
        """释放连接；已提交记录可由下一进程重新打开。

        关闭连接不会撤销已发生的业务动作，也不代表 Case 已完成。
        调用方应在异常路径中同样释放连接，本例使用 finally。
        执行者重启后使用相同数据库路径，才能读回既有动作。
        生产文件的备份、加密和保留期限属于部署管理职责。
        """
        self.connection.close()

    @staticmethod
    def _key(tenant, case_id, action_id):
        """检查可信动作身份，形成所有读取与变更共享的作用域。

        本地示例仅检查非空字符串，不验证真实用户是否拥有该身份。
        业务服务必须在调用账本前校验身份和 Case 的访问权限。
        所有 SQL 都使用参数化查询，身份不会被拼进 SQL 文本。
        同名 action_id 在不同 Case 中是不同动作，不能混用回执。
        本方法不将空字符串补成默认租户，避免扩大访问作用域。
        """
        key = (tenant, case_id, action_id)
        if any(not isinstance(value, str) or not value for value in key):
            raise ValueError("scoped action identity required")
        return key

    def get(self, tenant, case_id, action_id):
        """读取指定作用域的动作，返回独立的参数对象和真实账本状态。

        不存在记录时明确报错，不能从另一个租户寻找同名动作。
        返回参数从持久化文本重新解析，修改返回值不会改变原动作。
        查询回执前，调用方仍应核对外部服务与动作之间的对应关系。
        返回值是一次状态快照，不能作为稍后执行时的原子判断。
        要取得执行权应调用 claim，而不是先 get 再直接写业务。
        """
        key = self._key(tenant, case_id, action_id)
        row = self.connection.execute(
            "SELECT * FROM actions WHERE tenant=? AND case_id=? AND action_id=?", key
        ).fetchone()
        if row is None:
            raise KeyError(key)
        result = dict(row)
        result["arguments"] = json.loads(result["arguments"])
        return result

    def prepare(self, tenant, case_id, action_id, tool, arguments):
        """创建不可变业务动作，相同意图可重放，参数变化必须使用新动作。

        先计算稳定指纹，再通过唯一主键实现幂等准备。
        同一键已有记录时保留其审批、执行状态和回执，不重置进度。
        输入对象随后被修改也不会影响已保存的参数快照。
        跨租户相同动作名称有各自作用域，不会共享审批或结果。
        幂等准备允许重复规划，但不能隐含地重复执行外部工具。
        相同参数已有 unknown 状态时，应继续对账而不是重置为 pending。
        调用方必须先完成工具 schema 与业务语义校验，再保存动作。
        """
        key = self._key(tenant, case_id, action_id)
        fingerprint = action_fingerprint(tool, arguments)
        encoded = json.dumps(arguments, sort_keys=True, ensure_ascii=False, allow_nan=False)
        with self.connection:
            # INSERT 与指纹核对属于同一事务，冲突时不留下另一组参数。
            # 已存在的同键记录由主键保留；随后明确核对其不可变意图。
            self.connection.execute(
                "INSERT OR IGNORE INTO actions "
                "(tenant,case_id,action_id,tool,arguments,fingerprint,state) "
                "VALUES (?,?,?,?,?,?,'pending')", (*key, tool, encoded, fingerprint))
            # 既有动作不能因重新规划而变成另一个工具或另一组参数。
            if self.get(*key)["fingerprint"] != fingerprint:
                raise ValueError("action intent changed")
        return fingerprint

    def approve(self, tenant, case_id, action_id, fingerprint, expires_at):
        """保存对确定参数的批准，在领取时检查批准有效期。

        此接口假定调用方已经核验审批人的身份、权限和业务规则。
        指纹不匹配或动作已经领取时拒绝覆盖，避免批准另一个意图。
        expires_at 为整数时间点，使用方与 claim 必须使用同一时钟。
        完整生产批准还需审批人、策略版本和审计，不能只存一段文字。
        approval 列存的是本地意图绑定标记，不是可独立验证的授权令牌。
        当前示例允许待执行动作续期，但调用方每次仍要核验审批来源。
        已领取的动作不得通过更新审批回到可执行状态。
        """
        key = self._key(tenant, case_id, action_id)
        if type(expires_at) is not int or expires_at < 0:
            raise ValueError("valid approval expiry required")
        with self.connection:
            # 将状态与指纹作为 UPDATE 前提，避免先读后写之间的竞争。
            # 没有匹配行时统一拒绝，不泄露其他作用域的动作是否存在。
            cursor = self.connection.execute(
                "UPDATE actions SET approval=?, expires_at=? "
                "WHERE tenant=? AND case_id=? AND action_id=? "
                "AND state='pending' AND fingerprint=?",
                (fingerprint, expires_at, *key, fingerprint))
            if cursor.rowcount != 1:
                raise ValueError("approval does not match pending action")

    def claim(self, tenant, case_id, action_id, now):
        """以单条 SQL 原子领取有效批准的动作，仅一个竞争者成功。

        now 来自可信应用时钟，不应接受用户或模型提供的时间。
        批准时间恰好等于当前时间时视为过期，不能再执行。
        执行中、结果未知和已完成动作均不能重新领取。
        取得执行权后崩溃需要恢复与对账，本例没有自动任务租约。
        返回 False 同时覆盖未批准、已过期或已被领取，调用方可再查询。
        一旦领取成功，外部提交必须使用同一动作键实现服务端去重。
        外部提交前再次检查资源状态，批准不能锁定远程业务对象。
        """
        key = self._key(tenant, case_id, action_id)
        if type(now) is not int or now < 0:
            raise ValueError("valid current time required")
        with self.connection:
            # 领取和过期检查在同一数据库写操作里完成。
            # 两个独立连接竞争时，只有看到 pending 的更新者可以成功。
            cursor = self.connection.execute(
                "UPDATE actions SET state='executing' "
                "WHERE tenant=? AND case_id=? AND action_id=? AND state='pending' "
                "AND approval=fingerprint AND expires_at>?", (*key, now))
        return cursor.rowcount == 1

    def mark_unknown(self, tenant, case_id, action_id):
        """将已发出但无确定结果的动作标记为未知，要求后续核对。

        超时并非业务拒绝，也不证明外部写操作尚未发生。
        只允许从执行中转入未知，避免改变已经确认的成功状态。
        相同操作键应传给外部回执查询服务，不能生成新键重发。
        执行者在提交前崩溃也可能没有回执；缺失回执本身不证明失败。
        应结合外部服务的查询与幂等契约决定后续动作。
        本方法不判断超时时长；何时进入对账由可信运行时决定。
        """
        key = self._key(tenant, case_id, action_id)
        with self.connection:
            # 保留原参数、审批与动作键，只改变确定性不足的执行状态。
            # 状态条件阻止重复超时事件覆盖已经核实的成功事实。
            cursor = self.connection.execute(
                "UPDATE actions SET state='unknown' "
                "WHERE tenant=? AND case_id=? AND action_id=? AND state='executing'", key)
            if cursor.rowcount != 1:
                raise ValueError("action is not executing")

    def settle(self, tenant, case_id, action_id, receipt):
        """登记业务服务核验过的成功回执，重复登记同一回执保持幂等。

        本方法不能判断回执真假，调用方必须核对来源、签名与动作归属。
        executing 或 unknown 可以登记；尚未执行的动作不能凭文本变成功。
        同一动作出现不同成功回执时明确报冲突，应走业务对账。
        这是动作事实，不会自动关闭 Case 或恢复已取消的执行。
        迟到回执可以登记事实，是否继续流程由当前 Case 所有者决定。
        回执应能定位外部对象及操作键，不能使用模型生成的成功描述。
        本示例只保存文本标识，完整响应与验证证据应在受控存储中保留。
        """
        key = self._key(tenant, case_id, action_id)
        if not isinstance(receipt, str) or not receipt:
            raise ValueError("verified receipt required")
        with self.connection:
            # 允许从执行中或未知状态收敛，覆盖响应丢失后的独立核验。
            # 同键不同回执不能静默覆盖，否则可能隐藏重复外部写入。
            cursor = self.connection.execute(
                "UPDATE actions SET state='succeeded',receipt=? "
                "WHERE tenant=? AND case_id=? AND action_id=? "
                "AND state IN ('executing','unknown')", (receipt, *key))
            if cursor.rowcount != 1:
                row = self.get(*key)
                if row["state"] != "succeeded" or row["receipt"] != receipt:
                    raise ValueError("receipt conflicts with action state")


def run_demo():
    """演示合法模型选择和写结果未知后的回执核对，不执行真实写入。

    临时数据库只保存模拟数据，函数结束后由临时目录清理。
    demo-receipt 是虚构回执，不能据此证明任何外部业务成功。
    输出展示 unknown 与 succeeded 的区别，不假装网络超时就是失败。
        先选择满足工具能力的部署，再创建与模型调用 ID 无关的动作。
        人工批准与当前时间使用固定值，使正常和过期边界可重复演示。
        对账仅模拟“查询找到了原回执”，没有再次提交创建请求。
    """
    profiles = [ModelProfile("demo-text", frozenset({"text"}), "local", 1),
                ModelProfile("demo-tools", frozenset({"text", "tools"}), "local", 3)]
    model = select_model(profiles, {"tools"}, {"local"}, 5, {p.name for p in profiles})
    print("selected_model:", model.name)
    with TemporaryDirectory() as directory:
        ledger = ActionLedger(Path(directory) / "actions.sqlite")
        try:
            key = ("demo-tenant", "demo-case", "demo-action")
            fingerprint = ledger.prepare(*key, "create_ticket", {"order_id": "demo-order"})
            ledger.approve(*key, fingerprint, expires_at=200)
            if not ledger.claim(*key, now=100):
                raise RuntimeError("demo action could not be claimed")
            ledger.mark_unknown(*key)
            print("after_timeout:", ledger.get(*key)["state"])
            # 模拟独立业务查询已经找到既有回执，随后登记实际动作事实。
            ledger.settle(*key, "demo-receipt")
            print("after_reconciliation:", ledger.get(*key)["state"])
        finally:
            ledger.close()


if __name__ == "__main__":
    run_demo()
