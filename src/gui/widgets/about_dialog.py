"""关于对话框 - CustomTkinter 现代化版本"""
import customtkinter as ctk
import webbrowser
from ...config import manager as config_manager
from ..ctk_styles import ButtonStyles, Fonts, Sizes, Colors


class AboutDialog:
    """关于软件对话框 - 现代化 CustomTkinter 风格"""
    
    def __init__(self, parent, version, author, github_url):
        self.version = version
        self.author = author
        self.github_url = github_url
        
        # 创建对话框窗口
        self.dialog = ctk.CTkToplevel(parent)
        self.dialog.title("关于软件")
        self.dialog.geometry("450x350")
        self.dialog.resizable(False, False)
        
        # 居中显示
        self._center_window()
        
        # 设置为模态对话框
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # 设置图标 - 参考主界面，使用延迟加载以确保成功
        self.dialog.after(200, self._set_window_icon)
            
        self._setup_ui()

    def _set_window_icon(self):
        """设置窗口图标 - 强制使用 icon.ico"""
        try:
            if not self.dialog or not self.dialog.winfo_exists():
                return
            icon_path = config_manager.ASSETS_DIR / "icon.ico"
            if icon_path.exists():
                self.dialog.iconbitmap(str(icon_path))
        except Exception as e:
            print(f"关于窗口设置图标失败: {e}")
    
    def _center_window(self):
        """窗口居中"""
        self.dialog.update_idletasks()
        width = self.dialog.winfo_width()
        height = self.dialog.winfo_height()
        x = (self.dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (height // 2)
        self.dialog.geometry(f"{width}x{height}+{x}+{y}")
    
    def _setup_ui(self):
        """设置 UI 布局"""
        # 主容器
        main_frame = ctk.CTkFrame(self.dialog, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=Sizes.PADDING_LARGE, pady=Sizes.PADDING_LARGE)
        
        # 应用图标/标题区域
        header_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, Sizes.PADDING_LARGE))
        
        # 应用名称
        app_name = ctk.CTkLabel(
            header_frame,
            text="Easy-Proxifier-Toggler",
            font=Fonts.TITLE_LARGE,
        )
        app_name.pack(pady=(0, Sizes.PADDING_TINY))
        
        # 副标题
        subtitle = ctk.CTkLabel(
            header_frame,
            text="快速切换 Proxifier 运行状态的系统托盘工具",
            font=Fonts.BODY,
            text_color="gray"
        )
        subtitle.pack()
        
        # 信息卡片
        info_card = ctk.CTkFrame(
            main_frame,
            corner_radius=Sizes.CORNER_RADIUS_LARGE
        )
        info_card.pack(fill="both", expand=True, pady=Sizes.PADDING)
        
        # 版本信息
        version_frame = self._create_info_row(info_card, "版本", f"v{self.version}")
        version_frame.pack(fill="x", padx=Sizes.PADDING, pady=(Sizes.PADDING, Sizes.PADDING_SMALL))
        
        # 作者信息
        author_frame = self._create_info_row(info_card, "作者", self.author)
        author_frame.pack(fill="x", padx=Sizes.PADDING, pady=Sizes.PADDING_SMALL)
        
        # GitHub 链接
        github_frame = ctk.CTkFrame(info_card, fg_color="transparent")
        github_frame.pack(fill="x", padx=Sizes.PADDING, pady=Sizes.PADDING_SMALL)
        
        ctk.CTkLabel(
            github_frame,
            text="GitHub:",
            font=Fonts.BODY,
            anchor="w",
            width=80
        ).pack(side="left")
        
        github_link = ctk.CTkButton(
            github_frame,
            text="🔗 访问项目主页",
            command=lambda: webbrowser.open(self.github_url),
            **ButtonStyles.secondary(),
            width=200,
            anchor="w"
        )
        github_link.pack(side="left", padx=(Sizes.PADDING_SMALL, 0))
        
        # 许可证信息
        license_frame = self._create_info_row(info_card, "许可证", "MIT License")
        license_frame.pack(fill="x", padx=Sizes.PADDING, pady=(Sizes.PADDING_SMALL, Sizes.PADDING))
        
        # 底部按钮
        button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        button_frame.pack(fill="x", pady=(Sizes.PADDING, 0))
        
        close_btn = ctk.CTkButton(
            button_frame,
            text="关闭",
            command=self.dialog.destroy,
            **ButtonStyles.primary(),
            width=120
        )
        close_btn.pack(side="right")
    
    def _create_info_row(self, parent, label, value):
        """创建信息行"""
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        
        ctk.CTkLabel(
            frame,
            text=f"{label}:",
            font=Fonts.BODY,
            anchor="w",
            width=80
        ).pack(side="left")
        
        ctk.CTkLabel(
            frame,
            text=value,
            font=Fonts.BODY,
            anchor="w"
        ).pack(side="left", padx=(Sizes.PADDING_SMALL, 0))
        
        return frame
