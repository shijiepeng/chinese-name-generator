#!/usr/bin/env python3
"""
中文姓名生成器 - 主模块
支持多题材、批量导出、谐音检测、人设关联
"""

import json
import random
from typing import List, Dict, Optional, Tuple
from pathlib import Path

from .genres.modern import ModernGenre
from .genres.ancient import AncientGenre
from .genres.scifi import SciFiGenre
from .genres.mystery import MysteryGenre
from .genres.romance import RomanceGenre
from .genres.fantasy import FantasyGenre
from .pronunciation import PronunciationChecker
from .character_profile import CharacterProfile
from .exporter import NameExporter


class ChineseNameGenerator:
    """中文姓名生成器主类"""
    
    # 支持的题材
    GENRES = {
        'modern': ModernGenre,
        'ancient': AncientGenre,
        'scifi': SciFiGenre,
        'mystery': MysteryGenre,
        'romance': RomanceGenre,
        'fantasy': FantasyGenre,
    }
    
    def __init__(self, data_dir: Optional[str] = None):
        """
        初始化生成器
        
        Args:
            data_dir: 数据文件目录，默认为项目下的 data 目录
        """
        if data_dir is None:
            data_dir = Path(__file__).parent.parent / 'data'
        self.data_dir = Path(data_dir)
        
        # 加载姓氏库
        self.surnames = self._load_surnames()
        
        # 初始化各题材生成器
        self.genre_instances = {}
        for genre_name, genre_class in self.GENRES.items():
            self.genre_instances[genre_name] = genre_class(self.data_dir)
        
        # 初始化辅助功能
        self.pronunciation = PronunciationChecker()
        self.profile = CharacterProfile()
        self.exporter = NameExporter()
    
    def _load_surnames(self) -> Dict[str, List[str]]:
        """加载姓氏库"""
        surnames_file = self.data_dir / 'surnames.json'
        if surnames_file.exists():
            with open(surnames_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        # 默认姓氏库
        return {
            'common': [
                '王', '李', '张', '刘', '陈', '杨', '黄', '赵', '吴', '周',
                '徐', '孙', '马', '朱', '胡', '郭', '林', '何', '高', '罗',
                '郑', '梁', '谢', '宋', '唐', '许', '韩', '冯', '邓', '曹',
                '彭', '曾', '肖', '田', '董', '袁', '潘', '于', '蒋', '蔡',
                '余', '杜', '叶', '程', '苏', '魏', '吕', '丁', '任', '沈',
            ],
            'rare': [
                '姚', '卢', '姜', '崔', '钟', '谭', '陆', '汪', '范', '金',
                '石', '廖', '贾', '夏', '韦', '傅', '方', '白', '邹', '孟',
            ]
        }
    
    def generate(self, 
                 genre: str = 'modern',
                 gender: str = 'random',
                 count: int = 1,
                 with_profile: bool = False,
                 check_pronunciation: bool = True) -> List[Dict]:
        """
        生成姓名
        
        Args:
            genre: 题材类型 (modern/ancient/scifi/mystery/romance/fantasy)
            gender: 性别 (male/female/random)
            count: 生成数量
            with_profile: 是否附带人设
            check_pronunciation: 是否检查谐音
            
        Returns:
            姓名列表，每个姓名为包含详细信息的字典
        """
        if genre not in self.GENRES:
            raise ValueError(f"不支持的题材: {genre}，可选: {list(self.GENRES.keys())}")
        
        if gender not in ['male', 'female', 'random']:
            raise ValueError("gender 必须是 'male', 'female' 或 'random'")
        
        # 随机性别
        if gender == 'random':
            gender = random.choice(['male', 'female'])
        
        genre_instance = self.genre_instances[genre]
        results = []
        attempts = 0
        max_attempts = count * 10  # 防止无限循环
        
        while len(results) < count and attempts < max_attempts:
            attempts += 1
            
            # 选择姓氏
            surname_pool = self.surnames.get('common', self.surnames['common'])
            surname = random.choice(surname_pool)
            
            # 生成名字
            given_name = genre_instance.generate_name(gender)
            
            # 完整姓名
            full_name = surname + given_name
            
            # 谐音检查
            if check_pronunciation:
                issues = self.pronunciation.check(full_name)
                if issues:
                    continue  # 有谐音问题，重新生成
            
            # 构建结果
            result = {
                'name': full_name,
                'surname': surname,
                'given_name': given_name,
                'gender': gender,
                'genre': genre,
                'pinyin': self.pronunciation.to_pinyin(full_name),
            }
            
            # 添加人设
            if with_profile:
                result['profile'] = self.profile.generate(genre, gender)
            
            results.append(result)
        
        return results
    
    def generate_batch(self,
                      genres: Optional[List[str]] = None,
                      genders: Optional[List[str]] = None,
                      count_per_combo: int = 5,
                      with_profile: bool = True) -> Dict[str, List[Dict]]:
        """
        批量生成多个题材的姓名
        
        Args:
            genres: 题材列表，默认所有题材
            genders: 性别列表，默认男女都生成
            count_per_combo: 每种组合生成数量
            with_profile: 是否附带人设
            
        Returns:
            按题材分类的姓名字典
        """
        if genres is None:
            genres = list(self.GENRES.keys())
        if genders is None:
            genders = ['male', 'female']
        
        results = {}
        for genre in genres:
            genre_results = []
            for gender in genders:
                names = self.generate(
                    genre=genre,
                    gender=gender,
                    count=count_per_combo,
                    with_profile=with_profile
                )
                genre_results.extend(names)
            results[genre] = genre_results
        
        return results
    
    def export(self, 
               names: List[Dict], 
               filepath: str, 
               format: Optional[str] = None):
        """
        导出姓名到文件
        
        Args:
            names: 姓名列表
            filepath: 输出文件路径
            format: 格式 (json/csv/txt)，默认从文件扩展名推断
        """
        self.exporter.export(names, filepath, format)
    
    def get_genre_info(self) -> Dict[str, str]:
        """获取所有题材的信息"""
        info = {}
        for name, genre_class in self.GENRES.items():
            instance = genre_class(self.data_dir)
            info[name] = {
                'name': instance.name,
                'description': instance.description,
            }
        return info


# 便捷函数
def generate_names(genre: str = 'modern', 
                   gender: str = 'random',
                   count: int = 10,
                   with_profile: bool = False) -> List[Dict]:
    """便捷函数：快速生成姓名"""
    generator = ChineseNameGenerator()
    return generator.generate(genre, gender, count, with_profile)


if __name__ == '__main__':
    # 简单测试
    gen = ChineseNameGenerator()
    print("=== 现代都市风格 ===")
    names = gen.generate('modern', count=5, with_profile=True)
    for n in names:
        print(f"{n['name']} ({n['pinyin']}) - {n['gender']}")
        if 'profile' in n:
            print(f"  性格: {n['profile']['personality']}")
            print(f"  外貌: {n['profile']['appearance']}")
