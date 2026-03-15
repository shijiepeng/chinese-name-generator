#!/usr/bin/env python3
"""
谐音检测模块
"""

import re
from typing import List, Dict


class PronunciationChecker:
    """谐音检测器"""
    
    # 尴尬谐音列表（简化的拼音近似匹配）
    AWKWARD_PATTERNS = {
        # 不雅谐音
        '史珍香': '不雅谐音',
        '杜子腾': '不雅谐音',
        '范统': '不雅谐音',
        '朱逸群': '不雅谐音',
        '秦寿': '不雅谐音',
        '杨伟': '不雅谐音',
        '沈京兵': '不雅谐音',
        '蔡泰贤': '不雅谐音',
        '马统钙': '不雅谐音',
        '魏生津': '不雅谐音',
        # 可继续添加
    }
    
    # 姓氏与名字的冲突组合
    SURNAME_NAME_CONFLICTS = {
        '吴': ['德', '能', '用', '为', '力'],  # 吴德 -> 无德
        '贾': ['正经', '文明', '仁义'],  # 贾正经 -> 假正经
        '范': ['统', '建', '围'],  # 范统 -> 饭桶
        '朱': ['逸群', '投', '葛亮'],  # 朱逸群 -> 猪一群
        '秦': ['寿', '生', '授'],  # 秦寿 -> 禽兽
        '史': ['珍香', '浩', '劲'],  # 史珍香 -> 屎真香
    }
    
    # 简单的拼音映射（用于基础检测）
    PINYIN_MAP = {
        'a': '啊', 'ai': '爱', 'an': '安', 'ang': '昂', 'ao': '奥',
        'ba': '巴', 'bai': '白', 'ban': '班', 'bang': '帮', 'bao': '包',
        'bei': '北', 'ben': '本', 'beng': '崩', 'bi': '比', 'bian': '边',
        'biao': '标', 'bie': '别', 'bin': '宾', 'bing': '冰', 'bo': '波',
        'bu': '不', 'ca': '擦', 'cai': '才', 'can': '参', 'cang': '仓',
        'cao': '草', 'ce': '策', 'cen': '岑', 'ceng': '层', 'cha': '查',
        'chai': '柴', 'chan': '产', 'chang': '长', 'chao': '超', 'che': '车',
        'chen': '陈', 'cheng': '成', 'chi': '吃', 'chong': '充', 'chou': '抽',
        'chu': '出', 'chuai': '揣', 'chuan': '穿', 'chuang': '床', 'chui': '吹',
        'chun': '春', 'chuo': '戳', 'ci': '次', 'cong': '从', 'cou': '凑',
        'cu': '粗', 'cuan': '窜', 'cui': '催', 'cun': '村', 'cuo': '错',
        'da': '大', 'dai': '代', 'dan': '单', 'dang': '当', 'dao': '到',
        'de': '德', 'dei': '得', 'deng': '等', 'di': '地', 'dian': '点',
        'diao': '掉', 'die': '跌', 'ding': '丁', 'diu': '丢', 'dong': '东',
        'dou': '都', 'du': '读', 'duan': '段', 'dui': '对', 'dun': '顿',
        'duo': '多', 'e': '额', 'ei': '诶', 'en': '恩', 'er': '而',
        'fa': '发', 'fan': '反', 'fang': '方', 'fei': '飞', 'fen': '分',
        'feng': '风', 'fo': '佛', 'fou': '否', 'fu': '服', 'ga': '嘎',
        'gai': '该', 'gan': '干', 'gang': '刚', 'gao': '高', 'ge': '哥',
        'gei': '给', 'gen': '根', 'geng': '更', 'gong': '工', 'gou': '狗',
        'gu': '古', 'gua': '瓜', 'guai': '怪', 'guan': '关', 'guang': '光',
        'gui': '鬼', 'gun': '滚', 'guo': '国', 'ha': '哈', 'hai': '海',
        'han': '汉', 'hang': '行', 'hao': '好', 'he': '和', 'hei': '黑',
        'hen': '很', 'heng': '横', 'hong': '红', 'hou': '后', 'hu': '胡',
        'hua': '花', 'huai': '坏', 'huan': '欢', 'huang': '黄', 'hui': '回',
        'hun': '婚', 'huo': '火', 'ji': '机', 'jia': '家', 'jian': '见',
        'jiang': '江', 'jiao': '交', 'jie': '姐', 'jin': '金', 'jing': '京',
        'jiong': '窘', 'jiu': '九', 'ju': '句', 'juan': '卷', 'jue': '绝',
        'jun': '军', 'ka': '卡', 'kai': '开', 'kan': '看', 'kang': '康',
        'kao': '考', 'ke': '科', 'ken': '肯', 'keng': '坑', 'kong': '空',
        'kou': '口', 'ku': '哭', 'kua': '夸', 'kuai': '快', 'kuan': '宽',
        'kuang': '狂', 'kui': '亏', 'kun': '困', 'kuo': '扩', 'la': '拉',
        'lai': '来', 'lan': '蓝', 'lang': '狼', 'lao': '老', 'le': '了',
        'lei': '累', 'leng': '冷', 'li': '里', 'lia': '俩', 'lian': '连',
        'liang': '两', 'liao': '聊', 'lie': '列', 'lin': '林', 'ling': '令',
        'liu': '刘', 'long': '龙', 'lou': '楼', 'lu': '路', 'luan': '乱',
        'lue': '略', 'lun': '轮', 'luo': '罗', 'ma': '马', 'mai': '买',
        'man': '满', 'mang': '忙', 'mao': '毛', 'me': '么', 'mei': '美',
        'men': '门', 'meng': '梦', 'mi': '米', 'mian': '面', 'miao': '妙',
        'mie': '灭', 'min': '民', 'ming': '明', 'miu': '谬', 'mo': '魔',
        'mou': '某', 'mu': '木', 'na': '那', 'nai': '奶', 'nan': '男',
        'nang': '囊', 'nao': '脑', 'ne': '呢', 'nei': '内', 'nen': '嫩',
        'neng': '能', 'ni': '你', 'nian': '年', 'niang': '娘', 'niao': '鸟',
        'nie': '捏', 'nin': '您', 'ning': '宁', 'niu': '牛', 'nong': '农',
        'nou': '耨', 'nu': '努', 'nuan': '暖', 'nue': '虐', 'nuo': '诺',
        'o': '哦', 'ou': '欧', 'pa': '怕', 'pai': '拍', 'pan': '盘',
        'pang': '胖', 'pao': '跑', 'pei': '配', 'pen': '喷', 'peng': '朋',
        'pi': '皮', 'pian': '片', 'piao': '票', 'pie': '撇', 'pin': '品',
        'ping': '平', 'po': '破', 'pou': '剖', 'pu': '普', 'qi': '七',
        'qia': '恰', 'qian': '千', 'qiang': '强', 'qiao': '桥', 'qie': '且',
        'qin': '亲', 'qing': '青', 'qiong': '穷', 'qiu': '秋', 'qu': '去',
        'quan': '全', 'que': '却', 'qun': '群', 'ran': '然', 'rang': '让',
        'rao': '绕', 're': '热', 'ren': '人', 'reng': '仍', 'ri': '日',
        'rong': '容', 'rou': '肉', 'ru': '如', 'ruan': '软', 'rui': '瑞',
        'run': '润', 'ruo': '若', 'sa': '撒', 'sai': '赛', 'san': '三',
        'sang': '桑', 'sao': '扫', 'se': '色', 'sen': '森', 'seng': '僧',
        'sha': '沙', 'shai': '晒', 'shan': '山', 'shang': '上', 'shao': '少',
        'she': '社', 'shei': '谁', 'shen': '身', 'sheng': '生', 'shi': '是',
        'shou': '手', 'shu': '书', 'shua': '刷', 'shuai': '帅', 'shuan': '拴',
        'shuang': '双', 'shui': '水', 'shun': '顺', 'shuo': '说', 'si': '四',
        'song': '送', 'sou': '搜', 'su': '苏', 'suan': '算', 'sui': '岁',
        'sun': '孙', 'suo': '所', 'ta': '他', 'tai': '太', 'tan': '谈',
        'tang': '唐', 'tao': '逃', 'te': '特', 'teng': '疼', 'ti': '体',
        'tian': '天', 'tiao': '条', 'tie': '铁', 'ting': '听', 'tong': '同',
        'tou': '头', 'tu': '图', 'tuan': '团', 'tui': '推', 'tun': '吞',
        'tuo': '拖', 'wa': '挖', 'wai': '外', 'wan': '万', 'wang': '王',
        'wei': '为', 'wen': '文', 'weng': '翁', 'wo': '我', 'wu': '五',
        'xi': '西', 'xia': '下', 'xian': '先', 'xiang': '想', 'xiao': '小',
        'xie': '写', 'xin': '心', 'xing': '星', 'xiong': '兄', 'xiu': '休',
        'xu': '许', 'xuan': '选', 'xue': '学', 'xun': '寻', 'ya': '呀',
        'yan': '言', 'yang': '阳', 'yao': '要', 'ye': '也', 'yi': '一',
        'yin': '因', 'ying': '英', 'yo': '哟', 'yong': '用', 'you': '有',
        'yu': '于', 'yuan': '元', 'yue': '月', 'yun': '云', 'za': '杂',
        'zai': '在', 'zan': '赞', 'zang': '脏', 'zao': '早', 'ze': '则',
        'zei': '贼', 'zen': '怎', 'zeng': '增', 'zha': '炸', 'zhai': '摘',
        'zhan': '站', 'zhang': '张', 'zhao': '找', 'zhe': '这', 'zhei': '这',
        'zhen': '真', 'zheng': '正', 'zhi': '只', 'zhong': '中', 'zhou': '周',
        'zhu': '主', 'zhua': '抓', 'zhuai': '拽', 'zhuan': '转', 'zhuang': '装',
        'zhui': '追', 'zhun': '准', 'zhuo': '捉', 'zi': '子', 'zong': '总',
        'zou': '走', 'zu': '组', 'zuan': '钻', 'zui': '最', 'zun': '尊',
        'zuo': '做'
    }
    
    def __init__(self):
        """初始化谐音检测器"""
        pass
    
    def check(self, name: str) -> List[Dict]:
        """
        检查姓名是否有谐音问题
        
        Args:
            name: 完整姓名
            
        Returns:
            问题列表，每个问题包含类型和描述
        """
        issues = []
        
        # 检查已知的尴尬谐音
        if name in self.AWKWARD_PATTERNS:
            issues.append({
                'type': 'awkward',
                'description': self.AWKWARD_PATTERNS[name]
            })
        
        # 检查姓氏与名字的冲突
        surname = name[0]
        given_name = name[1:]
        if surname in self.SURNAME_NAME_CONFLICTS:
            conflicts = self.SURNAME_NAME_CONFLICTS[surname]
            for conflict in conflicts:
                if conflict in given_name:
                    issues.append({
                        'type': 'surname_conflict',
                        'description': f'姓氏"{surname}"与"{conflict}"组合可能产生不雅谐音'
                    })
                    break
        
        return issues
    
    def to_pinyin(self, name: str) -> str:
        """
        将姓名转换为拼音（简化版）
        
        Args:
            name: 中文姓名
            
        Returns:
            拼音字符串
        """
        # 这是一个简化版，实际应该使用 pypinyin 库
        # 这里返回一个占位符
        return ' '.join(['*'] * len(name))
