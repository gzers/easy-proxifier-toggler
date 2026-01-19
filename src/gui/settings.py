"""主控面板 - CustomTkinter 现代化版本"""
import customtkinter as ctk
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
from .ctk_styles import ButtonStyles, Fonts, Sizes, Colors, toggle_appearance_mode


class SettingsWindow:
    """主控面板类 - 现代化 CustomTkinter 风格"""
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
        """显示主控面板"""
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
        
        # 如果没有传入 root，自行创建
        if self.root is None:
            self.root = ctk.CTk()
            self.root.withdraw()
        
        # 使用 CTkToplevel 创建窗口
        self.window = ctk.CTkToplevel(self.root)
        self.window.title("Easy-Proxifier-Toggler 主控面板")
        
        # 窗口布局与大小
        self._center_window(720, 850)  # 稍微增加高度
        self.window.resizable(False, False)
        
        # 设置图标
        self.window.after(200, self._set_window_icon)
        
        # 加载初始配置
        self.initial_config = config_manager.load_config()
        
        self._create_layout()
        
        # 拦截关闭事件
        self.window.protocol("WM_DELETE_WINDOW", self._on_close)

    def _set_window_icon(self):
        """设置窗口图标 - 强制使用 icon.ico"""
        try:
            if not self.window or not self.window.winfo_exists():
                return
            icon_path = config_manager.ASSETS_DIR / "icon.ico"
            if icon_path.exists():
                self.window.iconbitmap(str(icon_path))
        except Exception as e:
            print(f"窗口设置图标失败: {e}")
    
    def _center_window(self, width, height):
        """窗口居中"""
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.window.geometry(f"{width}x{height}+{x}+{y}")
    
    def _create_layout(self):
        """组装各个模块化组件"""
        from .ctk_styles import StyledButton
        pad_x = Sizes.WINDOW_PAD_X
        
        # 1. 页脚组件（版本/作者）- 放在底部
        from .. import __version__, __author__
        self.footer = FooterFrame(self.window, __version__, __author__)
        self.footer.pack(side="bottom", fill="x", padx=pad_x, pady=(Sizes.PADDING_SMALL, Sizes.WINDOW_PAD_Y))
        
        # 2. 底部操作按钮区域 - 放在底部
        btn_frame = ctk.CTkFrame(self.window, fg_color="transparent")
        btn_frame.pack(side="bottom", fill="x", padx=pad_x, pady=(Sizes.PADDING_SMALL, Sizes.PADDING))
        
        # 左侧次要按钮
        secondary_btn_frame = ctk.CTkFrame(btn_frame, fg_color="transparent")
        secondary_btn_frame.pack(side="left")
        
        # 关于按钮
        about_btn = StyledButton(
            secondary_btn_frame,
            text="ℹ️ 关于软件",
            command=self._handle_about,
            style="secondary",
            width=Sizes.BUTTON_WIDTH_SMALL
        )
        about_btn.pack(side="left", padx=(0, Sizes.PADDING_SMALL))
        
        # 主题切换按钮
        theme_btn = StyledButton(
            secondary_btn_frame,
            text="🌓 切换主题",
            command=self._toggle_theme,
            style="secondary",
            width=Sizes.BUTTON_WIDTH_SMALL
        )
        theme_btn.pack(side="left")
        
        # 右侧主要按钮
        # 保存按钮
        save_btn = StyledButton(
            btn_frame,
            text="💾 保存修改",
            command=self._handle_save,
            style="primary",
            width=Sizes.BUTTON_WIDTH
        )
        save_btn.pack(side="right")
        
        # 重置按钮
        reset_btn = StyledButton(
            btn_frame,
            text="↩️ 撤销更改",
            command=self._handle_reset,
            style="secondary",
            width=Sizes.BUTTON_WIDTH_SMALL
        )
        reset_btn.pack(side="right", padx=(0, Sizes.PADDING_SMALL))
        
        # 3. 顶部标题区域 - 放在顶部
        logo_path = config_manager.ASSETS_DIR / "gzgg-logo.gif"
        self.header = HeaderFrame(
            self.window,
            title="Easy-Proxifier-Toggler",
            logo_path=logo_path
        )
        self.header.pack(fill="x", padx=pad_x, pady=(Sizes.WINDOW_PAD_Y, Sizes.PADDING))
        
        # 4. 中间可滚动卡片容器
        scroll_container = ctk.CTkScrollableFrame(
            self.window, 
            fg_color="transparent",
            scrollbar_button_color=(Colors.BORDER_LIGHT, Colors.BORDER_DARK),
            scrollbar_button_hover_color=Colors.PRIMARY
        )
        scroll_container.pack(fill="both", expand=True, padx=pad_x - 5, pady=0)
        
        # 统一内部卡片边距
        card_pad_x = 5
        
        self.status_panel = StatusFrame(scroll_container, self.initial_config)
        self.status_panel.pack(fill="x", padx=card_pad_x, pady=Sizes.PADDING_SMALL)
        
        self.config_panel = ConfigFrame(scroll_container, self.initial_config)
        self.config_panel.pack(fill="x", padx=card_pad_x, pady=Sizes.PADDING_SMALL)
        
        self.startup_panel = StartupFrame(scroll_container, self.initial_config)
        self.startup_panel.pack(fill="x", padx=card_pad_x, pady=Sizes.PADDING_SMALL)

    
    def _toggle_theme(self):
        """切换深色/浅色主题"""
        new_mode = toggle_appearance_mode()
        # 可以添加提示
        mode_text = "深色" if new_mode == "dark" else "浅色"
        print(f"已切换到{mode_text}模式")
    
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
        """关闭逻辑：停止任务并销毁窗口"""
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
