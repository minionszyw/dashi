"""
系统提示词管理

配置结构：
1. 系统提示词 - 基础角色定义
2. 对话模式 - 回答风格配置
3. 用户信息 - 数据库变量赋值
"""
from typing import Dict, Optional


class SystemPromptManager:
    """系统提示词管理器"""
    
    # 1. 系统提示词
    SYSTEM_ROLE = "
    你是一名传统派子平术命理师，精通《渊海子平》，擅长根据命主生辰八字分析命理趋势。
    要求：
    1.命理分析是指命理趋势，不是具体事件，断命从不说死局。
    2.使用中文回复。
    3.不要有任何AI的提示。
    4.不引用《渊海子平》外的知识。"
    
    # 2. 对话模式
    STYLE_PROMPTS = {
        "simple": "回答控制在50字以内，只考虑核心因素影响，简洁明了，直接给结论。",
        "balanced": "回答控制在50-100字，考虑多个核心因素的影响，平衡专业性与易懂性。",
        "professional": "全面综合考虑影响因素，详细阐述，深入分析，有理有据，无字数限制。"
    }
    
    @classmethod
    def build_system_prompt(
        cls,
        ai_style: str = "professional",
        bazi_info: Optional[Dict] = None
    ) -> str:
        """
        构建系统提示词
        
        组成：系统提示词 + 对话模式 + 用户信息
        """
        import logging
        logger = logging.getLogger(__name__)
        
        # 组装提示词
        prompt_parts = [cls.SYSTEM_ROLE]
        
        # 添加对话模式
        style_prompt = cls.STYLE_PROMPTS.get(ai_style, cls.STYLE_PROMPTS["professional"])
        prompt_parts.append(style_prompt)
        
        # 添加用户信息（如果有）
        if bazi_info:
            logger.info(f"✅ 注入八字信息: name={bazi_info.get('name')}, gender={bazi_info.get('gender')}")
            user_info = cls._build_user_info(bazi_info)
            prompt_parts.append(user_info)
        else:
            logger.info("ℹ️ 无八字档案，使用通用提示词")
        
        return "\n\n".join(prompt_parts)
    
    # 3. 用户信息字段映射
    _USER_INFO_FIELDS = [
        ('name', '姓名'),
        ('gender', '性别'),
        ('bazi', '八字'),
        ('jieqi_info', '节气'),
        ('dayun_info', '大运'),
        ('formatted_output', '详细分析')
    ]
    
    # 性别映射表
    _GENDER_MAP = {
        'male': '男',
        'female': '女',
        '男': '男',
        '女': '女'
    }
    
    @classmethod
    def _build_user_info(cls, bazi_info: Dict) -> str:
        """
        构建用户信息文本（数据库变量直接赋值）
        
        Returns:
            格式化的用户信息文本，如果没有任何信息则返回空字符串
        """
        info_parts = []
        
        for field_key, field_label in cls._USER_INFO_FIELDS:
            value = bazi_info.get(field_key)
            if not value:
                continue
            
            # 特殊处理：性别字段需要转换
            if field_key == 'gender':
                value = cls._GENDER_MAP.get(value, value)
            
            info_parts.append(f"{field_label}：{value}")
        
        return f"当前用户信息：\n" + "\n".join(info_parts) if info_parts else ""
    
    @classmethod
    def get_available_styles(cls) -> list:
        """获取所有可用的对话风格"""
        return list(cls.STYLE_PROMPTS.keys())
    
    @classmethod
    def validate_style(cls, ai_style: str) -> bool:
        """验证对话风格是否有效"""
        return ai_style in cls.STYLE_PROMPTS
