# AI对话功能架构

**版本**: v2.0  
**更新日期**: 2025-10-23

---

## 架构概览

```
┌─────────────────────────────────────────────────┐
│         前端 (uni-app Vue 3)                     │
│  用户输入 → 流式接收 → 打字机展示                 │
└────────────────┬────────────────────────────────┘
                 │ HTTP/SSE
                 ↓
┌─────────────────────────────────────────────────┐
│         后端 (FastAPI + LangChain)               │
│  API → LangChain服务 → OpenAI API               │
└────────────────┬────────────────────────────────┘
                 │
      ┌──────────┼──────────┐
      ↓          ↓          ↓
  PostgreSQL  提示词管理  DeepSeek
```

---

## 核心流程

### 1. 用户发起对话

**前端**：`pages/chat/index.vue`
```typescript
// 发送前检查是否有八字档案
if (!baziStore.profiles || baziStore.profiles.length === 0) {
  // 提示用户去设置出生信息
  return
}

// 用户发送消息
POST /api/v1/chat/message
{
  conversation_id: "uuid",
  content: "用户问题"
}
```

### 2. 后端处理消息

**API**：`api/v1/chat.py` → `send_message()`
- **检查用户是否有八字档案**（必须）
- 验证会话所有权
- 保存用户消息
- 调用LangChain服务（流式响应）

### 3. 加载会话配置

**服务**：`services/langchain_service.py` → `stream_chat()`

从数据库加载配置：
- `ai_style`：对话模式（simple/balanced/professional）
- `context_size`：上下文条数（5-50）
- `bazi_profile_id`：八字档案ID（可选）

### 4. 构建系统提示词

**提示词管理**：`prompts/system_prompts.py`

```python
SystemPromptManager.build_system_prompt(
    ai_style="balanced",      # 对话风格
    bazi_info={...}           # 用户八字信息（如果有）
)
```

**提示词结构**：
```
系统角色定义
    ↓
对话风格设置（根据ai_style）
    ↓
用户命理档案（如果关联了八字）
```

### 5. 加载历史上下文

从数据库查询最近 `context_size` 条消息，转换为LangChain格式：
- 用户消息 → `HumanMessage`
- AI回复 → `AIMessage`

### 6. 调用AI生成回复

```python
messages = [
    SystemMessage(content=system_prompt),  # 系统提示词
    *context_messages,                     # 历史对话
    HumanMessage(content=user_message)     # 当前问题
]

# 流式调用
async for chunk in self.llm.astream(messages):
    yield {"type": "token", "content": chunk.content, ...}
```

### 7. 流式返回前端

**SSE格式**：
```json
// 每个token
data: {"type": "token", "content": "字", "token_cost": 15}

// 完成
data: {"type": "done", "message_id": "uuid", "token_cost": 150}

// 错误
data: {"type": "error", "message": "错误信息"}
```

**前端处理**：
```typescript
// 逐字追加内容
if (chunk.type === 'token') {
  chatStore.appendAIMessageContent(aiMessage.id, chunk.content)
}
// 完成时更新ID和扣费
else if (chunk.type === 'done') {
  chatStore.finalizeAIMessage(aiMessage.id, chunk.message_id, chunk.token_cost)
  userStore.deductTokenBalance(chunk.token_cost)
}
```

### 8. 保存消息并扣费

- 保存AI回复到数据库
- 扣减用户token余额
- 提交事务

---

## 核心配置

### 对话模式（ai_style）

| 模式 | 值 | 特点 | 适用场景 |
|------|------|------|----------|
| 简单 | simple | 通俗易懂，避免术语 | 初学者 |
| 默认 | balanced | 平衡专业性与易懂性 | 一般用户 |
| 专业 | professional | 术语丰富，系统分析 | 专业用户 |

**配置位置**：
- 前端：`pages/profile/settings.vue`
- 存储：本地storage（ai_settings）+ 数据库（Conversation表）
- 后端：`prompts/system_prompts.py` 根据模式选择提示词

### 上下文记忆（context_size）

**范围**：5-50条（默认10条）

**影响**：
- 越大：记忆越长，回答更连贯，token消耗越高
- 越小：记忆越短，回答更独立，token消耗越低

**实现**：简单的滑动窗口（取最近N条消息）

### 八字信息注入（bazi_profile_id）

**触发条件**：会话关联了八字档案

**注入内容**：
- 姓名、性别
- 八字四柱
- 节气信息
- 大运信息
- 完整分析

**效果**：AI可以根据用户的八字信息提供个性化分析

---

## 用户设置持久化

### 保存流程

1. 用户在 `profile/settings.vue` 修改设置（如：5条，简单）
2. 点击"保存"按钮
3. 保存到本地存储：`storage.set('ai_settings', {contextSize: 5, aiStyle: 'simple'})`
4. 如果有当前会话，调用API更新会话：`updateConversation(id, {context_size: 5, ai_style: 'simple'})`

### 应用流程

**场景1：切换到已有会话**
- 从数据库加载会话，使用会话自己的配置

**场景2：创建新会话**
- 从本地存储读取 `ai_settings`
- 应用到新会话的 `context_size` 和 `ai_style`

**场景3：打开设置页**
- 优先显示当前会话的配置
- 如果没有当前会话，显示本地存储的配置

---

## 核心文件

| 文件 | 职责 |
|------|------|
| `api/v1/chat.py` | 对话API端点 |
| `services/langchain_service.py` | AI对话服务 |
| `prompts/system_prompts.py` | 提示词管理 |
| `models/conversation.py` | 会话模型 |
| `schemas/chat.py` | 请求/响应模型 |
| `frontend/pages/chat/index.vue` | 聊天页面 |
| `frontend/pages/profile/settings.vue` | 设置页面 |
| `frontend/stores/chat.ts` | 聊天状态管理 |

---

## 数据流图

```
用户输入
  ↓
[前端] 检查是否有八字档案
  ├─ 没有 → 提示去设置
  └─ 有 → 发送请求
  ↓
[API] 检查八字档案（双重校验）
  ↓
[API] 验证会话 + 保存用户消息
  ↓
[LangChain服务] 加载配置
  ├─ 对话模式 (ai_style)
  ├─ 上下文条数 (context_size)
  └─ 八字档案 (bazi_profile_id)
  ↓
[提示词管理] 构建提示词
  ├─ 系统角色
  ├─ 对话风格
  └─ 用户信息
  ↓
[数据库] 加载历史消息
  ↓
[LangChain] 组装消息 → [OpenAI API] 流式生成
  ↓
[后端] 流式返回 (SSE) → [前端] 逐字显示
  ↓
[后端] 保存AI消息 + 扣费
  ↓
完成
```

---

**最后更新**: 2025-10-23  
**文档版本**: v2.0（精简版）
