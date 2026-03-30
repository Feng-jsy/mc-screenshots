from pathlib import Path
from typing import List, Tuple, Callable, Optional
from ..utils.file_utils import safe_copy, ConflictMode

def organize_files(
    files: List[Tuple[Path, str]],
    output_root: Path,
    mode: str,
    progress_callback: Optional[Callable[[int, int], None]] = None,
    conflict_mode: ConflictMode = ConflictMode.RENAME
) -> None:
    """
    整理文件
    :param files: 源文件及版本名列表，每个元素为 (Path, version_name)
    :param output_root: 输出根目录
    :param mode: 模式 flat / by_version / by_date
    :param progress_callback: 进度回调 (current, total)
    :param conflict_mode: 冲突处理模式
    """
    total = len(files)
    for i, (src, version) in enumerate(files):
        # 确定目标文件名和路径
        if mode == "flat":
            dest = output_root / src.name
        elif mode == "by_version":
            # 直接使用扫描阶段得到的版本名
            dest = output_root / version / src.name
        elif mode == "by_date":
            # 从文件名提取日期（前10位，形如 2024-03-01）
            date_part = src.stem[:10] if len(src.stem) >= 10 else "unknown"
            dest = output_root / date_part / src.name
        else:
            dest = output_root / src.name

        safe_copy(src, dest, conflict_mode)

        if progress_callback:
            progress_callback(i + 1, total)