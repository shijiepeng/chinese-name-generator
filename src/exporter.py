#!/usr/bin/env python3
"""
导出功能模块
"""

import json
import csv
from typing import List, Dict, Optional
from pathlib import Path


class NameExporter:
    """姓名导出器"""
    
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
        filepath = Path(filepath)
        
        # 自动推断格式
        if format is None:
            format = filepath.suffix.lower().lstrip('.')
        
        if format == 'json':
            self._export_json(names, filepath)
        elif format == 'csv':
            self._export_csv(names, filepath)
        elif format == 'txt':
            self._export_txt(names, filepath)
        else:
            raise ValueError(f"不支持的格式: {format}，请使用 json/csv/txt")
    
    def _export_json(self, names: List[Dict], filepath: Path):
        """导出为 JSON"""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(names, f, ensure_ascii=False, indent=2)
    
    def _export_csv(self, names: List[Dict], filepath: Path):
        """导出为 CSV"""
        if not names:
            return
        
        # 确定字段
        fieldnames = ['name', 'surname', 'given_name', 'gender', 'genre', 'pinyin']
        
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for name in names:
                row = {k: v for k, v in name.items() if k in fieldnames}
                writer.writerow(row)
    
    def _export_txt(self, names: List[Dict], filepath: Path):
        """导出为 TXT"""
        with open(filepath, 'w', encoding='utf-8') as f:
            for name in names:
                line = f"{name['name']} ({name['pinyin']}) - {name['gender']}\n"
                f.write(line)
