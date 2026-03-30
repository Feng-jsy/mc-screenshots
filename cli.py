#!/usr/bin/env python3
"""
命令行接口：支持所有功能，可搭配 --help 查看参数。
"""
import argparse
import sys
import logging
from pathlib import Path
from src.core.scanner import scan_images
from src.core.organizer import organize_files
from src.utils.config_utils import ConfigManager
from src.utils.path_utils import detect_minecraft_versions
from src.utils.file_utils import setup_logging, ConflictMode

def main():
    parser = argparse.ArgumentParser(description="Minecraft Screenshots Pro - 命令行工具")
    parser.add_argument("source", nargs="?", help="源目录（Minecraft versions 文件夹）")
    parser.add_argument("-o", "--output", help="输出目录（默认桌面/输出文件夹）")
    parser.add_argument("-m", "--mode", choices=["flat", "by_version", "by_date"], default="flat",
                        help="输出模式：flat（平铺）、by_version（按版本）、by_date（按日期）")
    parser.add_argument("--only-screenshots", action="store_true",
                        help="仅提取 Minecraft 截图（基于文件名正则）")
    parser.add_argument("--conflict", choices=["overwrite", "rename"], default="rename",
                        help="文件冲突处理：overwrite（覆盖），rename（自动重命名）")
    parser.add_argument("--verbose", "-v", action="store_true", help="显示详细日志")
    parser.add_argument("--version", action="version", version="%(prog)s 1.0.0")
    args = parser.parse_args()

    setup_logging(args.verbose)

    # 加载配置
    config = ConfigManager()
    source_dir = args.source or config.get("source_root")
    output_dir = args.output or config.get("output_dir")

    # 自动检测源目录（若未提供且配置中也没有）
    if not source_dir:
        detected = detect_minecraft_versions()
        if detected:
            print(f"自动检测到 Minecraft 版本目录：{detected}")
            resp = input("是否使用此目录？(Y/n): ").strip().lower()
            if resp in ('', 'y', 'yes'):
                source_dir = detected
            else:
                source_dir = None
        if not source_dir:
            print("未提供源目录，请手动输入：")
            source_dir = input("路径: ").strip()
            if not source_dir:
                print("错误：未指定源目录。")
                sys.exit(1)
    source_dir = Path(source_dir)
    if not source_dir.exists():
        print(f"错误：源目录不存在: {source_dir}")
        sys.exit(1)

    if not output_dir:
        output_dir = Path.home() / "Desktop" / "输出文件夹"
    else:
        output_dir = Path(output_dir)

    print(f"源目录: {source_dir}")
    print(f"输出目录: {output_dir}")
    print(f"模式: {args.mode}")
    print(f"仅截图: {args.only_screenshots}")
    print(f"冲突处理: {args.conflict}")

    # 扫描图片（返回带版本名的列表）
    images = scan_images(source_dir, only_screenshots=args.only_screenshots)
    total = len(images)
    if total == 0:
        print("未找到任何符合条件的图片。")
        return

    print(f"找到 {total} 张图片，开始整理...")

    # 进度回调
    def progress_callback(current, total):
        percent = int(current / total * 100)
        print(f"\r进度: {current}/{total} ({percent}%)", end="")

    # 冲突模式转换
    conflict_mode = ConflictMode.OVERWRITE if args.conflict == "overwrite" else ConflictMode.RENAME

    organize_files(images, output_dir, args.mode, progress_callback, conflict_mode)
    print(f"\n完成！共处理 {total} 张图片。")
    print(f"输出目录: {output_dir}")

    # 保存本次使用的路径到配置
    config.set("source_root", str(source_dir))
    config.set("output_dir", str(output_dir))
    config.save()

if __name__ == "__main__":
    main()