import re

# Minecraft 默认截图命名格式：2024-03-01_12.34.56.png
SCREENSHOT_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}_\d{2}\.\d{2}\.\d{2}\.png$")

def is_minecraft_screenshot(filename: str) -> bool:
    """判断文件名是否符合 Minecraft 截图命名规范"""
    return bool(SCREENSHOT_PATTERN.match(filename))