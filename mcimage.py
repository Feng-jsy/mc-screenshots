#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Minecraft 图片提取工具
从指定版本的 .minecraft/versions 目录中提取图片，支持筛选截图/全量，平铺/按版本输出。
"""

import os
import shutil
import sys
from pathlib import Path

# ---------- 配置区域 ----------
SOURCE_ROOT = r"D:\MC  PCL2\.minecraft\versions"  # 源目录
TARGET_DIR_NAME = "输出文件夹"                  # 输出文件夹名称（在桌面）
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".gif", ".tiff", ".tif", ".webp"}
SCREENSHOT_KEYWORD = "\\screenshots\\"          # 截图路径关键字（自动适配系统分隔符）
# ----------------------------

def get_desktop():
    """获取桌面路径"""
    return Path(os.environ.get("USERPROFILE", os.path.expanduser("~"))) / "Desktop"

def get_target_dir():
    """返回桌面上的输出文件夹路径，并自动创建（如果不存在）"""
    target = get_desktop() / TARGET_DIR_NAME
    target.mkdir(exist_ok=True)
    return target

def is_image(file_path):
    """判断文件是否为图片"""
    return file_path.suffix.lower() in IMAGE_EXTENSIONS

def is_screenshot(file_path):
    """判断文件是否位于 screenshots 文件夹中"""
    # 使用 os.sep 来兼容不同系统（Windows 是 \，Linux/Mac 是 /）
    return SCREENSHOT_KEYWORD in str(file_path) or f"{os.sep}screenshots{os.sep}" in str(file_path)

def get_version_name(file_path):
    """
    从文件完整路径中提取版本名（versions 目录下的第一级子文件夹名）
    例如：D:\MC PCL2\.minecraft\versions\1.16.5\screenshots\a.png -> "1.16.5"
    """
    rel = file_path.relative_to(SOURCE_ROOT)  # 相对于源目录的路径
    parts = rel.parts
    if parts:
        return parts[0]  # 第一个路径段即为版本名
    return "unknown"

def copy_file(src, dst, verbose=False):
    """复制文件，返回是否成功"""
    try:
        dst.parent.mkdir(parents=True, exist_ok=True)  # 确保目标文件夹存在
        shutil.copy2(src, dst)
        if verbose:
            print(f"复制成功: {src.name} -> {dst}")
        return True
    except Exception as e:
        print(f"复制失败: {src.name} - {e}")
        return False

def collect_images(only_screenshots=True):
    """
    收集所有符合条件的图片文件。
    返回列表，每个元素为 Path 对象。
    """
    source = Path(SOURCE_ROOT)
    if not source.exists():
        print(f"错误：源目录不存在 -> {SOURCE_ROOT}")
        sys.exit(1)

    all_images = []
    for file in source.rglob("*"):
        if file.is_file() and is_image(file):
            if only_screenshots and not is_screenshot(file):
                continue
            all_images.append(file)
    return all_images

def show_menu():
    """显示菜单并获取用户选择"""
    print("\n" + "=" * 40)
    print("    Minecraft 图片提取工具".center(40))
    print("=" * 40)
    print(f"源目录: {SOURCE_ROOT}")
    print(f"输出目录: {get_target_dir()}\n")
    print("请选择操作模式：")
    print("  1 - 仅截图 + 平铺输出（文件名加版本前缀）")
    print("  2 - 仅截图 + 按版本文件夹输出（原文件名）")
    print("  3 - 全量   + 平铺输出（文件名加版本前缀）")
    print("  4 - 全量   + 按版本文件夹输出（原文件名）")
    print("  Q - 退出")
    choice = input("\n请输入数字 (1-4) 或 Q: ").strip().upper()
    return choice

def main():
    # 检查源目录是否存在
    if not Path(SOURCE_ROOT).exists():
        print(f"错误：源目录不存在 -> {SOURCE_ROOT}")
        input("按回车键退出...")
        sys.exit(1)

    while True:
        choice = show_menu()
        if choice == 'Q':
            print("退出程序。")
            break
        if choice not in ('1', '2', '3', '4'):
            print("输入无效，请重新选择。")
            continue

        # 解析模式
        only_screenshots = choice in ('1', '2')
        use_flat = choice in ('1', '3')

        mode_desc = {
            '1': "仅截图，平铺输出",
            '2': "仅截图，按版本文件夹输出",
            '3': "全量扫描，平铺输出",
            '4': "全量扫描，按版本文件夹输出",
        }[choice]

        print(f"\n您选择了: {mode_desc}")
        print("正在扫描文件，请稍候...")

        # 收集图片
        images = collect_images(only_screenshots)
        total = len(images)
        if total == 0:
            print("未找到符合条件的图片文件，请检查目录和筛选条件。")
            input("按回车键返回菜单...")
            continue

        print(f"找到 {total} 张图片，开始复制...")

        target_root = get_target_dir()
        success_count = 0
        error_count = 0

        # 使用 tqdm 显示进度条（如果已安装），否则用简单百分比
        try:
            from tqdm import tqdm
            iterator = tqdm(images, desc="复制进度", unit="张")
        except ImportError:
            print("提示：安装 tqdm 库可显示更好看的进度条（pip install tqdm）")
            iterator = images
            # 简单百分比
            for i, img in enumerate(images, 1):
                print(f"\r进度: {i}/{total} ({i*100//total}%)", end="")
                # 处理文件复制...
                # 需要把实际复制逻辑写在这里，所以我们将复制逻辑移到循环内
                # 这里为了简洁，先使用简单循环，下面重写
            # 但为了代码清晰，我们使用单独循环，且在上面导入失败时使用简单输出
            # 我们将复制逻辑单独写在一个循环中，避免重复代码
            # 因此需要调整一下结构

        # 由于 tqdm 和简单循环不同，我们重新组织一下代码，让两种方式共用复制逻辑
        # 下面实现一个统一的复制循环
        for i, img in enumerate(images, 1):
            # 简单百分比显示（如果 tqdm 未安装）
            if 'tqdm' not in sys.modules:
                print(f"\r进度: {i}/{total} ({i*100//total}%)", end="")

            # 获取版本名
            version = get_version_name(img)

            if use_flat:
                # 平铺输出：版本名_原文件名
                new_name = f"{version}_{img.name}"
                dest = target_root / new_name
            else:
                # 按版本文件夹输出
                version_folder = target_root / version
                dest = version_folder / img.name

            # 复制文件
            if copy_file(img, dest):
                success_count += 1
            else:
                error_count += 1

        if 'tqdm' not in sys.modules:
            print()  # 换行

        print(f"\n复制完成！成功: {success_count} 张，失败: {error_count} 张。")
        print(f"文件已保存至: {target_root}")
        input("按回车键返回菜单...")

if __name__ == "__main__":
    main()