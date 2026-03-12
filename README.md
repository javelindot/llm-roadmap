# LLM-Roadmap | 从NLP核心到LLM全栈实践（应用/微调/强化学习）
[![GitHub Stars](https://img.shields.io/github/stars/javelindot/llm-roadmap?style=social)](https://github.com/javelindot/llm-roadmap)
[![Last Updated](https://img.shields.io/github/last-commit/javelindot/llm-roadmap)](https://github.com/javelindot/llm-roadmap/commits/main)
[![License](https://img.shields.io/github/license/javelindot/llm-roadmap)](LICENSE)

### 🎯 仓库定位
一份**以NLP为起点**、聚焦「大语言模型应用落地+微调优化+强化学习对齐」的系统化学习路线图。区别于泛而全的资料，本仓库砍掉冗余的数学理论（仅作为扩展补充），直击核心：从NLP底层逻辑到LLM工程化应用，再到微调/RLHF强化学习优化，帮你快速从“懂NLP”到“能用好LLM”。

### 🗺️ 核心优势
- ✅ **NLP基础闭环**：已完成「NLP核心模块」，覆盖Transformer/注意力机制/预训练原理，是LLM学习的核心起点；
- ✅ **实战导向**：优先聚焦LLM应用、微调、强化学习等落地环节，拒绝“纸上谈兵”；
- ✅ **轻量化扩展**：数学仅作为补充模块（按需查阅），不占用核心学习路径；
- ✅ **超全思维导图**：所有核心知识点配套可视化思维导图，完整路线图如下：[AI大模型学习之路](/img/AI大模型学习之路.png "点击查看大图")，注意超级大图，建议在浏览器中查看。

## 📚 核心学习路径（思维导图驱动）
```mermaid
graph TD
    A[NLP核心] -->|Transformer/预训练/词向量| B[LLM场景化应用]
    B -->|RAG/Agent/多模态/Prompt| C[LLM工具链]
    C -->|HuggingFace/LangChain/SAA| D[LLM微调优化]
    D -->|LoRA/QLoRA/全量微调| E[强化学习对齐]
    E -->|RLHF/RLAIF/DPO| F[推理与部署]
    G[ML|DL|] -.->|按需补充| 
```

### 🔥 模块进度（持续完善中）
| 模块                | 完成度 | 核心内容                                                                 |
|---------------------|--------|--------------------------------------------------------------------------|
| NLP核心基础      | 100%   | Transformer架构/自注意力机制/预训练原理/词向量/文本预处理                |
| LLM场景化应用        | 0%    | Prompt工程化/RAG检索增强生成/Function Call/MCP/Skills/AI Agent/多模态LLM应用               |
| LLM工具链    | 0%    |        HuggingFace实操/LangChain核心组件/Spring AI Alibaba/模型调用规范          |
| LLM微调优化      | 0%    | LoRA/QLoRA轻量化微调/全量微调/数据集构建/超参数调优/效果评估            |
| 强化学习对齐     | 5%     | RLHF/RLAIF/DPO原理/奖励模型训练/对齐实战/偏好优化                       |
| LLM推理与部署    | 5%     | 模型量化/批量推理/FastAPI封装/Docker容器化/K8s调度/GPU优化              |
| 扩展补充     | 30%    | 线性代数/概率统计/优化理论（仅作为扩展，非核心路径）传统机器学习--》深度学（CNN｜RNN｜LSTM｜Transformer）                  |


## 🚀 快速开始（从NLP到LLM第一步）
### 1. 克隆仓库
```bash
git clone https://github.com/javelindot/llm-roadmap.git
cd llm-roadmap
```

### 2. 吃透NLP核心基础（LLM的底层逻辑）
```bash
# 查看NLP核心笔记+代码实战
open nlp

# 运行Transformer极简实现示例：待提供

# 暂时只有数学相关，后期会根据实际情况补充
open base
```

### 3. 上手LLM工具链（从“懂原理”到“能用模型”）
```bash

```

## 🤝 参与贡献（核心模块共建）
本仓库聚焦「NLP→LLM应用→微调→强化学习」的实战路径，目前核心模块仍在完善，诚邀你一起打造“最落地的LLM学习路线”：
1. **补充实战代码**：为微调/强化学习/部署模块补充可运行的示例（如LoRA微调LLaMA-2、RLHF极简实现）；
2. **完善思维导图**：为应用/微调模块梳理逻辑框架，补充关键知识点；
3. **纠错与优化**：修正NLP核心模块的代码/原理错误，优化Prompt工程最佳实践；
4. **场景案例贡献**：分享真实业务场景下的LLM应用案例（如企业级RAG、Agent落地）。

### 贡献流程
```bash
# 1. Fork仓库
# 2. 创建分支（聚焦具体模块）
git checkout -b feature/llm-finetune-lora
# 3. 提交修改（标注模块+内容）
git commit -m "补充-xxx模块： 补充xxx模块的代码实战OR笔记"
# 4. 推送分支
git push origin feature/llm-finetune-lora
# 5. 提交PR（附详细的内容说明）
```

## 📋 核心技术栈索引（按学习优先级）
| 阶段               | 核心技术/工具                          | 学习优先级 |
|--------------------|----------------------------------------|------------|
| NLP基础阶段        | Transformer/自注意力机制/预训练原理/词向量/文本预处理        | ⭐⭐⭐⭐⭐    |
| LLM工具阶段        | HuggingFace/LangChain/      | ⭐⭐⭐⭐      |
| LLM应用阶段        | Prompt/RAG/FunctionCall/Mcp/Skills/AI Agent/Manus/OpenClaw                | ⭐⭐⭐      |
| 微调/强化学习阶段  | LoRA/QLoRA/RLHF/DPO                    | ⭐⭐       |
| 部署阶段           | 模型量化/Docker/FastAPI                | ⭐⭐          |
| 数学扩展阶段       | 线性代数/概率统计/ML/DL（按需）| ⭐            |

## 欢迎参与
- 欢迎每一位参与贡献的开发者，让这份路线图更贴近工业级落地。

## 📄 许可证
本仓库采用 [MIT License](LICENSE) 开源，你可自由使用、修改、分发本仓库内容，商用需保留原作者信息。

---
⭐ **Star 本仓库**，解锁「从NLP核心到LLM微调/强化学习」的完整实战路径，持续跟进模块更新！
