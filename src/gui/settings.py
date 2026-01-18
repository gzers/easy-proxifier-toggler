"""主控面板 - 采用模块化组件设计"""
import tkinter as tk
from tkinter import messagebox
import webbrowser
from ..config import manager as config_manager
from ..utils import startup
from .widgets.status_frame import StatusFrame
from .widgets.config_frame import ConfigFrame
from .widgets.startup_frame import StartupFrame
from .widgets.footer_frame import FooterFrame
from .widgets.header_frame import HeaderFrame
from .widgets.about_dialog import AboutDialog
from .styles import create_styled_button, COLORS, FONTS


class SettingsWindow:
    """主控面板类 (聚合组件) - 修复为 Toplevel 架构以解决线程冲突"""
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(SettingsWindow, cls).__new__(cls)
        return cls._instance
    
    def __init__(self, root=None):
        # 确保只初始化一次
        if not hasattr(self, 'initialized'):
            self.root = root  # 外部传入的持久化 root
            self.window = None
            self.status_panel = None
            self.config_panel = None
            self.startup_panel = None
            self.initial_config = None
            self.initialized = True
    
    def show(self):
        """显示主控面板 - 切换到主线程安全的 Toplevel"""
        # 如果窗口已存在，直接唤醒
        if self.window is not None:
            try:
                if self.window.winfo_exists():
                    self.window.deiconify()
                    self.window.lift()
                    self.window.focus_force()
                    return
            except:
                self.window = None

        # 如果没有传入 root (例如直接运行该文件)，自行创建
        if self.root is None:
            self.root = tk.Tk()
            self.root.withdraw()

        # 使用 Toplevel 而不是 Tk
        self.window = tk.Toplevel(self.root)
        self.window.title("Easy-Proxifier-Toggler 主控面板")
        
        # 窗口布局与大小
        self._center_window(680, 760)
        self.window.configure(bg=COLORS["bg_window"])
        self.window.resizable(False, False)
        
        # 设置图标
        try:
            icon_path = config_manager.ASSETS_DIR / "icon.ico"
            if icon_path.exists():
                self.window.iconbitmap(str(icon_path))
        except:
            pass
            
        # 加载初始配置
        self.initial_config = config_manager.load_config()
        
        self._create_layout()
        
        # 拦截关闭事件，仅隐藏窗口或妥善销毁
        self.window.protocol("WM_DELETE_WINDOW", self._on_close)

    def _center_window(self, width, height):
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.window.geometry(f"{width}x{height}+{x}+{y}")

    def _create_layout(self):
        """组装各个模块化组件"""
        pad_x = 30
        
        # 1. 页脚组件 (版本/作者)
        from .. import __version__, __author__
        self.footer = FooterFrame(self.window, __version__, __author__, bg=COLORS["bg_window"])
        self.footer.pack(side=tk.BOTTOM, fill="x", pady=(5, 10))

        # 2. 底部操作按钮区域
        btn_frame = tk.Frame(self.window, bg=COLORS["bg_window"])
        btn_frame.pack(side=tk.BOTTOM, fill="x", pady=(5, 15))
        
        # 左侧放置次要按钮
        secondary_btn_frame = tk.Frame(btn_frame, bg=COLORS["bg_window"])
        secondary_btn_frame.pack(side=tk.LEFT)

        # 关于按钮
        create_styled_button(
            secondary_btn_frame, text="关于软件", 
            command=self._handle_about, 
            style="standard",
            width=10,
            icon="ℹ️"
        ).pack(side=tk.LEFT, padx=(pad_x, 10))

        # 保存按钮 (最右侧，高亮)
        create_styled_button(
            btn_frame, text="保存修改", 
            command=self._handle_save, 
            style="accent",
            width=12,
            icon="💾"
        ).pack(side=tk.RIGHT, padx=(10, pad_x))

        # 重置按钮
        create_styled_button(
            btn_frame, text="撤销更改", 
            command=self._handle_reset, 
            style="standard",
            width=10,
            icon="↩️"
        ).pack(side=tk.RIGHT, padx=10)

        # 3. 顶部标题区域
        logo_path = config_manager.ASSETS_DIR / "gzgg-logo.gif"
        self.header = HeaderFrame(
            self.window, 
            title="Easy-Proxifier-Toggler", 
            logo_path=logo_path,
            bg=COLORS["bg_window"]
        )
        self.header.pack(fill="x", padx=pad_x, pady=(20, 10))
        
        # 4. 中间卡片渲染 (状态/参数/启动)
        self.status_panel = StatusFrame(self.window, self.initial_config)
        self.status_panel.pack(fill="x", padx=pad_x, pady=8)
        
        self.config_panel = ConfigFrame(self.window, self.initial_config)
        self.config_panel.pack(fill="x", padx=pad_x, pady=8)
        
        self.startup_panel = StartupFrame(self.window, self.initial_config)
        self.startup_panel.pack(fill="x", padx=pad_x, pady=8)

    def _handle_about(self):
        """显示关于弹窗"""
        from .. import __version__, __author__, __github_url__
        AboutDialog(self.window, __version__, __author__, __github_url__)

    def _handle_save(self):
        """收集各组件数据并保存"""
        new_data = {**self.config_panel.get_data(), **self.startup_panel.get_data()}
        success = config_manager.update_config(**new_data)
        
        if success:
            if new_data["auto_start"]:
                startup.enable_auto_start()
            else:
                startup.disable_auto_start()
            self.status_panel.update_config(new_data)
            messagebox.showinfo("成功", "配置已保存到本地！")
        else:
            messagebox.showerror("错误", "保存失败。")

    def _handle_reset(self):
        """重置各组件的数据"""
        if messagebox.askyesno("确认", "确定要撤销更改并恢复初始状态吗？"):
            self.config_panel.set_data(self.initial_config)
            self.startup_panel.set_data(self.initial_config)
            self.status_panel.update_config(self.initial_config)

    def _on_close(self):
        """关闭逻辑：停止任务并销毁 Toplevel"""
        try:
            if self.status_panel:
                self.status_panel.stop_monitoring()
                self.status_panel = None
            if self.window:
                self.window.destroy()
        except:
            pass
        finally:
            self.window = None

def open_settings(root=None):
    """外部调用接口"""
    SettingsWindow(root).show()


if __name__ == "__main__":
    open_settings()
