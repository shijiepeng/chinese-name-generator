#!/usr/bin/env python3
"""
科幻未来题材
"""

import random
from .base import BaseGenre


class SciFiGenre(BaseGenre):
    """科幻未来题材"""
    
    name = "科幻未来"
    description = "科技感、未来感、独特的科幻风格"
    data_file = "scifi.json"
    
    def generate_name(self, gender: str) -> str:
        """生成科幻风格名字"""
        gender_data = self.data.get(gender, {})
        
        # 科幻风格偏好双字名
        names = gender_data.get('double', [])
        
        if names:
            return random.choice(names)
        
        # 备用方案：使用中性数字
        neutral = self.data.get('neutral', ['零', '一', '二', '三'])
        return random.choice(neutral) + random.choice(neutral)
