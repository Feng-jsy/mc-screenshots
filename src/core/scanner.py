from pathlib import Path
from typing import List, Tuple
from .detector import is_minecraft_screenshot

# 支持的图片扩展名
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".gif", ".tiff", ".tif", ".webp"}

def is_image(file_path: Path) -> bool:
    return file_path.suffix.lower() in IMAGE_EXTENSIONS

def scan_images(source_root: Path, only_screenshots: bool = False) -> List[Tuple[Path, str]]:
    """
    扫描所有图片文件，并返回 (文件路径, 版本名) 的列表。
    :param source_root: 源根目录（versions 文件夹）
    :param only_screenshots: 是否仅返回截图
    :return: 列表，每个元素为 (Path, version_name)
    """
    source_root = Path(source_root).resolve()
    if not source_root.exists():
        raise FileNotFoundError(f"源目录不存在: {source_root}")

    results = []
    for file in source_root.rglob("*"):
        if file.is_file() and is_image(file):
            if only_screenshots and not is_minecraft_screenshot(file.name):
                continue
            # 计算版本名：相对路径的第一级
            try:
                rel = file.relative_to(source_root)
                version = rel.parts[0] if rel.parts else "unknown"
            except ValueError:
                version = "unknown"
            results.append((file, version))
    return results