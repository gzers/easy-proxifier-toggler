"""
Proxifier Toggler - 主程序入口
一个简单的系统托盘工具，用于快速切换 Proxifier 的开关状态
"""
import sys
import os
from src.utils.admin import run_as_admin
from src.gui.tray_icon import setup_icon


def main():
    """主函数
    
    程序启动时会自动检查管理员权限，
    如果没有权限会弹出 UAC 对话框请求权限。
    开发模式（SKIP_ADMIN_CHECK=1）可以跳过权限检查。
    """
    # 首先启用 DPI 感知以改善渲染质量（必须在创建任何窗口之前）
    from src.gui.dpi_fix import enable_dpi_awareness
    enable_dpi_awareness()
    
    # 检查是否跳过管理员权限检查（开发模式）
    skip_admin = os.environ.get('SKIP_ADMIN_CHECK') == '1'
    
    if not skip_admin:
        # 自动请求管理员权限（会弹出 UAC 对话框）
        run_as_admin()
    
    # 检查启动时是否最小化
    from src.config import manager as config_manager
    start_minimized = config_manager.get_start_minimized()

    # 导入 CustomTkinter 而不是 tkinter
    import customtkinter as ctk
    from src.gui.settings import SettingsWindow
    from src.gui.tray_icon import setup_tray_async
    from src.gui.ctk_styles import DEFAULT_APPEARANCE_MODE, DEFAULT_COLOR_THEME

    # 设置 CustomTkinter 主题
    ctk.set_appearance_mode(DEFAULT_APPEARANCE_MODE)  # "dark", "light", or "system"
    ctk.set_default_color_theme(DEFAULT_COLOR_THEME)  # "blue", "green", "dark-blue"

    # 1. 创建 CTk 根对象（驻留后台）
    root = ctk.CTk()
    root.withdraw()

    # 2. 初始化持久化的设置窗口对象
    app = SettingsWindow(root)

    # 3. 异步启动托盘图标，并把 app 实例传入
    setup_tray_async(app)

    # 4. 根据配置决定是否初始打开界面
    if not start_minimized:
        # 使用 after 确保其在主循环启动后立即执行
        root.after(100, app.show)

    # 5. 进入主线程消息队列循环（此路之后只有退出）
    try:
        root.mainloop()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
