---
group: 6. AI Agent
id: agent-multi
title: Agent · Multi-Agent 架构与协作
toc: Agent · Multi-Agent
---

**单个 Agent 有天花板**。让它同时写代码、做设计、审合同、管项目？能力边界和上下文窗口都不允许。

**Multi-Agent = 多个专职 Agent 分工协作**，像一个小团队：产品经理提需求、架构师做设计、开发写代码、测试找 bug。

## 什么时候需要 Multi-Agent

| 单 Agent 够用的场景 | 需要 Multi-Agent 的场景 |
|---------------------|------------------------|
| 查天气、算数学题、写封邮件 | 完整软件开发（需求→设计→编码→测试） |
| 单次信息检索 + 总结 | 深度研报（数据收集→分析→撰写→审核） |
| 工具调用 ≤ 3 步的简单任务 | 复杂业务工作流（跨系统、多角色审批） |
| 个人助手 | 企业级自动化（客服、销售、运营联动） |

## 核心架构模式

### 模式 1：层级式（Hierarchical）

一个「主管 Agent」分配任务，多个「执行 Agent」干活。

```
        ┌─────────────┐
        │  Supervisor  │  ← 拆解任务、分配、汇总
        │   Agent      │
        └──────┬──────┘
               │
    ┌─────────┼─────────┐
    ↓         ↓         ↓
┌───────┐ ┌───────┐ ┌───────┐
│Research│ │ Code  │ │ Review│  ← 各干各的
│ Agent  │ │ Agent │ │ Agent │
└───────┘ └───────┘ └───────┘
```

**优点**：结构清晰， supervisor 能控制整体质量。
**缺点**：supervisor 是瓶颈，所有信息过它手。

### 模式 2：对等网络（Peer-to-Peer）

Agent 之间直接对话、协商，没有中心节点。

```
┌─────────┐ ←────→ ┌─────────┐
│  Writer │        │ Reviewer│
│  Agent  │ ←────→ │  Agent  │
└────┬────┘        └────┬────┘
     └──────────────────┘
```

**优点**：灵活，适合创意碰撞类任务。
**缺点**：容易发散、陷入无效讨论，需要终止条件。

### 模式 3：流水线（Pipeline）

像工厂流水线，前一环节的输出是后一环节的输入。

```
Input → [Agent A] → [Agent B] → [Agent C] → Output
         数据清洗      特征提取      报告生成
```

**优点**：高效、可预测，适合标准化流程。
**缺点**：环节之间耦合紧，前面错了后面全错。

## 通信协议：Agent 之间怎么对话

Multi-Agent 的核心挑战不是「写多个 Agent」，而是**它们之间怎么传递信息**。

### 方式 1：共享消息队列

```python
class MessageBus:
    def __init__(self):
        self.channels = defaultdict(list)

    def publish(self, channel: str, message: dict):
        self.channels[channel].append(message)

    def subscribe(self, channel: str, agent_id: str):
        """返回该 channel 中 agent_id 未读的消息"""
        msgs = [m for m in self.channels[channel] if agent_id not in m.get("read_by", [])]
        for m in msgs:
            m.setdefault("read_by", []).append(agent_id)
        return msgs

# Agent 循环中读取消息
async def agent_loop(agent_id: str, bus: MessageBus):
    while True:
        msgs = bus.subscribe("project_alpha", agent_id)
        if msgs:
            action = await llm.decide(msgs)  # 基于消息决定下一步
            bus.publish("project_alpha", {"from": agent_id, "content": action})
```

### 方式 2：结构化 Handoff

一个 Agent 把任务「交接」给另一个 Agent，附带完整上下文：

```python
class Handoff:
    def __init__(self, from_agent: str, to_agent: str, context: dict):
        self.from_agent = from_agent
        self.to_agent = to_agent
        self.context = context  # 包含已完成结果 + 下一步指令

async def handoff_task(handoff: Handoff, registry: dict):
    agent = registry[handoff.to_agent]
    # 新 Agent 拿到完整上下文，无缝接续
    return await agent.run(handoff.context)
```

## 主流框架实现

### AutoGen（Microsoft）

对话驱动：Agent 之间通过「群聊」协作。

```python
from autogen import ConversableAgent, GroupChat

# 定义两个角色
writer = ConversableAgent("writer", llm_config={...})
editor = ConversableAgent("editor", llm_config={...})

# 群聊：writer 写完给 editor 审
groupchat = GroupChat(agents=[writer, editor], messages=[])
manager = GroupChatManager(groupchat=groupchat, llm_config={...})

writer.initiate_chat(manager, message="写一篇关于 RAG 的技术文章")
# → writer 写 → editor 提修改意见 → writer 改 → ... 直到 editor 通过
```

### CrewAI

角色驱动：给每个 Agent 定义「角色、目标、背景故事」，让它们像团队成员一样协作。

```python
from crewai import Agent, Task, Crew

researcher = Agent(
    role="技术研究员",
    goal="收集最新大模型评测数据",
    backstory="你是一位资深 AI 研究员...",
    allow_delegation=False
)

writer = Agent(
    role="技术写手",
    goal="把研究数据写成通俗易懂的报告",
    backstory="你擅长把复杂技术讲清楚...",
    allow_delegation=False
)

# 定义任务 + 执行顺序
task1 = Task(description="收集 2025 年 Q1 国产大模型评测数据", agent=researcher)
task2 = Task(description="基于数据撰写对比分析报告", agent=writer, context=[task1])

crew = Crew(agents=[researcher, writer], tasks=[task1, task2])
result = crew.kickoff()
```

### LangGraph

状态机驱动：用图（Graph）定义 Agent 之间的流转关系。

```python
from langgraph.graph import StateGraph, END

# 定义状态
class State(dict):
    messages: list
    current_agent: str

# 定义节点（Agent）
def researcher_node(state):
    result = researcher_agent.run(state["messages"])
    return {"messages": state["messages"] + [result], "current_agent": "writer"}

def writer_node(state):
    result = writer_agent.run(state["messages"])
    return {"messages": state["messages"] + [result], "current_agent": "END"}

# 建图
graph = StateGraph(State)
graph.add_node("researcher", researcher_node)
graph.add_node("writer", writer_node)
graph.set_entry_point("researcher")
graph.add_edge("researcher", "writer")
graph.add_edge("writer", END)

app = graph.compile()
app.invoke({"messages": ["调研国产大模型"], "current_agent": "researcher"})
```

## 设计 Multi-Agent 系统的 checklist

- [ ] **角色边界清晰**：每个 Agent 的职责不重叠
- [ ] **通信格式统一**：约定好消息结构（JSON Schema）
- [ ] **有终止条件**：防止无限循环对话
- [ ] **错误传播可控**：一个 Agent 挂了不影响全局，或能优雅降级
- [ ] **状态可观测**：中间结果能被记录、回放、调试

:::callout 👥
**Multi-Agent 不是银弹**。90% 的场景单 Agent + 好工具就够了。只有当任务确实需要多个独立视角、多个专业领域、或多个并行流水线时，才值得引入 Multi-Agent 的复杂度。
:::
