#!/usr/bin/env python3
"""
使用示例
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.name_generator import ChineseNameGenerator


def demo_basic():
    """基础使用示例"""
    print("=" * 50)
    print("基础使用示例")
    print("=" * 50)
    
    gen = ChineseNameGenerator()
    
    # 生成 10 个现代都市风格的女性姓名
    print("\n现代都市风格（女性）：")
    names = gen.generate(genre='modern', gender='female', count=10)
    for n in names:
        print(f"  {n['name']} ({n['pinyin']})")


def demo_with_profile():
    """带人设的示例"""
    print("\n" + "=" * 50)
    print("带人设的示例")
    print("=" * 50)
    
    gen = ChineseNameGenerator()
    
    # 生成带人设的古代风格姓名
    print("\n古代/古风风格（带人设）：")
    names = gen.generate(genre='ancient', count=5, with_profile=True)
    for n in names:
        print(f"\n{n['name']} ({n['gender']})")
        print(f"  性格: {n['profile']['personality']}")
        print(f"  外貌: {n['profile']['appearance']}")
        print(f"  背景: {n['profile']['background']}")


def demo_all_genres():
    """展示所有题材"""
    print("\n" + "=" * 50)
    print("所有题材展示")
    print("=" * 50)
    
    gen = ChineseNameGenerator()
    genres = ['modern', 'ancient', 'scifi', 'mystery', 'romance', 'fantasy']
    genre_names = {
        'modern': '现代都市',
        'ancient': '古代/古风',
        'scifi': '科幻未来',
        'mystery': '悬疑推理',
        'romance': '言情',
        'fantasy': '西幻/异世界'
    }
    
    for genre in genres:
        print(f"\n{genre_names[genre]}：")
        names = gen.generate(genre=genre, gender='male', count=3)
        for n in names:
            print(f"  {n['name']}", end='')
        print()
        names = gen.generate(genre=genre, gender='female', count=3)
        for n in names:
            print(f"  {n['name']}", end='')
        print()


def demo_export():
    """导出示例"""
    print("\n" + "=" * 50)
    print("导出示例")
    print("=" * 50)
    
    gen = ChineseNameGenerator()
    
    # 生成并导出
    names = gen.generate(genre='modern', count=20, with_profile=True)
    
    # 导出为不同格式
    output_dir = Path(__file__).parent / 'output'
    output_dir.mkdir(exist_ok=True)
    
    gen.export(names, output_dir / 'names.json')
    print(f"已导出: {output_dir / 'names.json'}")
    
    gen.export(names, output_dir / 'names.csv')
    print(f"已导出: {output_dir / 'names.csv'}")
    
    gen.export(names, output_dir / 'names.txt')
    print(f"已导出: {output_dir / 'names.txt'}")


def demo_batch():
    """批量生成示例"""
    print("\n" + "=" * 50)
    print("批量生成示例")
    print("=" * 50)
    
    gen = ChineseNameGenerator()
    
    # 批量生成多个题材
    results = gen.generate_batch(
        genres=['modern', 'ancient', 'scifi'],
        count_per_combo=5
    )
    
    for genre, names in results.items():
        print(f"\n{genre}: 生成 {len(names)} 个姓名")
        for n in names[:3]:  # 只显示前3个
            print(f"  {n['name']} ({n['gender']})")


if __name__ == '__main__':
    demo_basic()
    demo_with_profile()
    demo_all_genres()
    demo_export()
    demo_batch()
    
    print("\n" + "=" * 50)
    print("所有示例运行完成！")
    print("=" * 50)
