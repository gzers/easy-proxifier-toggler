"""系统托盘图标管理"""
import time
import threading
import pystray
from PIL import Image, ImageDraw
from ..core import service, process
from ..config import manager as config_manager
from .settings import open_settings


def create_image():
    """获取托盘图标
    优先从 assets 目录加载外部图标，如果不存在则使用代码绘制备用图标
    """
    icon_path = config_manager.ASSETS_DIR / "icon.png"
    
    if icon_path.exists():
        try:
            return Image.open(icon_path)
        except Exception as e:
            print(f"加载外部图标失败: {e}")
            
    # 如果外部图标不存在或加载失败，创建备用图标
    width = 64
    height = 64
    image = Image.new('RGB', (width, height), (255, 255, 255))
    dc = ImageDraw.Draw(image)
    
    # 绘制一个蓝色圆圈
    dc.ellipse([8, 8, 56, 56], fill=(0, 120, 215), outline=(0, 90, 180))
    
    # 绘制一个白色的 "P" 字母
    dc.text((22, 18), "P", fill=(255, 255, 255))
    
    return image


def toggle_proxifier_state(icon, item):
    """切换 Proxifier 状态"""
    service_name = config_manager.get_service_name()
    proxifier_exe_path = config_manager.get_proxifier_exe_path()
    current_status = service.get_service_status(service_name)
    
    if current_status == "RUNNING":
        # 关闭逻辑
        icon.notify("正在关闭 Proxifier...", "切换状态")
        
        # 杀进程
        process.kill_proxifier(proxifier_exe_path)
        time.sleep(1)
        
        # 停服务
        if service.stop_service(service_name):
            icon.notify("Proxifier 已关闭。", "状态通知")
        else:
            icon.notify("Proxifier 关闭可能未完成。", "警告")
            
    elif current_status == "STOPPED" or current_status == "NOT_INSTALLED":
        # 开启逻辑
        icon.notify("正在开启 Proxifier...", "切换状态")
        
        # 启服务
        if service.start_service(service_name):
            # 启动软件
            if process.start_proxifier(proxifier_exe_path):
                icon.notify("Proxifier 已开启。", "状态通知")
            else:
                icon.notify("启动 Proxifier 失败！", "错误")
        else:
            icon.notify("驱动启动失败！", "错误")
    else:
        icon.notify(f"Proxifier 状态未知 ({current_status})", "警告")


def show_status(icon, item):
    """显示当前状态"""
    service_name = config_manager.get_service_name()
    proxifier_exe_path = config_manager.get_proxifier_exe_path()
    
    status = service.get_service_status(service_name)
    process_running = process.is_proxifier_running(proxifier_exe_path)
    
    status_text = f"服务状态: {status}\n进程运行: {'是' if process_running else '否'}"
    icon.notify(status_text, "Proxifier 状态")


def open_settings_window(icon, item):
    """在新线程中打开设置窗口，避免阻塞托盘图标"""
    threading.Thread(target=open_settings, daemon=True).start()


def quit_app(icon, item):
    """退出程序"""
    icon.stop()


def setup_icon():
    """设置托盘图标和菜单"""
    image = create_image()

    menu = pystray.Menu(
        pystray.MenuItem("切换 Proxifier", toggle_proxifier_state, default=True),
        pystray.MenuItem("查看状态", show_status),
        pystray.Menu.SEPARATOR,
        pystray.MenuItem("设置", open_settings_window),
        pystray.Menu.SEPARATOR,
        pystray.MenuItem("退出", quit_app)
    )

    from .. import __version__
    icon = pystray.Icon("Proxifier_Toggler", image, f"Proxifier 切换器 v{__version__}", menu)
    icon.run()
