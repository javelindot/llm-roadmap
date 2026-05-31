---
group: 5. Skills
id: skills-vs-tools
title: Skills · vs Tool / MCP
toc: Skills · 对比
---

Prompt / Function Call / MCP / Skills 四者**经常被混淆**。这一章把每个的本质和适用场景讲透。

## 一张图理解四者层级

```
┌────────────────────────────────────────────────┐
│                                                │
│            ┌─────────────────────┐             │
│            │      Skills         │ ← 任务级能力 │
│            │  (prompt + tools    │   按需加载   │
│            │  + templates +      │   完整方法论 │
│            │  examples)          │             │
│            └──────────┬──────────┘             │
│                       │                        │
│              使用     │     使用                │
│           ┌───────────┴────────────┐           │
│           ↓                        ↓           │
│  ┌──────────────┐         ┌──────────────┐    │
│  │ Function Call│         │     MCP      │    │
│  │              │         │              │    │
│  │ 程序内函数    │         │  跨程序协议   │    │
│  │ 调用         │         │  标准化       │    │
│  └──────┬───────┘         └──────┬───────┘    │
│         │                        │             │
│         └──────────┬─────────────┘             │
│                    ↓                           │
│           ┌──────────────────┐                 │
│           │     Prompt       │ ← 原子级指令    │
│           │   (指令文本)      │                 │
│           └──────────────────┘                 │
│                                                │
└────────────────────────────────────────────────┘
```

## 四者本质区别

| 抽象层 | 是什么 | 解决什么问题 | 何时引入 |
|--------|--------|--------------|----------|
| **Prompt** | 文字指令 | 让模型理解任务 | 2020+（LLM 诞生即有）|
| **Function Call** | 程序内函数调用 | 让模型能调外部 API | 2023.6（GPT 首次推出）|
| **MCP** | 跨程序协议 | 让工具能复用、跨平台 | 2024.11（Anthropic）|
| **Skills** | 任务级能力包 | 让复杂任务方法论可复用 | 2025（Claude）|

## 关键差异维度

### 1. 复用粒度

```
Prompt:     无法复用（每次重写或简单复制）
FC:         单函数复用（同一程序内）
MCP:        函数集复用（跨程序、跨用户）
Skills:     任务方法论复用（一整套 prompt + 工具 + 示例）
```

### 2. 加载方式

```
Prompt:     全程占 context
FC:         tool 定义全程占 context（即使没调用）
MCP:        tool 定义全程占 context
Skills:     按需加载（关键差异！）
```

100 个 Skills 索引可能就 500 token；如果每个都全量加载，可能 50000 token。

### 3. 谁来决策

```
Prompt:    用户决定（写什么用什么）
FC:        模型决定（用哪个 tool）
MCP:       模型决定（用哪个 tool，跨 Server 选）
Skills:    模型决定（先选 Skill，再让 Skill 内部选 tool）
```

### 4. 谁负责实现

```
Prompt:    应用开发者
FC:        应用开发者（写函数 + 注册 schema）
MCP:       Server 作者（任何人）→ Client 即插即用
Skills:    Skill 作者（任何人）→ Agent 加载即用
```

## 何时用什么：决策树

```
你的需求是什么？
│
├─ 单次对话 / 简单生成
│  → Prompt
│
├─ 让模型调某个内部 API
│  ├─ 只在自己应用用 → Function Call
│  └─ 想跨应用共享 → MCP Server
│
├─ 让模型操作某个标准化工具（GitHub / Slack / DB）
│  → 直接用现成的 MCP Server
│
├─ 整套完整任务方法论（含多步骤、多工具、模板、示例）
│  ├─ 一次性 → 直接写大 prompt + FC
│  └─ 复用 → 封装为 Skill
│
└─ 复杂业务流程 + 多 Skill 协作
   → Skills + Agent SDK
```

## 三个 vs 对比

### Skills vs Function Call

| | Skills | FC |
|---|--------|-----|
| 定位 | 任务级 | 函数级 |
| 包含 | 一整套方法论 | 单个函数 |
| 加载 | 按需 | 全程在 context |
| 例子 | "数据分析师" Skill | `query_database()` 函数 |

**关系**：Skills **内部使用** FC（Skill 里可以包含多个 FC）。

### Skills vs MCP

| | Skills | MCP |
|---|--------|-----|
| 本质 | 能力封装 | 通信协议 |
| 关注点 | 「怎么做某事」 | 「怎么标准化对接」 |
| 部署 | 文件/目录形式加载 | 独立进程 |
| 跨厂商 | Claude 生态（暂时）| 通用协议 |

**关系**：Skills **可以使用** MCP Server 提供的工具。Skill 里可以列出"用这个 MCP Server 的某些工具"。

### MCP vs Function Call

| | MCP | FC |
|---|-----|-----|
| 标准化 | 是（行业协议）| 否（各厂商不同）|
| 部署 | 独立进程 | 在应用代码内 |
| 跨用户 | 同一 Server 全网可用 | 每用户/每应用单独写 |
| 性能 | 多一层 IPC | 直接函数调用 |

**关系**：MCP 是 FC 的**标准化包装** —— Server 内部还是用 FC 实现。

## 实例对比：同一需求的 4 种实现

需求：「让 AI 帮我做季度销售报告」

### 方案 A: 纯 Prompt（最简单，最不可扩展）

```python
prompt = """
你是数据分析专家。请基于以下销售数据生成 Q3 报告：
[销售数据 CSV 内容]

要求：
1. 总销售额和环比
2. Top 5 产品
3. 区域分布
4. 趋势预测

输出：Markdown 格式
"""
result = claude(prompt)
```

✅ 简单
❌ 数据要手动塞 prompt，没法处理大文件
❌ 没法生成真实图表
❌ 换个时间段就要重写 prompt

### 方案 B: Prompt + Function Call

```python
tools = [
    {"name": "read_csv", "input_schema": {...}},
    {"name": "compute_stats", "input_schema": {...}},
    {"name": "generate_chart", "input_schema": {...}},
    {"name": "write_pdf", "input_schema": {...}}
]

messages = [{"role":"user", "content":"基于 q3_sales.csv 生成 PDF 报告"}]

# 用循环跑 tool calls
while True:
    resp = client.messages.create(model="...", tools=tools, messages=messages)
    if resp.stop_reason != "tool_use": break
    # 处理 tool_use ...
```

✅ 能处理大数据
✅ 真实生成 PDF
❌ 一整套 tools 每次都占 context
❌ "怎么写好报告"的方法论散落在 prompt 里
❌ 不同团队重复实现

### 方案 C: 用 MCP Server

```json
// Claude Desktop 配置
{
    "mcpServers": {
        "data": {
            "command": "npx",
            "args": ["-y", "@mycompany/sales-mcp-server"]
        }
    }
}
```

用户在 Claude Desktop 里："读 q3_sales.csv 生成报告"

✅ 工具跨用户共享（公司全员可用）
✅ MCP Server 一次部署，所有客户端用
❌ 还是"工具集合"，缺少"完整任务模板"
❌ 用户每次还得手写"怎么生成好报告"

### 方案 D: 封装为 Skill

```
skills/sales_report_generator/
├── SKILL.md                    ← 完整方法论
├── tools/
│   ├── read_csv.py
│   ├── compute_stats.py
│   └── generate_chart.py
├── templates/
│   └── q_report.jinja2          ← 报告模板
└── examples/
    └── good_q3_report.md        ← 优秀案例
```

```markdown
<!-- SKILL.md -->
# Sales Report Generator

## When to use
当用户需要生成销售相关报告时使用。

## Tools available
- read_csv: 读取 CSV 数据
- compute_stats: 计算统计指标
- generate_chart: 生成可视化

## Process
1. 用 read_csv 加载数据
2. 用 compute_stats 计算: 总额、环比、Top 产品、区域分布
3. 用 generate_chart 生成: 趋势图、饼图
4. 套用 templates/q_report.jinja2 生成最终报告
5. 输出 Markdown，结构参考 examples/good_q3_report.md
```

使用：

```python
agent = ClaudeAgent(skills=["sales_report_generator"])
agent.run("基于 q3_sales.csv 生成报告")
# Claude 自动:
# 1. 识别需要 sales_report_generator Skill
# 2. 加载该 Skill 完整内容
# 3. 按 Process 执行
# 4. 输出符合 templates 的报告
```

✅ 方法论可分享（其他团队直接拿来用）
✅ 按需加载（不用时不占 context）
✅ 一致性高（template 保证产出风格统一）
✅ 易维护（要改报告格式只改 template）

**这就是 Skills 的核心价值**。

## 何时升级到 Skills

按以下信号判断从 FC/MCP 升级到 Skills：

✅ **该用 Skills**:
- 同一任务被反复实现（说明有方法论可沉淀）
- prompt 越来越长（按需加载省 token）
- 团队希望分享"做某事的最佳实践"
- 产品形态是 Agent / 助手

❌ **暂时不用**:
- 单一简单工具（FC 够了）
- 一次性脚本
- 不用 Claude 生态

## Skills 的"灰色地带"

### Skills + MCP

Skills 内部可以调 MCP Server。例如：

```markdown
<!-- SKILL.md -->
## Tools available
- github (from MCP server `@modelcontextprotocol/server-github`)
- slack (from MCP server `@modelcontextprotocol/server-slack`)
```

这样 Skill 不需要自己实现 GitHub 集成，复用社区 MCP Server。

### Skills + 多个 LLM

Skills 内部可以指定不同步骤用不同模型：

```markdown
## Process
1. 用 Haiku（便宜）做意图分类
2. 用 Sonnet 做主要分析
3. 用 Sonnet Thinking 做关键决策
```

这种"模型路由"是 Skills 高级用法。

## 总结：四者的协同

```
真实生产架构:

Skills           ←  封装业务方法论
   ↓
Function Call    ←  本地小工具
+ MCP Servers    ←  跨平台标准工具
   ↓
Prompt           ←  指令文本
   ↓
LLM API（Claude / GPT / DeepSeek）
```

不是"二选一"，而是**分层使用**。

## 学习路径建议

按这个顺序学习，每一层为下一层打基础：

```
Week 1: Prompt 工程（100-107）
   ↓
Week 2: Function Call（200-204）
   ↓
Week 3: MCP（400-403）
   ↓
Week 4: Skills（500-503）← 你在这里
   ↓
Week 5+: Agent（600-604）
```

每往上一层，**抽象度变高、复用粒度变大**。

下一节：[编写 Skill](#skills-build) —— 动手做一个真实可用的 Skill。
