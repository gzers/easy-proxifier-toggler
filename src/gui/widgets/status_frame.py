import tkinter as tk
import threading
import time
from ...core import service, process
from ..styles import create_styled_button, COLORS, FONTS, FluentCard

class StatusFrame(FluentCard):
    """状态监控与切换控制板块 - Fluent UI 风格 (支持异步加载与线程安全)"""
    def __init__(self, master, config, **kwargs):
        super().__init__(master, title="当前状态", **kwargs)
        self.config = config
        self.is_monitoring = True
        
        # 内部状态
        self.last_status = {"service": "LOADING", "process": "LOADING"}
        self.loading_dots = 0
        
        # 显式指定 master，确保生命周期绑定
        self.service_status_var = tk.StringVar(master=self, value="正在获取")
        self.process_status_var = tk.StringVar(master=self, value="正在获取")
        
        self._setup_ui()
        self._start_monitor()
        self._animate_loading() # 启动加载动画

    def _setup_ui(self):
        # 整体采用两栏布局
        container = tk.Frame(self, bg=COLORS["bg_card"])
        container.pack(fill="both", expand=True)

        info_frame = tk.Frame(container, bg=COLORS["bg_card"])
        info_frame.grid(row=0, column=0, sticky="nsew")
        container.grid_columnconfigure(0, weight=1)
        
        # 驱动服务状态 (使用 Badge 风格)
        tk.Label(info_frame, text="驱动服务:", font=FONTS["normal"], fg=COLORS["text_secondary"], bg=COLORS["bg_card"]).grid(row=0, column=0, sticky="w", pady=5)
        
        self.service_badge = tk.Frame(info_frame, bg=COLORS["bg_hover"], padx=8, pady=2)
        self.service_badge.grid(row=0, column=1, sticky="w", padx=15)
        self.service_label = tk.Label(self.service_badge, textvariable=self.service_status_var, font=FONTS["bold"], bg=COLORS["bg_hover"])
        self.service_label.pack()
        
        # 进程状态
        tk.Label(info_frame, text="进程状态:", font=FONTS["normal"], fg=COLORS["text_secondary"], bg=COLORS["bg_card"]).grid(row=1, column=0, sticky="w", pady=5)
        
        self.process_badge = tk.Frame(info_frame, bg=COLORS["bg_hover"], padx=8, pady=2)
        self.process_badge.grid(row=1, column=1, sticky="w", padx=15)
        self.process_label = tk.Label(self.process_badge, textvariable=self.process_status_var, font=FONTS["bold"], bg=COLORS["bg_hover"])
        self.process_label.pack()
        
        # 切换按钮
        self.toggle_btn = create_styled_button(
            container, 
            text="切换服务状态", 
            command=self._handle_toggle,
            width=14,
            style="accent",
            icon="⚡"
        )
        self.toggle_btn.grid(row=0, column=1, sticky="e", padx=(10, 0))

    def _animate_loading(self):
        """处理‘正在获取’阶段的动画效果"""
        if not self.is_monitoring:
            return
            
        updating = False
        dots = "." * (self.loading_dots % 4)
        
        if self.last_status["service"] == "LOADING":
            self.service_status_var.set(f"正在获取{dots}")
            updating = True
            
        if self.last_status["process"] == "LOADING":
            self.process_status_var.set(f"正在获取{dots}")
            updating = True
            
        if updating:
            self.loading_dots += 1
            self.after(400, self._animate_loading)

    def _handle_toggle(self):
        """处理切换逻辑"""
        curr_s = self.service_status_var.get()
        s_name = self.config.get("service_name", "proxifierdrv")
        p_path = self.config.get("proxifier_exe_path", "")
        
        real_btn = self.toggle_btn
        real_btn.config(state=tk.DISABLED, text=" 正在处理...")
        
        def run_toggle():
            try:
                if "RUNNING" in curr_s:
                    process.kill_proxifier(p_path)
                    time.sleep(0.5)
                    service.stop_service(s_name)
                else:
                    if service.start_service(s_name):
                        process.start_proxifier(p_path)
            except:
                pass
            
            # 操作完成后通过 after 恢复 UI
            self.after(500, lambda: real_btn.config(state=tk.NORMAL, text="⚡ 切换服务状态"))
            
        threading.Thread(target=run_toggle, daemon=True).start()

    def _start_monitor(self):
        """开启异步监控线程"""
        def monitor_loop():
            while self.is_monitoring:
                try:
                    s_name = self.config.get("service_name", "proxifierdrv")
                    p_path = self.config.get("proxifier_exe_path", "")
                    
                    s_status = service.get_service_status(s_name)
                    p_running = process.is_proxifier_running(p_path)
                    
                    # 将结果推送到主线程更新
                    self.after(0, self._sync_ui, s_status, p_running)
                except:
                    pass
                time.sleep(2)
        
        thread = threading.Thread(target=monitor_loop, daemon=True)
        thread.start()

    def _sync_ui(self, s_status, p_running):
        """主线程安全刷新 UI"""
        # 检查组件是否还存在
        try:
            if not self.is_monitoring or not self.winfo_exists():
                return
        except tk.TclError:
            return

        # 判断状态是否发生变化，若是则刷新托盘图标
        status_changed = (self.last_status.get("service") != s_status)
        
        self.last_status["service"] = s_status
        self.last_status["process"] = "RUNNING" if p_running else "STOPPED"

        if status_changed:
            try:
                from ..tray_icon import refresh_tray_icon
                refresh_tray_icon()
            except ImportError:
                pass

        # 1. 更新服务状态文字与颜色
        if self.service_status_var:
            self.service_status_var.set(f"● {s_status}")
            
        if s_status == "RUNNING":
            s_bg, s_fg = COLORS["success_bg"], COLORS["success"]
        elif s_status == "STOPPED":
            s_bg, s_fg = COLORS["danger_bg"], COLORS["danger"]
        elif s_status == "NOT_INSTALLED":
            s_bg, s_fg = COLORS["warning"], COLORS["text_white"]
            if self.service_status_var:
                self.service_status_var.set("● 未安装")
        else:
            s_bg, s_fg = COLORS["bg_hover"], COLORS["text_secondary"]

        self.service_badge.config(bg=s_bg)
        self.service_label.config(bg=s_bg, fg=s_fg)

        # 2. 更新进程状态文字与颜色
        if self.process_status_var:
            self.process_status_var.set("● 运行中" if p_running else "● 已停止")
            
        if p_running:
            p_bg, p_fg = COLORS["success_bg"], COLORS["success"]
        else:
            p_bg, p_fg = COLORS["danger_bg"], COLORS["danger"]

        self.process_badge.config(bg=p_bg)
        self.process_label.config(bg=p_bg, fg=p_fg)

    def stop_monitoring(self):
        """停止刷新"""
        self.is_monitoring = False
        # 显式清理，防止 GC 时报错
        self.service_status_var = None
        self.process_status_var = None

    def update_config(self, new_config):
        """当外部路径修改时，重置状态并更新"""
        self.config = new_config
        # 触发一次即时刷新提示（或者重置为加载中）
        self.last_status = {"service": "LOADING", "process": "LOADING"}
        if self.winfo_exists():
            self._animate_loading()

