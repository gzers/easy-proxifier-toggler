"""基本参数配置板块 - CustomTkinter 现代化版本"""
import customtkinter as ctk
from tkinter import filedialog
from ..ctk_styles import CTkCard, ButtonStyles, EntryStyles, Fonts, Sizes, Colors


class ConfigFrame(CTkCard):
    """基本参数配置板块 - 现代化 CustomTkinter 风格"""
    
    def __init__(self, master, config, **kwargs):
        super().__init__(master, title="基本配置", **kwargs)
        
        # 配置变量
        self.path_var = ctk.StringVar(value=config.get("proxifier_exe_path", ""))
        self.service_var = ctk.StringVar(value=config.get("service_name", "proxifierdrv"))
        
        self._setup_ui()
    
    def _setup_ui(self):
        """设置 UI 布局"""
        from ..ctk_styles import StyledButton
        # 主容器
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=Sizes.PADDING, pady=Sizes.PADDING)
        
        # Proxifier 路径配置
        ctk.CTkLabel(
            container,
            text="Proxifier 可执行文件路径:",
            font=Fonts.BODY,
            anchor="w"
        ).pack(anchor="w", pady=(0, Sizes.PADDING_TINY))
        
        # 路径输入框和浏览按钮
        path_frame = ctk.CTkFrame(container, fg_color="transparent")
        path_frame.pack(fill="x", pady=(0, Sizes.PADDING))
        
        self.path_entry = ctk.CTkEntry(
            path_frame,
            textvariable=self.path_var,
            placeholder_text="请选择 Proxifier.exe 文件路径",
            **EntryStyles.default()
        )
        self.path_entry.pack(side="left", fill="x", expand=True, padx=(0, Sizes.PADDING_SMALL))
        
        browse_btn = StyledButton(
            path_frame,
            text="📁 浏览",
            command=self._browse_file,
            style="secondary",
            width=100
        )
        browse_btn.pack(side="right")
        
        # 服务名称配置
        ctk.CTkLabel(
            container,
            text="驱动服务名称:",
            font=Fonts.BODY,
            anchor="w"
        ).pack(anchor="w", pady=(Sizes.PADDING_SMALL, Sizes.PADDING_TINY))
        
        self.service_entry = ctk.CTkEntry(
            container,
            textvariable=self.service_var,
            placeholder_text="proxifierdrv",
            **EntryStyles.default()
        )
        self.service_entry.pack(fill="x", pady=(0, Sizes.PADDING_TINY))
        
        # 提示文字
        ctk.CTkLabel(
            container,
            text="* 通常为 'proxifierdrv'，不熟悉请勿修改",
            font=Fonts.CAPTION,
            text_color="gray",
            anchor="w"
        ).pack(anchor="w")
    
    def _browse_file(self):
        """浏览文件对话框"""
        filename = filedialog.askopenfilename(
            title="选择 Proxifier 可执行文件",
            filetypes=[("可执行文件", "*.exe"), ("所有文件", "*.*")]
        )
        if filename:
            self.path_var.set(filename)
    
    def get_data(self):
        """获取当前配置数据"""
        return {
            "proxifier_exe_path": self.path_var.get().strip(),
            "service_name": self.service_var.get().strip()
        }
    
    def set_data(self, config):
        """设置配置数据"""
        self.path_var.set(config.get("proxifier_exe_path", ""))
        self.service_var.set(config.get("service_name", "proxifierdrv"))
