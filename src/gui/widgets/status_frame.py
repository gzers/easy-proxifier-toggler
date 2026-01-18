import tkinter as tk
import threading
import time
from ...core import service, process
from ..styles import create_styled_button, COLORS, FONTS, FluentCard

class StatusFrame(FluentCard):
    """状态监控与切换控制板块 - Fluent UI 风格"""
    def __init__(self, master, config, **kwargs):
        super().__init__(master, title="当前状态", **kwargs)
        self.config = config
        self.is_monitoring = True
        
        self.service_status_var = tk.StringVar(value="获取中...")
        self.process_status_var = tk.StringVar(value="获取中...")
        
        self._setup_ui()
        self._start_monitor()

    def _setup_ui(self):
        info_frame = tk.Frame(self, bg=COLORS["bg_card"])
        info_frame.pack(side=tk.LEFT, fill="both", expand=True)
        
        # 驱动服务状态
        tk.Label(info_frame, text="驱动服务:", font=FONTS["normal"], fg=COLORS["text_secondary"], bg=COLORS["bg_card"]).grid(row=0, column=0, sticky="w", pady=2)
        self.service_label = tk.Label(info_frame, textvariable=self.service_status_var, font=FONTS["title"], bg=COLORS["bg_card"])
        self.service_label.grid(row=0, column=1, sticky="w", padx=10)
        
        # 进程状态
        tk.Label(info_frame, text="进程状态:", font=FONTS["normal"], fg=COLORS["text_secondary"], bg=COLORS["bg_card"]).grid(row=1, column=0, sticky="w", pady=2)
        self.process_label = tk.Label(info_frame, textvariable=self.process_status_var, font=FONTS["title"], bg=COLORS["bg_card"])
        self.process_label.grid(row=1, column=1, sticky="w", padx=10)
        
        # 切换按钮
        self.toggle_btn = create_styled_button(
            self, 
            text="切换状态", 
            command=self._handle_toggle,
            width=12,
            style="accent"
        )
        self.toggle_btn.pack(side=tk.RIGHT, padx=5)

    def _handle_toggle(self):
        """处理切换逻辑"""
        curr_s = self.service_status_var.get()
        s_name = self.config.get("service_name", "proxifierdrv")
        p_path = self.config.get("proxifier_exe_path", "")
        
        real_btn = self.toggle_btn
        real_btn.config(state=tk.DISABLED, text="处理中...")
        
        def run_toggle():
            if curr_s == "RUNNING":
                process.kill_proxifier(p_path)
                time.sleep(0.5)
                service.stop_service(s_name)
            else:
                if service.start_service(s_name):
                    process.start_proxifier(p_path)
            
            # 操作完成后恢复按钮状态
            self.after(500, lambda: real_btn.config(state=tk.NORMAL, text="切换状态"))
            
        threading.Thread(target=run_toggle, daemon=True).start()

    def _start_monitor(self):
        """开启异步监控"""
        def monitor_loop():
            while self.is_monitoring:
                try:
                    s_name = self.config.get("service_name", "proxifierdrv")
                    p_path = self.config.get("proxifier_exe_path", "")
                    
                    s_status = service.get_service_status(s_name)
                    p_running = process.is_proxifier_running(p_path)
                    
                    self.service_status_var.set(s_status)
                    self.process_status_var.set("运行中" if p_running else "已停止")
                    
                    # 动态颜色
                    self.service_label.config(fg=COLORS["success"] if s_status == "RUNNING" else COLORS["danger"])
                    self.process_label.config(fg=COLORS["success"] if p_running else COLORS["danger"])
                except:
                    pass
                time.sleep(2)
        
        threading.Thread(target=monitor_loop, daemon=True).start()

    def stop_monitoring(self):
        """停止刷新"""
        self.is_monitoring = False

    def update_config(self, new_config):
        """当外部路径修改时，更新该组件引用的配置"""
        self.config = new_config
