"""管理员权限相关工具"""
import os
import sys
import ctypes


def is_admin():
    """检查是否以管理员身份运行"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception:
        return False


def run_as_admin():
    """请求管理员权限并重新启动脚本
    
    如果当前没有管理员权限，会弹出 UAC 对话框请求权限，
    然后重新启动程序并退出当前进程。
    """
    if not is_admin():
        try:
            # 获取命令行参数
            params = ' '.join([f'"{arg}"' for arg in sys.argv[1:]])
            
            if getattr(sys, 'frozen', False):
                # 如果是打包后的 EXE，直接通过 "runas" 运行 EXE 本身
                target = sys.executable
            else:
                # 如果是脚本，通过 Python 解释器运行脚本
                target = sys.executable
                params = f'"{os.path.abspath(sys.argv[0])}" {params}'
            
            # 使用 ShellExecuteW 以管理员身份重新启动
            ctypes.windll.shell32.ShellExecuteW(
                None, "runas", target, params, None, 1
            )
            
            # 退出当前进程
            sys.exit(0)
        except Exception as e:
            print(f"请求管理员权限失败: {e}")
            print("请手动以管理员身份运行此程序")
            sys.exit(1)
