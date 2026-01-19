"""页脚组件 - CustomTkinter 现代化版本"""
import customtkinter as ctk
from ..ctk_styles import Fonts, Sizes, Colors


class FooterFrame(ctk.CTkFrame):
    """页脚组件 - 显示版本和作者信息"""
    
    def __init__(self, master, version="", author="", **kwargs):
        # 设置透明背景
        kwargs.setdefault("fg_color", "transparent")
        super().__init__(master, **kwargs)
        
        self.version = version
        self.author = author
        
        self._setup_ui()
    
    def _setup_ui(self):
        """设置 UI 布局"""
        # 分隔线
        separator = ctk.CTkFrame(self, height=1, fg_color=Colors.BORDER_DARK)
        separator.pack(fill="x", pady=(0, Sizes.PADDING_SMALL))
        
        # 信息容器
        info_frame = ctk.CTkFrame(self, fg_color="transparent")
        info_frame.pack(fill="x")
        
        # 版本信息（左侧）
        version_label = ctk.CTkLabel(
            info_frame,
            text=f"版本 {self.version}",
            font=Fonts.CAPTION,
            anchor="w"
        )
        version_label.pack(side="left")
        
        # 作者信息（右侧）
        author_label = ctk.CTkLabel(
            info_frame,
            text=f"作者: {self.author}",
            font=Fonts.CAPTION,
            anchor="e"
        )
        author_label.pack(side="right")
