import random
import os
from typing import List, Tuple, Optional

class WordGame:
    """英语单词猜词游戏核心逻辑"""
    
    def __init__(self):
        self.word_library = {}  # 词库字典 {词库名: 单词列表}
        self.current_library = None  # 当前选择的词库名
        self.target_word = ""  # 目标单词
        self.word_length = 0  # 目标单词长度
        self.max_attempts = 0  # 最大尝试次数
        self.attempts = []  # 已尝试的单词列表
        self.game_over = True  # 游戏是否结束
        self.won = False  # 是否获胜
        
    def load_word_libraries(self, wordlib_dir: str = "wordlib") -> dict:
        """加载词库目录下的所有词库文件"""
        if not os.path.exists(wordlib_dir):
            return {}
            
        libraries = {}
        for filename in os.listdir(wordlib_dir):
            if filename.endswith('.txt'):
                library_name = filename.replace('.txt', '')
                filepath = os.path.join(wordlib_dir, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        words = [word.strip().lower() for word in f.readlines() if word.strip()]
                    libraries[library_name] = words
                except Exception as e:
                    print(f"加载词库 {filename} 失败: {e}")
                    
        self.word_library = libraries
        return libraries
    
    def select_library(self, library_name: str) -> bool:
        """选择词库"""
        if library_name in self.word_library:
            self.current_library = library_name
            return True
        return False
    
    def get_available_lengths(self) -> List[int]:
        """获取当前词库中可用的单词长度"""
        if not self.current_library:
            return []
        
        lengths = set()
        for word in self.word_library[self.current_library]:
            lengths.add(len(word))
        return sorted(list(lengths))
    
    def start_new_game(self, word_length: int) -> bool:
        """开始新游戏"""
        if not self.current_library:
            return False
            
        # 筛选指定长度的单词
        available_words = [word for word in self.word_library[self.current_library] 
                          if len(word) == word_length]
        
        if not available_words:
            return False
            
        # 随机选择目标单词
        self.target_word = random.choice(available_words)
        self.word_length = word_length
        self.max_attempts = word_length + 1
        self.attempts = []
        self.game_over = False
        self.won = False
        
        return True
    
    def is_valid_word(self, word: str) -> bool:
        """检查单词是否在词库中"""
        if not self.current_library:
            return False
        return word.lower() in self.word_library[self.current_library]
    
    def make_guess(self, word: str) -> Optional[List[Tuple[str, str]]]:
        """进行猜测，返回颜色反馈"""
        word = word.lower().strip()
        
        # 检查单词长度
        if len(word) != self.word_length:
            return None
            
        # 检查单词是否在词库中
        if not self.is_valid_word(word):
            return None
            
        # 添加到尝试列表
        self.attempts.append(word)
        
        # 生成颜色反馈
        feedback = self._generate_feedback(word)
        
        # 检查游戏状态
        if word == self.target_word:
            self.game_over = True
            self.won = True
        elif len(self.attempts) >= self.max_attempts:
            self.game_over = True
            self.won = False
            
        return feedback
    
    def _generate_feedback(self, word: str) -> List[Tuple[str, str]]:
        """生成颜色反馈：('字母', '颜色')"""
        feedback = []
        target_letters = list(self.target_word)
        word_letters = list(word)
        
        # 第一遍：标记绿色（正确位置）
        for i in range(len(word_letters)):
            if word_letters[i] == target_letters[i]:
                feedback.append((word_letters[i], 'green'))
                target_letters[i] = '*'  # 标记已使用
                word_letters[i] = '#'  # 标记已处理
            else:
                feedback.append((word_letters[i], 'red'))
        
        # 第二遍：标记黄色（错误位置）
        for i in range(len(word_letters)):
            if word_letters[i] != '#':  # 未处理的字母
                if word_letters[i] in target_letters:
                    # 找到第一个未使用的相同字母
                    for j in range(len(target_letters)):
                        if target_letters[j] == word_letters[i]:
                            target_letters[j] = '*'
                            feedback[i] = (word_letters[i], 'yellow')
                            break
                # 否则保持红色
                
        return feedback
    
    def get_game_status(self) -> dict:
        """获取游戏状态"""
        return {
            'target_word': self.target_word,
            'word_length': self.word_length,
            'max_attempts': self.max_attempts,
            'current_attempts': len(self.attempts),
            'attempts': self.attempts.copy(),
            'game_over': self.game_over,
            'won': self.won,
            'remaining_attempts': self.max_attempts - len(self.attempts)
        }
    
    def get_library_info(self) -> dict:
        """获取词库信息"""
        if not self.current_library:
            return {}
            
        words = self.word_library[self.current_library]
        length_stats = {}
        for word in words:
            length = len(word)
            length_stats[length] = length_stats.get(length, 0) + 1
            
        return {
            'name': self.current_library,
            'total_words': len(words),
            'length_stats': length_stats
        } 