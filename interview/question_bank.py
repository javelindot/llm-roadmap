"""单题 Markdown 的公共读取规则，供导入和答案同步共用。"""
import re
from pathlib import Path

import yaml

FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---(?:\n|$)(.*)\Z", re.DOTALL)
ANSWER_HEADING_RE = re.compile(r"^##\s*答案\s*$", re.MULTILINE)
PENDING_ANSWERS = {"", "（待补充）", "(待补充)"}


def read_question(path: Path):
    """读取元数据和完整答案；格式错误时中止，避免静默覆盖内容。"""
    text = path.read_text(encoding="utf-8-sig")
    match = FRONTMATTER_RE.match(text)
    if not match:
        raise ValueError(f"{path.name}: 缺少有效 frontmatter")
    try:
        meta = yaml.safe_load(match.group(1))
    except yaml.YAMLError as exc:
        raise ValueError(f"{path.name}: frontmatter 解析失败: {exc}") from exc
    if not isinstance(meta, dict):
        raise ValueError(f"{path.name}: frontmatter 必须是对象")
    qid = meta.get("id", "")
    if not isinstance(qid, str) or not re.fullmatch(r"q-[1-9]\d*", qid):
        raise ValueError(f"{path.name}: 无效题号 {qid!r}")
    if path.stem != qid:
        raise ValueError(f"{path.name}: 文件名与题号 {qid} 不一致")
    if not isinstance(meta.get("title"), str) or not meta["title"].strip():
        raise ValueError(f"{path.name}: 缺少题目标题")
    if type(meta.get("hasAnswer")) is not bool:
        raise ValueError(f"{path.name}: hasAnswer 必须是 true 或 false")

    # 答案内允许二级标题和代码围栏，不能在后续标题处截断正文。
    answer_heading = ANSWER_HEADING_RE.search(match.group(2))
    if not answer_heading:
        raise ValueError(f"{path.name}: 缺少 ## 答案 标题")
    answer = match.group(2)[answer_heading.end():].strip()
    if answer in PENDING_ANSWERS:
        meta["hasAnswer"] = False
        answer = ""
    return meta, answer


def load_question_bank(directory: Path):
    """先校验所有单题，再返回按数值题号排列的题库，保证写入前发现错误。"""
    records = {}
    for path in sorted(directory.glob("q-*.md")):
        meta, answer = read_question(path)
        qid = meta["id"]
        if qid in records:
            raise ValueError(f"重复题号: {qid}")
        records[qid] = (meta, answer)
    return dict(sorted(records.items(), key=lambda item: int(item[0][2:])))
