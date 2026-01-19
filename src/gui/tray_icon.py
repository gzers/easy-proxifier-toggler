"""系统托盘图标管理"""
import time
import threading
import pystray
from PIL import Image, ImageDraw
from ..core import service, process
from ..config import manager as config_manager
from .settings import open_settings


# 全局引用与缓存
_app_instance = None
_icon_instance = None
_icon_images = {
    "active": None,
    "inactive": None
}


def create_image(active=True):
    """获取托盘图标
    直接加载预生成的活动/非活动状态图标
    
    Args:
        active: True 为彩色(活动)图标，False 为灰度(非活动)图标
    """
    # 检查缓存
    cache_key = "active" if active else "inactive"
    if _icon_images[cache_key]:
        return _icon_images[cache_key]

    # 根据状态选择对应的图标文件
    icon_filename = "icon.png" if active else "icon_inactive.png"
    icon_path = config_manager.ASSETS_DIR / icon_filename
    
    # 加载图标
    if icon_path.exists():
        try:
            image = Image.open(icon_path)
            _icon_images[cache_key] = image
            return image
        except Exception as e:
            print(f"加载图标失败 ({icon_filename}): {e}")
    
    # 如果加载失败，抛出错误或使用一个极简的透明占位（不再生成复杂的带字母图标）
    # 既然用户要求不要代码生成的图标，我们就只尝试加载
    print(f"警告: 找不到图标文件 {icon_path}，请检查 assets 目录。")
    return Image.new('RGBA', (64, 64), (0, 0, 0, 0))


def update_icon_state(icon):
    """根据服务状态更新图标"""
    service_name = config_manager.get_service_name()
    status = service.get_service_status(service_name)
    
    # 状态判定：RUNNING 为活动，其他为非活动
    is_active = (status == "RUNNING")
    
    # 获取对应图标
    new_image = create_image(active=is_active)
    
    # 如果当前图标与新图标不同，才更新
    if icon.icon != new_image:
        icon.icon = new_image


def refresh_tray_icon():
    """供外部调用的刷新物理接口（无轮询，按需调用）"""
    if _icon_instance:
        update_icon_state(_icon_instance)


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
    
    # 操作后立即更新一次图标
    update_icon_state(icon)


def show_status(icon, item):
    """显示当前状态"""
    service_name = config_manager.get_service_name()
    proxifier_exe_path = config_manager.get_proxifier_exe_path()
    
    status = service.get_service_status(service_name)
    process_running = process.is_proxifier_running(proxifier_exe_path)
    
    status_text = f"服务状态: {status}\n进程运行: {'是' if process_running else '否'}"
    icon.notify(status_text, "Proxifier 状态")


def open_settings_window(icon, item):
    """通过主线程安全地显示设置面板"""
    if _app_instance:
        _app_instance.root.after(0, _app_instance.show)


def quit_app(icon, item):
    """安全退出程序"""
    icon.stop()
    if _app_instance and _app_instance.root:
        _app_instance.root.after(0, _app_instance.root.quit)


def setup_icon(app_instance=None):
    """设置托盘图标和菜单"""
    global _app_instance, _icon_instance
    _app_instance = app_instance
    
    # 初始创建图标
    image = create_image(active=True)

    menu = pystray.Menu(
        pystray.MenuItem("切换 Proxifier", toggle_proxifier_state, default=True),
        pystray.MenuItem("查看状态", show_status),
        pystray.Menu.SEPARATOR,
        pystray.MenuItem("主界面", open_settings_window),
        pystray.Menu.SEPARATOR,
        pystray.MenuItem("退出", quit_app)
    )

    from .. import __version__
    _icon_instance = pystray.Icon("Proxifier_Toggler", image, f"Proxifier 切换器 v{__version__}", menu)
    
    # 启动时根据实际状态同步一次图标
    update_icon_state(_icon_instance)
    
    _icon_instance.run()

def setup_tray_async(app_instance):
    """在后台线程启动托盘图标"""
    thread = threading.Thread(target=setup_icon, args=(app_instance,), daemon=True)
    thread.start()
    return thread
