---
group: 5. Skills
id: skills-deploy
title: Skills · 部署与最佳实践
toc: Skills · 部署
---

写好 Skill 只是第一步，**怎么让团队用起来 + 在生产环境跑稳**才是难点。这一章讲部署和运维。

## 部署模式 1：本地嵌入（最简单）

Skill 直接放进应用代码库。

```
my_app/
├── app.py
├── skills/
│   ├── csv_analyzer/
│   ├── code_reviewer/
│   └── report_writer/
└── requirements.txt
```

```python
# app.py
from claude_agent_sdk import Agent, Skill
from pathlib import Path

# 自动加载 skills/ 下所有 Skill
skill_dir = Path(__file__).parent / "skills"
skills = [Skill.from_directory(d) for d in skill_dir.iterdir() if d.is_dir()]

agent = Agent(model="claude-sonnet-4-5", skills=skills)

@app.post("/chat")
def chat(message: str):
    return agent.run(message)
```

✅ **优点**：零运维、即时生效、版本随应用走
❌ **缺点**：Skills 跨应用复用困难

适合：单应用、Skill 数量 < 20。

## 部署模式 2：Skill 包仓库（团队级）

把 Skill 发布为 Python 包。

```
my_company_skills/
├── csv_analyzer/
├── code_reviewer/
└── pyproject.toml
```

```toml
# pyproject.toml
[project]
name = "mycompany-skills"
version = "0.1.0"

[project.entry-points."claude_agent_sdk.skills"]
csv_analyzer = "mycompany_skills.csv_analyzer:SKILL"
code_reviewer = "mycompany_skills.code_reviewer:SKILL"
```

发布到内部 PyPI：

```bash
uv publish --repository internal-pypi
```

各应用用：

```python
# 任何应用
pip install mycompany-skills

from claude_agent_sdk import Agent, discover_skills
agent = Agent(model="...", skills=discover_skills(package="mycompany_skills"))
```

✅ **优点**：Skill 跨应用复用、版本独立管理、CI/CD 友好
❌ **缺点**：需要包管理基础设施

适合：中等规模公司、Skill > 10 + 多个应用。

## 部署模式 3：Skill 注册中心（企业级）

中心化的 Skill 服务器：

```
┌──────────────────────────────────────┐
│       Skill Registry Service          │
│  (类似 npm registry / Docker Hub)     │
│                                       │
│  GET  /skills              列出所有   │
│  GET  /skills/{name}       获取 Skill │
│  POST /skills              发布       │
│  PATCH /skills/{name}      更新       │
└────────────────┬─────────────────────┘
                 │ HTTPS
                 ↓
┌────────────────────────────────────────┐
│       各应用 / 各团队 / 个人           │
│       动态拉取 Skill 使用              │
└────────────────────────────────────────┘
```

```python
from claude_agent_sdk import Agent, RemoteSkill

# 从远程注册中心拉取
agent = Agent(
    model="claude-sonnet-4-5",
    skills=[
        RemoteSkill("https://skills.company.com/skills/csv_analyzer"),
        RemoteSkill("https://skills.company.com/skills/code_reviewer")
    ]
)
```

✅ **优点**：全公司统一管理、热更新、可治理
❌ **缺点**：基础设施成本

适合：大型公司、跨团队、合规要求高。

## 部署模式 4：Skills + MCP 混合

Skills 内部调用 MCP Server，**Skill 提供方法论、MCP 提供工具实现**。

```markdown
<!-- SKILL.md -->
## Tools available

直接使用以下 MCP Servers 暴露的工具：

- `github` (MCP server: `@modelcontextprotocol/server-github`)
- `slack` (MCP server: `@modelcontextprotocol/server-slack`)
- `postgres` (MCP server: `@modelcontextprotocol/server-postgres`)
```

```python
# Agent 端
from claude_agent_sdk import Agent, Skill, MCPServer

agent = Agent(
    model="claude-sonnet-4-5",
    skills=[Skill.from_directory("./skills/incident_handler")],
    mcp_servers=[
        MCPServer(name="github", url="npx -y @modelcontextprotocol/server-github"),
        MCPServer(name="slack", url="npx -y @modelcontextprotocol/server-slack")
    ]
)
```

✅ **优点**：MCP 工具生态 + Skill 方法论复用
❌ **缺点**：架构稍复杂

适合：希望最大化复用社区资源的团队。

## 生产环境必备：可观测性

### 1. Trace 每次 Skill 调用

```python
from langfuse import Langfuse
from claude_agent_sdk import Agent

lf = Langfuse()

agent = Agent(
    model="claude-sonnet-4-5",
    skills=skills,
    tracer=lf  # 自动 trace
)

# 每次 agent.run() 都会记录:
# - 哪些 Skills 被加载
# - 每步调用了哪些 tool
# - 每个 tool 的 input/output/耗时
# - LLM token 消耗
# - 最终输出
```

在 Langfuse / Phoenix / LangSmith 面板能看完整调用链。

### 2. 关键指标监控

| 指标 | 目标 | 告警阈值 |
|------|------|---------|
| Skill 加载成功率 | >99% | <95% |
| Tool 调用成功率 | >95% | <90% |
| 单次任务平均耗时 | <30s | >60s |
| 单次任务 token 消耗 | <10K | >50K |
| Skill 加载次数（每 Skill） | 监控分布 | 长尾 Skill 考虑下线 |
| 用户满意度（👍/👎）| >85% | <70% |

### 3. 错误分类

```python
# 在 Agent 层 wrap
try:
    result = agent.run(message)
except SkillLoadError as e:
    # Skill 定义有问题
    log.error(f"Skill load failed: {e.skill_name}")
    fallback_response()
except ToolCallError as e:
    # 工具执行失败
    log.error(f"Tool failed: {e.tool_name}, args: {e.args}")
    if e.is_retryable:
        retry()
except LLMRateLimitError:
    # 模型限流
    backoff_and_retry()
```

## 性能优化

### 1. Skill 索引最小化

每个 Skill 在「索引」阶段只占几百 token —— 控制好 Skill 的 description / when to use 长度。

```markdown
# ❌ 啰嗦
description: This skill is designed to help users perform comprehensive data 
analysis tasks including but not limited to statistical analysis, data 
visualization, anomaly detection, trend identification, correlation analysis, 
and the generation of detailed analytical reports based on user-provided CSV 
or Excel files...

# ✅ 简洁
description: 分析 CSV/Excel 数据，输出统计指标、可视化和洞察报告
```

### 2. 按需加载策略

只在该 Skill 真正需要时才加载完整内容：

```python
# Agent SDK 自动按需加载，但你可以显式控制
agent = Agent(
    model="...",
    skills=skills,
    skill_loading="lazy"  # 默认。"eager" 会全部预加载
)
```

### 3. Prompt Caching

Skill 的 system prompt 通常重复 → 用 Anthropic Prompt Caching：

```python
agent = Agent(
    model="claude-sonnet-4-5",
    skills=skills,
    cache_skills=True  # 加载的 Skill prompt 自动加 cache_control
)
# 同样的 Skill 第 2 次起便宜 90%
```

### 4. 并行 Skill 评估

如果用户问题不明确，模型可能要"试探"多个 Skill：

```python
# 并行加载多个候选 Skill 描述（不是完整内容）
candidate_skills = agent.shortlist_skills(message, top_k=3)
# 让模型从 3 个候选中选最匹配的，再加载完整内容
```

## 安全考虑

### 1. Skill 信任分级

不是所有 Skill 都同样安全：

```python
agent = Agent(
    skills=[
        Skill.from_directory("./skills/csv_analyzer", trust="high"),  # 内部开发
        Skill.from_url("...", trust="medium"),                        # 公司内部分享
        RemoteSkill("...", trust="low")                               # 外部下载
    ],
    confirmation_required_for=["medium", "low"]  # 低信任 Skill 调用要用户确认
)
```

### 2. Skill 沙箱化

Skill 内的工具运行在受限环境：

```python
agent = Agent(
    skills=skills,
    sandbox={
        "filesystem": ["/workspace"],  # 只能访问指定目录
        "network": ["*.company.com"],  # 只能访问内网
        "max_memory_mb": 1024,
        "max_runtime_sec": 300
    }
)
```

### 3. 审计日志

记录所有 Skill 加载和工具调用：

```python
audit_log.append({
    "user_id": user.id,
    "skill": skill_name,
    "tool": tool_name,
    "args": tool_args,
    "result": tool_result,
    "timestamp": now()
})
```

对合规要求高的行业（金融、医疗）必备。

## CI/CD 流程

完整的 Skill 发布流程：

```
开发者改 Skill
   ↓
本地测试 (pytest tests/)
   ↓
提交 PR
   ↓ 触发
CI:
  1. Skill 格式校验 (SKILL.md 必须字段)
  2. 单元测试 Skill 内工具
  3. 集成测试 (用测试 prompt 跑通 Skill)
  4. 评测对比 (新版 vs 老版的关键指标)
   ↓ 通过
Code Review
   ↓
Merge
   ↓ 自动
发布到 Skill Registry
   ↓ 通知
各应用拉取最新版
```

### 评测脚本示例

```python
# tests/eval_csv_analyzer.py
EVAL_CASES = [
    {
        "input": "分析 /test/sales.csv，找异常订单",
        "expected_tools": ["load_csv", "detect_outliers"],
        "expected_keywords": ["异常", "订单", "建议"]
    },
    ...
]

def test_csv_analyzer_v2():
    agent = Agent(skills=[Skill.from_directory("./skills/csv_analyzer")])
    
    for case in EVAL_CASES:
        result = agent.run(case["input"])
        
        # 检查工具调用
        called_tools = [c.name for c in agent.trace.tool_calls]
        for expected_tool in case["expected_tools"]:
            assert expected_tool in called_tools
        
        # 检查关键词
        for kw in case["expected_keywords"]:
            assert kw in result
```

PR 自动跑 → 准确率 / 工具调用准确率必须 ≥ 老版本，否则阻塞合入。

## 治理：Skill 数量增长的应对

当 Skills 数量 > 50 后会遇到问题：
- 模型加载选择变慢
- Skill 间能力重叠
- 维护混乱

### 应对策略

1. **分类标签**
   ```yaml
   tags: [data, finance, internal]
   ```
   按 tags 给 Agent 创建时只加载相关分类。

2. **使用统计**
   监控每个 Skill 的使用频次，**长尾未使用的考虑下线**。

3. **重叠检测**
   定期评估 Skills 的 description 相似度，重叠的合并或拆分。

4. **分层架构**
   ```
   核心 Skills（全员可用）  ← 10 个
   部门 Skills（按团队）    ← 各 5-10 个
   个人 Skills（用户自建）  ← 任意
   ```

## 最佳实践清单

```
开发:
  ☐ SKILL.md 字段完整
  ☐ When to use 清晰
  ☐ Tools 描述详尽
  ☐ 有 examples
  ☐ 单元测试覆盖

发布:
  ☐ 版本号语义化（semver）
  ☐ CHANGELOG 维护
  ☐ CI 自动评测
  ☐ Code Review 通过

部署:
  ☐ 接入 trace
  ☐ 配置 prompt caching
  ☐ 设置沙箱限制
  ☐ 监控告警接入

运维:
  ☐ 每周看使用统计
  ☐ 每月清理长尾 Skill
  ☐ 每季度审视架构
  ☐ 安全审计日志归档
```

## 总结：Skills 学完后

完成本章后你应该能：

✅ 判断什么场景该用 Skills（vs Prompt / FC / MCP）
✅ 设计一个清晰的 Skill 结构
✅ 编写可生产的 Skill（含 tools / templates / examples）
✅ 集成进 Claude Agent SDK
✅ 部署 Skills 给团队 / 公司使用
✅ 监控、评测、迭代 Skills

## 下一站：AI Agent

学完 Skills，你已经掌握了**所有「能力封装」层的技术**。

下一模块讲 [AI Agent](#agent-concept) —— **如何让模型自主编排这些能力完成复杂任务**。Skills 是 Agent 的「能力库」，Agent 是 Skills 的「调度器」，两者天作之合。

学完 Agent 模块，你就掌握了 2026 年 LLM 应用开发的**完整技术栈**。
