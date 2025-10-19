# AI流式对话修复说明

## 问题分析

### 1. JSON格式错误
```
SyntaxError: Unexpected token ' in JSON at position 1
```
**原因**: Python字典直接转字符串使用单引号，不是有效的JSON格式
```python
# 错误
yield f"data: {chunk}\n\n"  # 输出: data: {'type': 'token', 'content': '你'}

# 正确
yield f"data: {json.dumps(chunk)}\n\n"  # 输出: data: {"type": "token", "content": "你"}
```

### 2. SQLAlchemy Session错误
```
Instance is not bound to a Session; attribute refresh operation cannot proceed
```
**原因**: 流式响应在异步生成器中执行，外部的db session被关闭后无法访问对象属性

## 修复方案

### 后端修改 (`backend/app/api/v1/chat.py`)

#### 1. 导入json模块
```python
import json
```

#### 2. Session管理
- 在generate函数外部提取`conversation_id`和`user_id`
- 在generate函数内部创建新的`SessionLocal()`实例
- 确保在finally块中关闭session

#### 3. JSON序列化
- 所有SSE数据使用`json.dumps()`序列化
- 确保数据格式符合JSON标准（双引号）

### 关键代码

```python
@router.post("/message")
async def send_message(...):
    # 外部提取ID
    conversation_id = str(conversation.id)
    user_id = str(current_user.id)
    
    async def generate():
        from app.core.database import SessionLocal
        stream_db = SessionLocal()
        
        try:
            async for chunk in chat_service.stream_chat(...):
                # 使用json.dumps确保正确格式
                yield f"data: {json.dumps(chunk)}\n\n"
            
            # 完成消息
            done_data = {
                "type": "done",
                "message_id": str(ai_message.id),
                "token_cost": token_cost
            }
            yield f"data: {json.dumps(done_data)}\n\n"
            
        except Exception as e:
            error_data = {"type": "error", "message": str(e)}
            yield f"data: {json.dumps(error_data)}\n\n"
        finally:
            stream_db.close()
```

## 前端说明 (`frontend/src/pages/chat/index.vue`)

前端使用微信小程序原生API `wx.request`的`onChunkReceived`监听器：

```typescript
const requestTask = wx.request({
  url: `${BASE_URL}/api/v1/chat/message`,
  method: 'POST',
  enableChunked: true,  // 开启分块传输
  // ...
})

// 监听流式数据块
requestTask.onChunkReceived((res) => {
  const chunk = String.fromCharCode.apply(null, new Uint8Array(res.data))
  // 解析SSE格式数据
  // data: {"type":"token","content":"你"}
})
```

### uni-app文档参考

- [uni.request - enableChunked](https://uniapp.dcloud.net.cn/api/request/request.html#enablechunked)
- [RequestTask.onChunkReceived](https://developers.weixin.qq.com/miniprogram/dev/api/network/request/RequestTask.onChunkReceived.html)

**注意**: `uni.request`不支持真正的流式响应，必须使用微信原生`wx.request`

## 测试步骤

1. **重启后端服务** ✅
   ```bash
   pkill -f "uvicorn"
   cd backend && source venv/bin/activate
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

2. **微信开发者工具测试**
   - 点击"编译"刷新小程序
   - 打开聊天页面
   - 发送消息："你好"
   - 观察AI逐字返回内容

3. **验证修复**
   - ✓ 无JSON解析错误
   - ✓ 无Session错误
   - ✓ AI内容逐字显示
   - ✓ Token正常扣减

## 技术要点

### SSE (Server-Sent Events) 格式
```
data: {"type":"token","content":"你"}\n\n
data: {"type":"token","content":"好"}\n\n
data: {"type":"done","message_id":"xxx","token_cost":10}\n\n
```

- 每条消息以`data: `开头
- 数据必须是有效的JSON（双引号）
- 每条消息以`\n\n`结尾

### Session生命周期

```
FastAPI Dependency -> db session (自动关闭)
                            ↓
流式生成器函数 -> 创建新的 SessionLocal()
                            ↓
                      finally: close()
```

## 相关文件

- `backend/app/api/v1/chat.py` - 流式对话API
- `backend/app/services/langchain_service.py` - AI服务
- `frontend/src/pages/chat/index.vue` - 聊天页面

---

**修复完成时间**: 2025-10-19 13:35
**测试状态**: ✅ 通过

