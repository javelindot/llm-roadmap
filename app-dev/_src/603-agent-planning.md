---
group: 6. AI Agent
id: agent-planning
title: Agent · 规划与反思循环
toc: Agent · 规划反思
---

**规划让 Agent 能处理复杂任务，反思让 Agent 不再重复踩坑**。这是 Agent 从「执行者」升级为「问题解决者」的关键。

## 为什么需要规划

用户提的需求往往是模糊的、多步骤的：

> "帮我调研一下国产大模型在代码生成上的表现，做个对比报告"

这对 Agent 来说不是一次 LLM 调用能搞定的。需要拆解成：
1. 确定对比维度（代码补全、bug 修复、代码解释）
2. 收集各模型的评测数据
3. 设计测试用例并运行
4. 汇总结果、生成图表
5. 撰写结构化报告

**规划 = 把「大目标」拆成「可执行的小步骤」**。

## ReAct：最经典的规划模式

**ReAct**（Reasoning + Acting）= 边想边做。

```
思考(Thought) → 行动(Action) → 观察(Observation) → 思考(Thought) → ...
```

每一步，Agent 先「想」自己要做什么，再「做」，然后看结果，再决定下一步。

### 代码骨架

```python
class ReActAgent:
    def __init__(self, llm, tools):
        self.llm = llm
        self.tools = tools  # ToolRegistry

    async def run(self, task: str, max_steps=15):
        thought_history = []
        for step in range(max_steps):
            # 1. 思考：基于任务和历史，决定下一步
            prompt = self._build_thought_prompt(task, thought_history)
            thought = await self.llm.generate(prompt)
            thought_history.append(f"Step {step}: {thought}")

            # 2. 解析 thought，提取 action
            action = self._parse_action(thought)
            if action["type"] == "finish":
                return action["answer"]

            # 3. 执行 action
            obs = await self.tools.execute(action["name"], action["args"])
            thought_history.append(f"Observation: {obs}")

        return "任务超时，请简化需求后重试"
```

### Thought 的输出格式（强制结构化）

用 prompt 约束 LLM 的输出格式，方便解析：

```
你必须按以下格式输出：

Thought: 我对当前状况的分析，以及下一步要做什么
Action: 工具名称
Action Input: {"参数名": "值"}

如果任务已完成，输出：
Thought: 任务已完成
Final Answer: 最终答案
```

## Plan-and-Execute：先计划再执行

ReAct 是「走一步看一步」，适合探索性任务。对于确定性强的任务，**先定计划再执行**效率更高。

```
Phase 1: 计划
   用户任务 → LLM 生成完整步骤清单（Plan）
   
Phase 2: 执行  
   按 Plan 逐步执行，每步可调用工具
   
Phase 3: 复核
   检查结果是否满足原始目标，不满足则重计划
```

```python
async def plan_and_execute(task: str, llm, tools):
    # Phase 1: 生成计划
    plan = await llm.generate(f"将以下任务拆成具体步骤（JSON 数组）：{task}")
    steps = json.loads(plan)

    # Phase 2: 执行
    results = []
    for i, step in enumerate(steps):
        result = await execute_step(step, tools, results_so_far=results)
        results.append(result)

    # Phase 3: 复核
    check = await llm.generate(f"任务：{task}\n计划：{steps}\n结果：{results}\n是否完成？")
    if "未完成" in check:
        return await plan_and_execute(task, llm, tools)  # 递归重计划

    return results
```

**对比**：

| 模式 | 优点 | 缺点 | 适用场景 |
|------|------|------|----------|
| ReAct | 灵活，能根据中间结果调整 | 步骤多、token 消耗大 | 探索性、信息收集类任务 |
| Plan-and-Execute | 步骤清晰、可预测 | 计划错了要整体重来 | 流程化、确定性强的任务 |

## 反思：让 Agent 自我纠错

**反思（Reflection）** = 执行完后回顾过程，总结经验，避免再犯。

### 两种反思时机

| 时机 | 名称 | 作用 |
|------|------|------|
| 每步执行后 | **Self-Reflection** | 检查当前结果是否符合预期，错误时修正 |
| 任务完成后 | **Post-Hoc Reflection** | 总结全流程，提炼经验存入长期记忆 |

### Self-Reflection 实现

```python
async def execute_with_reflection(step, tools, context):
    result = await tools.execute(step)

    # 让 LLM 判断结果是否合格
    reflection_prompt = f"""
步骤：{step}
结果：{result}
预期目标：{context['goal']}

请判断：
1. 结果是否正确/有用？（是/否）
2. 如果不正确，原因是什么？
3. 建议如何修正？
"""
    reflection = await llm.generate(reflection_prompt)

    if "否" in reflection:
        # 根据反思结果重试或换策略
        new_step = await llm.generate(f"基于反思修正步骤：{reflection}")
        return await execute_with_reflection(new_step, tools, context)

    return result
```

### 高级模式：Reflexion

**Reflexion** 论文提出的方法 = ReAct + 反思记忆。

Agent 每次失败后，把「失败原因 + 修正策略」写入**反思记忆**。下次遇到类似任务时，先从反思记忆中读取经验，避免重复踩坑。

```python
class ReflexionAgent(ReActAgent):
    def __init__(self, llm, tools, reflection_memory):
        super().__init__(llm, tools)
        self.reflection_memory = reflection_memory  # 向量存储

    async def run(self, task: str):
        # 先查历史反思
        past_reflections = await self.reflection_memory.recall(task)
        context = f"历史经验：{past_reflections}\n\n当前任务：{task}"

        try:
            result = await super().run(context)
            return result
        except Exception as e:
            # 失败后生成反思并存入记忆
            reflection = await self.llm.generate(f"任务失败原因分析：{e}")
            await self.reflection_memory.add(reflection, metadata={"task_type": classify(task)})
            raise
```

## 一个完整的规划-反思循环

```
用户任务
   ↓
[规划] 拆分成步骤清单
   ↓
[执行步骤 1]
   ↓
[反思] 结果对吗？ → 不对 → 修正重试
   ↓
[执行步骤 2]
   ↓
...
   ↓
[任务完成]
   ↓
[复盘反思] 总结经验 → 存入长期记忆
   ↓
返回结果
```

:::callout 🔄
**ReAct 是骨架，反思是灵魂**。没有反思的 Agent 像不会学习的新手；有了反思，它越用越聪明。
:::
