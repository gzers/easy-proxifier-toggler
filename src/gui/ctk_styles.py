"""CustomTkinter 现代样式配置模块

提供统一的颜色方案、字体配置和样式常量
支持深色/浅色主题切换
"""
import customtkinter as ctk

# ============================================================================
# 主题配置
# ============================================================================

# 设置默认外观模式：dark, light, system
DEFAULT_APPEARANCE_MODE = "dark"

# 设置默认颜色主题：blue, green, dark-blue
DEFAULT_COLOR_THEME = "blue"

# 初始化主题
ctk.set_appearance_mode(DEFAULT_APPEARANCE_MODE)
ctk.set_default_color_theme(DEFAULT_COLOR_THEME)


# ============================================================================
# 颜色方案定义
# ============================================================================

class Colors:
    """现代化配色方案 - 支持深色/浅色主题"""
    
    # 主色调（品牌色）
    PRIMARY = "#1f6aa5"           # 现代蓝
    PRIMARY_HOVER = "#1a5a8f"     # 悬停时的深蓝
    PRIMARY_DARK = "#144a73"      # 激活时的更深蓝
    
    # 成功状态
    SUCCESS = "#2fa572"           # 现代绿
    SUCCESS_BG = "#d4f4dd"        # 浅绿背景（浅色主题）
    SUCCESS_BG_DARK = "#1a4d2e"   # 深绿背景（深色主题）
    
    # 危险/错误状态
    DANGER = "#d32f2f"            # 现代红
    DANGER_BG = "#fde7e9"         # 浅红背景（浅色主题）
    DANGER_BG_DARK = "#5c1a1a"    # 深红背景（深色主题）
    
    # 警告状态
    WARNING = "#f57c00"           # 现代橙
    WARNING_BG = "#fff3e0"        # 浅橙背景（浅色主题）
    WARNING_BG_DARK = "#5c3d00"   # 深橙背景（深色主题）
    
    # 中性色（深色主题）
    BG_DARK = "#1a1a1a"           # 深色背景
    CARD_DARK = "#2b2b2b"         # 深色卡片背景
    HOVER_DARK = "#3a3a3a"        # 深色悬停背景
    TEXT_DARK = "#e0e0e0"         # 深色主题文字
    TEXT_SECONDARY_DARK = "#a0a0a0"  # 深色主题次要文字
    
    # 中性色（浅色主题）
    BG_LIGHT = "#f5f5f5"          # 浅色背景
    CARD_LIGHT = "#ffffff"        # 浅色卡片背景
    HOVER_LIGHT = "#e8e8e8"       # 浅色悬停背景
    TEXT_LIGHT = "#1a1a1a"        # 浅色主题文字
    TEXT_SECONDARY_LIGHT = "#666666"  # 浅色主题次要文字
    
    # 边框和分隔线
    BORDER_DARK = "#404040"       # 深色主题边框
    BORDER_LIGHT = "#d0d0d0"      # 浅色主题边框


# ============================================================================
# 字体配置
# ============================================================================

class Fonts:
    """统一的字体配置"""
    
    # 标题字体
    TITLE_LARGE = ("Microsoft YaHei UI", 24, "bold")    # 大标题
    TITLE = ("Microsoft YaHei UI", 16, "bold")          # 标题
    SUBTITLE = ("Microsoft YaHei UI", 14, "bold")       # 副标题
    
    # 正文字体
    BODY_LARGE = ("Microsoft YaHei UI", 13)             # 大正文
    BODY = ("Microsoft YaHei UI", 12)                   # 正文
    BODY_SMALL = ("Microsoft YaHei UI", 11)             # 小正文
    
    # 特殊字体
    CAPTION = ("Microsoft YaHei UI", 10)                # 说明文字
    CODE = ("Consolas", 11)                             # 代码/路径
    BUTTON = ("Microsoft YaHei UI", 12, "bold")         # 按钮文字


# ============================================================================
# 尺寸和间距配置
# ============================================================================

class Sizes:
    """统一的尺寸和间距配置 - 单一来源，修改此处即可影响全局"""
    
    # 圆角半径 - 优化以减少锯齿
    CORNER_RADIUS_LARGE = 8       # 大圆角（卡片、主窗口）
    CORNER_RADIUS = 6             # 标准圆角（按钮、徽章）
    CORNER_RADIUS_SMALL = 4       # 小圆角（输入框、小切换开关）
    
    # 边框宽度
    BORDER_WIDTH = 2              # 标准边框
    BORDER_WIDTH_THIN = 1         # 细边框
    
    # 窗口间距 (布局统一)
    WINDOW_PAD_X = 30             # 主窗口左右边距
    WINDOW_PAD_Y = 20             # 主窗口上下边距
    
    # 内边距
    PADDING_LARGE = 20            # 大内边距
    PADDING = 15                  # 标准内边距
    PADDING_SMALL = 10            # 小内边距
    PADDING_TINY = 5              # 微小内边距
    
    # 按钮尺寸
    BUTTON_HEIGHT = 36            # 按钮高度
    BUTTON_WIDTH_LARGE = 140      # 大按钮宽度
    BUTTON_WIDTH = 120            # 标准按钮宽度
    BUTTON_WIDTH_SMALL = 110      # 小按钮宽度
    
    # 输入框尺寸
    ENTRY_HEIGHT = 36             # 输入框高度
    
    # 图标尺寸
    ICON_SIZE_LARGE = 48          # 大图标 (Logo)
    ICON_SIZE_SMALL = 20          # 小图标 (按钮内)


# ============================================================================
# 组件样式预设
# ============================================================================

class ButtonStyles:
    """按钮样式预设"""
    
    @staticmethod
    def primary():
        """主要按钮样式（蓝色）"""
        return {
            "fg_color": Colors.PRIMARY,
            "hover_color": Colors.PRIMARY_HOVER,
            "text_color": "#ffffff",  # 蓝色背景固定用白色文字
            "corner_radius": Sizes.CORNER_RADIUS,
            "font": Fonts.BUTTON,
            "height": Sizes.BUTTON_HEIGHT,
        }
    
    @staticmethod
    def success():
        """成功按钮样式（绿色）"""
        return {
            "fg_color": Colors.SUCCESS,
            "hover_color": "#268a5f",
            "text_color": "#ffffff",  # 绿色背景固定用白色文字
            "corner_radius": Sizes.CORNER_RADIUS,
            "font": Fonts.BUTTON,
            "height": Sizes.BUTTON_HEIGHT,
        }
    
    @staticmethod
    def danger():
        """危险按钮样式（红色）"""
        return {
            "fg_color": Colors.DANGER,
            "hover_color": "#b71c1c",
            "text_color": "#ffffff",  # 红色背景固定用白色文字
            "corner_radius": Sizes.CORNER_RADIUS,
            "font": Fonts.BUTTON,
            "height": Sizes.BUTTON_HEIGHT,
        }
    
    @staticmethod
    def secondary():
        """次要按钮样式（灰色边框）- 已适配主题切换"""
        return {
            "fg_color": "transparent",
            "border_color": (Colors.BORDER_LIGHT, Colors.BORDER_DARK),
            "text_color": (Colors.TEXT_LIGHT, Colors.TEXT_DARK),
            "border_width": Sizes.BORDER_WIDTH,
            "corner_radius": Sizes.CORNER_RADIUS,
            "font": Fonts.BUTTON,
            "height": Sizes.BUTTON_HEIGHT,
        }


class FrameStyles:
    """框架样式预设"""
    
    @staticmethod
    def card():
        """卡片样式"""
        return {
            "corner_radius": Sizes.CORNER_RADIUS_LARGE,
            "border_width": 0,
        }
    
    @staticmethod
    def card_bordered():
        """带边框的卡片样式"""
        return {
            "corner_radius": Sizes.CORNER_RADIUS_LARGE,
            "border_width": Sizes.BORDER_WIDTH_THIN,
        }


class EntryStyles:
    """输入框样式预设"""
    
    @staticmethod
    def default():
        """默认输入框样式"""
        return {
            "corner_radius": Sizes.CORNER_RADIUS_SMALL,
            "border_width": Sizes.BORDER_WIDTH,
            "font": Fonts.BODY,
            "height": Sizes.ENTRY_HEIGHT,
        }


# ============================================================================
# 工具函数
# ============================================================================

def get_current_mode():
    """获取当前外观模式"""
    return ctk.get_appearance_mode()


def set_appearance_mode(mode: str):
    """设置外观模式
    
    Args:
        mode: "dark", "light", 或 "system"
    """
    ctk.set_appearance_mode(mode)


def toggle_appearance_mode():
    """切换外观模式（深色/浅色）"""
    current = get_current_mode()
    new_mode = "light" if current == "Dark" else "dark"
    set_appearance_mode(new_mode)
    return new_mode


def get_status_colors(status: str, is_dark_mode: bool = None):
    """根据状态获取对应的颜色
    
    Args:
        status: 状态字符串（success, danger, warning）
        is_dark_mode: 是否深色模式，None 则自动检测
    
    Returns:
        tuple: (前景色, 背景色)
    """
    if is_dark_mode is None:
        is_dark_mode = get_current_mode() == "Dark"
    
    if status.lower() in ["success", "running", "active"]:
        fg = Colors.SUCCESS
        bg = Colors.SUCCESS_BG_DARK if is_dark_mode else Colors.SUCCESS_BG
    elif status.lower() in ["danger", "error", "stopped", "inactive"]:
        fg = Colors.DANGER
        bg = Colors.DANGER_BG_DARK if is_dark_mode else Colors.DANGER_BG
    elif status.lower() in ["warning", "pending"]:
        fg = Colors.WARNING
        bg = Colors.WARNING_BG_DARK if is_dark_mode else Colors.WARNING_BG
    else:
        # 默认中性色
        fg = Colors.TEXT_DARK if is_dark_mode else Colors.TEXT_LIGHT
        bg = Colors.HOVER_DARK if is_dark_mode else Colors.HOVER_LIGHT
    
    return fg, bg


# ============================================================================
# 自定义快捷组件 - 进一步统一 UI
# ============================================================================

class StyledButton(ctk.CTkButton):
    """预设样式的按钮，自动读取 Sizes 配置"""
    def __init__(self, master, style="primary", **kwargs):
        if style == "primary":
            p_style = ButtonStyles.primary()
        elif style == "success":
            p_style = ButtonStyles.success()
        elif style == "danger":
            p_style = ButtonStyles.danger()
        else:
            p_style = ButtonStyles.secondary()
            
        # 合并默认样式与传入参数
        for k, v in p_style.items():
            kwargs.setdefault(k, v)
        
        super().__init__(master, **kwargs)

class CTkCard(ctk.CTkFrame):
    """现代卡片容器组件 - 已统一圆角"""
    
    def __init__(self, master, title=None, **kwargs):
        # 应用卡片样式
        style = FrameStyles.card()
        kwargs.update(style)
        
        super().__init__(master, **kwargs)
        
        # 如果有标题，添加标题标签
        if title:
            title_label = ctk.CTkLabel(
                self,
                text=title,
                font=Fonts.SUBTITLE,
                anchor="w"
            )
            title_label.pack(anchor="w", padx=Sizes.PADDING, pady=(Sizes.PADDING, Sizes.PADDING_SMALL))


class CTkStatusBadge(ctk.CTkFrame):
    """状态徽章组件 - 已统一圆角"""
    
    def __init__(self, master, status="", **kwargs):
        super().__init__(master, corner_radius=Sizes.CORNER_RADIUS, **kwargs)
        
        self.status_label = ctk.CTkLabel(
            self,
            text=status,
            font=Fonts.BODY_SMALL,
        )
        self.status_label.pack(padx=Sizes.PADDING_SMALL, pady=Sizes.PADDING_TINY)
    
    def set_status(self, status: str, status_type: str = "neutral"):
        """设置状态文本和颜色
        
        Args:
            status: 状态文本
            status_type: 状态类型（success, danger, warning, neutral）
        """
        self.status_label.configure(text=status)
        fg, bg = get_status_colors(status_type)
        self.configure(fg_color=bg)
        self.status_label.configure(text_color=fg)

