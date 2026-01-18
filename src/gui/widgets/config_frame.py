import tkinter as tk
from tkinter import filedialog
from ..styles import create_styled_button, COLORS, FONTS

from ..styles import create_styled_button, COLORS, FONTS, FluentCard, apply_fluent_entry

class ConfigFrame(FluentCard):
    """基本参数配置板块 - Fluent UI 风格"""
    def __init__(self, master, config, **kwargs):
        super().__init__(master, title="基本配置", **kwargs)
        
        # 显式绑定 master，配合 Toplevel 架构防止跨线程 GC 导致的报错
        self.path_var = tk.StringVar(master=self, value=config.get("proxifier_exe_path", ""))
        self.service_var = tk.StringVar(master=self, value=config.get("service_name", "proxifierdrv"))
        
        self._setup_ui()

    def _setup_ui(self):
        # Proxifier 路径
        tk.Label(self, text="Proxifier 可执行文件路径:", font=FONTS["normal"], fg=COLORS["text_secondary"], bg=COLORS["bg_card"]).pack(anchor="w")
        path_frame = tk.Frame(self, bg=COLORS["bg_card"])
        path_frame.pack(fill="x", pady=(8, 15)) # 增加间距
        
        path_entry = tk.Entry(path_frame, textvariable=self.path_var)
        apply_fluent_entry(path_entry)
        path_entry.pack(side=tk.LEFT, fill="x", expand=True, padx=(0, 10))
        
        create_styled_button(path_frame, text="浏览", command=self._browse_file, width=8, style="standard", icon="📁").pack(side=tk.RIGHT)
        
        # 服务名称
        tk.Label(self, text="驱动服务名称:", font=FONTS["normal"], fg=COLORS["text_secondary"], bg=COLORS["bg_card"]).pack(anchor="w")
        service_entry = tk.Entry(self, textvariable=self.service_var)
        apply_fluent_entry(service_entry)
        service_entry.pack(fill="x", pady=(8, 5))
        tk.Label(self, text="* 通常为 'proxifierdrv'，不熟悉请勿修改", font=FONTS["small"], fg="gray", bg=COLORS["bg_card"]).pack(anchor="w", pady=(0, 5))

    def _browse_file(self):
        filename = filedialog.askopenfilename(
            title="选择 Proxifier 可执行文件",
            filetypes=[("可执行文件", "*.exe"), ("所有文件", "*.*")]
        )
        if filename:
            self.path_var.set(filename)

    def get_data(self):
        """获取当前输入的数据"""
        return {
            "proxifier_exe_path": self.path_var.get().strip(),
            "service_name": self.service_var.get().strip()
        }

    def set_data(self, config):
        """重置数据"""
        self.path_var.set(config.get("proxifier_exe_path", ""))
        self.service_var.set(config.get("service_name", "proxifierdrv"))
