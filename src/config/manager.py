"""配置管理器"""
import sys
import os
import json
from pathlib import Path

# 默认配置
DEFAULT_CONFIG = {
    "proxifier_exe_path": r"D:\Software\Common\Proxifier\Proxifier.exe",
    "service_name": "proxifierdrv",
    "auto_start": False,  # 是否开机启动
    "start_minimized": True  # 启动时是否最小化（不最小化则打开设置界面）
}

# 获取项目根目录
if getattr(sys, 'frozen', False):
    # 打包环境（EXE 运行）
    # 获取 EXE 所在的目录用于存放配置文件
    PROJECT_ROOT = Path(sys.executable).parent
    # 获取内部资源目录（assets 所在）
    RESOURCE_ROOT = Path(sys._MEIPASS)
else:
    # 源码环境（直接运行 Python）
    PROJECT_ROOT = Path(__file__).parent.parent.parent
    RESOURCE_ROOT = PROJECT_ROOT

CONFIG_DIR = PROJECT_ROOT / "config"
CONFIG_FILE = CONFIG_DIR / "config.json"
ASSETS_DIR = RESOURCE_ROOT / "assets"


def _ensure_config_dir():
    """确保配置目录存在"""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)


def load_config():
    """加载配置文件，如果不存在则创建默认配置"""
    _ensure_config_dir()
    
    if not CONFIG_FILE.exists():
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG.copy()
    
    try:
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        # 确保所有必需的键都存在
        for key in DEFAULT_CONFIG:
            if key not in config:
                config[key] = DEFAULT_CONFIG[key]
        
        return config
    except Exception as e:
        print(f"加载配置文件失败: {e}")
        return DEFAULT_CONFIG.copy()


def save_config(config):
    """保存配置到文件"""
    _ensure_config_dir()
    
    try:
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=4)
        return True
    except Exception as e:
        print(f"保存配置文件失败: {e}")
        return False


def get_proxifier_exe_path():
    """获取 Proxifier 可执行文件路径"""
    config = load_config()
    return config.get("proxifier_exe_path", DEFAULT_CONFIG["proxifier_exe_path"])


def get_service_name():
    """获取服务名称"""
    config = load_config()
    return config.get("service_name", DEFAULT_CONFIG["service_name"])


def update_config(proxifier_exe_path=None, service_name=None, auto_start=None, start_minimized=None):
    """更新配置"""
    config = load_config()
    
    if proxifier_exe_path is not None:
        config["proxifier_exe_path"] = proxifier_exe_path
    
    if service_name is not None:
        config["service_name"] = service_name
    
    if auto_start is not None:
        config["auto_start"] = auto_start
    
    if start_minimized is not None:
        config["start_minimized"] = start_minimized
    
    return save_config(config)


def get_auto_start():
    """获取是否开机启动"""
    config = load_config()
    return config.get("auto_start", DEFAULT_CONFIG["auto_start"])


def get_start_minimized():
    """获取启动时是否最小化"""
    config = load_config()
    return config.get("start_minimized", DEFAULT_CONFIG["start_minimized"])
