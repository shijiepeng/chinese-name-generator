#!/usr/bin/env python3
"""
言情题材
"""

import random
from .base import BaseGenre


class RomanceGenre(BaseGenre):
    """言情题材"""
    
    name = "言情"
    description = "柔美、浪漫、有情感的言情风格"
    data_file = "romance.json"
    
    def generate_name(self, gender: str) -> str:
        """生成言情风格名字"""
        gender_data = self.data.get(gender, {})
        
        # 言情风格偏好双字名，柔美
        if random.random() < 0.85:
            names = gender_data.get('double', [])
        else:
            names = gender_data.get('single', [])
        
        if names:
            return random.choice(names)
        
        # 备用方案
        fallback = ['温暖', '阳光', '深情'] if gender == 'male' else ['甜蜜', '柔软', '娇俏']
        return random.choice(fallback)
