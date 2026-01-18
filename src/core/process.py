"""Proxifier 进程管理模块"""
import os
import subprocess
from .service import run_command_admin


def is_proxifier_running(proxifier_exe_path):
    """检查 Proxifier 进程是否在运行"""
    try:
        exe_name = os.path.basename(proxifier_exe_path)
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = subprocess.SW_HIDE
        
        # 使用过滤器加速查询
        output = subprocess.check_output(
            f'tasklist /FI "IMAGENAME eq {exe_name}" /NH',
            shell=True,
            text=True,
            startupinfo=startupinfo,
            stderr=subprocess.DEVNULL
        )
        return exe_name.lower() in output.lower()
    except Exception:
        return False


def start_proxifier(proxifier_exe_path):
    """启动 Proxifier 进程"""
    try:
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = subprocess.SW_HIDE
        
        subprocess.Popen(
            f'"{proxifier_exe_path}"',
            shell=True,
            startupinfo=startupinfo
        )
        return True
    except Exception as e:
        print(f"启动 Proxifier 失败: {e}")
        return False


def kill_proxifier(proxifier_exe_path):
    """终止 Proxifier 进程"""
    run_command_admin(f"taskkill /f /im {os.path.basename(proxifier_exe_path)}")
