#!/usr/bin/env python3
"""
Minecraft Screenshots Pro - 主入口
无参数时启动图形界面，有参数时启动命令行。
"""
import sys

def main():
    if len(sys.argv) > 1:
        # 启动命令行模式
        from cli import main as cli_main
        cli_main()
    else:
        # 启动图形界面
        from src.gui.app import run_app
        run_app()

if __name__ == "__main__":
    main()