# MCP（Model Context Protocol）

## 引言

随着大语言模型（LLM, Large Language Model）在各类智能应用中的广泛应用，如何高效、安全、标准化地为 LLM 提供上下文信息，成为 AI 应用开发中的核心问题。在传统的 AI 应用开发中，开发者往往需要为每一个 LLM 或 AI 服务单独设计数据接口和上下文传递方式，这不仅导致了重复开发、接口混乱，还带来了安全和维护上的巨大挑战。

正是在这一背景下，**Model Context Protocol（MCP，模型上下文协议）** 应运而生。MCP 是由人工智能公司 Anthropic 于 2024 年 11 月 25 日正式开源的开放标准协议，旨在解决大型语言模型与外部数据源、工具集成的碎片化问题，推动 AI 从被动问答转向主动执行复杂任务。该协议的核心理念是 "标准化 LLM 上下文输入"，即为 LLM 提供一种统一、可扩展、安全的数据和工具接入方式。

本报告将从技术原理、架构设计、运行机制、代码实现等多个维度，深入剖析 MCP 技术的核心内容，通过代码示例、流程图、时序图等形式，为读者提供全面而清晰的技术解析。

## 一、MCP 技术概述与定位

### 1.1 技术背景与发展历程

MCP 技术的发展可以追溯到 2023 年底，Anthropic 公司在这一时期提出了 MCP 的概念雏形。2024 年 4 月，Anthropic 在内部会议中首次提出 MCP 草案，作为 Claude"Computer Use" 功能的支撑协议，焦点是权限沙盒和日志功能，这标志着 MCP 从概念走向规范的起点。

经过近 7 个月的技术研发和标准化工作，**2024 年 11 月 25 日**，Anthropic 正式将 MCP 开源，发布了规范版本 2024-11-05，并同时发布了 Python 和 TypeScript 的初始 SDK。这一发布引起了整个 AI 行业的广泛关注，OpenAI 在同年 12 月宣布支持 MCP 协议，赋予其类似 HTTP 的底层基础设施属性。

截至 2025 年 12 月，MCP 已通过 Linux 基金会旗下的 **AI Agent Foundation（AAIF）** 实现标准化管理，获得 OpenAI、微软、谷歌、亚马逊等 30 余家科技巨头的支持，全球公开 MCP 服务器数量超过 10,000 个，SDK 月下载量突破 9700 万次，成为 AI 代理生态的 "USB-C 接口"。

### 1.2 技术定义与核心价值

MCP（Model Context Protocol，模型上下文协议）是一种为现代人工智能和大模型服务场景设计的开放式协议，旨在标准化大型语言模型与外部数据源和工具之间的交互方式。从技术本质来看，MCP 是一套开源的标准化连接框架，其核心价值如同为 AI 应用打造了 "统一插座"—— 就像 USB-C 接口统一了不同设备的充电与数据传输标准，MCP 通过规范接口协议，让大语言模型能无缝对接外部数据库、专业工具与第三方服务，实现 "即插即用" 的高效集成。

MCP 的核心理念包括四个关键方面：



1. **标准化**：为 LLM 提供统一的上下文输入协议，避免各自为政的接口混乱

2. **可扩展性**：支持多种数据源、工具和 LLM 服务的灵活集成

3. **安全性**：在本地或私有基础设施内安全地处理敏感数据

4. **生态开放性**：鼓励社区和厂商共同参与，持续丰富 MCP 的集成能力

从功能定位来看，MCP 相当于给大模型定义了一个标准的 "USB 接口"，通过调用 MCP 服务器，模型可以直接获取来自不同应用的数据信息。这种设计理念使得 AI 模型能够有效控制计算机的各类软件，实现 "AI 智能体" 功能，类似 AI 智能体领域的 "书同文，车同轨"。

### 1.3 技术定位与应用场景

MCP 在技术架构中占据着关键的桥梁地位，它位于 AI 模型与外部世界之间，负责建立标准化、双向的通信通道。在实际应用中，MCP 的典型应用场景已覆盖多类数据交互需求：

**内容抓取类应用**：



* Fetch MCP：快速抓取网页文本、图片链接

* Twitter MCP：同步社交平台动态

**企业级应用场景**：



* 智能导购：实时调取全渠道库存数据，动态推荐商品，基于用户行为与供应链状态生成个性化购买方案

* 旅游规划：实时整合交通、天气及景区人流数据，动态调整行程，基于用户偏好生成个性化路线

* 科研协作：整合多源实验数据与跨平台文献资源，智能生成研究模型，通过动态权限管理协调多机构协作

**垂直行业应用**：

在电商领域，百度构建了 "电商智能体"，AI 助手可直接调用库存数据库、商品评价系统和支付接口，实现 "从对话到下单" 的全流程自动化。在出行领域，高德 MCP 2.0 通过专属地图工具，将出行规划、导航启动、酒店推荐等步骤从 6 次操作缩减为 "一键完成"。

## 二、MCP 技术核心原理与架构设计

### 2.1 设计理念与技术选择

MCP 的设计灵感来源于软件开发领域的**Language Server Protocol（LSP）**，后者通过标准化协议成功解决了 IDE 与语言工具的集成问题。LSP 的革命性突破在于创建了编辑器前端与语言后端解耦的标准化通信架构 —— 通过定义 JSON-RPC 规范下的跨进程交互协议，使得语言智能服务能够以可插拔的方式适配任意编辑器。

MCP 正是在这一背景下诞生的，它将 LSP 的思想应用于 AI 领域，旨在为模型提供一个标准化的上下文访问接口。与 LSP 解决编辑器与语言的 "M x N" 问题类似，MCP 旨在解决 "AI 模型" 与 "外部工具" 之间的 "N x M" 集成难题。

从设计原则来看，LSP 解决了 "多对多" 的集成问题，通过创建通用语言让各方能够 "交流"，统一协议后让 "编辑器 - 语言" 各自只需要实现一次。MCP 继承了这一设计哲学，同时进行了创新：**LSP 是被动响应式的（你问我答），而 MCP 还支持 Agent 主动发起的工作流，更适合自主执行任务的场景**。

### 2.2 核心架构设计

MCP 采用**客户端 - 主机 - 服务器（Client-Host-Server）三层架构**，其中每个主机可以运行多个客户端实例。这种架构使用户能够在应用程序中集成 AI 功能，同时保持明确的安全边界和隔离关注点。基于 JSON-RPC，MCP 提供了一个有状态的会话协议，专注于上下文交换和客户端与服务器之间的采样协调。

#### 2.2.1 核心组件详解

**主机（Host）**：

主机进程充当容器和协调者，是整个 MCP 系统的核心。其主要职责包括：



* 创建和管理多个客户端实例

* 控制客户端连接权限和生命周期

* 执行安全策略和同意要求

* 处理用户授权决策

* 协调 AI/LLM 集成和采样

* 管理跨客户端的上下文聚合

在实际应用中，主机通常是用户直接交互的界面，如 Claude Desktop、集成开发环境（IDE）或其他 AI 工具。

**客户端（Client）**：

每个客户端由主机创建，并维护一个隔离的服务器连接。客户端的核心功能包括：



* 为每个服务器建立一个有状态的会话

* 处理协议协商和功能交换

* 双向路由协议消息

* 管理订阅和通知

* 维护服务器之间的安全边界

主机应用程序创建和管理多个客户端，**每个客户端与特定服务器具有 1:1 的关系**，确保连接的隔离性和安全性。

**服务器（Server）**：

服务器提供专门的上下文和功能，通过 MCP 原语公开资源、工具和提示。服务器的设计遵循以下原则：



* 独立运行，具有明确的职责

* 通过客户端接口请求采样

* 必须遵守安全约束

* 可以是本地进程或远程服务

服务器专注于特定的、明确的功能，简单的接口最小化实现开销，明确的分离使代码易于维护。

#### 2.2.2 架构设计原则

MCP 建立在几个关键设计原则之上：



1. **服务器应该非常容易构建**：主机应用程序处理复杂的编排职责，服务器专注于特定的、明确的功能，简单的接口最小化实现开销

2. **服务器应该高度可组合**：每个服务器在隔离中提供专注的功能，多个服务器可以无缝组合，共享协议实现互操作性，模块化设计支持可扩展性

3. **服务器不应读取整个对话**：服务器不应读取整个对话，也不应 "看到" 其他服务器，服务器仅接收必要的上下文信息，完整的对话历史保留在主机中，每个服务器连接保持隔离，跨服务器交互由主机控制

4. **功能可以逐步添加**：核心协议提供最少的必需功能，需要时可以协商额外的功能，服务器和客户端独立演进，协议设计为未来可扩展，保持向后兼容性

### 2.3 核心原语系统

MCP 的核心在于其定义的**原语系统**，这些原语定义了客户端和服务器可以相互提供的功能类型。服务器可以暴露三种核心原语，每种原语在控制层次结构中具有不同的特点：



| 原语类型          | 控制主体   | 描述               | 典型示例             |
| ------------- | ------ | ---------------- | ---------------- |
| 提示（Prompts）   | 用户控制   | 由用户选择调用的交互式模板    | 斜杠命令、菜单选项        |
| 资源（Resources） | 应用程序控制 | 由客户端附加和管理的上下文数据  | 文件内容、Git 历史      |
| 工具（Tools）     | 模型控制   | 向 LLM 公开以采取行动的函数 | API POST 请求、文件写入 |

**提示（Prompts）**：

提示是预定义的模板或指令，指导语言模型交互。用户可以通过选择不同的提示模板来引导模型执行特定任务，例如选择 "代码审查" 提示来让模型分析代码质量。

**资源（Resources）**：

资源是为模型提供额外上下文的结构化数据或内容。资源可以是静态的（如文档内容）或动态的（如实时数据流），通过统一的接口提供给模型使用。

**工具（Tools）**：

工具是允许模型执行动作或检索信息的可执行函数。与传统的函数调用不同，MCP 的工具调用具有更强的上下文感知能力，能够理解调用的语义和目的。

### 2.4 数据结构与消息格式

MCP 基于**JSON-RPC 2.0 规范**构建，确保消息结构统一、易序列化。JSON-RPC 是一个轻量级的远程过程调用协议，采用 JSON 编码，具有人类可读和易于调试的优点。

MCP 定义了三种类型的消息：



1. **请求（Request）**：双向消息，可以从客户端发送到服务器，也可以反向发送。必须包含字符串或整数类型的 ID，在同一会话中，请求方不能重复使用相同的 ID，可以包含可选的参数对象。



```json
{
  "jsonrpc": "2.0",
  "id": "string | number",
  "method": "string",
  "params?": {
    "key": "value"
  }
}
```



1. **响应（Response）**：作为对请求的回复而发送。必须包含与对应请求相同的 ID，必须设置 result 或 error 其中之一（不能同时设置），错误码必须是整数，可以包含可选的结果数据。



```json
{
  "jsonrpc": "2.0",
  "id": "string | number",
  "result?": {
    "[key: string]": "unknown"
  },
  "error?": {
    "code": "number",
    "message": "string",
    "data?": "unknown"
  }
}
```



1. **通知（Notification）**：不需要响应的单向消息，可以从客户端发送到服务器，也可以反向发送。不能包含 ID 字段，用于状态更新和事件通知，可以包含可选的参数对象，减少通信开销，支持异步操作。



```
{

 "jsonrpc": "2.0",

 "method": "string",

 "params?": {

   "\[key: string]": "unknown"

 }

}
```

### 2.5 能力协商机制

MCP 使用基于功能的协商系统，客户端和服务器在初始化期间明确声明其支持的功能。功能确定会话期间可用的协议功能和原语。

**服务器可以声明的功能**包括：



* 资源订阅（resource subscription）

* 工具支持（tool support）

* 提示模板（prompt templates）

* 日志记录（logging）

**客户端可以声明的功能**包括：



* 采样支持（sampling support）

* 通知处理（notification handling）

* 根目录信息（roots information）

能力协商的过程如下：



1. 客户端发送初始化请求，包含其支持的协议版本和能力列表

2. 服务器响应，包含其支持的协议版本和能力列表

3. 双方协商出共同支持的功能集

4. 在整个会话期间，双方必须尊重声明的功能

这种能力协商机制确保了客户端和服务器对支持的功能有清晰的理解，同时保持协议的可扩展性。例如，实现资源订阅通知需要服务器声明订阅支持，工具调用需要服务器声明工具功能。

## 三、MCP 技术运行机制与工作流程

### 3.1 初始化流程详解

MCP 为客户端 - 服务器连接定义了严格的生命周期，确保正确的能力协商和状态管理。**初始化阶段必须是客户端与服务器之间的第一次交互**，在这个阶段，客户端与服务器会完成以下关键操作：



1. 建立协议版本兼容性

2. 交换并协商能力

3. 共享实现细节

整个初始化过程类似于 TCP 的三次握手，包含四个关键步骤：

#### 3.1.1 初始化请求（Initialize Request）

客户端首先发送`initialize`请求，这个请求包含以下关键信息：



* 支持的协议版本

* 客户端能力声明

* 客户端实现信息

初始化请求的 JSON 格式示例：



```
{

 "jsonrpc": "2.0",

 "id": 1,

 "method": "initialize",

 "params": {

   "protocolVersion": "2024-11-05",

   "capabilities": {

     "roots": {

       "listChanged": true

     },

     "sampling": {}

   },

   "clientInfo": {

     "name": "ExampleClient",

     "version": "1.0.0"

   }

 }

}
```

#### 3.1.2 初始化响应（Initialize Response）

服务器接收到初始化请求后，会立即以**HTTP 202 Accepted**状态码关闭该 POST 请求（如果使用 HTTP 传输），然后发送初始化响应。响应中包含服务器支持的协议版本、能力声明和服务器信息。

初始化响应的 JSON 格式示例：



```
{

 "jsonrpc": "2.0",

 "id": 1,

 "result": {

   "protocolVersion": "2024-11-05",

   "capabilities": {

     "logging": {},

     "prompts": {

       "listChanged": true

     },

     "resources": {

       "subscribe": true,

       "listChanged": true

     },

     "tools": {

       "listChanged": true

     }

   },

   "serverInfo": {

     "name": "ExampleServer",

     "version": "1.0.0"

   }

 }

}
```

#### 3.1.3 初始化完成通知（Initialized Notification）

客户端接受响应完成能力协商后，会发送一个`initialized`初始化通知，确认连接成功建立。这个通知是一个不需要响应的单向消息。

初始化完成通知的 JSON 格式示例：



```
{

 "jsonrpc": "2.0",

 "method": "initialized"

}
```

#### 3.1.4 正常通信阶段

完成上述三步后，客户端和服务器进入正常通信阶段，开始交换业务数据。此时，双方已经就协议版本、支持的功能等达成一致，可以按照协商好的能力进行数据交互。

### 3.2 消息交换机制

连接初始化完成后，MCP 客户端和服务器进入消息交换阶段，这是通信流程的核心部分。在这个阶段，双方可以交换请求、响应和通知，实现各种功能交互。

MCP 支持三种主要的消息交换模式：



1. **请求 - 响应模式**：客户端发送请求，服务器处理后返回响应

2. **通知模式**：单向消息传递，不需要响应

3. **流式模式**：支持长时间的数据传输和实时更新

在实际的工作流程中，一个完整的调用过程包括以下阶段：



```
用户发起请求(IDE 或聊天界面提交指令)

 ↓

主机准备上下文(Host 提供工具列表、环境信息)

 ↓

模型决策与调用(模型选择并调用合适工具)

 ↓

客户端转发执行(Client 以 JSON-RPC 向服务器发送调用请求)

 ↓

服务器执行操作(完成任务并返回结果)

 ↓

结果整合与回答(模型基于结果生成最终输出)
```

### 3.3 数据传输机制

MCP 目前定义了两种标准的客户端 - 服务器通信传输机制：

#### 3.3.1 标准输入输出（stdio）传输

在 stdio 传输机制中，客户端将 MCP 服务器作为子进程启动。服务器在其标准输入（stdin）上接收 JSON-RPC 消息，并将响应写入其标准输出（stdout）。

**stdio 传输的技术规范**：



* 消息以换行符分隔，不得包含嵌入的换行符

* 服务器可以将 UTF-8 字符串写入其标准错误（stderr）进行日志记录，客户端可以捕获、转发或忽略此日志记录

* 服务器不得向其 stdout 写入任何不是有效 MCP 消息的内容

* 客户端不得向服务器的 stdin 写入任何不是有效 MCP 消息的内容

stdio 传输的工作流程图：



```
Client Process

  ↓

  ├── Launch Subprocess (MCP Server)

  ├── Write JSON-RPC messages to stdin

  └── Read JSON-RPC responses from stdout
```

#### 3.3.2 基于 SSE 的 HTTP 传输

在 SSE 传输机制中，服务器作为独立进程运行，可以处理多个客户端连接。服务器必须提供两个端点：



1. **SSE 端点**：供客户端建立连接并接收来自服务器的消息

2. **HTTP POST 端点**：供客户端向服务器发送消息

当客户端连接时，服务器必须发送一个`endpoint`事件，其中包含一个 URI，供客户端用于发送消息。所有后续的客户端消息必须作为 HTTP POST 请求发送到此端点。服务器消息作为 SSE `message`事件发送，消息内容以 JSON 编码在事件数据中。

SSE 传输的工作流程图：



```
Client              Server

  ↓                   ↓

  ├── Open SSE Connection         ◄───────── SSE Handshake

  ├── Receive endpoint event      │

  ├── Send HTTP POST messages     ├───► Process request

  └── Receive SSE message events  ◄───────── Send response
```

#### 3.3.3 自定义传输机制

客户端和服务器可以实现其他自定义传输机制，以满足其特定需求。该协议是传输无关的，可以在任何支持双向消息交换的通信通道上实现。选择支持自定义传输的实现者必须确保它们保留 MCP 定义的 JSON-RPC 消息格式和生命周期要求。

### 3.4 生命周期管理

MCP 将请求生命周期视为一个**有限状态自动机**，任何一个请求在任意时间点都处于某一标准状态，并根据执行结果或外部事件触发状态迁移，形成一条清晰可控的语义执行路径[(69)](https://jishuzhan.net/article/1989579845760778242)。

MCP 定义了以下生命周期阶段[(63)](https://mcp.transdocs.org/specification/2025-06-18/basic/lifecycle)：



1. **初始化阶段（Initialization）**：功能协商和协议版本达成一致

2. **正常操作阶段（Normal Operation）**：进行正常的协议通信，双方都遵守协商好的功能

3. **关闭阶段（Shutdown）**：优雅地终止连接

在关闭阶段，客户端会发送断开连接通知，服务器关闭连接并清理相关资源。这种优雅的关闭机制确保了数据的完整性和系统的稳定性。

### 3.5 错误处理机制

MCP 定义了标准的错误代码体系，包括标准 JSON-RPC 错误代码和 MCP 特定的错误代码[(89)](https://mcpcn.com/docs/concepts/architecture/)：

**标准 JSON-RPC 错误代码**：



* ParseError = -32700

* InvalidRequest = -32600

* MethodNotFound = -32601

* InvalidParams = -32602

* InternalError = -32603

建议的 MCP 错误码体系采用类似 HTTP 状态码的 5 段式设计，但更细分、更语义化[(88)](https://blog.csdn.net/zhuhelong520/article/details/147465207)：



| 错误码范围  | 级别    | 描述        | 示例         |
| ------ | ----- | --------- | ---------- |
| 50000+ | 系统级别  | 内部异常、不可预期 | 50001 内部错误 |
| 40000+ | 客户端错误 | 请求错误、参数错误 | 40001 无效参数 |
| 30000+ | 重定向   | 需要进一步操作   | 30001 需要授权 |
| 20000+ | 成功    | 操作成功      | 20000 操作成功 |
| 10000+ | 信息    | 通知性消息     | 10001 资源更新 |

错误响应的 JSON 格式示例：



```
{

 "jsonrpc": "2.0",

 "id": 1,

 "error": {

   "code": -32601,

   "message": "Method not found",

   "data": {

     "method": "unknown\_method"

   }

 }

}
```

## 四、MCP 技术代码实现分析

### 4.1 Python SDK 实现示例

MCP Python SDK 提供了完整的 MCP 协议实现，支持构建 MCP 客户端和服务器，使用标准传输如 stdio 和 SSE，处理所有 MCP 协议消息和生命周期事件。

#### 4.1.1 MCP 服务器实现

MCP 服务器遵循装饰器方式来注册 MCP 原语（如资源、提示和工具）的处理函数，目标是为向 LLM 客户端暴露功能提供简单接口。

**示例：创建一个简单的 MCP 服务器**



```
from mcp.server import MCPServer, types

\# 创建MCP服务器实例

server = MCPServer("example-server")

\# 注册提示（Prompt）原语

@server.prompt()

def example\_prompt() -> types.Prompt:

   return types.Prompt(

       name="example-prompt",

       description="An example prompt template",

       arguments=\[

           types.PromptArgument(

               name="arg1",

               description="Example argument",

               required=True

           )

       ]

   )

\# 注册工具（Tool）原语

@server.tool()

def greet(name: str) -> str:

   """Say hello to someone"""

   return f"Hello, {name}!"

\# 注册资源（Resource）原语

@server.resource("example://{resource\_id}")

def get\_resource(resource\_id: str) -> str:

   """Get content of a resource by ID"""

   return f"Resource content for ID: {resource\_id}"

\# 启动服务器（使用stdio传输）

if \_\_name\_\_ == "\_\_main\_\_":

   server.run(transport="stdio")
```

#### 4.1.2 MCP 客户端实现

MCP 客户端可以连接到任何 MCP 服务器，发送请求并处理响应。

**示例：创建 MCP 客户端**



```
from mcp.client import MCPClient

import asyncio

async def main():

   # 创建MCP客户端，连接到本地服务器

   client = MCPClient("http://localhost:8080")

  

   # 初始化连接

   await client.initialize()

  

   # 列出服务器支持的工具

   tools = await client.list\_tools()

   print("Available tools:", tools)

  

   # 调用greet工具

   result = await client.call\_tool("greet", {"name": "Alice"})

   print("Tool call result:", result)

  

   # 获取提示信息

   prompt = await client.get\_prompt("example-prompt", {"arg1": "value"})

   print("Prompt details:", prompt)

  

   # 读取资源

   resource = await client.read\_resource("example://123")

   print("Resource content:", resource)

  

   # 关闭连接

   await client.shutdown()

if \_\_name\_\_ == "\_\_main\_\_":

   asyncio.run(main())
```

#### 4.1.3 使用装饰器注册原语的优势

MCP Python SDK 使用装饰器方式注册原语的主要优势包括：



1. **代码简洁性**：通过装饰器语法，代码更加简洁易读

2. **类型安全**：使用类型注解确保参数类型正确

3. **自动文档生成**：函数文档字符串自动转换为原语描述

4. **错误检查**：SDK 会自动检查原语定义的完整性

### 4.2 TypeScript/JavaScript 实现示例

TypeScript 实现使用官方 SDK，提供了与 Python 类似的功能。

#### 4.2.1 MCP 服务器实现（TypeScript）



```
import { McpServer, ResourceTemplate } from "@modelcontextprotocol/sdk/server/mcp.js";

import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";

// 创建MCP服务器

const server = new McpServer({ name: "Demo", version: "1.0.0" });

// 注册工具

server.registerTool("greet", {

   description: "Say hello to someone",

   parameters: {

       name: {

           type: "string",

           description: "Name of the person to greet",

           required: true

       }

   },

   execute: async (args) => {

       return \`Hello, \${args.name}!\`;

   }

});

// 注册资源

server.registerResource("example://{resourceId}", {

   description: "Get resource content by ID",

   parameters: {

       resourceId: {

           type: "string",

           description: "Resource ID to retrieve"

       }

   },

   read: async (args) => {

       return {

           contentType: "text/plain",

           content: \`Resource content for ID: \${args.resourceId}\`

       };

   }

});

// 启动服务器（使用stdio传输）

const transport = new StdioServerTransport();

await server.start(transport);
```

#### 4.2.2 MCP 客户端实现（JavaScript）



```
const { McpClient } = require("@modelcontextprotocol/sdk/client/mcp.js");

const { SseClientTransport } = require("@modelcontextprotocol/sdk/client/sse.js");

async function main() {

   // 创建MCP客户端，使用SSE传输连接到服务器

   const transport = new SseClientTransport("http://localhost:8080");

   const client = new McpClient("client-1", "1.0.0", transport);

  

   // 连接到服务器

   await client.connect();

  

   // 列出工具

   const tools = await client.listTools();

   console.log("Available tools:", tools);

  

   // 调用工具

   const result = await client.callTool("greet", { name: "Bob" });

   console.log("Tool result:", result);

  

   // 关闭连接

   await client.disconnect();

}

main().catch(console.error);
```

### 4.3 Java 实现示例

Java 实现使用 Spring AI 框架，提供了基于注解的 MCP 服务器开发方式。

#### 4.3.1 MCP 服务器实现（Java）



```
import org.springframework.stereotype.Component;

import org.springframework.ai.mcp.annotation.McpServer;

import org.springframework.ai.mcp.annotation.McpTool;

import org.springframework.ai.mcp.annotation.McpResource;

// 创建MCP服务器

@McpServer("java-example-server")

@Component

public class JavaExampleServer {

  

   // 注册工具

   @McpTool(description = "Say hello to someone")

   public String greet(

       @McpToolParam(description = "Name of the person to greet", required = true)

       String name

   ) {

       return "Hello, " + name + "!";

   }

  

   // 注册资源

   @McpResource(uri = "example://{resourceId}", description = "Get resource content by ID")

   public String getResource(

       @McpResourceParam(description = "Resource ID to retrieve")

       String resourceId

   ) {

       return "Resource content for ID: " + resourceId;

   }

}
```

#### 4.3.2 MCP 客户端实现（Java）



```
import org.springframework.ai.mcp.client.McpClient;

import org.springframework.ai.mcp.client.McpClientBuilder;

import org.springframework.http.HttpStatus;

public class JavaExampleClient {

  

   public static void main(String\[] args) {

       // 创建MCP客户端

       McpClient client = McpClientBuilder.builder()

           .serverUrl("http://localhost:8080")

           .build();

      

       // 调用工具

       String result = client.callTool("greet",

           Map.of("name", "Charlie"),

           String.class

       );

      

       System.out.println("Tool result: " + result);

      

       // 读取资源

       String resource = client.readResource("example://456", String.class);

       System.out.println("Resource content: " + resource);

      

       // 关闭客户端

       client.shutdown();

   }

}
```

### 4.4 Go 实现示例

Go 语言实现提供了高性能的 MCP 服务器和客户端。

#### 4.4.1 MCP 服务器实现（Go）



```
package main

import (

       "context"

       "fmt"

       "github.com/mark3labs/mcp-go/mcp"

)

func main() {

       // 创建MCP服务器

       server := mcp.NewServer("go-example-server", "1.0.0")

      

       // 注册工具

       server.RegisterTool("greet", \&mcp.Tool{

               Description: "Say hello to someone",

               Parameters: \[]mcp.Parameter{

                       {

                               Name:        "name",

                               Description: "Name of the person to greet",

                               Type:        mcp.String,

                               Required:    true,

                       },

               },

               Execute: func(ctx context.Context, args map\[string]interface{}) (interface{}, error) {

                       name, ok := args\["name"].(string)

                       if !ok {

                               return nil, fmt.Errorf("name must be a string")

                       }

                       return fmt.Sprintf("Hello, %s!", name), nil

               },

       })

      

       // 注册资源

       server.RegisterResource("example://{resource\_id}", \&mcp.Resource{

               Description: "Get resource content by ID",

               Parameters: \[]mcp.Parameter{

                       {

                               Name:        "resource\_id",

                               Description: "Resource ID to retrieve",

                               Type:        mcp.String,

                       },

               },

               Read: func(ctx context.Context, args map\[string]interface{}) (mcp.ResourceContent, error) {

                       id, ok := args\["resource\_id"].(string)

                       if !ok {

                               return mcp.ResourceContent{}, fmt.Errorf("resource\_id must be a string")

                       }

                       return mcp.ResourceContent{

                               ContentType: "text/plain",

                               Content:     \[]byte(fmt.Sprintf("Resource content for ID: %s", id)),

                       }, nil

               },

       })

      

       // 启动服务器（使用stdio传输）

       server.Serve(context.Background(), mcp.StdioTransport())

}
```

### 4.5 代码实现规范与最佳实践

为确保 MCP 代码的质量和可维护性，建议遵循以下规范：



1. **命名规范**：

* 原语名称使用小写字母，单词间用连字符分隔（如`example-prompt`）

* 函数和方法使用驼峰命名法（如`getPrompt`）

* 参数名称使用有意义的描述性名称

1. **文档规范**：

* 每个原语必须包含清晰的描述

* 参数说明要详细，包括类型、是否必需、示例值

* 使用标准的文档注释格式

1. **错误处理规范**：

* 所有工具和资源方法都应该返回明确的错误信息

* 使用标准的错误码体系

* 避免在生产环境中返回敏感信息

1. **安全性规范**：

* 对所有输入参数进行验证和清理

* 实施适当的权限控制

* 使用安全的传输协议（HTTPS/TLS 1.3）

## 五、MCP 技术性能与安全性分析

### 5.1 性能特征分析

根据 MCP 协议性能基准测试，MCP 服务器展现出强大的并发处理能力。在持续负载测试中，**单实例 QPS 可达 1000 + 请求 / 秒**。不同传输协议的性能表现如下：



| 传输协议            | 平均延迟 | 最大 QPS | 内存占用 |
| --------------- | ---- | ------ | ---- |
| HTTP/1.1        | 45ms | 850    | 中等   |
| Streamable HTTP | 35ms | 1200   | 较低   |
| SSE             | 55ms | 700    | 较高   |

然而，不同编程语言实现之间存在显著的性能差异。在 390 万次请求、三轮独立测试的结果中，不同语言之间的性能差距达到数量级级别 —— 某些场景下甚至相差 93 倍。

**性能瓶颈分析**显示，主要的性能限制因素包括：



1. **序列化 / 反序列化开销**（影响权重 35%）：CPU 密集型操作，占用大量计算资源

2. **并发控制冲突**（影响权重 25%）：锁竞争导致线程阻塞，降低系统并发度

为了优化性能，建议采用以下策略：



* 使用**Streamable HTTP**传输，相比 HTTP + SSE 具有更好的稳定性，在高并发场景下表现更优，响应时间更短且更稳定

* 优化 JSON 序列化库，选择高性能的实现

* 采用连接池技术，减少连接建立的开销

* 使用异步处理模型，提高并发处理能力

### 5.2 安全性机制分析

MCP 协议在设计之初就将安全性作为核心考量，实现了多层次的安全防护机制。

#### 5.2.1 传输层安全

MCP 强制要求所有通信使用**TLS 1.3 加密传输**，禁止明文 HTTP。这确保了数据在传输过程中的机密性和完整性，防止中间人攻击和数据嗅探。

在高安全场景（如金融领域），MCP 支持**双向认证（mTLS）**，要求 Client 和 Server 互相验证证书，防止伪造客户端或服务器。

#### 5.2.2 身份认证机制

MCP 实现了强身份认证机制，主要包括：



1. **双向认证**：使用 OAuth 2.0 或 HMAC 确保身份真实性。MCP 请求必须经过强身份认证，防止未授权客户端冒充 Agent。Agent 启动时从 secrets manager 获取 token，Server 用相同 key 重新计算，比对是否一致。

2. **密码学客户端身份验证**：通过 RFC 7591 软件声明或客户端 ID 元数据文档进行强制性安全配置文件验证，防止未经授权的客户端注册和通过动态客户端注册滥用进行的身份冒充攻击。

3. **能力声明的密码学证明**：MCP Server 在接入 Host 时，需提交包含工具能力、开发者信息、安全资质的数字证书，通过非对称加密算法完成能力真实性验证，杜绝恶意 Server 伪装。

#### 5.2.3 消息完整性保护

MCP 实现了双向消息认证与完整性保护，对 Host 与 Server 之间的所有交互消息进行加密签名，确保消息来源合法、内容未被篡改，防范中间人攻击与 Server 端 Prompt 注入。

安全机制的技术架构图：



```
Client                          Server

  ↓                               ↓

  ├── TLS 1.3 Encryption          ├── TLS 1.3 Encryption

  ├── HMAC Authentication         ├── HMAC Authentication

  ├── JSON-RPC Message            ├── JSON-RPC Message

  └── Digital Signature           └── Digital Signature
```

### 5.3 权限管理与审计机制

#### 5.3.1 权限管理

MCP 采用 \*\*"零信任" 模型 \*\*，Server 在初始化时声明所需权限（如文件读 / 写），用户明确授权后才可连接。权限管理遵循以下原则：



1. **最小权限原则**：每个 Server 只拥有完成其任务所需的最小权限

2. **细粒度控制**：可以对不同的资源、工具设置不同的访问权限

3. **动态授权**：根据上下文和用户身份动态调整权限

#### 5.3.2 审计机制

MCP 实现了完善的审计机制，包括：



1. **结构化审计日志**：为所有 MCP 操作、工具执行及安全事件实施详细且可搜索的日志记录

2. **实时安全监控**：部署 SIEM 系统，结合 AI 驱动的异常检测，专为 MCP 工作负载设计

3. **事件响应整合**：将日志系统连接至自动化事件响应工作流

### 5.4 安全最佳实践

根据 MCP 安全最佳实践指南（2025 年版），实施 MCP 系统时应遵循以下关键安全措施：



1. **输入验证与净化**：

* 验证并净化所有输入，防止注入攻击、混淆代理问题以及提示注入漏洞

* 对所有工具参数及 API 输入实施严格的 JSON 架构验证

* 使用 Microsoft Prompt Shields 及 Azure Content Safety 过滤提示和响应中的恶意内容

1. **认证与授权卓越**：

* 委派认证给已建立的身份提供者（如 Microsoft Entra ID、OAuth 2.1 提供者），避免自行实现认证

* 依最小权限原则实施细分且针对工具的权限

* 使用短时效存取令牌，搭配安全旋转与适当受众验证

* 对所有管理与敏感操作要求多因素认证（MFA）

1. **进阶速率限制与资源保护**：

* 在用户、会话、工具及资源层面实施速率限制，防止滥用

* 使用基于机器学习的速率限制，动态调整使用模式与威胁指标

* 设定适当的计算资源、记忆体用量及执行时间限制

* 部署全面的分布式阻断服务防护与流量分析系统

1. **安全存储实践**：

* 重要密码学操作采用 HSM 支持的金钥存储（如 Azure Key Vault、AWS CloudHSM）

* 妥善实施金钥旋转、分离与存取管控

* 将所有 API 金钥、令牌与凭证存放于专用的秘密管理系统

### 5.5 安全风险评估与应对

尽管 MCP 提供了多层次的安全保护，但仍存在一些潜在风险需要关注：



1. **工具投毒攻击（TPA）**：恶意工具可能在返回结果中注入恶意代码或敏感信息

2. **中间人攻击**：虽然有 TLS 保护，但仍需防范证书伪造等攻击

3. **权限提升攻击**：通过漏洞利用提升权限，访问未授权的资源

4. **数据泄露风险**：敏感数据可能通过不当的日志记录或错误处理泄露

针对这些风险，建议采取以下应对措施：



* 实施严格的工具签名和验证机制

* 定期进行安全审计和漏洞扫描

* 建立完善的安全事件响应机制

* 对敏感数据实施额外的加密保护

## 六、MCP 技术应用案例与发展趋势

### 6.1 行业应用案例

MCP 技术在多个行业已经取得了显著的应用成果，展现出强大的实用价值。

#### 6.1.1 金融行业应用

在金融领域，MCP 技术的应用带来了革命性的变化。**招商银行智能风控引擎**接入 MCP 后，实现了 10 + 外部数据源（征信、舆情、交易记录）的实时对接，风险识别准确率提升 22%，欺诈案件减少 40%。

某股份制银行将 TextIn MCP Server 与大模型结合，构建了智能信贷审批系统：



* **合同解析**：自动提取借款合同中的金额、期限、担保条款等关键信息，处理时间从 2 小时缩短至 15 分钟

* **风险识别**：通过语义分析识别合同中的法律风险条款，辅助信贷经理决策，风险识别准确率提升至 98%

* **文档生成**：根据审批结果自动生成贷后管理报告，报告生成效率提升 80%

在量化交易领域，某量化基金使用 MCP 实现了高频交易优化：



* 微秒级市场数据分析（延迟＜50μs）

* 动态调整对冲策略（每秒处理 10 万 + 订单）

* 年化收益提升 23%，回撤降低 18%

#### 6.1.2 制造业应用

在智能制造领域，MCP 技术与工业物联网深度融合。某汽车焊装线的应用案例显示：



* 部署 200 + 边缘计算节点

* 集成 5000 + 份维修手册

* 成效：故障响应时间从 4 小时缩短至 15 分钟，MTBF（平均故障间隔时间）提升 40%

在半导体制造领域，某企业的光刻机系统通过 MCP 实时同步 ASML 官方知识库，实现异常代码自动解析（覆盖 98% 错误类型），非计划停机减少 67%。

#### 6.1.3 电商行业应用

百度在其电商平台 "百度优选" 上部署了国内首个 MCP 驱动的全自动购物链路，解决了传统 AI 导购 "只看不买" 的痛点：



* **智能视觉导购**：用户上传服装图片，AI 通过 MCP 调用多模态解析服务推荐相似商品

* **自动交易执行**：AI 直接对接支付网关完成下单、结算全流程

* **MCP 服务器**：部署在百度云，封装图像识别、支付、物流等功能

#### 6.1.4 教育行业应用

某教育科技公司通过 MCP 接入 LMS 系统和课堂录屏分析工具，取得了显著成效：



* 个性化学习路径生成速度从 15 分钟压缩至 40 秒

* 知识点掌握率提升 25%

### 6.2 技术发展趋势

#### 6.2.1 智能化程度升级

未来的 MCP 协议将突破现有工具调用的局限，向 **"主动服务"** 进化。通过引入强化学习机制，MCP 客户端能够观察用户行为模式，预测潜在需求。

下一代 MCP 协议的发展方向包括：



1. **多模态交互融合**：整合语音、手势、眼动追踪等交互方式，实现更加自然的人机交互

2. **分布式计算革命**：MCP 协议正在推动 "边缘智能" 的普及，在设备端部署轻量化 MCP 节点，实现毫秒级响应

3. **AI 智能体市场**：MCP 协议将催生 "AI 智能体市场"，各种专业化的 AI 智能体可以像 APP 一样被轻松安装和使用

#### 6.2.2 技术演进路线图

根据 MCP 工作组公布的 2.0 路线图，未来的技术发展重点包括：



| 时间节点   | 技术重点     | 核心特性                              |
| ------ | -------- | --------------------------------- |
| 2025Q4 | 边缘计算支持   | 在本地设备部署轻量化 MCP 节点，实现知识库的离线访问与实时同步 |
| 2026Q2 | 量子加密传输   | 采用量子加密技术，提供无条件安全的通信通道             |
| 2027   | 神经符号系统集成 | 结合神经网络的感知能力和符号系统的推理能力             |

#### 6.2.3 多模态扩展

下一代 MCP 协议草案显示，规范将增加对图像、视频等非结构化数据的支持。这意味着 MCP 将支持文本、图像、语音、视频的混合检索，实现跨模态语义对齐（如 "展示 2024 年 Q3 财报中的增长曲线"）。

### 6.3 生态建设与标准化进展

截至 2025 年 12 月，MCP 生态系统已经取得了巨大成功：



* 通过 Linux 基金会旗下的 AI Agent Foundation（AAIF）实现标准化管理

* 获得 OpenAI、微软、谷歌、亚马逊等 30 余家科技巨头的支持

* 全球公开 MCP 服务器数量超过 10,000 个

* SDK 月下载量突破 9700 万次

* 成为 AI 代理生态的 "USB-C 接口"

从 GitHub 上的开源项目到阿里云、腾讯云的商业化实践，MCP 协议正在重塑 AI 应用开发范式。未来，MCP 有望成为连接 AI 模型与现实世界的神经网络，推动人工智能技术进入真正的 "增强智能" 时代。

### 6.4 面临的挑战与机遇

#### 6.4.1 技术挑战



1. **协议普及度**：MCP 作为新兴协议，仍需时间推动行业广泛采纳

2. **生态建设**：需要更多高质量的服务器、客户端和工具集成

3. **性能优化**：在大规模数据和高并发场景下，需持续优化协议性能

4. **安全防护**：标准化接口也带来新的安全挑战，需要完善的权限和审计机制

#### 6.4.2 发展机遇



1. **市场需求爆发**：随着 AI 应用的普及，对标准化接口的需求急剧增长

2. **技术成熟度提升**：各大厂商的支持加速了技术的成熟和标准化

3. **跨行业应用**：从开发工具到企业应用，MCP 的应用场景不断扩展

4. **商业模式创新**：MCP 有望催生新的 AI 服务市场和商业模式

## 七、总结与展望

### 7.1 技术总结

通过对 MCP（Model Context Protocol）技术的深度分析，我们可以得出以下核心结论：

**技术定位明确**：MCP 是由 Anthropic 公司于 2024 年 11 月 25 日开源的开放标准协议，旨在解决大型语言模型与外部数据源、工具集成的碎片化问题。它被定位为 AI 领域的 "USB-C 接口"，通过标准化协议实现 AI 模型与外部世界的无缝连接。

**架构设计精巧**：MCP 采用客户端 - 主机 - 服务器三层架构，基于 JSON-RPC 2.0 规范，通过三种核心原语（提示、资源、工具）实现模型与上下文的交互。这种设计继承了 LSP 的思想，同时创新性地支持 Agent 主动发起的工作流。

**运行机制完善**：从严格的初始化流程（类似三次握手）到灵活的消息交换机制，从多种传输方式支持到完善的错误处理体系，MCP 建立了一套完整、可靠的运行机制。

**实现生态丰富**：目前已拥有 Python、TypeScript、Java、Go 等多种语言的 SDK 实现，支持 stdio、SSE HTTP 等传输方式，为不同场景提供了灵活的选择。

**性能安全并重**：单实例可支持 1000+ QPS 的并发处理能力，同时通过 TLS 1.3 加密、双向认证、权限管理等机制确保了系统的安全性。

### 7.2 发展展望

展望未来，MCP 技术的发展将呈现以下趋势：

**技术演进方向**：



1. 智能化程度不断提升，从被动响应向主动服务进化

2. 多模态交互能力增强，支持文本、图像、语音、视频的混合处理

3. 边缘计算深度融合，实现更快速、更智能的本地处理

4. 量子加密等新技术的引入，提供更高等级的安全保障

**应用场景拓展**：



1. 从开发工具到企业应用，MCP 将渗透到更多行业和领域

2. 智能体市场的形成，各类专业化 AI 智能体将通过 MCP 实现互联互通

3. 与物联网、5G/6G 等技术的结合，开创全新的智能应用场景

**生态系统成熟**：



1. 标准化进程加速，更多厂商和组织将加入 MCP 生态

2. 开发工具和框架的完善，降低 MCP 应用的开发门槛

3. 商业模式的创新，基于 MCP 的新型 AI 服务将不断涌现

### 7.3 对读者的建议

对于不同类型的读者，我们提出以下建议：

**对于技术决策者**：



* 将 MCP 作为企业 AI 战略的重要组成部分，提前布局标准化能力

* 评估现有系统与 MCP 的兼容性，制定逐步迁移计划

* 关注 MCP 生态的发展动态，及时把握技术红利

**对于技术架构师**：



* 深入理解 MCP 的设计理念和架构原则，将其融入系统设计

* 评估不同传输方式和编程语言实现的优劣，选择最适合的技术栈

* 重视安全性设计，确保 MCP 集成不会带来新的安全风险

**对于开发工程师**：



* 熟练掌握至少一种 MCP SDK，能够快速开发 MCP 客户端和服务器

* 遵循代码规范和最佳实践，确保代码质量和可维护性

* 积极参与 MCP 社区，贡献代码和最佳实践

**对于研究者**：



* 关注 MCP 与其他 AI 技术（如 RAG、多模态模型）的结合研究

* 探索 MCP 在特定领域的创新应用

* 参与 MCP 标准的制定和完善工作

MCP 技术的出现标志着 AI 应用开发进入了一个新的阶段。通过标准化的协议和接口，开发者可以更专注于业务逻辑的实现，而不必重复解决与外部系统集成的问题。随着技术的不断成熟和生态的日益完善，MCP 有望成为 AI 时代最重要的基础设施之一，为人工智能技术的广泛应用和创新发展奠定坚实基础。

根据行业预测，到 2027 年，85% 的企业知识库将采用 MCP 协议实现智能化升级。这场由 MCP 引领的技术变革，将重塑整个 AI 产业的格局，推动人类社会向更加智能的未来迈进。

**参考资料**

\[1] AI的“万能插头” BAT全面支持MCP\_中经TMT[ http://m.toutiao.com/group/7494818210803139113/?upstream\_biz=doubao](http://m.toutiao.com/group/7494818210803139113/?upstream_biz=doubao)

\[2] 大厂竞相押注的MCP是啥?\_南方周末[ http://m.toutiao.com/group/7503620603241316874/?upstream\_biz=doubao](http://m.toutiao.com/group/7503620603241316874/?upstream_biz=doubao)

\[3] AI上演权力游戏，MCP与A2A筑起“小院高墙”?[ https://m.thepaper.cn/newsDetail\_forward\_30638710](https://m.thepaper.cn/newsDetail_forward_30638710)

\[4] 爆火的MCP，凭什么让巨头纷纷入局?\_光明网[ http://m.toutiao.com/group/7499055095729308175/?upstream\_biz=doubao](http://m.toutiao.com/group/7499055095729308175/?upstream_biz=doubao)

\[5] 腾易科技发布汽车领域MCP服务矩阵，与百度，华为，荣耀AI生态平台全面对接-新华网[ http://www.news.cn/tech/20250806/2ddcf70ebb3749b9bd69fda8ddc56461/c.html](http://www.news.cn/tech/20250806/2ddcf70ebb3749b9bd69fda8ddc56461/c.html)

\[6] 国内首家!百度智能云千帆已率先兼容MCP\_光明网[ http://m.toutiao.com/group/7488574478747468351/?upstream\_biz=doubao](http://m.toutiao.com/group/7488574478747468351/?upstream_biz=doubao)

\[7] MCP，AI时代的“书同文，车同轨”\_21世纪经济报道[ http://m.toutiao.com/group/7502058753270759971/?upstream\_biz=doubao](http://m.toutiao.com/group/7502058753270759971/?upstream_biz=doubao)

\[8] MCP 协议规范[ https://mcp.programnotes.cn/specification](https://mcp.programnotes.cn/specification)

\[9] MCP到底是什么?\_MCPFlow-MCP技术社区[ https://mcp.csdn.net/682bfcf001ee522510976a13.html](https://mcp.csdn.net/682bfcf001ee522510976a13.html)

\[10] 一文掌握 MCP 上下文协议:从理论到实践-阿里云开发者社区[ https://developer.aliyun.com/article/1659874](https://developer.aliyun.com/article/1659874)

\[11] Claude MCP - 模型上下文协议[ https://mcp.programnotes.cn/](https://mcp.programnotes.cn/)

\[12] Model Context Protocol(MCP)深度解析\_MCPFlow-MCP技术社区[ https://mcp.csdn.net/681c0dd4c89bb164988e0941.html](https://mcp.csdn.net/681c0dd4c89bb164988e0941.html)

\[13] MCP构建大模型连接外部工具的统一标准接口-开发者社区-阿里云[ https://developer.aliyun.com/article/1660724](https://developer.aliyun.com/article/1660724)

\[14] 释放大模型潜力:Model Context Protocol 引领 API 开发新纪元-腾讯云开发者社区-腾讯云[ https://cloud.tencent.com/developer/article/2498563](https://cloud.tencent.com/developer/article/2498563)

\[15] Introducing the Model Context Protocol \ Anthropic[ https://www.anthropic.com/news/model-context-protocol](https://www.anthropic.com/news/model-context-protocol)

\[16] MCP协议发展历程与里程碑深度解析\_算法\_百态老人-火山引擎 ADG 社区[ https://adg.csdn.net/69708099437a6b40336a76e7.html](https://adg.csdn.net/69708099437a6b40336a76e7.html)

\[17] MCP (Model Context Protocol) 发展史大事年表\_mcp协议发展历程时间图-CSDN博客[ https://blog.csdn.net/weixin\_43870191/article/details/155238591](https://blog.csdn.net/weixin_43870191/article/details/155238591)

\[18] MCP协议推动AI工具标准化与自主智能应用普及[ https://www.iesdouyin.com/share/video/7484875450158681402/?region=\&mid=7484875402939763507\&u\_code=0\&did=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&iid=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&with\_sec\_did=1\&video\_share\_track\_ver=\&titleType=title\&share\_sign=P9xbmYRkQzb02jDVmfLTQsqviY1Ia6UJ9qTCbh1NczI-\&share\_version=280700\&ts=1773319856\&from\_aid=1128\&from\_ssr=1\&share\_track\_info=%7B%22link\_description\_type%22%3A%22%22%7D](https://www.iesdouyin.com/share/video/7484875450158681402/?region=\&mid=7484875402939763507\&u_code=0\&did=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&iid=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&with_sec_did=1\&video_share_track_ver=\&titleType=title\&share_sign=P9xbmYRkQzb02jDVmfLTQsqviY1Ia6UJ9qTCbh1NczI-\&share_version=280700\&ts=1773319856\&from_aid=1128\&from_ssr=1\&share_track_info=%7B%22link_description_type%22%3A%22%22%7D)

\[19] 模型上下文协议(MCP):演进历程、功能特性与Peta的崛起-CSDN博客[ https://blog.csdn.net/powerjuly/article/details/158231557](https://blog.csdn.net/powerjuly/article/details/158231557)

\[20] mcp技术综述:ai与外部世界的标准化连接器[ https://blog.csdn.net/qiwsir/article/details/156306500](https://blog.csdn.net/qiwsir/article/details/156306500)

\[21] 现代 软件 开发者 斯坦福 CS 146 S 课程 第四 讲 # 小 工蚁 # mcp # 斯坦福 课程 # 和 AI 一起 写 代码[ https://www.iesdouyin.com/share/video/7612632803213167910/?region=\&mid=7612632851229526793\&u\_code=0\&did=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&iid=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&with\_sec\_did=1\&video\_share\_track\_ver=\&titleType=title\&share\_sign=teOdhv8SCso1sMr9\_cWTslQucEdAsAx3RoDdjX9wwsY-\&share\_version=280700\&ts=1773319856\&from\_aid=1128\&from\_ssr=1\&share\_track\_info=%7B%22link\_description\_type%22%3A%22%22%7D](https://www.iesdouyin.com/share/video/7612632803213167910/?region=\&mid=7612632851229526793\&u_code=0\&did=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&iid=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&with_sec_did=1\&video_share_track_ver=\&titleType=title\&share_sign=teOdhv8SCso1sMr9_cWTslQucEdAsAx3RoDdjX9wwsY-\&share_version=280700\&ts=1773319856\&from_aid=1128\&from_ssr=1\&share_track_info=%7B%22link_description_type%22%3A%22%22%7D)

\[22] 一口气讲清楚:FC、MCP、A2A-腾讯云开发者社区-腾讯云[ https://cloud.tencent.com/developer/article/2519584](https://cloud.tencent.com/developer/article/2519584)

\[23] MCP 模型上下文协议-腾讯云开发者社区-腾讯云[ https://cloud.tencent.cn/developer/article/2507289](https://cloud.tencent.cn/developer/article/2507289)

\[24] Model Context Protocol[ https://mlops.community/model-context-protocol/](https://mlops.community/model-context-protocol/)

\[25] 大模型三大核心技术:Agent、MCP与Function Call的赋能逻辑与实践指南\_agent mcp 大模型-CSDN博客[ https://blog.csdn.net/weixin\_59191169/article/details/152002723](https://blog.csdn.net/weixin_59191169/article/details/152002723)

\[26] 部署通义千问3+MCP-AI智能体开发-技术解决方案-阿里云[ https://www.aliyun.com/solution/tech-solution/mcp-agent](https://www.aliyun.com/solution/tech-solution/mcp-agent)

\[27] MCP:解锁AI与现实世界交互新范式在人工智能飞速发展的今天，大模型的能力边界不断被刷新。然而，一个核心问题始终困扰开发 - 掘金[ https://juejin.cn/post/7501205056948338724](https://juejin.cn/post/7501205056948338724)

\[28] MCP标准化机制推动AI落地现实任务执行[ https://www.iesdouyin.com/share/video/7521382333509864723/?region=\&mid=7521382417605643049\&u\_code=0\&did=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&iid=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&with\_sec\_did=1\&video\_share\_track\_ver=\&titleType=title\&share\_sign=xBkXpms7kFXYQ\_xcoyinr4FH.9diapS1aNDm86eQsAQ-\&share\_version=280700\&ts=1773319867\&from\_aid=1128\&from\_ssr=1\&share\_track\_info=%7B%22link\_description\_type%22%3A%22%22%7D](https://www.iesdouyin.com/share/video/7521382333509864723/?region=\&mid=7521382417605643049\&u_code=0\&did=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&iid=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&with_sec_did=1\&video_share_track_ver=\&titleType=title\&share_sign=xBkXpms7kFXYQ_xcoyinr4FH.9diapS1aNDm86eQsAQ-\&share_version=280700\&ts=1773319867\&from_aid=1128\&from_ssr=1\&share_track_info=%7B%22link_description_type%22%3A%22%22%7D)

\[29] MCP - Model Context Protocol大模型时代的互联互通新标准-腾讯云开发者社区-腾讯云[ https://cloud.tencent.com.cn/developer/article/2516186](https://cloud.tencent.com.cn/developer/article/2516186)

\[30] 别再只听说 AI!一文搞懂 AIGC、Agent、MCP，小白也能上手学大模型\_mcp center-CSDN博客[ https://blog.csdn.net/weixin\_72959097/article/details/152084909](https://blog.csdn.net/weixin_72959097/article/details/152084909)

\[31] Model Context Protocol(MCP):AI集成的新基石在人工智能领域，特别是大型语言模型的应用中，如何 - 掘金[ https://juejin.cn/post/7483449728394248204](https://juejin.cn/post/7483449728394248204)

\[32] 详解模型上下文协议MCP(二)MCP能否撼动甚至颠覆Function Call的地位?目前跟“MCP”类似的大模型协议有哪些?\_和mcp类似的有什么-CSDN博客[ https://blog.csdn.net/star\_nwe/article/details/147162458](https://blog.csdn.net/star_nwe/article/details/147162458)

\[33] 手写LSP MCP消除大模型幻觉，让AI-IDE真正理解代码，打通LSP与AI的任督二脉阅读本文你将学会:LSP、MCP - 掘金[ https://juejin.cn/post/7533474784086392858](https://juejin.cn/post/7533474784086392858)

\[34] MCP协议简化AI与多数据源集成[ https://www.iesdouyin.com/share/video/7525810327709388091/?region=\&mid=7525810280920648482\&u\_code=0\&did=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&iid=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&with\_sec\_did=1\&video\_share\_track\_ver=\&titleType=title\&share\_sign=nVhBg5EsCnISFvE21r8HOdNbadXEx.tnQ6qNjfkh9iA-\&share\_version=280700\&ts=1773319867\&from\_aid=1128\&from\_ssr=1\&share\_track\_info=%7B%22link\_description\_type%22%3A%22%22%7D](https://www.iesdouyin.com/share/video/7525810327709388091/?region=\&mid=7525810280920648482\&u_code=0\&did=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&iid=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&with_sec_did=1\&video_share_track_ver=\&titleType=title\&share_sign=nVhBg5EsCnISFvE21r8HOdNbadXEx.tnQ6qNjfkh9iA-\&share_version=280700\&ts=1773319867\&from_aid=1128\&from_ssr=1\&share_track_info=%7B%22link_description_type%22%3A%22%22%7D)

\[35] 模型上下文协议(MCP):演进历程、功能特性与Peta的崛起-CSDN博客[ https://blog.csdn.net/powerjuly/article/details/158231557](https://blog.csdn.net/powerjuly/article/details/158231557)

\[36] 关于MCP最值得看的一篇:MCP创造者聊MCP的起源、架构优势和未来 - 智源社区[ https://hub.baai.ac.cn/view/45132](https://hub.baai.ac.cn/view/45132)

\[37] 旁听斯坦福的AI编程课(第四讲):MCP，给AI装上万能插头\_闻数起舞[ http://m.toutiao.com/group/7611714790762775040/?upstream\_biz=doubao](http://m.toutiao.com/group/7611714790762775040/?upstream_biz=doubao)

\[38] 架构 – Model Context Protocol Specification[ https://model-context-protocol.github.io/specification/architecture/](https://model-context-protocol.github.io/specification/architecture/)

\[39] 模型上下文协议 (MCP) -架构-CSDN博客[ https://blog.csdn.net/weixin\_44821345/article/details/158073250](https://blog.csdn.net/weixin_44821345/article/details/158073250)

\[40] MCP 架构全解析:Host、Client 与 Server 的协同机制\_mcp host client server-CSDN博客[ https://blog.csdn.net/gs80140/article/details/147563832](https://blog.csdn.net/gs80140/article/details/147563832)

\[41] MCP工作流程解析：核心组件与工具调用机制[ https://www.iesdouyin.com/share/video/7512021945412635916/?region=\&mid=7512022199125969700\&u\_code=0\&did=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&iid=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&with\_sec\_did=1\&video\_share\_track\_ver=\&titleType=title\&share\_sign=O4omEuQw9eZ0gkolLvPu4rZ5z7xTLAFrnCnXCF5.oGo-\&share\_version=280700\&ts=1773319885\&from\_aid=1128\&from\_ssr=1\&share\_track\_info=%7B%22link\_description\_type%22%3A%22%22%7D](https://www.iesdouyin.com/share/video/7512021945412635916/?region=\&mid=7512022199125969700\&u_code=0\&did=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&iid=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&with_sec_did=1\&video_share_track_ver=\&titleType=title\&share_sign=O4omEuQw9eZ0gkolLvPu4rZ5z7xTLAFrnCnXCF5.oGo-\&share_version=280700\&ts=1773319885\&from_aid=1128\&from_ssr=1\&share_track_info=%7B%22link_description_type%22%3A%22%22%7D)

\[42] MCP(Model Context Protocol，模型上下文协议) | 华为开发者联盟[ https://developer.huawei.com/consumer/cn/blog/topic/03206468650714195](https://developer.huawei.com/consumer/cn/blog/topic/03206468650714195)

\[43] Architecture[ https://modelcontextprotocol.info/specification/draft/architecture/](https://modelcontextprotocol.info/specification/draft/architecture/)

\[44] 【MCP协议】 架构设计模型上下文协议(MCP)采用客户端-宿主-服务端架构，单个宿主可运行多个客户端实例。该架构支持用 - 掘金[ https://juejin.cn/post/7498277142770876466](https://juejin.cn/post/7498277142770876466)

\[45] Transports[ https://modelcontextprotocol.info/docs/concepts/transports/](https://modelcontextprotocol.info/docs/concepts/transports/)

\[46] MCP 协议规范[ https://mcp.programnotes.cn/specification](https://mcp.programnotes.cn/specification)

\[47] 传输 – MCP 中文站(Model Context Protocol 中文)[ https://mcpcn.com/docs/concepts/transports/](https://mcpcn.com/docs/concepts/transports/)

\[48] 第二章:mcp协议规范与核心能力——深入AI的“USB-C”接口标准-CSDN博客[ https://blog.csdn.net/liangxh2010/article/details/153183555](https://blog.csdn.net/liangxh2010/article/details/153183555)

\[49] mcp-course/units/en/unit1/communication-protocol.mdx at main · huggingface/mcp-course · GitHub[ https://github.com/huggingface/mcp-course/blob/main/units/en/unit1/communication-protocol.mdx](https://github.com/huggingface/mcp-course/blob/main/units/en/unit1/communication-protocol.mdx)

\[50] MCP的原理以及基础应用\_mcp主机与客户端-CSDN博客[ https://blog.csdn.net/html7123/article/details/150532877](https://blog.csdn.net/html7123/article/details/150532877)

\[51] 服务器功能 – Model Context Protocol (MCP)[ https://modelcontextprotocol.info/zh-cn/specification/2025-11-25/server/](https://modelcontextprotocol.info/zh-cn/specification/2025-11-25/server/)

\[52] MCP介绍:Model Context Protocol详解\_wx65dfdaaec020c的技术博客\_51CTO博客[ https://blog.51cto.com/plcode/14503352](https://blog.51cto.com/plcode/14503352)

\[53] MCP、RAG与Agent的核心概念及协作关系解析[ https://www.iesdouyin.com/share/video/7554382963561188643/?region=\&mid=7554382932690225939\&u\_code=0\&did=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&iid=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&with\_sec\_did=1\&video\_share\_track\_ver=\&titleType=title\&share\_sign=pgPr4MywoP3ggzJ5C3leGxPy\_d0PsBuLeRaoQfD6.nY-\&share\_version=280700\&ts=1773319893\&from\_aid=1128\&from\_ssr=1\&share\_track\_info=%7B%22link\_description\_type%22%3A%22%22%7D](https://www.iesdouyin.com/share/video/7554382963561188643/?region=\&mid=7554382932690225939\&u_code=0\&did=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&iid=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&with_sec_did=1\&video_share_track_ver=\&titleType=title\&share_sign=pgPr4MywoP3ggzJ5C3leGxPy_d0PsBuLeRaoQfD6.nY-\&share_version=280700\&ts=1773319893\&from_aid=1128\&from_ssr=1\&share_track_info=%7B%22link_description_type%22%3A%22%22%7D)

\[54] MCP远程服务 - 腾讯云[ https://cloud.tencent.com/developer/mcp/server/10243](https://cloud.tencent.com/developer/mcp/server/10243)

\[55] 一文掌握 MCP 上下文协议:从理论到实践\_mcp语法-CSDN博客[ https://blog.csdn.net/2401\_85592132/article/details/154697320](https://blog.csdn.net/2401_85592132/article/details/154697320)

\[56] 深入解析模型上下文协议 (MCP):架构、流程与应用实践-CSDN博客[ https://blog.csdn.net/2302\_81075415/article/details/149963356](https://blog.csdn.net/2302_81075415/article/details/149963356)

\[57] 【愚公系列】《MCP协议与AI Agent开发》007-MCP的基本原理(MCP上下文结构与层级划分)\_agent开发 mcp ppt-CSDN博客[ https://blog.csdn.net/aa2528877987/article/details/154321359](https://blog.csdn.net/aa2528877987/article/details/154321359)

\[58] 【愚公系列】《MCP协议与AI Agent开发》010-MCP协议标准与规范体系(协议消息结构设计)\_人工智能\_愚公搬代码-火山引擎 ADG 社区[ https://adg.csdn.net/6970a0a5437a6b40336af9fe.html](https://adg.csdn.net/6970a0a5437a6b40336af9fe.html)

\[59] MCP上下文架构解析与开发实战[ https://www.iesdouyin.com/share/video/7600964726255848745/?region=\&mid=7600965320136477486\&u\_code=0\&did=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&iid=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&with\_sec\_did=1\&video\_share\_track\_ver=\&titleType=title\&share\_sign=c8FCu1aoRq\_yx7XJONBEyS4Wl4fW4IzrRCuFw5W3k3o-\&share\_version=280700\&ts=1773319892\&from\_aid=1128\&from\_ssr=1\&share\_track\_info=%7B%22link\_description\_type%22%3A%22%22%7D](https://www.iesdouyin.com/share/video/7600964726255848745/?region=\&mid=7600965320136477486\&u_code=0\&did=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&iid=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&with_sec_did=1\&video_share_track_ver=\&titleType=title\&share_sign=c8FCu1aoRq_yx7XJONBEyS4Wl4fW4IzrRCuFw5W3k3o-\&share_version=280700\&ts=1773319892\&from_aid=1128\&from_ssr=1\&share_track_info=%7B%22link_description_type%22%3A%22%22%7D)

\[60] MCP官方文档:架构概述本文档对模型上下文协议(MCP)进行概述，涵盖其应用范围、核心概念，并通过示例展示每个核心概念。 - 掘金[ https://juejin.cn/post/7536988874670784550](https://juejin.cn/post/7536988874670784550)

\[61] 一文掌握 MCP 上下文协议:从理论到实践-腾讯云开发者社区-腾讯云[ https://cloud.tencent.com.cn/developer/article/2509998](https://cloud.tencent.com.cn/developer/article/2509998)

\[62] MCP模型上下文协议-CSDN博客[ https://blog.csdn.net/weixin\_41646716/article/details/150602694](https://blog.csdn.net/weixin_41646716/article/details/150602694)

\[63] 生命周期 - Model Context Protocol | MCP 中文文档[ https://mcp.transdocs.org/specification/2025-06-18/basic/lifecycle](https://mcp.transdocs.org/specification/2025-06-18/basic/lifecycle)

\[64] MCP 协议规范[ https://mcp.programnotes.cn/specification](https://mcp.programnotes.cn/specification)

\[65] MCP框架解析大模型工具调用与协作机制[ https://www.iesdouyin.com/share/video/7504702818008223016/?region=\&mid=7504705063667960586\&u\_code=0\&did=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&iid=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&with\_sec\_did=1\&video\_share\_track\_ver=\&titleType=title\&share\_sign=R5dhJaITVf5VWNwNHjJxs75vuLijgYKe6IElGZ.zACA-\&share\_version=280700\&ts=1773319923\&from\_aid=1128\&from\_ssr=1\&share\_track\_info=%7B%22link\_description\_type%22%3A%22%22%7D](https://www.iesdouyin.com/share/video/7504702818008223016/?region=\&mid=7504705063667960586\&u_code=0\&did=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&iid=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&with_sec_did=1\&video_share_track_ver=\&titleType=title\&share_sign=R5dhJaITVf5VWNwNHjJxs75vuLijgYKe6IElGZ.zACA-\&share_version=280700\&ts=1773319923\&from_aid=1128\&from_ssr=1\&share_track_info=%7B%22link_description_type%22%3A%22%22%7D)

\[66] \[MCP系列1]大模型是如何使用MCP工具的?-从MCP协议核心架构到传输协议(一万七千字通俗详解版)-CSDN博客[ https://blog.csdn.net/qq\_33778762/article/details/147990225](https://blog.csdn.net/qq_33778762/article/details/147990225)

\[67] 一文详解模型上下文协议MCP-腾讯云开发者社区-腾讯云[ https://cloud.tencent.cn/developer/article/2514924](https://cloud.tencent.cn/developer/article/2514924)

\[68] 2026年AI开发新标准!MCP协议:快速入门手册\_弘一一[ http://m.toutiao.com/group/7611936245559706166/?upstream\_biz=doubao](http://m.toutiao.com/group/7611936245559706166/?upstream_biz=doubao)

\[69] 【愚公系列】《MCP协议与AI Agent开发》011-MCP协议标准与规范体系(交互协议与状态码体系) - 技术栈[ https://jishuzhan.net/article/1989579845760778242](https://jishuzhan.net/article/1989579845760778242)

\[70] Lifecycle[ https://modelcontextprotocol.info/specification/draft/basic/lifecycle/](https://modelcontextprotocol.info/specification/draft/basic/lifecycle/)

\[71] 别再被MCP协议绕晕!一文搞懂连接流程与核心架构-CSDN博客[ https://blog.csdn.net/Y525698136/article/details/151708015](https://blog.csdn.net/Y525698136/article/details/151708015)

\[72] MCP协议分层结构与核心功能解析[ https://www.iesdouyin.com/share/video/7567755725506710794/?region=\&mid=7567755785201699603\&u\_code=0\&did=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&iid=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&with\_sec\_did=1\&video\_share\_track\_ver=\&titleType=title\&share\_sign=JfimRtjFRwdMRPmtsXx\_gRfXIWxaeD5IQuN19mMzqfw-\&share\_version=280700\&ts=1773319923\&from\_aid=1128\&from\_ssr=1\&share\_track\_info=%7B%22link\_description\_type%22%3A%22%22%7D](https://www.iesdouyin.com/share/video/7567755725506710794/?region=\&mid=7567755785201699603\&u_code=0\&did=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&iid=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&with_sec_did=1\&video_share_track_ver=\&titleType=title\&share_sign=JfimRtjFRwdMRPmtsXx_gRfXIWxaeD5IQuN19mMzqfw-\&share_version=280700\&ts=1773319923\&from_aid=1128\&from_ssr=1\&share_track_info=%7B%22link_description_type%22%3A%22%22%7D)

\[73] 智能体 MCP 协议技术原理与应用实践[ http://www.uml.org.cn/ai/202510271.asp](http://www.uml.org.cn/ai/202510271.asp)

\[74] 手搓Manus?MCP 原理解析与MCP Client实践\_阿里云开发者[ http://m.toutiao.com/group/7494188874915267106/?upstream\_biz=doubao](http://m.toutiao.com/group/7494188874915267106/?upstream_biz=doubao)

\[75] 别再被MCP协议绕晕!一文搞懂连接流程与核心架构-CSDN博客[ https://blog.csdn.net/Y525698136/article/details/151708015](https://blog.csdn.net/Y525698136/article/details/151708015)

\[76] Lifecycle[ https://modelcontextprotocol.info/specification/draft/basic/lifecycle/](https://modelcontextprotocol.info/specification/draft/basic/lifecycle/)

\[77] 格局打开!Function Calling只是“点”，MCP是“线”，A2A才是“面”!一文讲透AI交互的升维思考!-CSDN博客[ https://blog.csdn.net/Python\_cocola/article/details/155199344](https://blog.csdn.net/Python_cocola/article/details/155199344)

\[78] MCP:基础概念、快速应用和背后原理当Claude桌面助手自动整理会议纪要、Midjourney插件实时读取本地设计稿时 - 掘金[ https://juejin.cn/post/7542798105018581030](https://juejin.cn/post/7542798105018581030)

\[79] 手搓Manus?MCP 原理解析与MCP Client实践\_腾讯新闻[ https://view.inews.qq.com/a/20250415A021WK00](https://view.inews.qq.com/a/20250415A021WK00)

\[80] 抓包理解MCP模型上下文协议 - 汇智网[ http://www.hubwiz.com/blog/understanding-model-context-protocol-through-packet-capture/](http://www.hubwiz.com/blog/understanding-model-context-protocol-through-packet-capture/)

\[81] \[MCP系列1]大模型是如何使用MCP工具的?-从MCP协议核心架构到传输协议(一万七千字通俗详解版)-CSDN博客[ https://blog.csdn.net/qq\_33778762/article/details/147990225](https://blog.csdn.net/qq_33778762/article/details/147990225)

\[82] AI生态的“USB-C接口“暗藏危机?MCP协议全解析:技术原理、运行流程与六大安全风险深度揭秘-CSDN博客[ https://blog.csdn.net/qq\_25535969/article/details/157044917](https://blog.csdn.net/qq_25535969/article/details/157044917)

\[83] MCP工作流程解析：核心组件与工具调用机制[ https://www.iesdouyin.com/share/video/7512021945412635916/?region=\&mid=7512022199125969700\&u\_code=0\&did=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&iid=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&with\_sec\_did=1\&video\_share\_track\_ver=\&titleType=title\&share\_sign=O4omEuQw9eZ0gkolLvPu4rZ5z7xTLAFrnCnXCF5.oGo-\&share\_version=280700\&ts=1773319934\&from\_aid=1128\&from\_ssr=1\&share\_track\_info=%7B%22link\_description\_type%22%3A%22%22%7D](https://www.iesdouyin.com/share/video/7512021945412635916/?region=\&mid=7512022199125969700\&u_code=0\&did=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&iid=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&with_sec_did=1\&video_share_track_ver=\&titleType=title\&share_sign=O4omEuQw9eZ0gkolLvPu4rZ5z7xTLAFrnCnXCF5.oGo-\&share_version=280700\&ts=1773319934\&from_aid=1128\&from_ssr=1\&share_track_info=%7B%22link_description_type%22%3A%22%22%7D)

\[84] 模型上下文协议(MCP):让AI真正\_看见\_互联网世界在人工智能飞速发展的今天，大语言模型(LLM)如Claude、GP - 掘金[ https://juejin.cn/post/7496029815637426195](https://juejin.cn/post/7496029815637426195)

\[85] MCP架构详解 - 《MCP赋能之道:构建下一代企业级AI自动化系统》 - 严富坤的知识库专栏(yanfukun.com)[ https://www.yanfukun.com/read/mcp/arch-detail](https://www.yanfukun.com/read/mcp/arch-detail)

\[86] Agent、Skills、MCP :AI 智能体的三层技术架构与协同原理\_高阶程序猿[ http://m.toutiao.com/group/7587245700111532570/?upstream\_biz=doubao](http://m.toutiao.com/group/7587245700111532570/?upstream_biz=doubao)

\[87] MCP (Model Context Protocol) 交互流程[ https://github.com/Jiaoding/VegetaBot/blob/develop/docs/mcp-protocol.md](https://github.com/Jiaoding/VegetaBot/blob/develop/docs/mcp-protocol.md)

\[88] MCP 错误码体系与问题排查实战:让大模型服务更可预期\_mcp的错误处理:如何优雅地处理异常-CSDN博客[ https://blog.csdn.net/zhuhelong520/article/details/147465207](https://blog.csdn.net/zhuhelong520/article/details/147465207)

\[89] 核心架构 – MCP 中文站(Model Context Protocol 中文)[ https://mcpcn.com/docs/concepts/architecture/](https://mcpcn.com/docs/concepts/architecture/)

\[90] PLCopen状态机编程核心规范与运动控制指令解析[ https://www.iesdouyin.com/share/video/7582439152319253770/?region=\&mid=7582440103050562330\&u\_code=0\&did=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&iid=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&with\_sec\_did=1\&video\_share\_track\_ver=\&titleType=title\&share\_sign=nkR8vhOrF3wYUqMfcDzX6toV3cNZcmupjXB56yInZ\_A-\&share\_version=280700\&ts=1773319950\&from\_aid=1128\&from\_ssr=1\&share\_track\_info=%7B%22link\_description\_type%22%3A%22%22%7D](https://www.iesdouyin.com/share/video/7582439152319253770/?region=\&mid=7582440103050562330\&u_code=0\&did=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&iid=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&with_sec_did=1\&video_share_track_ver=\&titleType=title\&share_sign=nkR8vhOrF3wYUqMfcDzX6toV3cNZcmupjXB56yInZ_A-\&share_version=280700\&ts=1773319950\&from_aid=1128\&from_ssr=1\&share_track_info=%7B%22link_description_type%22%3A%22%22%7D)

\[91] Docker MCP网关异常响应处理全解析(错误码深度剖析+实战修复)-CSDN博客[ https://blog.csdn.net/VarChat/article/details/156002779](https://blog.csdn.net/VarChat/article/details/156002779)

\[92] Error Handling[ https://github.com/WordPress/mcp-adapter/blob/trunk/docs/guides/error-handling.md](https://github.com/WordPress/mcp-adapter/blob/trunk/docs/guides/error-handling.md)

\[93] MCP协议:打破LLM限制的模型上下文新标准 | ceyewan[ https://ceyewan.github.io/posts/ai-agent/model-context-protocol-crash-course/](https://ceyewan.github.io/posts/ai-agent/model-context-protocol-crash-course/)

\[94] 【MCP协议】 授权机制1. 引言 1.1 目的与范围 模型上下文协议(Model Context Protocol, - 掘金[ https://juejin.cn/post/7500234308432658443](https://juejin.cn/post/7500234308432658443)

\[95] 传输 – Model Context Protocol Specification[ https://model-context-protocol.github.io/specification/basic/transports/](https://model-context-protocol.github.io/specification/basic/transports/)

\[96] 理解 MCP 的三种传输方式:stdio、SSE 与 Streamable HTTP-CSDN博客[ https://blog.csdn.net/weixin\_48321392/article/details/158502657](https://blog.csdn.net/weixin_48321392/article/details/158502657)

\[97] MCP 支持三种传输协议:stdio，http，sse详解，小学生一看都能懂stdio、http和sse这三种传输协议在 - 掘金[ https://juejin.cn/post/7538356328705769481](https://juejin.cn/post/7538356328705769481)

\[98] MCP 的 传输 方式 ， stdio 和 HTTP MCP 中 定义 了 两 类 三种 传输 方式 ， 两 类 方式 是 stdio 和 HTTP ， 三种 分别 是 stdio ， HTTP SSE 和 Stream able HTTP 。



\# mcp # 人工 智能 # AI[ https://www.iesdouyin.com/share/video/7534649730064715043/?region=\&mid=7534649857697401642\&u\_code=0\&did=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&iid=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&with\_sec\_did=1\&video\_share\_track\_ver=\&titleType=title\&share\_sign=y2SrEORV90DmoaO6t9aXhJavR7Ru8NE5jphz7RDXS7s-\&share\_version=280700\&ts=1773319950\&from\_aid=1128\&from\_ssr=1\&share\_track\_info=%7B%22link\_description\_type%22%3A%22%22%7D](https://www.iesdouyin.com/share/video/7534649730064715043/?region=\&mid=7534649857697401642\&u_code=0\&did=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&iid=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&with_sec_did=1\&video_share_track_ver=\&titleType=title\&share_sign=y2SrEORV90DmoaO6t9aXhJavR7Ru8NE5jphz7RDXS7s-\&share_version=280700\&ts=1773319950\&from_aid=1128\&from_ssr=1\&share_track_info=%7B%22link_description_type%22%3A%22%22%7D)

\[99] Transports[ https://modelcontextprotocol.info/specification/draft/basic/transports/](https://modelcontextprotocol.info/specification/draft/basic/transports/)

\[100] MCP的通信机制\_51CTO博客\_mcp原理[ https://blog.51cto.com/u\_15588078/13568462](https://blog.51cto.com/u_15588078/13568462)

\[101] MCP 传输方式，stdio、HTTP SSE 和 Streamable HTTP\_成富\_Alex[ http://m.toutiao.com/group/7540629321174532623/?upstream\_biz=doubao](http://m.toutiao.com/group/7540629321174532623/?upstream_biz=doubao)

\[102] MCP Python SDK[ https://github.com/tumf/mcp-python-sdk](https://github.com/tumf/mcp-python-sdk)

\[103] 5分钟上手MCP Python SDK:科研数据AI处理的零代码方案-CSDN博客[ https://blog.csdn.net/gitblog\_00932/article/details/152060632](https://blog.csdn.net/gitblog_00932/article/details/152060632)

\[104] 从零开始玩转MCP:手把手教你用Python搭建AI万能插头\_python\_码力金矿-MCP技术社区[ https://mcp.csdn.net/6816c595da5d787fd5d92f94.html](https://mcp.csdn.net/6816c595da5d787fd5d92f94.html)

\[105] MCP消息协议与传输模式开发实战解析[ https://www.iesdouyin.com/share/video/7588080948426181924/?region=\&mid=7588081409371032354\&u\_code=0\&did=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&iid=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&with\_sec\_did=1\&video\_share\_track\_ver=\&titleType=title\&share\_sign=A1G6rOvNmTTXLKUZsrsX05uzFeYGe0qZt0e2Y1fGUfo-\&share\_version=280700\&ts=1773319969\&from\_aid=1128\&from\_ssr=1\&share\_track\_info=%7B%22link\_description\_type%22%3A%22%22%7D](https://www.iesdouyin.com/share/video/7588080948426181924/?region=\&mid=7588081409371032354\&u_code=0\&did=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&iid=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&with_sec_did=1\&video_share_track_ver=\&titleType=title\&share_sign=A1G6rOvNmTTXLKUZsrsX05uzFeYGe0qZt0e2Y1fGUfo-\&share_version=280700\&ts=1773319969\&from_aid=1128\&from_ssr=1\&share_track_info=%7B%22link_description_type%22%3A%22%22%7D)

\[106] 客户端开发 – MCP 中文站(Model Context Protocol 中文)[ https://mcpcn.com/docs/quickstart/client/](https://mcpcn.com/docs/quickstart/client/)

\[107] Developing Your MCP Server[ https://ibm.github.io/mcp-context-forge/best-practices/developing-your-mcp-server-python/](https://ibm.github.io/mcp-context-forge/best-practices/developing-your-mcp-server-python/)

\[108] Python SDK | MQTT.AI[ https://www.emqx.com/mqtt-for-ai/mcp-over-mqtt/sdk/python/](https://www.emqx.com/mqtt-for-ai/mcp-over-mqtt/sdk/python/)

\[109] 动手学Agent应用开发(TS/JS 最简实践指南)\_node.js开发agent-CSDN博客[ https://blog.csdn.net/u014388408/article/details/157069972](https://blog.csdn.net/u014388408/article/details/157069972)

\[110] @neural-nexus/mcp-in-browser[ https://www.npmjs.com/package/@neural-nexus/mcp-in-browser](https://www.npmjs.com/package/@neural-nexus/mcp-in-browser)

\[111] 构建mcp客户端-node.js[ https://mcpcn.com/docs/tutorials/building-a-client-node/](https://mcpcn.com/docs/tutorials/building-a-client-node/)

\[112] MCP初学者指南(4)-CSDN博客[ https://blog.csdn.net/goodfornothi/article/details/148754089](https://blog.csdn.net/goodfornothi/article/details/148754089)

\[113] MCP TypeScript SDK 初体验:挑战快速搭建一个 AI 应用!-腾讯云开发者社区-腾讯云[ https://cloud.tencent.com.cn/developer/article/2513171](https://cloud.tencent.com.cn/developer/article/2513171)

\[114] ts-mcp[ https://www.npmjs.com/package/ts-mcp](https://www.npmjs.com/package/ts-mcp)

\[115] MCP (Model Context Protocol) JavaScript 开发指南[ https://github.com/zhaokang555/guozaoke-mcp-server/blob/master/mcp-development-guide.md](https://github.com/zhaokang555/guozaoke-mcp-server/blob/master/mcp-development-guide.md)

\[116] Annotation-driven MCP Java SDK[ https://github.com/thought2code/mcp-annotated-java-sdk](https://github.com/thought2code/mcp-annotated-java-sdk)

\[117] Getting Started with Model Context Protocol (MCP)[ https://docs.spring.io/spring-ai/reference/guides/getting-started-mcp.html](https://docs.spring.io/spring-ai/reference/guides/getting-started-mcp.html)

\[118] Java 实战:使用 Model Context Protocol(MCP)实现智能数据集成\_java mcp-CSDN博客[ https://blog.csdn.net/2301\_78858041/article/details/147475070](https://blog.csdn.net/2301_78858041/article/details/147475070)

\[119] Java实现MCP Server配置与使用教程[ https://www.iesdouyin.com/share/video/7496139059824282880/?region=\&mid=7496140687394491148\&u\_code=0\&did=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&iid=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&with\_sec\_did=1\&video\_share\_track\_ver=\&titleType=title\&share\_sign=fGC2JgvnNeJkjdaXYXLPIptl73AeQP5I3sb8EzsC82Y-\&share\_version=280700\&ts=1773319986\&from\_aid=1128\&from\_ssr=1\&share\_track\_info=%7B%22link\_description\_type%22%3A%22%22%7D](https://www.iesdouyin.com/share/video/7496139059824282880/?region=\&mid=7496140687394491148\&u_code=0\&did=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&iid=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&with_sec_did=1\&video_share_track_ver=\&titleType=title\&share_sign=fGC2JgvnNeJkjdaXYXLPIptl73AeQP5I3sb8EzsC82Y-\&share_version=280700\&ts=1773319986\&from_aid=1128\&from_ssr=1\&share_track_info=%7B%22link_description_type%22%3A%22%22%7D)

\[120] 【亲测免费】 Model Context Protocol Java SDK 使用教程-CSDN博客[ https://blog.csdn.net/gitblog\_00159/article/details/147006593](https://blog.csdn.net/gitblog_00159/article/details/147006593)

\[121] awesome-copilot/instructions/java-mcp-server.instructions.md at main · github/awesome-copilot · GitHub[ https://github.com/github/awesome-copilot/blob/main/instructions/java-mcp-server.instructions.md](https://github.com/github/awesome-copilot/blob/main/instructions/java-mcp-server.instructions.md)

\[122] Java开发者深度指南!用MCP接口高效集成AI能力(从入门到高阶实战)引言:为什么Java开发者需要关注MCP? 在A - 掘金[ https://juejin.cn/post/7496005453353713673](https://juejin.cn/post/7496005453353713673)

\[123] A Go implementation of the Model Context Protocol (MCP), enabling seamless integration between LLM applications and external data sources and tools.[ https://github.com/mark3labs/mcp-go/](https://github.com/mark3labs/mcp-go/)

\[124] 一文弄懂用Go实现MCP服务:从STDIO到Streamable HTTP的完整实现什么是MCP? MCP总体架构 MC - 掘金[ https://juejin.cn/post/7515386210703097919](https://juejin.cn/post/7515386210703097919)

\[125] Go-MCP：基于MCP协议的Go语言实现助力LLM[ https://www.iesdouyin.com/share/video/7493845954643217683/?region=\&mid=7493846350988167975\&u\_code=0\&did=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&iid=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&with\_sec\_did=1\&video\_share\_track\_ver=\&titleType=title\&share\_sign=bXcWSAgg2q2YiqWo8Vzjx\_qyctoJentII5S71AmoEI8-\&share\_version=280700\&ts=1773319986\&from\_aid=1128\&from\_ssr=1\&share\_track\_info=%7B%22link\_description\_type%22%3A%22%22%7D](https://www.iesdouyin.com/share/video/7493845954643217683/?region=\&mid=7493846350988167975\&u_code=0\&did=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&iid=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&with_sec_did=1\&video_share_track_ver=\&titleType=title\&share_sign=bXcWSAgg2q2YiqWo8Vzjx_qyctoJentII5S71AmoEI8-\&share_version=280700\&ts=1773319986\&from_aid=1128\&from_ssr=1\&share_track_info=%7B%22link_description_type%22%3A%22%22%7D)

\[126] MCP协议实战指南:mcp-go跨语言兼容性与性能优化深度解析-CSDN博客[ https://blog.csdn.net/gitblog\_00753/article/details/156076917](https://blog.csdn.net/gitblog_00753/article/details/156076917)

\[127] MCP Go首页、文档和下载 - MCP 的 Go 实现 - OSCHINA - 中文开源技术交流社区[ https://www.oschina.net/p/mcp-go](https://www.oschina.net/p/mcp-go)

\[128] MCP协议性能基准测试:mcp-for-beginners全面压测分析报告-CSDN博客[ https://blog.csdn.net/gitblog\_01186/article/details/152068099](https://blog.csdn.net/gitblog_01186/article/details/152068099)

\[129] Python 慢了 93 倍?!这项 MCP 基准测试震惊了开发者当你真正跨语言测量 MCP 服务器性能时，会发生什么? - 掘金[ https://juejin.cn/post/7612572336241311778](https://juejin.cn/post/7612572336241311778)

\[130] MCP 的性能瓶颈与优化:从理论分析到工业级实践-CSDN博客[ https://blog.csdn.net/lxcxjxhx/article/details/156758864](https://blog.csdn.net/lxcxjxhx/article/details/156758864)

\[131] 软件并发性能测试的核心指标与目标解析[ https://www.iesdouyin.com/share/video/7530569424911289643/?region=\&mid=7530569469376990015\&u\_code=0\&did=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&iid=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&with\_sec\_did=1\&video\_share\_track\_ver=\&titleType=title\&share\_sign=LG6qSeSo8iihMXWakJmaFN3SHUzDJ0fhtuH2ExZBXqA-\&share\_version=280700\&ts=1773319998\&from\_aid=1128\&from\_ssr=1\&share\_track\_info=%7B%22link\_description\_type%22%3A%22%22%7D](https://www.iesdouyin.com/share/video/7530569424911289643/?region=\&mid=7530569469376990015\&u_code=0\&did=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&iid=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&with_sec_did=1\&video_share_track_ver=\&titleType=title\&share_sign=LG6qSeSo8iihMXWakJmaFN3SHUzDJ0fhtuH2ExZBXqA-\&share_version=280700\&ts=1773319998\&from_aid=1128\&from_ssr=1\&share_track_info=%7B%22link_description_type%22%3A%22%22%7D)

\[132] MCP通信模型与状态管理:异步优先的分布式协议设计-CSDN博客[ https://security-hyacinth.blog.csdn.net/article/details/156560895](https://security-hyacinth.blog.csdn.net/article/details/156560895)

\[133] MCP 协议:为什么 Streamable HTTP 是最佳选择?\_阿里云云原生[ http://m.toutiao.com/group/7498247727772451347/?upstream\_biz=doubao](http://m.toutiao.com/group/7498247727772451347/?upstream_biz=doubao)

\[134] n8n MCP工具完整指南:2025年Model Context Protocol最佳实践在人工智能快速发展的2025年 - 掘金[ https://juejin.cn/post/7521654005606039561](https://juejin.cn/post/7521654005606039561)

\[135] 别让 AI “乱来”!MCP 安全实战:从认证、权限到审计全链路防护\_mcp 如何防止token泄漏后被利用-CSDN博客[ https://blog.csdn.net/sara\_han/article/details/156028034](https://blog.csdn.net/sara_han/article/details/156028034)

\[136] MCP Under the Lens: A Multi-Framework Security Analysis of the Model Context Protocol(pdf)[ https://objects.githubusercontent.com/github-production-repository-file-5c1aeb/862570523/25681261?X-Amz-Algorithm=AWS4-HMAC-SHA256\&X-Amz-Credential=AKIAVCODYLSA53PQK4ZA%2F20260308%2Fus-east-1%2Fs3%2Faws4\_request\&X-Amz-Date=20260308T035652Z\&X-Amz-Expires=300\&X-Amz-Signature=b2f6d6840b380d692ab4fdc11f7987799a4164c38d8706f4a9107fee06787c1f\&X-Amz-SignedHeaders=host\&response-content-disposition=attachment%3Bfilename%3DMCPShark\_Paper\_v2.pdf\&response-content-type=application%2Fpdf](https://objects.githubusercontent.com/github-production-repository-file-5c1aeb/862570523/25681261?X-Amz-Algorithm=AWS4-HMAC-SHA256\&X-Amz-Credential=AKIAVCODYLSA53PQK4ZA%2F20260308%2Fus-east-1%2Fs3%2Faws4_request\&X-Amz-Date=20260308T035652Z\&X-Amz-Expires=300\&X-Amz-Signature=b2f6d6840b380d692ab4fdc11f7987799a4164c38d8706f4a9107fee06787c1f\&X-Amz-SignedHeaders=host\&response-content-disposition=attachment%3Bfilename%3DMCPShark_Paper_v2.pdf\&response-content-type=application%2Fpdf)

\[137] 挑看网络安全:MCP 协议安全与智能体可信交互\_Chinado[ http://m.toutiao.com/group/7615183822334493210/?upstream\_biz=doubao](http://m.toutiao.com/group/7615183822334493210/?upstream_biz=doubao)

\[138] Teleport以身份与访问控制强化MCP安全[ https://www.iesdouyin.com/share/video/7557201848931831067/?region=\&mid=7557202000640265002\&u\_code=0\&did=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&iid=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&with\_sec\_did=1\&video\_share\_track\_ver=\&titleType=title\&share\_sign=PCRjFm0prY3hG7IepL.e717\_2ULUOLioztxRN.uuKS0-\&share\_version=280700\&ts=1773319997\&from\_aid=1128\&from\_ssr=1\&share\_track\_info=%7B%22link\_description\_type%22%3A%22%22%7D](https://www.iesdouyin.com/share/video/7557201848931831067/?region=\&mid=7557202000640265002\&u_code=0\&did=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&iid=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&with_sec_did=1\&video_share_track_ver=\&titleType=title\&share_sign=PCRjFm0prY3hG7IepL.e717_2ULUOLioztxRN.uuKS0-\&share_version=280700\&ts=1773319997\&from_aid=1128\&from_ssr=1\&share_track_info=%7B%22link_description_type%22%3A%22%22%7D)

\[139] Agent篇---MCP 安全防御指南:构建可信的 AI 连接层-CSDN博客[ https://lotus.blog.csdn.net/article/details/158745233](https://lotus.blog.csdn.net/article/details/158745233)

\[140] Shadow Escape零点击攻击:MCP协议成AI Agent“后门”，静默窃密撕开企业数据防线\_首个零点击攻击利用mcp协议通过流行ai agent静默窃取数据-CSDN博客[ https://blog.csdn.net/weixin\_42376192/article/details/154070738](https://blog.csdn.net/weixin_42376192/article/details/154070738)

\[141] MCP 安全最佳實踐 2025[ https://github.com/microsoft/mcp-for-beginners/blob/update-translations/translations/zh-HK/02-Security/mcp-best-practices.md](https://github.com/microsoft/mcp-for-beginners/blob/update-translations/translations/zh-HK/02-Security/mcp-best-practices.md)

\[142] MCP 的落地场景和实践应用从金融风控到工业质检，从智能家居到医疗诊断，MCP 已在多领域验证其价值。MCP有望成为AI - 掘金[ https://juejin.cn/post/7527846239938232355](https://juejin.cn/post/7527846239938232355)

\[143] AI模型突破99.99%解析精度，文档处理领域的AI革命!\_textin mcp-CSDN博客[ https://blog.csdn.net/wsh5620/article/details/148047793](https://blog.csdn.net/wsh5620/article/details/148047793)

\[144] 3 分钟 上手 阿里 百 宝箱 MCP ， 解锁 智能 体 新 可能 从 电商 客服 到 金融 分析 ， 详解 阿里 百 宝箱 MCP 如何 快速 搭建 实用 智能 体 ， 3 分钟 入门 ， 解锁 跨 行业 AI 应用 新 姿势 。 # AI # MCP # 阿里 百 宝箱 # 扣子 空间[ https://www.iesdouyin.com/share/video/7525026386449370383/?region=\&mid=7525026464132123446\&u\_code=0\&did=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&iid=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&with\_sec\_did=1\&video\_share\_track\_ver=\&titleType=title\&share\_sign=CYC0vMO7q3UdOyfJc9cbO40UoiWXkzQj5jsMZ96U7mM-\&share\_version=280700\&ts=1773320013\&from\_aid=1128\&from\_ssr=1\&share\_track\_info=%7B%22link\_description\_type%22%3A%22%22%7D](https://www.iesdouyin.com/share/video/7525026386449370383/?region=\&mid=7525026464132123446\&u_code=0\&did=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&iid=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&with_sec_did=1\&video_share_track_ver=\&titleType=title\&share_sign=CYC0vMO7q3UdOyfJc9cbO40UoiWXkzQj5jsMZ96U7mM-\&share_version=280700\&ts=1773320013\&from_aid=1128\&from_ssr=1\&share_track_info=%7B%22link_description_type%22%3A%22%22%7D)

\[145] 揭秘知识库MCP应用:为什么它比传统RAG更强大? | BetterYeah AI智能体[ https://www.betteryeah.com/blog/knowledge-base-mcp-application-advantages-over-traditional-rag](https://www.betteryeah.com/blog/knowledge-base-mcp-application-advantages-over-traditional-rag)

\[146] 未来趋势:MCP服务如何重塑AI开发生态?开发者必看的四大方向\_数据分析 mcp服务-CSDN博客[ https://blog.csdn.net/lbh73/article/details/147727912](https://blog.csdn.net/lbh73/article/details/147727912)

\[147] mcp协议:大模型从“孤岛”到“超级大脑”的进化密码[ https://www.enicn.com/Enicn/2025/article\_0411/83561.html](https://www.enicn.com/Enicn/2025/article_0411/83561.html)

\[148] 什么是MCP模式?AI 从业者必备的 “底层思维工具”\_人人都是产品经理[ http://m.toutiao.com/group/7579557339444625939/?upstream\_biz=doubao](http://m.toutiao.com/group/7579557339444625939/?upstream_biz=doubao)

\[149] MCP系列第十四集:MCP协议的发展方向和潜在机会\_mcp发展方向-CSDN博客[ https://blog.csdn.net/charles666666/article/details/147784322](https://blog.csdn.net/charles666666/article/details/147784322)

\[150] MCP协议技术演进与行业应用全景解析:从开源生态到商业落地的深度探索\_mcp 行业动态-CSDN博客[ https://blog.csdn.net/HHM200642/article/details/147541320](https://blog.csdn.net/HHM200642/article/details/147541320)

\[151] MCP 与 Agent ： 重构 AI 世界 的 " 数字 DNA "[ https://www.iesdouyin.com/share/video/7493331384531127552/?region=\&mid=7493332604284848922\&u\_code=0\&did=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&iid=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&with\_sec\_did=1\&video\_share\_track\_ver=\&titleType=title\&share\_sign=vnqASgGhbm4thnEsFYuVi9q6roNTKVl7qefIE0R9I4k-\&share\_version=280700\&ts=1773320014\&from\_aid=1128\&from\_ssr=1\&share\_track\_info=%7B%22link\_description\_type%22%3A%22%22%7D](https://www.iesdouyin.com/share/video/7493331384531127552/?region=\&mid=7493332604284848922\&u_code=0\&did=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&iid=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&with_sec_did=1\&video_share_track_ver=\&titleType=title\&share_sign=vnqASgGhbm4thnEsFYuVi9q6roNTKVl7qefIE0R9I4k-\&share_version=280700\&ts=1773320014\&from_aid=1128\&from_ssr=1\&share_track_info=%7B%22link_description_type%22%3A%22%22%7D)

\[152] 开篇:MCP理论理解和学习\_mcp 学习 理解-CSDN博客[ https://blog.csdn.net/yang2330648064/article/details/148196745](https://blog.csdn.net/yang2330648064/article/details/148196745)

\[153] MCP 集成电路制造工艺的最新进展-云社区-华为云[ https://bbs.huaweicloud.com/blogs/451871](https://bbs.huaweicloud.com/blogs/451871)

\[154] 一文带你 “看见“ MCP 的过程，彻底理解 MCP 的概念-CSDN博客[ https://blog.csdn.net/u012210662/article/details/148286429](https://blog.csdn.net/u012210662/article/details/148286429)

> （注：文档部分内容可能由 AI 生成）