---
group: 5. Skills
id: skills-overview
title: Skills · 概览
toc: Skills · 概览
---

**Skill 是以 SKILL.md 为入口的任务说明与资源包。** 它沉淀适用条件、工作步骤、验证规则、脚本和输出模板，由支持它的 Agent 运行时发现并按需读取。

## 技能包解决什么问题

同一种报告、代码审查或数据清洗任务，往往反复需要相同流程和验收标准。把这些内容维护在一个目录中，可以随代码版本发布，并减少每次复制长提示词的工作。

技能描述告诉运行时何时考虑该技能；正文说明如何完成；资源提供详细参考和实现。模型仍可能选错技能、漏读资源或违反流程，所以必须保留评测与执行层限制。

## 标准目录

```text
csv-analyzer/
  SKILL.md
  scripts/       # 可选，确定性计算
  references/    # 可选，按需读取的详细规则
  assets/        # 可选，模板等资源
```

Agent Skills 已有开放格式规范，不能将它描述为某个 Claude 型号专有能力。各产品支持的发现路径、权限字段与执行方式仍可能不同，移植前需检查兼容性。

## 渐进式加载

| 阶段 | 内容 | 工程关注点 |
|------|------|------------|
| 发现 | name、description 等元数据 | 描述准确、避免能力重叠 |
| 选择 | 读取 SKILL.md 正文 | 触发条件、步骤和停止条件 |
| 执行 | 按需读取参考文件或运行脚本 | 工具授权、依赖、资源预算 |
| 验证 | 检查结果与证据 | 任务成功、格式、错误与回归 |

按需读取可以减少无关内容，但实际 token 数取决于技能数量、描述和运行时。读取的内容是否从后续上下文移除、是否命中缓存，也取决于运行时，不能假定任务结束即自动卸载。

## 技能文件与执行权限

SKILL.md 是说明文件，不会把一个 Python 文件自动注册成工具，也不会自行开启网络、Shell 或数据库权限。运行时需要提供读取/执行能力，并由服务端或宿主控制授权。

例如“核对销售报表”的技能可以要求读取数据、运行金额汇总脚本、生成报告；如果没有计算工具，它应请求已有统计结果，不能凭文本猜出数值。退款或发消息则还需要独立业务工具和明确权限。

## Claude Agent SDK 的接入方式

Python SDK 使用 query 或 ClaudeSDKClient，以及 ClaudeAgentOptions。项目技能通常放在 .claude/skills/ 下，接入时明确配置发现来源、可用工具与权限。完整示例见 [编写技能](502-skills-build.html)。

教程中 SDK 接口根据官方源码核对；集成时固定包版本并检查对应文档。不要使用未经验证的 Agent、Skill.from_directory 或 RemoteSkill 等类名当作真实 SDK API。

## 适用条件

适合重复的多步骤任务、有可共享方法和输出标准的团队流程。简单单次请求可能只需普通提示词；必须精确遵循顺序的事务流程，仍应使用程序或状态机控制。

验收至少包含：应触发与不应触发的请求、缺失资源、错误数据、工具失败，以及工具不可用时是否诚实降级。

## 参考资料

- [Agent Skills 格式规范](https://agentskills.io/specification)
- [Anthropic 技能示例](https://github.com/anthropics/skills)
- [Claude Agent SDK Python](https://github.com/anthropics/claude-agent-sdk-python)
- [SDK 技能接入文档](https://platform.claude.com/docs/en/agent-sdk/skills)

下一节：[Skills、Tool 与 MCP 的职责](501-skills-vs-tools.html)。
