# AI对话功能架构流程

**版本**: v1.1.1  
**更新日期**: 2025-10-21

---

## 📊 整体架构图

```
┌─────────────────────────────────────────────────────────────────┐
│                          前端 (uni-app)                          │
│                                                                   │
│  用户输入 → 发送消息 → 接收流式响应 → 展示对话                    │
└─────────────────────────┬───────────────────────────────────────┘
                          │ HTTP/SSE
                          ↓
┌─────────────────────────────────────────────────────────────────┐
│                       后端 API (FastAPI)                          │
│                                                                   │
│  ┌──────────────┐    ┌───────────────┐    ┌─────────────────┐  │
│  │  auth.py     │ →  │   chat.py     │ →  │ langchain_      │  │
│  │  JWT验证     │    │  /message端点  │    │ service.py      │  │
│  └──────────────┘    └───────────────┘    └─────────────────┘  │
└─────────────────────────┬───────────────────────────────────────┘
                          │
            ┌─────────────┼─────────────┐
            ↓             ↓             ↓
    ┌──────────┐  ┌─────────────┐  ┌──────────┐
    │PostgreSQL│  │  prompts/   │  │ OpenAI   │
    │  数据库  │  │ system_     │  │ API      │
    │          │  │ prompts.py  │  │ (DeepSeek)│
    └──────────┘  └─────────────┘  └──────────┘
```

---

## 🔄 完整对话流程

### 阶段1: 用户发起对话

```
前端 (chat/index.vue)
  ↓
用户输入消息
  ↓
调用 sendMessage() 方法
  ↓
POST /api/v1/chat/message
  {
    conversation_id: "uuid",
    content: "用户问题"
  }
```

---

### 阶段2: 后端接收请求

**文件**: `backend/app/api/v1/chat.py`

```python
@router.post("/message")
async def send_message(
    message_data: MessageCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(check_token_balance)  # JWT验证 + 余额检查
):
    # 1. 验证会话所有权
    conversation = db.query(Conversation).filter(
        Conversation.id == message_data.conversation_id,
        Conversation.user_id == current_user.id
    ).first()
    
    # 2. 保存用户消息
    user_message = Message(
        conversation_id=conversation.id,
        role="user",
        content=message_data.content
    )
    db.add(user_message)
    db.commit()
    
    # 3. 调用AI服务（流式响应）
    return StreamingResponse(
        generate(),  # 生成器函数
        media_type="text/event-stream"
    )
```

---

### 阶段3: 加载会话配置

**文件**: `backend/app/services/langchain_service.py`

```python
async def stream_chat(
    self,
    user_message: str,
    conversation_id: str,
    user_id: str,
    db: Session
):
    # 1. 获取会话配置
    conversation = db.query(Conversation).filter(
        Conversation.id == conversation_id
    ).first()
    
    # 关键配置：
    ai_style = conversation.ai_style           # 对话模式 (simple/balanced/professional)
    context_size = conversation.context_size   # 上下文条数 (5-50)
    bazi_profile_id = conversation.bazi_profile_id  # 八字档案ID
```

**配置说明**：

| 配置项 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| `ai_style` | string | "professional" | 对话模式，影响AI回答风格 |
| `context_size` | int | 10 | 上下文记忆条数 |
| `bazi_profile_id` | UUID | null | 关联的八字档案ID |

---

### 阶段4: 加载八字档案（如果有）

```python
# 2. 获取八字信息（如果有关联）
bazi_info = None
if conversation.bazi_profile_id:
    profile = db.query(BaziProfile).filter(
        BaziProfile.id == conversation.bazi_profile_id
    ).first()
    
    if profile:
        # 组合完整信息
        bazi_info = {
            'name': profile.name,              # 姓名
            'gender': profile.gender,          # 性别
            'bazi': profile.bazi_result['bazi'],           # 八字四柱
            'jieqi_info': profile.bazi_result['jieqi_info'],  # 节气信息
            'dayun_info': profile.bazi_result['dayun_info'],  # 大运信息
            'formatted_output': profile.bazi_result['formatted_output']  # 详细分析
        }
```

**数据库结构**：

```sql
-- BaziProfile 表
id              UUID
user_id         UUID
name            VARCHAR(50)     -- 姓名
gender          VARCHAR(10)     -- 性别
birth_info      JSONB          -- 出生信息
bazi_result     JSONB          -- 八字结果（包含上述4个字段）
```

---

### 阶段5: 构建系统提示词

**文件**: `backend/app/prompts/system_prompts.py`

```python
class SystemPromptManager:
    
    # 1. 系统角色定义
    SYSTEM_ROLE = """你是一位专业的命理分析师，精通八字命理。"""
    
    # 2. 对话模式配置
    STYLE_PROMPTS = {
        "simple": """简单模式提示词...""",
        "balanced": """平衡模式提示词...""",
        "professional": """专业模式提示词..."""
    }
    
    # 3. 构建完整提示词
    @classmethod
    def build_system_prompt(cls, ai_style, bazi_info):
        # 组合：系统角色 + 对话风格 + 用户信息
        prompt_parts = [
            cls.SYSTEM_ROLE,                           # 基础角色
            cls.STYLE_PROMPTS[ai_style],              # 对话风格
            cls._format_bazi_profile(bazi_info)       # 用户档案（如果有）
        ]
        return "\n".join(prompt_parts)
```

**提示词结构**：

```
你是一位专业的命理分析师，精通八字命理。

**回答风格**：专业模式
- 使用专业的命理术语
- 深入详细地分析八字结构
...

═══════════════════════════════
📋 当前用户命理档案
═══════════════════════════════

👤 姓名：张三
⚧ 性别：男
🎋 八字四柱：癸酉 辛酉 癸卯 乙卯
🌸 节气信息：生于白露节气后12天
🔮 大运信息：阴男，逆排，4岁起运
...
```

---

### 阶段6: 加载历史上下文

```python
def _load_context_messages(
    self,
    conversation_id: str,
    context_size: int,
    db: Session
) -> list:
    """加载上下文消息"""
    
    # 查询最近N条消息
    messages = db.query(Message).filter(
        Message.conversation_id == conversation_id
    ).order_by(Message.created_at.desc()).limit(context_size).all()
    
    # 转换为LangChain格式
    context = []
    for msg in reversed(messages):
        if msg.role == "user":
            context.append(HumanMessage(content=msg.content))
        elif msg.role == "assistant":
            context.append(AIMessage(content=msg.content))
    
    return context
```

**上下文机制**：
- 按时间倒序取最近 `context_size` 条消息
- 转换为LangChain的消息格式
- 反转后按时间正序排列
- 包含用户消息和AI回复

---

### 阶段7: 组装消息并调用AI

```python
# 构建完整消息列表
messages = [
    SystemMessage(content=system_prompt),    # 1. 系统提示词
    *context_messages,                       # 2. 历史对话
    HumanMessage(content=user_message)       # 3. 当前问题
]

# 流式调用OpenAI API
async for chunk in self.llm.astream(messages):
    content = chunk.content
    if content:
        full_response += content
        token_count += 1
        
        # 流式返回每个token
        yield {
            "type": "token",
            "content": content,
            "token_cost": token_count
        }
```

**LangChain配置**：

```python
self.llm = ChatOpenAI(
    model=settings.OPENAI_MODEL,           # "deepseek-chat"
    temperature=settings.OPENAI_TEMPERATURE, # 0.7
    max_tokens=settings.OPENAI_MAX_TOKENS,  # 2000
    streaming=True,                         # 开启流式
    openai_api_base=settings.OPENAI_BASE_URL,  # DeepSeek API
    openai_api_key=settings.OPENAI_API_KEY
)
```

---

### 阶段8: 流式返回结果

**后端 → 前端**：

```python
# 后端返回格式（SSE）
yield f"data: {json.dumps(chunk)}\n\n"

# chunk 格式：
{
    "type": "token",          # 消息类型：token/done/error
    "content": "字",          # 当前token内容
    "token_cost": 15          # 累计token数
}

# 完成后：
{
    "type": "done",
    "message_id": "uuid",
    "token_cost": 150
}
```

**前端处理**：

```typescript
// frontend/src/pages/chat/index.vue
const response = await fetch(url, {...})
const reader = response.body.getReader()

while (true) {
  const { done, value } = await reader.read()
  if (done) break
  
  // 解析SSE数据
  const chunk = JSON.parse(data)
  
  if (chunk.type === 'token') {
    // 追加内容到消息
    chatStore.appendAIMessageContent(aiMessage.id, chunk.content)
  } else if (chunk.type === 'done') {
    // 完成，更新消息ID和token消耗
    chatStore.finalizeAIMessage(aiMessage.id, chunk.message_id, chunk.token_cost)
  }
}
```

---

### 阶段9: 保存消息和扣费

```python
# 保存AI回复
ai_message = Message(
    conversation_id=conversation_id,
    role="assistant",
    content=full_response,      # 完整回复内容
    token_cost=token_count       # token消耗
)
stream_db.add(ai_message)

# 扣减用户余额
user = stream_db.query(User).filter(User.id == user_id).first()
if user:
    user.token_balance -= token_cost

stream_db.commit()
```

---

## 🎯 关键配置点

### 1. 对话模式 (ai_style)

| 模式 | 值 | 提示词特点 | 适用场景 |
|------|------|----------|----------|
| 简单 | simple | 简洁通俗，避免术语 | 初学者 |
| 平衡 | balanced | 术语+解释，适度深入 | 一般用户 |
| 专业 | professional | 引经据典，系统分析 | 专业用户 |

**配置位置**：
- 前端：`pages/profile/settings.vue`
- 后端：`Conversation.ai_style` 字段
- 提示词：`prompts/system_prompts.py`

---

### 2. 上下文记忆 (context_size)

**配置范围**：
- 前端滑块：5-20条
- 后端限制：5-50条
- 默认值：10条

**影响**：
- 越大：记忆越长，token消耗越高
- 越小：记忆越短，token消耗越低

**实现**：简单的滑动窗口，取最近N条消息

---

### 3. 八字信息注入 (bazi_profile_id)

**触发条件**：
```python
if conversation.bazi_profile_id is not None:
    # 加载八字档案
    # 注入到系统提示词
```

**数据来源**：
1. 用户在"八字排盘"页填写信息
2. 后端调用 `BaziService.calculate()` 计算
3. 保存到 `BaziProfile` 表
4. 创建会话时关联 `bazi_profile_id`

**注入内容**：
- 姓名、性别
- 八字四柱
- 节气信息
- 大运信息
- 完整分析

---

## 📝 日志输出

**调试日志**（在 `langchain_service.py` 中）：

```python
logger.info(f"📌 会话ID: {conversation_id}")
logger.info(f"🎨 对话模式: {conversation.ai_style}")
logger.info(f"📊 上下文条数: {conversation.context_size}")
logger.info(f"🔗 关联八字档案ID: {conversation.bazi_profile_id}")

if conversation.bazi_profile_id:
    logger.info(f"🔍 正在查询八字档案: {conversation.bazi_profile_id}")
    if profile:
        logger.info(f"✅ 八字档案加载成功: {profile.name} ({profile.gender})")
        logger.info(f"   八字字段: {list(profile.bazi_result.keys())}")
    else:
        logger.warning(f"⚠️ 未找到八字档案: {conversation.bazi_profile_id}")
else:
    logger.info("ℹ️ 当前会话未关联八字档案")
```

---

## 🔧 核心代码文件

| 文件 | 职责 | 关键方法 |
|------|------|----------|
| `api/v1/chat.py` | 对话API端点 | `send_message()` |
| `services/langchain_service.py` | AI对话服务 | `stream_chat()` |
| `prompts/system_prompts.py` | 提示词管理 | `build_system_prompt()` |
| `models/conversation.py` | 会话数据模型 | - |
| `models/message.py` | 消息数据模型 | - |
| `models/bazi_profile.py` | 八字档案模型 | - |

---

## 🎨 数据流示意图

```
用户输入
    ↓
前端发送请求
    ↓
[后端 API] 验证会话 + 保存用户消息
    ↓
[LangChain服务] 加载配置
    ├─ 对话模式 (ai_style)
    ├─ 上下文条数 (context_size)
    └─ 八字档案 (bazi_profile_id)
    ↓
[SystemPromptManager] 构建提示词
    ├─ 系统角色 (SYSTEM_ROLE)
    ├─ 对话风格 (STYLE_PROMPTS[ai_style])
    └─ 用户信息 (_format_bazi_profile)
    ↓
[PostgreSQL] 加载历史消息 (context_size条)
    ↓
[LangChain] 组装消息
    ├─ SystemMessage (提示词)
    ├─ HumanMessage/AIMessage (历史)
    └─ HumanMessage (当前问题)
    ↓
[OpenAI API] 流式生成回复
    ↓
[后端] 流式返回 (SSE)
    ↓
[前端] 逐字显示
    ↓
[后端] 保存AI消息 + 扣费
    ↓
完成
```

---

## 🚀 扩展点

### 1. 添加新的对话模式

**步骤**：
1. 在 `system_prompts.py` 中添加新模式
2. 在前端 `settings.vue` 中添加选项
3. 测试效果

### 2. 优化上下文管理

**可能方案**：
- 智能摘要：长对话自动摘要
- 重要性排序：保留最重要的对话
- 滑动窗口 + 摘要混合

### 3. 多模型支持

**可能方案**：
- 添加模型选择配置
- 不同场景使用不同模型
- 成本和质量平衡

---

## 📚 相关文档

- [开发文档](development.md)
- [架构设计](design.md)
- [更新日志](../CHANGELOG.md)

---

**最后更新**: 2025-10-21  
**维护者**: 开发团队

