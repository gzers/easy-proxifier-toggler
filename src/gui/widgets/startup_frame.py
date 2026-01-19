"""启动选项配置板块 - CustomTkinter 现代化版本"""
import customtkinter as ctk
from ..ctk_styles import CTkCard, Fonts, Sizes


class StartupFrame(CTkCard):
    """启动选项配置板块 - 现代化 CustomTkinter 风格"""
    
    def __init__(self, master, config, **kwargs):
        super().__init__(master, title="启动选项", **kwargs)
        
        # 配置变量
        self.auto_start_var = ctk.BooleanVar(value=config.get("auto_start", False))
        self.start_minimized_var = ctk.BooleanVar(value=config.get("start_minimized", True))
        
        self._setup_ui()
    
    def _setup_ui(self):
        """设置 UI 布局"""
        # 主容器
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=Sizes.PADDING, pady=Sizes.PADDING)
        
        # 开机自启动选项 - 使用现代化的 Switch
        auto_start_frame = ctk.CTkFrame(container, fg_color="transparent")
        auto_start_frame.pack(fill="x", pady=Sizes.PADDING_SMALL)
        
        ctk.CTkLabel(
            auto_start_frame,
            text="开机自动启动",
            font=Fonts.BODY,
            anchor="w"
        ).pack(side="left", fill="x", expand=True)
        
        self.auto_start_switch = ctk.CTkSwitch(
            auto_start_frame,
            text="",
            variable=self.auto_start_var,
            onvalue=True,
            offvalue=False
        )
        self.auto_start_switch.pack(side="right")
        
        # 启动时最小化选项
        minimized_frame = ctk.CTkFrame(container, fg_color="transparent")
        minimized_frame.pack(fill="x", pady=Sizes.PADDING_SMALL)
        
        ctk.CTkLabel(
            minimized_frame,
            text="启动时最小化到托盘",
            font=Fonts.BODY,
            anchor="w"
        ).pack(side="left", fill="x", expand=True)
        
        self.minimized_switch = ctk.CTkSwitch(
            minimized_frame,
            text="",
            variable=self.start_minimized_var,
            onvalue=True,
            offvalue=False
        )
        self.minimized_switch.pack(side="right")
        
        # 提示文字
        ctk.CTkLabel(
            container,
            text="* 建议启用最小化选项，程序将在后台静默运行",
            font=Fonts.CAPTION,
            text_color="gray",
            anchor="w"
        ).pack(anchor="w", pady=(Sizes.PADDING_SMALL, 0))
    
    def get_data(self):
        """获取当前配置数据"""
        return {
            "auto_start": self.auto_start_var.get(),
            "start_minimized": self.start_minimized_var.get()
        }
    
    def set_data(self, config):
        """设置配置数据"""
        self.auto_start_var.set(config.get("auto_start", False))
        self.start_minimized_var.set(config.get("start_minimized", True))
