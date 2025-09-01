#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
英语单词趣味猜词游戏
主程序入口
"""

import sys
import os

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ui import WordGameUI

def main():
    """主函数"""
    try:
        # 创建并运行游戏界面
        app = WordGameUI()
        app.run()
    except Exception as e:
        print(f"程序启动失败: {e}")
        input("按回车键退出...")
        sys.exit(1)

if __name__ == "__main__":
    main() 