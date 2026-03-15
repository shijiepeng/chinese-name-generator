#!/usr/bin/env python3
"""
现代都市题材
"""

import random
from .base import BaseGenre


class ModernGenre(BaseGenre):
    """现代都市题材"""
    
    name = "现代都市"
    description = "时尚、简洁、国际化的现代风格"
    data_file = "modern.json"
    
    def generate_name(self, gender: str) -> str:
        """生成现代风格名字"""
        gender_data = self.data.get(gender, {})
        
        # 70% 概率双字名，30% 概率单字名
        if random.random() < 0.7:
            names = gender_data.get('double', [])
        else:
            names = gender_data.get('single', [])
        
        if names:
            return random.choice(names)
        
        # 备用方案
        fallback = ['明', '伟', '强', '磊'] if gender == 'male' else ['丽', '娜', '敏', '静']
        return random.choice(fallback)
