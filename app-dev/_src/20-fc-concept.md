---
group: 2. Function Call
id: fc-concept
title: Function Call · 工作原理
toc: Function Call · 原理
---

Function Call 让大模型从「**纯文本输出**」进化到「**结构化调用外部能力**」。核心三步：

1. 开发者声明可用函数列表（JSON Schema）
2. 模型读取用户输入后，决定是否调用某个函数
3. 开发者执行函数、把结果返还模型，模型生成最终回复
