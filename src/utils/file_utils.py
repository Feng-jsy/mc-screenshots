import shutil
import logging
from pathlib import Path
from enum import Enum

class ConflictMode(Enum):
    OVERWRITE = "overwrite"
    RENAME = "rename"

def safe_copy(src: Path, dst: Path, conflict_mode: ConflictMode = ConflictMode.RENAME) -> None:
    """
    复制文件，根据冲突模式处理已存在的目标文件。
    :param src: 源文件
    :param dst: 目标路径（可能被修改）
    :param conflict_mode: OVERWRITE 直接覆盖；RENAME 自动添加数字后缀
    """
    dst = Path(dst)
    # 确保目标目录存在
    dst.parent.mkdir(parents=True, exist_ok=True)

    if conflict_mode == ConflictMode.OVERWRITE:
        shutil.copy2(src, dst)
        logging.debug(f"已覆盖: {dst}")
        return

    # RENAME 模式：自动添加后缀
    if not dst.exists():
        shutil.copy2(src, dst)
        logging.debug(f"已复制: {dst}")
        return

    base = dst.stem
    ext = dst.suffix
    counter = 1
    while True:
        new_dst = dst.parent / f"{base}_{counter}{ext}"
        if not new_dst.exists():
            shutil.copy2(src, new_dst)
            logging.debug(f"已复制并重命名: {new_dst}")
            break
        counter += 1

def setup_logging(verbose: bool = False):
    """
    配置日志输出。verbose=True 时输出 DEBUG 级别信息（如每个文件的复制详情），
    否则只输出 INFO 级别（进度、结果）。
    """
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )