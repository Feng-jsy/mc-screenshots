import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
from ..utils.file_utils import ConflictMode

class UI:
    def __init__(self, root, config, on_start_callback):
        self.root = root
        self.config = config
        self.on_start = on_start_callback

        self.root.title("Minecraft Screenshots Pro")
        self.root.geometry("600x550")
        self.root.resizable(False, False)

        # 变量
        self.source_var = tk.StringVar(value=config.get("source_root", ""))
        self.output_var = tk.StringVar(value=config.get("output_dir", ""))
        self.mode_var = tk.StringVar(value=config.get("mode", "flat"))
        self.only_screenshots_var = tk.BooleanVar(value=config.get("only_screenshots", True))
        self.conflict_var = tk.StringVar(value=config.get("conflict", "rename"))

        # 源目录
        tk.Label(root, text="Minecraft versions 目录:").pack(anchor="w", padx=10, pady=(10,0))
        self.source_entry = tk.Entry(root, textvariable=self.source_var, width=70)
        self.source_entry.pack(padx=10, pady=5)
        self.source_btn = tk.Button(root, text="浏览...", command=self.select_source)
        self.source_btn.pack(padx=10, pady=(0,10), anchor="w")

        # 输出目录
        tk.Label(root, text="输出目录:").pack(anchor="w", padx=10)
        self.output_entry = tk.Entry(root, textvariable=self.output_var, width=70)
        self.output_entry.pack(padx=10, pady=5)
        self.output_btn = tk.Button(root, text="浏览...", command=self.select_output)
        self.output_btn.pack(padx=10, pady=(0,10), anchor="w")

        # 仅截图选项
        tk.Checkbutton(root, text="仅提取 Minecraft 官方截图", variable=self.only_screenshots_var).pack(anchor="w", padx=10, pady=5)

        # 输出方式
        tk.Label(root, text="输出方式:").pack(anchor="w", padx=10, pady=(10,0))
        mode_frame = tk.Frame(root)
        mode_frame.pack(anchor="w", padx=10, pady=5)
        tk.Radiobutton(mode_frame, text="平铺（所有文件在同一文件夹）", variable=self.mode_var, value="flat").pack(anchor="w")
        tk.Radiobutton(mode_frame, text="按版本分类", variable=self.mode_var, value="by_version").pack(anchor="w")
        tk.Radiobutton(mode_frame, text="按日期分类（基于文件名）", variable=self.mode_var, value="by_date").pack(anchor="w")

        # 冲突处理
        tk.Label(root, text="文件冲突处理:").pack(anchor="w", padx=10, pady=(10,0))
        conflict_frame = tk.Frame(root)
        conflict_frame.pack(anchor="w", padx=10, pady=5)
        tk.Radiobutton(conflict_frame, text="覆盖原有文件", variable=self.conflict_var, value="overwrite").pack(anchor="w")
        tk.Radiobutton(conflict_frame, text="自动重命名（如 file_1.png）", variable=self.conflict_var, value="rename").pack(anchor="w")

        # 进度条
        self.progress = ttk.Progressbar(root, length=400, mode='determinate')
        self.progress.pack(pady=20)

        # 开始按钮
        self.start_btn = tk.Button(root, text="开始整理", command=self.start, bg="#4CAF50", fg="white", font=("Arial", 12, "bold"))
        self.start_btn.pack(pady=10)

        # 状态标签
        self.status_var = tk.StringVar(value="就绪")
        self.status_label = tk.Label(root, textvariable=self.status_var, bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X)

    def select_source(self):
        path = filedialog.askdirectory(title="选择 Minecraft versions 目录")
        if path:
            self.source_var.set(path)

    def select_output(self):
        path = filedialog.askdirectory(title="选择输出目录")
        if path:
            self.output_var.set(path)

    def start(self):
        source = self.source_var.get().strip()
        output = self.output_var.get().strip()

        if not source:
            messagebox.showerror("错误", "请选择 Minecraft versions 目录")
            return
        if not output:
            messagebox.showerror("错误", "请选择输出目录")
            return

        self.start_btn.config(state=tk.DISABLED)
        self.progress["value"] = 0
        self.status_var.set("正在扫描图片...")
        self.root.update()

        # 保存配置
        self.config.set("source_root", source)
        self.config.set("output_dir", output)
        self.config.set("mode", self.mode_var.get())
        self.config.set("only_screenshots", self.only_screenshots_var.get())
        self.config.set("conflict", self.conflict_var.get())
        self.config.save()

        # 启动后台线程
        import threading
        def run():
            # 转换冲突模式
            conflict_mode = ConflictMode.OVERWRITE if self.conflict_var.get() == "overwrite" else ConflictMode.RENAME
            self.on_start(
                source, output,
                self.mode_var.get(),
                self.only_screenshots_var.get(),
                conflict_mode,
                self.update_progress,
                self.on_finish
            )
        threading.Thread(target=run, daemon=True).start()

    def update_progress(self, current, total):
        # 使用 after 确保线程安全更新 UI
        def _update():
            percent = int((current / total) * 100)
            self.progress["value"] = percent
            self.status_var.set(f"正在复制... {current}/{total} ({percent}%)")
        self.root.after(0, _update)

    def on_finish(self, success_count, error_count):
        def _finish():
            self.start_btn.config(state=tk.NORMAL)
            self.progress["value"] = 0
            self.status_var.set(f"完成！成功: {success_count} 张，失败: {error_count} 张")
            messagebox.showinfo("完成", f"整理完成！\n成功: {success_count} 张\n失败: {error_count} 张")
        self.root.after(0, _finish)