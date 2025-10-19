# AI对话功能测试说明

## 问题原因

微信小程序的 `uni.request` 不支持真正的Server-Sent Events(SSE)流式响应，导致前端必须等待完整响应后才能显示AI消息。

## 修复方案

使用微信小程序原生API `wx.request` 的 `onChunkReceived` 回调来处理流式数据。

### 修改文件

- `frontend/src/pages/chat/index.vue` - 第237-312行

### 关键改动

```typescript
const requestTask = wx.request({
  enableChunked: true,
  // ...
})

requestTask.onChunkReceived((res) => {
  // 实时处理每个数据块
})
```

## 测试步骤

1. 在微信开发者工具中点击"编译"
2. 打开聊天页面
3. 发送消息："你好"
4. 观察AI应该逐字返回内容

## 技术栈

- 后端：FastAPI + StreamingResponse
- AI服务：DeepSeek (OpenAI兼容API)
- 前端：uni-app + 微信小程序原生API

