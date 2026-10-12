---
group: 8. 全栈 AI App
id: streaming-ui
title: AI App · 流式协议与交互状态
toc: AI App · 流式协议与交互状态
---

一个可用的 AI 界面需要展示文本，也要区分排队、检索、调用工具、等待审批、结束和失败。后端应发送明确事件，让界面按状态更新。

## 先选通信方式

| 方式 | 适合场景 | 需要注意 |
|------|----------|----------|
| POST + fetch 流式读取 | 聊天提交和服务端连续返回 | 取消信号、增量解析、认证 |
| EventSource / SSE | 单向事件订阅 | 原生 EventSource 使用 GET，不能任意添加认证头 |
| WebSocket | 双向事件与频繁控制消息 | 心跳、断线恢复、连接鉴权 |
| WebRTC | 低延迟音视频 | 媒体设备、网络协商、会话安全 |

流式协议和模型供应商 SDK 是不同层次。可使用现有 AI SDK 统一消息和工具事件，也可在后端适配自己的事件契约；同一产品应保持事件字段和状态语义一致。

## 定义可恢复的事件契约

```json
{
  "request_id": "task-123",
  "seq": 12,
  "type": "tool_result",
  "payload": {"tool": "read_order", "status": "succeeded"}
}
```

建议至少支持 started、text_delta、tool_started、tool_result、approval_required、completed、failed、cancelled。seq 在同一请求内递增，客户端按 request_id 和 seq 去重。

如果要求断线恢复，服务端需要保留可重放事件，并明确保留时间、鉴权方式和断点。仅添加 seq 字段不会自动获得重连能力。

## 正确解析流

网络读取到的一块字节可能只包含半个 UTF-8 字符、半条 JSON 或多条事件。使用支持增量解码的 TextDecoder，保留未完成的文本缓冲；SSE 按空行切事件，JSON Lines 按完整行解析。

反向代理和应用服务应允许逐步发送数据并关闭不必要的响应缓冲。连接建立后 HTTP 状态码通常无法再改变，因此运行时错误还需要以协议中的 failed 事件表达。

## UI 状态与取消

```text
待提交 -> 排队 -> 检索 / 生成 / 工具调用
                    -> 等待审批 -> 继续执行
                    -> 完成 / 失败 / 取消
```

用户点击停止后，前端通过 AbortController 等机制取消网络读取，服务端也应收到取消信号并停止可取消的模型和工具工作。已完成的写操作不能撤销，要显示真实回执；允许后台继续的任务需要独立任务 ID。

避免流式片段持续触发整篇 Markdown 重新渲染。可以批量刷新文本，在结束后统一格式化，并使用成熟的 Markdown 解析器和 HTML 清洗器。引用、工具结果和错误应有独立状态，不能只靠文本推断。

## 验收场景

模拟慢网络、事件跨块、重复事件、工具超时、鉴权过期、用户停止和浏览器重连。检查界面是否重复追加文本、出现假完成、丢失引用或在取消后继续扣费。

## 参考资料

- [MDN Streams API](https://developer.mozilla.org/en-US/docs/Web/API/Streams_API)
- [MDN Server-Sent Events](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events)
- [AI SDK 文档](https://ai-sdk.dev/docs)
