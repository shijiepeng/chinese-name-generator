#!/usr/bin/env python3
"""
古代/古风题材
"""

import random
from .base import BaseGenre


class AncientGenre(BaseGenre):
    """古代/古风题材"""
    
    name = "古代/古风"
    description = "典雅、诗意、有文化底蕴的古典风格"
    data_file = "ancient.json"
    
    def generate_name(self, gender: str) -> str:
        """生成古风名字"""
        gender_data = self.data.get(gender, {})
        
        # 古风偏好双字名
        if random.random() < 0.8:
            names = gender_data.get('double', [])
        else:
            names = gender_data.get('single', [])
        
        if names:
            return random.choice(names)
        
        # 备用方案
        fallback = ['子墨', '云轩', '景行'] if gender == 'male' else ['婉儿', '若曦', '清婉']
        return random.choice(fallback)
