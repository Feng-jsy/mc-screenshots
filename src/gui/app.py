import tkinter as tk
from pathlib import Path
from .ui import UI
from ..utils.config_utils import ConfigManager
from ..core.scanner import scan_images
from ..core.organizer import organize_files
from ..utils.file_utils import ConflictMode

def run_app():
    root = tk.Tk()
    config = ConfigManager()
    app = App(root, config)
    root.mainloop()

class App:
    def __init__(self, root, config):
        self.config = config
        self.ui = UI(root, config, self.start_processing)

    def start_processing(self, source, output, mode, only_screenshots, conflict_mode, progress_callback, finish_callback):
        """在后台线程中运行"""
        source_path = Path(source)
        output_path = Path(output)

        try:
            images = scan_images(source_path, only_screenshots)
            total = len(images)
            if total == 0:
                finish_callback(0, 0)
                return

            organize_files(images, output_path, mode, progress_callback, conflict_mode)
            # 由于 organize_files 不返回成功数，这里假设全部成功
            finish_callback(total, 0)
        except Exception as e:
            # 发生异常时通知界面
            finish_callback(0, 0)
            raise