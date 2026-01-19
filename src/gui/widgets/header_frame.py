"""页眉组件 - CustomTkinter 现代化版本"""
import customtkinter as ctk
from PIL import Image
from ..ctk_styles import Fonts, Sizes


class HeaderFrame(ctk.CTkFrame):
    """页眉组件 - 显示应用标题和 Logo"""
    
    def __init__(self, master, title="", logo_path=None, **kwargs):
        # 设置透明背景
        kwargs.setdefault("fg_color", "transparent")
        super().__init__(master, **kwargs)
        
        self.title_text = title
        self.logo_path = logo_path
        
        self._setup_ui()
    
    def _setup_ui(self):
        """设置 UI 布局"""
        # 主容器 - 水平布局
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(fill="x", expand=True)
        
        # Logo 图片（如果提供）
        # if self.logo_path and self.logo_path.exists():
        #     try:
        #         # 加载并调整 logo 大小
        #         logo_image = Image.open(self.logo_path)
        #         # 调整大小
        #         size = Sizes.ICON_SIZE_LARGE
        #         logo_image = logo_image.resize((size, size), Image.Resampling.LANCZOS)
        #         logo_photo = ctk.CTkImage(
        #             light_image=logo_image,
        #             dark_image=logo_image,
        #             size=(size, size)
        #         )
                
        #         logo_label = ctk.CTkLabel(
        #             container,
        #             image=logo_photo,
        #             text=""
        #         )
        #         logo_label.pack(side="left", padx=(0, Sizes.PADDING))
        #         # 保持引用防止被垃圾回收
        #         logo_label.image = logo_photo
        #     except Exception as e:
        #         print(f"加载 Logo 失败: {e}")
        
        # 标题文字
        title_label = ctk.CTkLabel(
            container,
            text=self.title_text,
            font=Fonts.TITLE_LARGE,
            anchor="w"
        )
        title_label.pack(side="left", fill="x", expand=True)
