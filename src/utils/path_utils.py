import os
from pathlib import Path

def detect_minecraft_versions() -> Path | None:
    """
    返回官方启动器 versions 目录路径，如果不存在则返回 None。
    """
    appdata = os.getenv("APPDATA")
    if appdata:
        path = Path(appdata) / ".minecraft" / "versions"
        if path.exists():
            return path
    return None