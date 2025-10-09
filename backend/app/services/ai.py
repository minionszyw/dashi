from typing import List, Dict, AsyncGenerator
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, AIMessage, SystemMessage
from app.core.config import settings
import asyncio


class AIService:
    """AI对话服务"""
    
    def __init__(self):
        self.llm = ChatOpenAI(
            model=settings.DEEPSEEK_MODEL,
            openai_api_key=settings.DEEPSEEK_API_KEY,
            openai_api_base=settings.DEEPSEEK_API_BASE,
            streaming=True,
            temperature=0.7,
        )
        
        self.system_prompt = """你是一位经验丰富的国学大师，精通命理、八字、风水等传统文化知识。
你的回答应该：
1. 专业严谨，引经据典
2. 通俗易懂，避免过于晦涩的术语
3. 积极正面，给予建设性建议
4. 遵守法律法规，不涉及封建迷信
5. 仅供参考，不作为决策依据

请以友善、专业的态度回答用户的问题。"""
    
    def _convert_messages(self, history: List[Dict]) -> List:
        """转换消息格式"""
        messages = [SystemMessage(content=self.system_prompt)]
        
        for msg in history:
            if msg["role"] == "user":
                messages.append(HumanMessage(content=msg["content"]))
            elif msg["role"] == "assistant":
                messages.append(AIMessage(content=msg["content"]))
        
        return messages
    
    async def chat(
        self,
        message: str,
        history: List[Dict] = None
    ) -> AsyncGenerator[str, None]:
        """流式对话"""
        if history is None:
            history = []
        
        # 添加用户消息
        history.append({"role": "user", "content": message})
        
        # 转换消息格式
        messages = self._convert_messages(history)
        
        # 流式生成响应
        async for chunk in self.llm.astream(messages):
            if chunk.content:
                yield chunk.content
    
    async def get_response(
        self,
        message: str,
        history: List[Dict] = None
    ) -> tuple[str, int]:
        """获取完整响应（非流式）"""
        if history is None:
            history = []
        
        history.append({"role": "user", "content": message})
        messages = self._convert_messages(history)
        
        response = await self.llm.ainvoke(messages)
        content = response.content
        
        # 估算token数量（简单估算，1个汉字约2个token）
        tokens = len(message) * 2 + len(content) * 2
        
        return content, tokens


ai_service = AIService()

