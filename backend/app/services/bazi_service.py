"""
八字计算服务
"""
import sys
import os

# 添加bazi模块到Python路径
sys.path.append(os.path.join(os.path.dirname(__file__), '../../bazi'))

from bazi.bazi_tool import BaZiCalculator


class BaziService:
    """八字计算服务"""
    
    def calculate(
        self,
        name: str,
        gender: str,
        calendar: str,
        year: int,
        month: int,
        day: int,
        hour: int,
        minute: int,
        birth_city: str,
        current_city: str = None
    ) -> dict:
        """
        计算八字
        
        Args:
            name: 姓名
            gender: 性别
            calendar: 日历类型
            year: 年
            month: 月
            day: 日
            hour: 时
            minute: 分
            birth_city: 出生城市
            current_city: 现居城市
            
        Returns:
            八字结果字典
        """
        calculator = BaZiCalculator(
            name=name,
            gender=gender,
            calendar=calendar,
            year=year,
            month=month,
            day=day,
            hour=hour,
            minute=minute,
            birth_city=birth_city,
            current_city=current_city
        )
        
        # 构建结果字典
        result = {
            "bazi": calculator.ba_zi,
            "jieqi_info": calculator.jie_qi_info,
            "dayun_info": calculator.da_yun_info,
            "formatted_output": calculator.format_output()
        }
        
        return result

