#!/usr/bin/env python3
"""
人设生成模块
"""

import random
from typing import Dict


class CharacterProfile:
    """角色人设生成器"""
    
    def __init__(self):
        """初始化人设生成器"""
        pass
    
    def generate(self, genre: str, gender: str) -> Dict:
        """
        生成角色人设
        
        Args:
            genre: 题材类型
            gender: 性别
            
        Returns:
            人设字典
        """
        # 从题材数据中获取特征
        # 这里简化处理，实际应该从各题材的数据文件中读取
        
        personality_traits = {
            'male': ['自信', '果断', '沉稳', '幽默', '理性', '坚韧', '开朗', '正直',
                     '冷静', '热情', '专注', '创新', '务实', '担当', '豁达'],
            'female': ['温柔', '独立', '聪慧', '优雅', '活泼', '细腻', '大方', '知性',
                       '坚强', '善良', '敏锐', '自信', '开朗', '沉稳', '浪漫']
        }
        
        appearance_traits = {
            'male': ['身材高大', '五官端正', '气质儒雅', '阳光帅气', '成熟稳重',
                     '清瘦干练', '眉清目秀', '英气逼人', '温文尔雅', '精神抖擞'],
            'female': ['长发及腰', '短发干练', '五官精致', '气质优雅', '身材高挑',
                       '明眸皓齿', '肤白貌美', '清新脱俗', '时尚靓丽', '温婉可人']
        }
        
        backgrounds = [
            '出生于书香门第，父母都是大学教授',
            '来自普通工薪家庭，靠自己的努力打拼',
            '家境优渥，从小接受精英教育',
            '单亲家庭长大，性格独立坚强',
            '海外留学归来，视野开阔',
            '小城市出身，在大城市奋斗',
            '创业家庭背景，有商业头脑',
            '艺术世家，从小受艺术熏陶',
            '军人家庭，纪律性强',
            '医生家庭，理性冷静'
        ]
        
        return {
            'personality': random.choice(personality_traits.get(gender, personality_traits['male'])),
            'appearance': random.choice(appearance_traits.get(gender, appearance_traits['male'])),
            'background': random.choice(backgrounds),
        }
