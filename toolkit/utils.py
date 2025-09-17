#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
工具函数模块
为游戏功能扩展预留接口
"""

import os
import json
import time
from typing import Dict, List, Any

class GameUtils:
    """游戏工具类"""
    
    @staticmethod
    def save_game_stats(stats: Dict[str, Any], filename: str = "game_stats.json"):
        """保存游戏统计信息"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(stats, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"保存游戏统计失败: {e}")
            return False
    
    @staticmethod
    def load_game_stats(filename: str = "game_stats.json") -> Dict[str, Any]:
        """加载游戏统计信息"""
        try:
            if os.path.exists(filename):
                with open(filename, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"加载游戏统计失败: {e}")
        return {}
    
    @staticmethod
    def validate_word(word: str) -> bool:
        """验证单词格式"""
        if not word:
            return False
        # 检查是否只包含字母
        return word.isalpha()
    
    @staticmethod
    def get_word_difficulty(word: str) -> str:
        """评估单词难度"""
        length = len(word)
        if length <= 3:
            return "简单"
        elif length <= 5:
            return "中等"
        elif length <= 7:
            return "困难"
        else:
            return "极难"
    
    @staticmethod
    def calculate_score(attempts: int, max_attempts: int, word_length: int) -> int:
        """计算游戏得分"""
        base_score = 100
        attempt_penalty = (attempts - 1) * 10
        length_bonus = word_length * 5
        return max(0, base_score - attempt_penalty + length_bonus)

class WordLibraryUtils:
    """词库工具类"""
    
    @staticmethod
    def create_word_library(words: List[str], filename: str) -> bool:
        """创建新词库"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                for word in words:
                    f.write(word.lower().strip() + '\n')
            return True
        except Exception as e:
            print(f"创建词库失败: {e}")
            return False
    
    @staticmethod
    def merge_word_libraries(files: List[str], output_file: str) -> bool:
        """合并多个词库"""
        try:
            all_words = set()
            for file in files:
                if os.path.exists(file):
                    with open(file, 'r', encoding='utf-8') as f:
                        words = [word.strip().lower() for word in f.readlines() if word.strip()]
                        all_words.update(words)
            
            with open(output_file, 'w', encoding='utf-8') as f:
                for word in sorted(all_words):
                    f.write(word + '\n')
            return True
        except Exception as e:
            print(f"合并词库失败: {e}")
            return False
    
    @staticmethod
    def get_library_stats(filename: str) -> Dict[str, Any]:
        """获取词库统计信息"""
        try:
            if not os.path.exists(filename):
                return {}
            
            with open(filename, 'r', encoding='utf-8') as f:
                words = [word.strip().lower() for word in f.readlines() if word.strip()]
            
            length_stats = {}
            for word in words:
                length = len(word)
                length_stats[length] = length_stats.get(length, 0) + 1
            
            return {
                'total_words': len(words),
                'unique_words': len(set(words)),
                'length_stats': length_stats,
                'avg_length': sum(len(word) for word in words) / len(words) if words else 0
            }
        except Exception as e:
            print(f"获取词库统计失败: {e}")
            return {}

class ConfigManager:
    """配置管理器"""
    
    def __init__(self, config_file: str = "config.json"):
        self.config_file = config_file
        self.config = self.load_config()
    
    def load_config(self) -> Dict[str, Any]:
        """加载配置"""
        default_config = {
            'default_library': 'cet4',
            'default_length': 5,
            'theme': 'default',
            'sound_enabled': True,
            'auto_save': True
        }
        
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    # 合并默认配置
                    for key, value in default_config.items():
                        if key not in config:
                            config[key] = value
                    return config
        except Exception as e:
            print(f"加载配置失败: {e}")
        
        return default_config
    
    def save_config(self) -> bool:
        """保存配置"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"保存配置失败: {e}")
            return False
    
    def get(self, key: str, default=None):
        """获取配置值"""
        return self.config.get(key, default)
    
    def set(self, key: str, value: Any):
        """设置配置值"""
        self.config[key] = value
        self.save_config()

# 扩展接口预留
class ExtensionInterface:
    """扩展接口基类"""
    
    def __init__(self):
        self.name = "基础扩展"
        self.version = "1.0.0"
    
    def on_game_start(self, game_data: Dict[str, Any]):
        """游戏开始时调用"""
        pass
    
    def on_game_end(self, game_data: Dict[str, Any]):
        """游戏结束时调用"""
        pass
    
    def on_guess_made(self, guess_data: Dict[str, Any]):
        """每次猜测时调用"""
        pass
    
    def get_ui_elements(self) -> List[Dict[str, Any]]:
        """返回额外的UI元素"""
        return [] 