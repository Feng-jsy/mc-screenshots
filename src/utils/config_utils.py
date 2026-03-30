import json
from pathlib import Path

class ConfigManager:
    def __init__(self):
        # 配置文件放在项目根目录（与 main.py 同级）
        self.config_path = Path(__file__).parent.parent.parent / "config.json"
        self._data = self._load()

    def _load(self):
        if self.config_path.exists():
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return {}

    def save(self):
        with open(self.config_path, "w", encoding="utf-8") as f:
            json.dump(self._data, f, indent=2, ensure_ascii=False)

    def get(self, key, default=None):
        return self._data.get(key, default)

    def set(self, key, value):
        self._data[key] = value