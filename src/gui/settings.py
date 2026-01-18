"""设置窗口 GUI"""
import tkinter as tk
from tkinter import filedialog, messagebox
from ..config import manager as config_manager


class SettingsWindow:
    """设置窗口类"""
    
    def __init__(self):
        self.window = None
        self.proxifier_path_var = None
        self.service_name_var = None
        self.auto_start_var = None
        self.start_minimized_var = None
    
    def show(self):
        """显示设置窗口"""
        # 如果窗口已经存在，则将其置于前台
        if self.window is not None:
            try:
                self.window.lift()
                self.window.focus_force()
                return
            except:
                pass
        
        # 创建新窗口
        self.window = tk.Tk()
        self.window.title("Proxifier Toggler 设置")
        
        # 设置窗口大小并居中
        self._center_window(600, 380)
        self.window.resizable(False, False)
        
        # 设置窗口图标
        try:
            from ..config import manager as config_manager
            icon_path = config_manager.ASSETS_DIR / "icon.ico"
            if icon_path.exists():
                self.window.iconbitmap(str(icon_path))
        except Exception as e:
            print(f"设置窗口图标失败: {e}")
            
        # 加载当前配置
        config = config_manager.load_config()
        
        # 创建界面元素
        self._create_widgets(config)
        
        # 窗口关闭事件
        self.window.protocol("WM_DELETE_WINDOW", self._on_close)
        
        # 运行窗口
        self.window.mainloop()
    
    def _center_window(self, width, height):
        """将窗口居中显示"""
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        
        self.window.geometry(f"{width}x{height}+{x}+{y}")

    def _create_widgets(self, config):
        """创建界面元素"""
        # 标题
        title_label = tk.Label(
            self.window,
            text="Proxifier Toggler 配置",
            font=("Microsoft YaHei UI", 14, "bold")
        )
        title_label.pack(pady=15)
        
        # Proxifier 可执行文件路径
        path_frame = tk.Frame(self.window)
        path_frame.pack(pady=10, padx=20, fill=tk.X)
        
        path_label = tk.Label(
            path_frame,
            text="Proxifier 可执行文件路径:",
            font=("Microsoft YaHei UI", 10),
            width=20,
            anchor='w'
        )
        path_label.pack(side=tk.LEFT, padx=(0, 10))
        
        self.proxifier_path_var = tk.StringVar(value=config["proxifier_exe_path"])
        path_entry = tk.Entry(
            path_frame,
            textvariable=self.proxifier_path_var,
            font=("Consolas", 9),
            width=40
        )
        path_entry.pack(side=tk.LEFT, padx=(0, 10), fill=tk.X, expand=True)
        
        browse_button = tk.Button(
            path_frame,
            text="浏览...",
            command=self._browse_file,
            font=("Microsoft YaHei UI", 9),
            width=8
        )
        browse_button.pack(side=tk.LEFT)
        
        # 服务名称
        service_frame = tk.Frame(self.window)
        service_frame.pack(pady=10, padx=20, fill=tk.X)
        
        service_label = tk.Label(
            service_frame,
            text="服务名称:",
            font=("Microsoft YaHei UI", 10),
            width=20,
            anchor='w'
        )
        service_label.pack(side=tk.LEFT, padx=(0, 10))
        
        self.service_name_var = tk.StringVar(value=config["service_name"])
        service_entry = tk.Entry(
            service_frame,
            textvariable=self.service_name_var,
            font=("Consolas", 9),
            width=40
        )
        service_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # 提示信息
        hint_label = tk.Label(
            self.window,
            text="提示: 服务名称默认为 'proxifierdrv'，一般无需修改",
            font=("Microsoft YaHei UI", 8),
            fg="gray"
        )
        hint_label.pack(pady=5)
        
        # 分隔线
        separator = tk.Frame(self.window, height=1, bg="lightgray")
        separator.pack(fill=tk.X, padx=20, pady=10)
        
        # 选项区域
        options_frame = tk.Frame(self.window)
        options_frame.pack(pady=10, padx=20, fill=tk.X)
        
        # 开机启动复选框
        self.auto_start_var = tk.BooleanVar(value=config.get("auto_start", False))
        auto_start_check = tk.Checkbutton(
            options_frame,
            text="开机自动启动",
            variable=self.auto_start_var,
            font=("Microsoft YaHei UI", 10),
            cursor="hand2"
        )
        auto_start_check.pack(anchor='w', pady=5)
        
        # 启动时最小化复选框
        self.start_minimized_var = tk.BooleanVar(value=config.get("start_minimized", True))
        start_minimized_check = tk.Checkbutton(
            options_frame,
            text="启动时最小化到托盘（不勾选则打开设置界面）",
            variable=self.start_minimized_var,
            font=("Microsoft YaHei UI", 10),
            cursor="hand2"
        )
        start_minimized_check.pack(anchor='w', pady=5)
        
        # 版本号显示
        from .. import __version__
        version_label = tk.Label(
            self.window,
            text=f"Version {__version__}",
            font=("Consolas", 8),
            fg="lightgray"
        )
        version_label.pack(side=tk.BOTTOM, pady=5)
        
        # 按钮区域
        button_frame = tk.Frame(self.window)
        button_frame.pack(pady=20)
        
        save_button = tk.Button(
            button_frame,
            text="保存",
            command=self._save_config,
            font=("Microsoft YaHei UI", 10),
            width=10,
            bg="#0078D4",
            fg="white",
            relief=tk.FLAT,
            cursor="hand2"
        )
        save_button.pack(side=tk.LEFT, padx=10)
        
        cancel_button = tk.Button(
            button_frame,
            text="取消",
            command=self._on_close,
            font=("Microsoft YaHei UI", 10),
            width=10,
            relief=tk.FLAT,
            cursor="hand2"
        )
        cancel_button.pack(side=tk.LEFT, padx=10)
    
    def _browse_file(self):
        """浏览文件对话框"""
        filename = filedialog.askopenfilename(
            title="选择 Proxifier 可执行文件",
            filetypes=[("可执行文件", "*.exe"), ("所有文件", "*.*")],
            initialdir="C:\\Program Files"
        )
        
        if filename:
            self.proxifier_path_var.set(filename)
    
    def _save_config(self):
        """保存配置"""
        proxifier_path = self.proxifier_path_var.get().strip()
        service_name = self.service_name_var.get().strip()
        auto_start = self.auto_start_var.get()
        start_minimized = self.start_minimized_var.get()
        
        # 验证输入
        if not proxifier_path:
            messagebox.showerror("错误", "Proxifier 可执行文件路径不能为空！")
            return
        
        if not service_name:
            messagebox.showerror("错误", "服务名称不能为空！")
            return
        
        # 保存配置
        success = config_manager.update_config(
            proxifier_exe_path=proxifier_path,
            service_name=service_name,
            auto_start=auto_start,
            start_minimized=start_minimized
        )
        
        if success:
            # 同步开机启动设置到注册表
            from ..utils import startup
            if auto_start:
                startup_success = startup.enable_auto_start()
                if not startup_success:
                    messagebox.showwarning("警告", "配置已保存，但设置开机启动失败！\n请检查是否有足够的权限。")
                    return
            else:
                startup.disable_auto_start()
            
            messagebox.showinfo("成功", "配置已保存！\n\n注意: 配置将在下次操作时生效。")
            self._on_close()
        else:
            messagebox.showerror("错误", "保存配置失败！")
    
    def _on_close(self):
        """关闭窗口"""
        if self.window:
            self.window.destroy()
            self.window = None


def open_settings():
    """打开设置窗口（供外部调用）"""
    settings = SettingsWindow()
    settings.show()


if __name__ == "__main__":
    # 测试设置窗口
    open_settings()
