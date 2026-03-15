#!/usr/bin/env python3
"""
西幻/异世界题材
"""

import random
from .base import BaseGenre


class FantasyGenre(BaseGenre):
    """西幻/异世界题材"""
    
    name = "西幻/异世界"
    description = "奇幻、神秘、有魔法感的幻想风格"
    data_file = "fantasy.json"
    
    def generate_name(self, gender: str) -> str:
        """生成西幻风格名字"""
        gender_data = self.data.get(gender, {})
        
        # 西幻风格偏好双字名
        names = gender_data.get('double', [])
        
        if names:
            return random.choice(names)
        
        # 备用方案
        fallback = ['魔法', '龙骑', '圣光'] if gender == 'male' else ['精灵', '仙女', '魔女']
        return random.choice(fallback)
