#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
打包脚本 - 将Python程序打包为exe文件
"""

import os
import sys
import subprocess
import shutil

def check_pyinstaller():
    """检查是否安装了pyinstaller"""
    try:
        import PyInstaller
        return True
    except ImportError:
        return False

def install_pyinstaller():
    """安装pyinstaller"""
    print("正在安装pyinstaller...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--user", "pyinstaller"])
        return True
    except subprocess.CalledProcessError:
        print("安装pyinstaller失败")
        return False

def build_exe():
    """打包为exe文件"""
    print("开始打包程序...")
    
    # 检查pyinstaller
    if not check_pyinstaller():
        if install_pyinstaller():
            print("PyInstaller 安装完成，正在重新启动打包脚本...")
            os.execv(sys.executable, [sys.executable] + sys.argv)
        else:
            return False
    
    # 判断add-data分隔符
    if sys.platform.startswith('win'):
        add_data_sep = ';'
    else:
        add_data_sep = ':'
    add_data_arg = f"--add-data=wordlib{add_data_sep}wordlib"
    
    icon_file = "favicon.ico"
    icon_arg = f"--icon={icon_file}"
    
    # 构建命令
    if os.path.exists(icon_file):
        cmd = [
            sys.executable, "-m", "pyinstaller",
            "--onefile",           # 打包为单个文件
            "--windowed",          # 无控制台窗口
            "--name=WordGame",     # 可执行文件名
            add_data_arg,           # 包含词库目录
            icon_arg,               # 图标参数
            "main.py"
        ]
    else:
        cmd = [
            sys.executable, "-m", "pyinstaller",
            "--onefile",           # 打包为单个文件
            "--windowed",          # 无控制台窗口
            "--name=WordGame",     # 可执行文件名
            add_data_arg,           # 包含词库目录
            "main.py"
        ]
    
    try:
        print("执行打包命令:", " ".join(cmd))
        subprocess.check_call(cmd)
        
        # 检查生成的文件
        exe_path = os.path.join("dist", "WordGame.exe")
        if os.path.exists(exe_path):
            print(f"打包成功！可执行文件: {exe_path}")
            return True
        else:
            print("打包失败：未找到生成的exe文件")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"打包失败: {e}")
        return False

def clean_build():
    """清理构建文件"""
    print("清理构建文件...")
    dirs_to_remove = ["build", "__pycache__"]
    files_to_remove = ["WordGame.spec"]
    
    for dir_name in dirs_to_remove:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"已删除目录: {dir_name}")
    
    for file_name in files_to_remove:
        if os.path.exists(file_name):
            os.remove(file_name)
            print(f"已删除文件: {file_name}")

def main():
    """主函数"""
    print("=== 英语单词猜词游戏打包工具 ===\n")
    
    # 检查必要文件
    required_files = ["main.py", "core.py", "ui.py", "utils.py", "wordlib"]
    missing_files = []
    
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print("错误：缺少必要文件:")
        for file in missing_files:
            print(f"  - {file}")
        return False
    
    print("检查完成，所有必要文件都存在")
    
    # 询问是否清理
    clean = input("\n是否清理之前的构建文件？(y/n): ").lower().strip()
    if clean == 'y':
        clean_build()
    
    # 开始打包
    if build_exe():
        print("\n=== 打包完成 ===")
        print("可执行文件位于 dist/WordGame.exe")
        print("你可以将此文件分发给其他用户使用")
        return True
    else:
        print("\n=== 打包失败 ===")
        return False

if __name__ == "__main__":
    success = main()
    if not success:
        input("\n按回车键退出...")
        sys.exit(1) 