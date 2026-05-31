---
group: 5. Skills
id: skills-overview
title: Skills · 概览
toc: Skills · 概览
---

**Skills**（技能）= Claude 4.5 引入的「**按需加载的领域能力包**」。介于 **Prompt 工程**（最轻量）和 **Tool / MCP**（最重型）之间，填补了一个长期空白。

## 一个简单认知：Skills = 「**配方书**」

```
Prompt Engineering   →  一道道单独的菜
Function Call / Tool →  厨房工具（刀、锅）
MCP                  →  接外卖（外部能力）
Skills               →  整本菜谱书（带配料 + 步骤 + 工具调用 + 输出格式）
```

Skill 不是一个工具，而是**完成某类任务的完整能力包**，包含：
- 该任务的系统 prompt
- 该任务用到的工具列表
- 该任务的中间步骤模板
- 该任务的输出格式约定
- （可选）该任务的预置资源（如示例、参考数据）

## 为什么需要 Skills

### 痛点 1：Prompt + Tool 组合太分散

做一个「PDF 报告生成」功能，传统做法：

```python
# 系统 prompt
SYSTEM_PROMPT = "你是报告生成助手..."

# 工具 1: 读 PDF
def read_pdf(path): ...
# 工具 2: 抽取关键数据
def extract_data(text): ...
# 工具 3: 生成图表
def create_chart(data): ...
# 工具 4: 输出 PDF
def write_pdf(content): ...

# 业务代码
def generate_report(input_pdf):
    # 一堆胶水代码组装 prompt + tools
    ...
```

**问题**：换个场景（如「数据分析报告」），整套又要重写。

### 痛点 2：复用难

公司有 10 个团队都在做"基于客户数据生成洞察报告"，每个团队都从零写一套 prompt + tool 组合。

### 痛点 3：Prompt 太长

复杂任务的 prompt 动辄上千行。塞在主 prompt 里：
- 每次调用都付全文 token 费
- 主 prompt 越长，模型越容易"跑偏"

### Skills 的解决方案

把**完整能力**封装成 Skill，按需加载：

```python
# 不用每次写一长串 prompt 和工具
agent = ClaudeAgent(
    skills=["pdf_report_generator", "data_analyst", "customer_insight"]
)
result = agent.run("基于上月销售数据生成季度报告")
# Claude 自动判断: 这需要 pdf_report_generator + data_analyst
# 按需加载这两个 Skill，复用其 prompt 和工具
```

## Skills 的核心特性

### 1. 按需加载（Lazy Loading）

Skill 只在**模型判断需要时**才加载到 context：

```
对话开始: 只有基础 system prompt + Skill 索引（每个 Skill 几句话描述）
   ↓
用户问"帮我生成销售报告" → 模型决定加载 pdf_report_generator
   ↓
该 Skill 的完整 prompt + 工具 + 模板被注入 context
   ↓
执行任务
   ↓
任务完成，Skill 退出 context（节省后续 token）
```

**省 token**：100 个 Skills 的索引可能只占几百 token，而每个 Skill 单独完整可能上千。

### 2. 自包含（Self-Contained）

一个 Skill 包含所有它需要的东西：

```
skills/pdf_report_generator/
├── SKILL.md             ← Skill 主定义（prompt + 元信息）
├── tools/               ← 该 Skill 用到的工具
│   ├── extract_pdf.py
│   └── render_chart.py
├── templates/           ← 输出模板
│   └── report.jinja2
├── examples/            ← Few-shot 示例
│   ├── good_report.md
│   └── bad_report.md
└── resources/           ← 静态资源
    └── style_guide.md
```

可移动、可分享、可版本化。

### 3. 可组合（Composable）

多个 Skills 可以组合：

```python
agent = ClaudeAgent(skills=[
    "data_analyst",      # 提取数据
    "chart_generator",   # 画图
    "report_writer",     # 写文字
    "pdf_exporter"       # 导出 PDF
])
# 模型自主决定调用顺序和组合方式
```

### 4. 模型自主选择

Claude 自动决定**用不用、用哪些 Skill**：

```
用户: "帮我看看 sales.csv"
   ↓
Claude 扫描可用 Skills:
  - data_analyst: 处理 CSV ✓
  - pdf_generator: 不需要
  - email_sender: 不需要
   ↓
加载 data_analyst Skill → 分析数据 → 回答
```

## Skills vs Prompt / Tool / MCP

| 维度 | Prompt | Function Call | MCP | **Skills** |
|------|--------|--------------|-----|----------|
| **粒度** | 一句话指令 | 单个函数 | 服务集合 | 完整能力包 |
| **包含** | 文字 | 函数定义 | 多个 tools | prompt + tools + templates + 示例 |
| **加载方式** | 全程在 context | 全程在 context | 全程在 context | **按需加载** |
| **复用粒度** | 难复用 | 单工具复用 | Server 级复用 | **任务级复用** |
| **决策权** | 用户写 | 模型选工具 | 模型选工具 | **模型选 Skill 再选工具** |
| **典型用途** | 单次任务 | 调 API | 集成生态 | 复杂业务能力 |

**总结**：
- **Prompt**：原子级，最轻量
- **Function Call**：函数级，调能力
- **MCP**：协议级，分享能力
- **Skills**：任务级，封装方法论

## 真实应用场景

### 场景 1：客服全栈助手

```python
skills = [
    "intent_classifier",     # 意图分类
    "knowledge_base_qa",    # 基于知识库回答
    "refund_processor",     # 退款流程
    "escalate_to_human"     # 转人工
]
agent = ClaudeAgent(skills=skills)
# 一句话搞定所有客服场景
```

### 场景 2：数据分析师

```python
skills = [
    "csv_analyzer",          # CSV 数据处理
    "sql_query_writer",      # 写 SQL
    "chart_generator",       # 生成可视化
    "insight_extractor",     # 提取业务洞察
    "report_writer"          # 生成报告
]
agent = ClaudeAgent(skills=skills)
agent.run("分析这份用户行为数据，找出留存关键因素")
```

### 场景 3：开发者助手

```python
skills = [
    "code_reviewer",         # Code review
    "bug_diagnosis",         # 故障诊断
    "test_generator",        # 生成测试
    "refactor_assistant"     # 重构建议
]
```

## Skills 在 Claude 生态的位置

```
┌─────────────────────────────────────────┐
│       Claude Agent SDK / Console        │
│  ┌────────────────────────────────────┐ │
│  │       Skills (高层能力包)            │ │
│  │   ┌─────┬──────┬──────────┐        │ │
│  │   │     │      │          │        │ │
│  │   ↓     ↓      ↓          ↓        │ │
│  │  使用   使用   使用       使用      │ │
│  └────────────────────────────────────┘ │
│        │              │                 │
│        ↓              ↓                 │
│  ┌──────────┐  ┌─────────────┐          │
│  │ Tool/FC  │  │ MCP Servers │          │
│  └──────────┘  └─────────────┘          │
│        │              │                 │
│        ↓              ↓                 │
│      Python       NPM / Docker          │
│      自定义        全网生态              │
└─────────────────────────────────────────┘
```

Skills 是**最高层抽象**，下游可以用 Tool / FC / MCP 任意组合实现。

## Skills 与 Claude Agent SDK

Anthropic 2025 发布的 **Claude Agent SDK** 把 Skills 作为一等公民：

```python
from claude_agent_sdk import Agent, Skill

agent = Agent(
    model="claude-sonnet-4-5",
    skills=[Skill.from_directory("./skills/data_analyst")]
)
agent.run("分析这份销售数据")
```

如果你用 Claude 做生产级应用，**Skills 应该是默认架构**。

## Skills 不适合什么场景

❌ **简单一次性任务**：直接写 prompt 更快
❌ **纯对话场景**：不需要复杂能力组合
❌ **不用 Claude 的项目**：Skills 目前是 Claude 生态特有

## 入门路径

| 章节 | 内容 |
|------|------|
| [Skills vs Tool / MCP](#skills-vs-tools) | 三者差异 & 何时用 |
| [编写 Skill](#skills-build) | 第一个 Skill 实战 |
| [部署与最佳实践](#skills-deploy) | 生产级 Skill |

## 业界资源

- [Anthropic Skills 官方文档](https://docs.claude.com/skills) (2025)
- [Claude Agent SDK GitHub](https://github.com/anthropics/claude-agent-sdk)
- [Awesome Claude Skills](https://github.com/anthropics/awesome-skills) ← 官方示例库

下一节：[Skills vs Tools](#skills-vs-tools) —— 彻底搞清楚这三者的关系。
