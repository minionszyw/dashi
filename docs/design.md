# 架构设计文档

## 1. 系统架构

### 1.1 整体架构

```
┌─────────────────────────────────────────────────────────┐
│                     微信小程序前端                        │
│              (uni-app + Vue 3 + TypeScript)             │
└──────────────────────┬──────────────────────────────────┘
                       │ HTTPS/WSS
                       ↓
┌─────────────────────────────────────────────────────────┐
│                     API Gateway                          │
│                  (Nginx反向代理)                         │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ↓
┌─────────────────────────────────────────────────────────┐
│                   后端服务层                             │
│                  (FastAPI + Python)                      │
│  ┌─────────────┬──────────────┬─────────────────────┐  │
│  │  认证模块   │   业务模块   │    AI对话模块       │  │
│  │  (JWT)      │  (八字/支付)  │ (LangChain/Graph)   │  │
│  └─────────────┴──────────────┴─────────────────────┘  │
└──────────────────────┬─────────────────┬────────────────┘
                       │                 │
              ┌────────┴────────┐   ┌───┴─────┐
              ↓                 ↓   ↓         ↓
        ┌──────────┐      ┌──────────┐  ┌──────────┐
        │PostgreSQL│      │  Redis   │  │ OpenAI   │
        │  (数据)  │      │  (缓存)  │  │  API     │
        └──────────┘      └──────────┘  └──────────┘
```

### 1.2 技术选型理由

#### 前端：uni-app
- ✅ 一次开发，多端部署（微信/支付宝/H5/App）
- ✅ Vue 3生态完善，开发效率高
- ✅ 原生支持微信小程序API

#### 后端：FastAPI
- ✅ 异步高性能（基于ASGI）
- ✅ 自动生成API文档
- ✅ 类型注解，开发体验好
- ✅ 与Python八字计算模块无缝集成

#### AI框架：LangChain + LangGraph
- ✅ 统一AI模型接口，易于切换模型
- ✅ LangGraph提供状态管理和流程编排
- ✅ 完善的工具链和社区支持
- ✅ 可追溯的对话历史

#### 数据库：PostgreSQL + Redis
- ✅ PostgreSQL支持JSON字段，适合存储复杂数据
- ✅ Redis提供高速缓存和分布式锁
- ✅ 成熟稳定，性能优秀

## 2. 数据模型设计

### 2.1 ER图

```
┌─────────────┐
│   Users     │
│─────────────│
│ id (PK)     │
│ openid      │◄────┐
│ nickname    │     │
│ avatar_url  │     │
│ birth_info  │     │
│ token_bal   │     │
└─────────────┘     │
                    │
┌───────────────────┼────────────────┐
│                   │                │
│             ┌─────┴────────┐       │
│             │Conversations │       │
│             │──────────────│       │
│             │ id (PK)      │       │
│     ┌───────┤ user_id (FK) │       │
│     │       │ title        │       │
│     │       │ context_size │       │
│     │       │ ai_style     │       │
│     │       └──────────────┘       │
│     │              │               │
│     │              │               │
│     ↓              ↓               ↓
│┌──────────┐  ┌──────────┐  ┌──────────────┐
││ Messages │  │BaziProf  │  │    Orders    │
││──────────│  │──────────│  │──────────────│
││id (PK)   │  │id (PK)   │  │ id (PK)      │
││conv_id   │  │user_id   │  │ user_id (FK) │
││role      │  │name      │  │ amount       │
││content   │  │bazi_info │  │ token_amt    │
││token_cost│  │bazi_res  │  │ status       │
│└──────────┘  └──────────┘  └──────────────┘
```

### 2.2 数据字典

#### users（用户表）
| 字段 | 类型 | 说明 | 约束 |
|------|------|------|------|
| id | UUID | 主键 | PK |
| openid | VARCHAR(100) | 微信openid | UNIQUE, NOT NULL |
| nickname | VARCHAR(50) | 昵称 | |
| avatar_url | TEXT | 头像URL | |
| gender | VARCHAR(10) | 性别 | |
| birth_info | JSONB | 出生信息 | |
| token_balance | INTEGER | Token余额 | DEFAULT 100 |
| created_at | TIMESTAMP | 创建时间 | |
| updated_at | TIMESTAMP | 更新时间 | |

#### conversations（会话表）
| 字段 | 类型 | 说明 | 约束 |
|------|------|------|------|
| id | UUID | 主键 | PK |
| user_id | UUID | 用户ID | FK(users.id) |
| title | VARCHAR(100) | 会话标题 | |
| bazi_profile_id | UUID | 八字档案ID | |
| context_size | INTEGER | 上下文大小 | DEFAULT 10 |
| ai_style | VARCHAR(50) | AI风格 | DEFAULT 'professional' |
| created_at | TIMESTAMP | 创建时间 | |
| updated_at | TIMESTAMP | 更新时间 | |
| deleted_at | TIMESTAMP | 删除时间（软删除） | |

#### messages（消息表）
| 字段 | 类型 | 说明 | 约束 |
|------|------|------|------|
| id | UUID | 主键 | PK |
| conversation_id | UUID | 会话ID | FK(conversations.id) |
| role | VARCHAR(20) | 角色 | NOT NULL |
| content | TEXT | 内容 | NOT NULL |
| token_cost | INTEGER | Token消耗 | DEFAULT 0 |
| metadata | JSONB | 元数据 | |
| created_at | TIMESTAMP | 创建时间 | |

## 3. API设计

### 3.1 认证流程

```
前端                        后端                      微信服务器
 │                          │                            │
 │  wx.login()获取code      │                            │
 ├─────────────────────────>│                            │
 │                          │                            │
 │                          │  code换取openid/session_key│
 │                          ├───────────────────────────>│
 │                          │                            │
 │                          │<───────────────────────────┤
 │                          │    返回openid              │
 │                          │                            │
 │                          │  查询/创建用户              │
 │                          │  生成JWT token             │
 │<─────────────────────────┤                            │
 │    返回token和用户信息    │                            │
 │                          │                            │
```

### 3.2 AI对话流程

```
前端                              后端                       LangChain/OpenAI
 │                                │                              │
 │  发送消息                       │                              │
 ├───────────────────────────────>│                              │
 │                                │                              │
 │                                │  1. 检查token余额             │
 │                                │  2. 加载历史上下文             │
 │                                │  3. 构建Prompt                │
 │                                │                              │
 │                                │  调用LangChain流式API         │
 │                                ├─────────────────────────────>│
 │                                │                              │
 │                                │<─────────────────────────────┤
 │                                │     流式返回chunk             │
 │<───────────────────────────────┤                              │
 │   SSE流式推送                   │                              │
 │                                │                              │
 │                                │  保存消息，扣减token          │
 │                                │                              │
```

### 3.3 API端点设计

#### 认证相关
```
POST /api/v1/auth/wx-login
请求：{ "code": "wx_code" }
响应：{ "token": "jwt_token", "user": {...} }

POST /api/v1/auth/refresh
请求：{ "refresh_token": "..." }
响应：{ "token": "new_jwt_token" }
```

#### AI对话
```
POST /api/v1/chat/message
请求：{
  "conversation_id": "uuid",
  "content": "今年运势如何？"
}
响应：SSE流式推送
data: {"type": "token", "content": "根据"}
data: {"type": "token", "content": "您的"}
data: {"type": "token", "content": "八字..."}
data: {"type": "done", "message_id": "uuid", "token_cost": 150}
```

## 4. LangChain架构设计

### 4.1 LangGraph状态图

```python
from langgraph.graph import StateGraph
from typing import TypedDict, Annotated

class ChatState(TypedDict):
    user_input: str
    user_id: str
    conversation_id: str
    bazi_info: dict
    context_messages: list
    response: str
    token_cost: int

# 定义节点
def check_balance(state: ChatState) -> ChatState:
    """检查token余额"""
    pass

def load_context(state: ChatState) -> ChatState:
    """加载上下文历史"""
    pass

def build_prompt(state: ChatState) -> ChatState:
    """构建prompt"""
    pass

def call_llm(state: ChatState) -> ChatState:
    """调用LLM"""
    pass

def save_message(state: ChatState) -> ChatState:
    """保存消息"""
    pass

# 构建图
graph = StateGraph(ChatState)
graph.add_node("check_balance", check_balance)
graph.add_node("load_context", load_context)
graph.add_node("build_prompt", build_prompt)
graph.add_node("call_llm", call_llm)
graph.add_node("save_message", save_message)

# 定义边
graph.add_edge("check_balance", "load_context")
graph.add_edge("load_context", "build_prompt")
graph.add_edge("build_prompt", "call_llm")
graph.add_edge("call_llm", "save_message")

graph.set_entry_point("check_balance")
graph.set_finish_point("save_message")

app = graph.compile()
```

### 4.2 Prompt模板设计

```python
from langchain.prompts import ChatPromptTemplate

system_template = """你是一位专业的命理分析师，精通八字命理。

用户档案：
姓名：{name}
性别：{gender}
八字：{bazi}
节气信息：{jieqi_info}
大运信息：{dayun_info}

对话风格：{ai_style}

请根据用户的问题，结合八字信息进行专业分析。注意：
1. 分析要有理有据，引用命理术语
2. 语言要{style_tone}
3. 回答要有实用性建议
4. 保持命理文化的严肃性

历史对话：
{chat_history}
"""

prompt = ChatPromptTemplate.from_messages([
    ("system", system_template),
    ("human", "{user_input}")
])
```

## 5. 性能优化

### 5.1 数据库优化

#### 索引设计
```sql
-- 用户表
CREATE INDEX idx_users_openid ON users(openid);

-- 会话表
CREATE INDEX idx_conversations_user_id ON conversations(user_id);
CREATE INDEX idx_conversations_created_at ON conversations(created_at DESC);
CREATE INDEX idx_conversations_deleted_at ON conversations(deleted_at);

-- 消息表
CREATE INDEX idx_messages_conversation_id ON messages(conversation_id);
CREATE INDEX idx_messages_created_at ON messages(created_at DESC);
```

#### 查询优化
- 使用连接池（pool_size=10, max_overflow=20）
- 分页查询（limit/offset）
- 避免N+1查询（使用joinedload）

### 5.2 缓存策略

#### Redis缓存设计
```python
# 用户信息缓存
key: "user:{user_id}"
value: JSON序列化的用户信息
ttl: 3600秒（1小时）

# 会话列表缓存
key: "conversations:{user_id}"
value: 会话ID列表
ttl: 1800秒（30分钟）

# 热点会话缓存
key: "conversation:{conversation_id}"
value: JSON序列化的会话信息
ttl: 3600秒
```

### 5.3 API限流

```python
# 基于Redis的令牌桶算法
@limiter.limit("10/minute")  # 每分钟10次
async def send_message(request: Request):
    pass

# 基于用户的限流
@limiter.limit("100/hour", key_func=get_user_id)
async def create_conversation(request: Request):
    pass
```

### 5.4 前端优化

- **虚拟列表**：消息列表超过50条使用虚拟滚动
- **防抖节流**：输入框防抖500ms
- **本地缓存**：使用uni.storage缓存会话列表
- **懒加载**：图片和历史消息按需加载
- **预加载**：预取最近会话的前10条消息

## 6. 安全设计

### 6.1 认证授权

- JWT Token认证
- Token有效期7天
- Refresh Token轮换
- API接口权限校验

### 6.2 数据安全

- HTTPS加密传输
- 敏感信息（出生信息）加密存储
- SQL参数化查询
- XSS/CSRF防护

### 6.3 业务安全

- Token余额检查
- 消息内容审核（敏感词过滤）
- 频率限制
- 异常行为监控

## 7. 监控与日志

### 7.1 日志设计

```python
# 日志格式
{
    "timestamp": "2025-10-18T10:30:00Z",
    "level": "INFO",
    "module": "chat",
    "user_id": "uuid",
    "action": "send_message",
    "duration_ms": 1234,
    "status": "success",
    "details": {...}
}
```

### 7.2 监控指标

- API响应时间
- 数据库查询性能
- Token消耗统计
- 错误率
- 并发用户数

## 8. 部署架构

### 8.1 Docker部署

```
┌─────────────────────────────────────┐
│         Docker Compose              │
│  ┌──────────┐  ┌──────────┐        │
│  │PostgreSQL│  │  Redis   │        │
│  └──────────┘  └──────────┘        │
│  ┌──────────────────────────┐      │
│  │   FastAPI Backend        │      │
│  │   (Uvicorn workers=4)    │      │
│  └──────────────────────────┘      │
└─────────────────────────────────────┘
               ↑
               │
        ┌──────┴───────┐
        │    Nginx     │
        │ (反向代理+SSL)│
        └──────────────┘
```

### 8.2 扩展方案

#### 水平扩展
```
           Nginx (负载均衡)
                 │
        ┌────────┼────────┐
        ↓        ↓        ↓
     Backend1 Backend2 Backend3
        └────────┼────────┘
                 ↓
        PostgreSQL (主从复制)
```

---

**文档版本**：v1.0  
**最后更新**：2025-10-18  
**维护者**：开发团队

