#!/usr/bin/env python3
"""
悬疑推理题材
"""

import random
from .base import BaseGenre


class MysteryGenre(BaseGenre):
    """悬疑推理题材"""
    
    name = "悬疑推理"
    description = "冷静、理性、有深度的悬疑风格"
    data_file = "mystery.json"
    
    def generate_name(self, gender: str) -> str:
        """生成悬疑风格名字"""
        gender_data = self.data.get(gender, {})
        
        # 悬疑风格偏好双字名，显得沉稳
        if random.random() < 0.75:
            names = gender_data.get('double', [])
        else:
            names = gender_data.get('single', [])
        
        if names:
            return random.choice(names)
        
        # 备用方案
        fallback = ['沉墨', '冷静', '深邃'] if gender == 'male' else ['冷静', '清澈', '明亮']
        return random.choice(fallback)
