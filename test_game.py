#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
游戏功能测试脚本
"""

from core import WordGame

def test_word_game():
    """测试游戏核心功能"""
    print("=== 英语单词猜词游戏测试 ===\n")
    
    # 创建游戏实例
    game = WordGame()
    
    # 测试词库加载
    print("1. 测试词库加载...")
    libraries = game.load_word_libraries()
    if libraries:
        print(f"   成功加载 {len(libraries)} 个词库:")
        for name, words in libraries.items():
            print(f"   - {name}: {len(words)} 个单词")
    else:
        print("   错误：未找到词库文件")
        return
    
    # 测试词库选择
    print("\n2. 测试词库选择...")
    library_name = list(libraries.keys())[0]
    if game.select_library(library_name):
        print(f"   成功选择词库: {library_name}")
        
        # 获取词库信息
        info = game.get_library_info()
        print(f"   词库信息: {info['total_words']} 个单词")
        
        # 获取可用长度
        lengths = game.get_available_lengths()
        print(f"   可用单词长度: {lengths[:10]}...")  # 只显示前10个
    else:
        print("   错误：词库选择失败")
        return
    
    # 测试游戏开始
    print("\n3. 测试游戏开始...")
    test_length = 5
    if test_length in lengths:
        if game.start_new_game(test_length):
            status = game.get_game_status()
            print(f"   成功开始游戏，目标单词长度: {test_length}")
            print(f"   最大尝试次数: {status['max_attempts']}")
            print(f"   目标单词: {status['target_word']} (测试用)")
        else:
            print("   错误：游戏开始失败")
            return
    else:
        print(f"   错误：词库中没有长度为 {test_length} 的单词")
        return
    
    # 测试单词验证
    print("\n4. 测试单词验证...")
    test_words = ["hello", "world", "test", "invalid"]
    for word in test_words:
        is_valid = game.is_valid_word(word)
        print(f"   单词 '{word}': {'有效' if is_valid else '无效'}")
    
    # 测试猜测功能
    print("\n5. 测试猜测功能...")
    target = status['target_word']
    print(f"   目标单词: {target}")
    
    # 模拟一些猜测
    test_guesses = ["hello", "world", target]
    for guess in test_guesses:
        if len(guess) == test_length:
            feedback = game.make_guess(guess)
            if feedback:
                print(f"   猜测 '{guess}':")
                for i, (letter, color) in enumerate(feedback):
                    print(f"      {i+1}: {letter} ({color})")
                
                # 检查游戏状态
                status = game.get_game_status()
                if status['game_over']:
                    print(f"   游戏结束，结果: {'胜利' if status['won'] else '失败'}")
                    break
            else:
                print(f"   猜测 '{guess}': 无效单词")
    
    print("\n=== 测试完成 ===")

if __name__ == "__main__":
    test_word_game() 