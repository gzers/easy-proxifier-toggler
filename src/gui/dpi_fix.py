"""DPI 感知优化模块 - 改善 Windows 高 DPI 显示器上的渲染质量"""
import sys
import ctypes


def enable_dpi_awareness():
    """启用 DPI 感知以改善高 DPI 显示器上的渲染质量
    
    这可以显著改善 CustomTkinter 在 Windows 上的圆角渲染质量，
    减少锯齿和模糊问题。
    """
    if sys.platform == 'win32':
        try:
            # 尝试设置进程 DPI 感知级别
            # 这会让 Windows 正确缩放应用程序
            ctypes.windll.shcore.SetProcessDpiAwareness(2)  # PROCESS_PER_MONITOR_DPI_AWARE
        except Exception:
            try:
                # 如果上面的方法失败，尝试旧版 API
                ctypes.windll.user32.SetProcessDPIAware()
            except Exception:
                # 如果都失败了，忽略错误继续运行
                pass


def set_windows_scaling():
    """设置 Windows 缩放优化"""
    if sys.platform == 'win32':
        try:
            # 告诉 Windows 我们的应用程序支持高 DPI
            import os
            os.environ['QT_AUTO_SCREEN_SCALE_FACTOR'] = '1'
            os.environ['QT_ENABLE_HIGHDPI_SCALING'] = '1'
        except Exception:
            pass
