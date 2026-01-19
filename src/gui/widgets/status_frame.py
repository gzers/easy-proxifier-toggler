"""状态监控与切换控制板块 - CustomTkinter 现代化版本"""
import customtkinter as ctk
import threading
import time
from ...core import service, process
from ..ctk_styles import (
    CTkCard, CTkStatusBadge, ButtonStyles, Fonts, Sizes, Colors, get_status_colors
)


class StatusFrame(CTkCard):
    """状态监控与切换控制板块 - 现代化 CustomTkinter 风格"""
    
    def __init__(self, master, config, **kwargs):
        super().__init__(master, title="当前状态", **kwargs)
        self.config = config
        self.is_monitoring = True
        
        # 内部状态
        self.last_status = {"service": "LOADING", "process": "LOADING"}
        self.loading_dots = 0
        
        # 状态变量
        self.service_status_var = ctk.StringVar(value="正在获取")
        self.process_status_var = ctk.StringVar(value="正在获取")
        
        self._setup_ui()
        self._start_monitor()
        self._animate_loading()
    
    def _setup_ui(self):
        """设置 UI 布局"""
        # 主容器 - 使用网格布局
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=Sizes.PADDING, pady=Sizes.PADDING)
        
        # 配置网格权重
        container.grid_columnconfigure(0, weight=1)
        container.grid_columnconfigure(1, weight=0)
        
        # 左侧信息区域
        info_frame = ctk.CTkFrame(container, fg_color="transparent")
        info_frame.grid(row=0, column=0, sticky="nsew", padx=(0, Sizes.PADDING))
        
        # 驱动服务状态行
        service_row = ctk.CTkFrame(info_frame, fg_color="transparent")
        service_row.pack(fill="x", pady=Sizes.PADDING_SMALL)
        
        ctk.CTkLabel(
            service_row,
            text="驱动服务:",
            font=Fonts.BODY,
            anchor="w"
        ).pack(side="left", padx=(0, Sizes.PADDING_SMALL))
        
        # 服务状态徽章
        self.service_badge = CTkStatusBadge(service_row)
        self.service_badge.pack(side="left")
        self.service_label = self.service_badge.status_label
        self.service_label.configure(textvariable=self.service_status_var)
        
        # 进程状态行
        process_row = ctk.CTkFrame(info_frame, fg_color="transparent")
        process_row.pack(fill="x", pady=Sizes.PADDING_SMALL)
        
        ctk.CTkLabel(
            process_row,
            text="进程状态:",
            font=Fonts.BODY,
            anchor="w"
        ).pack(side="left", padx=(0, Sizes.PADDING_SMALL))
        
        # 进程状态徽章
        self.process_badge = CTkStatusBadge(process_row)
        self.process_badge.pack(side="left")
        self.process_label = self.process_badge.status_label
        self.process_label.configure(textvariable=self.process_status_var)
        
        # 右侧切换按钮
        from ..ctk_styles import StyledButton
        self.toggle_btn = StyledButton(
            container,
            text="⚡ 切换服务状态",
            command=self._handle_toggle,
            style="primary",
            width=Sizes.BUTTON_WIDTH_LARGE
        )
        self.toggle_btn.grid(row=0, column=1, sticky="e")
    
    def _animate_loading(self):
        """处理加载动画"""
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
        
        # 禁用按钮并显示处理中状态
        self.toggle_btn.configure(state="disabled", text="⏳ 正在处理...")
        
        def run_toggle():
            try:
                if "RUNNING" in curr_s:
                    # 关闭流程
                    process.kill_proxifier(p_path)
                    time.sleep(0.5)
                    service.stop_service(s_name)
                else:
                    # 开启流程
                    if service.start_service(s_name):
                        process.start_proxifier(p_path)
            except Exception as e:
                print(f"切换失败: {e}")
            
            # 恢复按钮状态
            self.after(500, lambda: self.toggle_btn.configure(
                state="normal",
                text="⚡ 切换服务状态"
            ))
        
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
                    
                    # 推送到主线程更新
                    self.after(0, self._sync_ui, s_status, p_running)
                except Exception as e:
                    print(f"监控错误: {e}")
                
                time.sleep(2)
        
        threading.Thread(target=monitor_loop, daemon=True).start()
    
    def _sync_ui(self, s_status, p_running):
        """主线程安全刷新 UI"""
        try:
            if not self.is_monitoring or not self.winfo_exists():
                return
        except Exception:
            return
        
        # 检查状态变化
        status_changed = (self.last_status.get("service") != s_status)
        
        self.last_status["service"] = s_status
        self.last_status["process"] = "RUNNING" if p_running else "STOPPED"
        
        # 刷新托盘图标
        if status_changed:
            try:
                from ..tray_icon import refresh_tray_icon
                refresh_tray_icon()
            except ImportError:
                pass
        
        # 更新服务状态
        if s_status == "RUNNING":
            self.service_status_var.set("● RUNNING")
            self.service_badge.set_status("● RUNNING", "success")
        elif s_status == "STOPPED":
            self.service_status_var.set("● STOPPED")
            self.service_badge.set_status("● STOPPED", "danger")
        elif s_status == "NOT_INSTALLED":
            self.service_status_var.set("● 未安装")
            self.service_badge.set_status("● 未安装", "warning")
        else:
            self.service_status_var.set(f"● {s_status}")
            self.service_badge.set_status(f"● {s_status}", "neutral")
        
        # 更新进程状态
        if p_running:
            self.process_status_var.set("● 运行中")
            self.process_badge.set_status("● 运行中", "success")
        else:
            self.process_status_var.set("● 已停止")
            self.process_badge.set_status("● 已停止", "danger")
    
    def stop_monitoring(self):
        """停止监控"""
        self.is_monitoring = False
        self.service_status_var = None
        self.process_status_var = None
    
    def update_config(self, new_config):
        """更新配置"""
        self.config = new_config
        self.last_status = {"service": "LOADING", "process": "LOADING"}
        if self.winfo_exists():
            self._animate_loading()
