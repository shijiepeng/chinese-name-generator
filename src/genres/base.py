#!/usr/bin/env python3
"""
题材基类
"""

import json
import random
from abc import ABC, abstractmethod
from pathlib import Path


class BaseGenre(ABC):
    """题材基类"""
    
    name = "基础题材"
    description = "基础题材描述"
    data_file = None
    
    def __init__(self, data_dir: Path):
        """
        初始化
        
        Args:
            data_dir: 数据文件目录
        """
        self.data_dir = data_dir
        self.data = self._load_data()
    
    def _load_data(self) -> dict:
        """加载数据文件"""
        if self.data_file is None:
            return {}
        
        data_path = self.data_dir / self.data_file
        if data_path.exists():
            with open(data_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    @abstractmethod
    def generate_name(self, gender: str) -> str:
        """
        生成名字
        
        Args:
            gender: 性别 (male/female)
            
        Returns:
            名字字符串
        """
        pass
    
    def get_personality(self, gender: str) -> str:
        """获取性格特征"""
        traits = self.data.get('personality_traits', {})
        if gender in traits:
            return random.choice(traits[gender])
        return ""
    
    def get_appearance(self, gender: str) -> str:
        """获取外貌特征"""
        traits = self.data.get('appearance_traits', {})
        if gender in traits:
            return random.choice(traits[gender])
        return ""
    
    def get_background(self) -> str:
        """获取背景"""
        backgrounds = self.data.get('backgrounds', [])
        if backgrounds:
            return random.choice(backgrounds)
        return ""
