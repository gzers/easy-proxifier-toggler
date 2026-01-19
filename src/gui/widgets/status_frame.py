"""状态监控与切换控制板块 - CustomTkinter 现代化版本 (Fluent UI)"""
import customtkinter as ctk
import threading
import time
from ...core import service, process
from ..ctk_styles import Fonts, Sizes, Colors, get_status_colors


class StatusFrame(ctk.CTkFrame):
    """状态监控与切换控制板块 - Fluent Design 风格"""
    
    def __init__(self, master, config, **kwargs):
        # 应用卡片样式
        kwargs.setdefault("corner_radius", Sizes.CORNER_RADIUS_LARGE)
        kwargs.setdefault("border_width", 0)
        kwargs.setdefault("height", 180)  # 设置固定高度，确保切换按钮可见
        super().__init__(master, **kwargs)
        
        # 禁用自动扩展，保持固定高度
        self.pack_propagate(False)
        
        self.config = config
        self.is_monitoring = True
        
        # 内部状态
        self.last_status = {"service": "LOADING", "process": "LOADING"}
        self.loading_dots = 0
        
        self._setup_ui()
        self._start_monitor()
        self._animate_loading()
    
    def _setup_ui(self):
        """设置 UI 布局 - Fluent 风格"""
        # 主容器 - 减少上下留白
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=Sizes.PADDING_LARGE, pady=Sizes.PADDING_SMALL)
        
        # 标题 - 更轻量的样式
        title_label = ctk.CTkLabel(
            container,
            text="当前状态",
            font=("Microsoft YaHei UI", 14, "normal"),
            text_color=(Colors.TEXT_SECONDARY_LIGHT, Colors.TEXT_SECONDARY_DARK),
            anchor="w"
        )
        title_label.pack(anchor="w", pady=(0, Sizes.PADDING_TINY))
        
        # 状态信息区域 - 单行布局，固定高度
        status_row = ctk.CTkFrame(container, fg_color="transparent", height=32)
        status_row.pack(fill="x", pady=(0, Sizes.PADDING_TINY))
        status_row.pack_propagate(False)  # 防止子组件撑大容器
        
        # 左侧：驱动服务状态（横向布局）
        self._create_status_inline(status_row, "驱动服务", "service", side="left")
        
        # 中间竖线分隔
        separator_line = ctk.CTkFrame(
            status_row,
            width=1,
            fg_color=(Colors.BORDER_LIGHT, Colors.BORDER_DARK)
        )
        separator_line.pack(side="left", fill="y", padx=Sizes.PADDING_LARGE, pady=4)
        
        # 右侧：进程状态（横向布局）
        self._create_status_inline(status_row, "进程状态", "process", side="left")
        
        # 分割线
        separator = ctk.CTkFrame(
            container,
            height=1,
            fg_color=(Colors.BORDER_LIGHT, Colors.BORDER_DARK)
        )
        separator.pack(fill="x", pady=(Sizes.PADDING_TINY, Sizes.PADDING_SMALL))
        
        # 切换按钮 - 单独一行，居中
        from ..ctk_styles import StyledButton
        self.toggle_btn = StyledButton(
            container,
            text="⚡  切换服务状态",
            command=self._handle_toggle,
            style="primary",
            width=180,
            height=42,
            corner_radius=Sizes.CORNER_RADIUS_LARGE,
            font=("Microsoft YaHei UI", 13, "bold")
        )
        self.toggle_btn.pack(anchor="center", pady=(Sizes.PADDING, 0))
    
    def _create_status_inline(self, parent, label_text, status_type, side="left"):
        """创建单个状态项（横向单行布局）
        
        Args:
            parent: 父容器
            label_text: 标签文本
            status_type: 状态类型 ("service" 或 "process")
            side: pack 的 side 参数
        """
        # 整个状态项容器（等宽）
        item_container = ctk.CTkFrame(parent, fg_color="transparent")
        item_container.pack(side=side, fill="both", expand=True)
        
        # 状态指示器（8px 圆点）
        indicator_container = ctk.CTkFrame(item_container, fg_color="transparent", width=12, height=12)
        indicator_container.pack(side="left", padx=(0, 6))
        indicator_container.pack_propagate(False)
        
        if status_type == "service":
            self.service_indicator = ctk.CTkLabel(
                indicator_container,
                text="●",
                font=("Microsoft YaHei UI", 10),
                text_color=Colors.TEXT_SECONDARY_DARK
            )
            self.service_indicator.pack(expand=True)
        else:
            self.process_indicator = ctk.CTkLabel(
                indicator_container,
                text="●",
                font=("Microsoft YaHei UI", 10),
                text_color=Colors.TEXT_SECONDARY_DARK
            )
            self.process_indicator.pack(expand=True)
        
        # 标签文本
        ctk.CTkLabel(
            item_container,
            text=label_text,
            font=("Microsoft YaHei UI", 12),
            anchor="w"
        ).pack(side="left", padx=(0, 12))
        
        # 状态徽章（固定宽度等宽，固定高度）
        badge_container = ctk.CTkFrame(
            item_container,
            corner_radius=8,
            fg_color="transparent",
            width=120,  # 设置固定宽度，让两个徽章等宽
            height=28   # 设置固定高度，防止占满面板
        )
        badge_container.pack(side="left")
        badge_container.pack_propagate(False)  # 保持固定尺寸
        
        if status_type == "service":
            self.service_badge = badge_container
            self.service_status_label = ctk.CTkLabel(
                badge_container,
                text="正在获取...",
                font=("Microsoft YaHei UI", 11),
                text_color=Colors.TEXT_SECONDARY_DARK
            )
            self.service_status_label.pack(padx=12, pady=4, expand=True)
        else:
            self.process_badge = badge_container
            self.process_status_label = ctk.CTkLabel(
                badge_container,
                text="正在获取...",
                font=("Microsoft YaHei UI", 11),
                text_color=Colors.TEXT_SECONDARY_DARK
            )
            self.process_status_label.pack(padx=12, pady=4, expand=True)
    
    def _animate_loading(self):
        """处理加载动画"""
        if not self.is_monitoring:
            return
        
        updating = False
        dots = "." * (self.loading_dots % 4)
        
        if self.last_status["service"] == "LOADING":
            self.service_status_label.configure(text=f"正在获取{dots}")
            updating = True
        
        if self.last_status["process"] == "LOADING":
            self.process_status_label.configure(text=f"正在获取{dots}")
            updating = True
        
        if updating:
            self.loading_dots += 1
            self.after(400, self._animate_loading)
    
    def _handle_toggle(self):
        """处理切换逻辑"""
        curr_s = self.service_status_label.cget("text")
        s_name = self.config.get("service_name", "proxifierdrv")
        p_path = self.config.get("proxifier_exe_path", "")
        
        # 禁用按钮并显示处理中状态
        self.toggle_btn.configure(state="disabled", text="⏳  正在处理...")
        
        def run_toggle():
            try:
                if "RUNNING" in curr_s or "运行中" in curr_s:
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
                text="⚡  切换服务状态"
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
        """主线程安全刷新 UI - Fluent 风格语义化状态"""
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
        
        # 更新服务状态 - 语义化设计
        if s_status == "RUNNING":
            # 成功状态：绿色 + ✓
            self.service_indicator.configure(text_color=Colors.SUCCESS)
            self.service_status_label.configure(
                text="✓  RUNNING",
                text_color=Colors.SUCCESS
            )
            self.service_badge.configure(
                fg_color=self._get_subtle_bg(Colors.SUCCESS)
            )
        elif s_status == "STOPPED":
            # 停止状态：灰色 + ⏸
            gray_color = Colors.TEXT_SECONDARY_DARK
            self.service_indicator.configure(text_color=gray_color)
            self.service_status_label.configure(
                text="⏸  STOPPED",
                text_color=gray_color
            )
            self.service_badge.configure(
                fg_color=self._get_subtle_bg(gray_color)
            )
        elif s_status == "NOT_INSTALLED":
            # 警告状态：橙色 + ⚠
            self.service_indicator.configure(text_color=Colors.WARNING)
            self.service_status_label.configure(
                text="⚠  未安装",
                text_color=Colors.WARNING
            )
            self.service_badge.configure(
                fg_color=self._get_subtle_bg(Colors.WARNING)
            )
        else:
            # 其他状态：中性色
            neutral_color = Colors.TEXT_SECONDARY_DARK
            self.service_indicator.configure(text_color=neutral_color)
            self.service_status_label.configure(
                text=f"●  {s_status}",
                text_color=neutral_color
            )
            self.service_badge.configure(
                fg_color=self._get_subtle_bg(neutral_color)
            )
        
        # 更新进程状态 - 语义化设计
        if p_running:
            # 运行中：绿色 + ✓
            self.process_indicator.configure(text_color=Colors.SUCCESS)
            self.process_status_label.configure(
                text="✓  运行中",
                text_color=Colors.SUCCESS
            )
            self.process_badge.configure(
                fg_color=self._get_subtle_bg(Colors.SUCCESS)
            )
        else:
            # 已停止：灰色 + ⏸
            gray_color = Colors.TEXT_SECONDARY_DARK
            self.process_indicator.configure(text_color=gray_color)
            self.process_status_label.configure(
                text="⏸  已停止",
                text_color=gray_color
            )
            self.process_badge.configure(
                fg_color=self._get_subtle_bg(gray_color)
            )
    
    def _get_subtle_bg(self, color):
        """获取轻量化背景色 - 模拟 rgba 透明效果
        
        Args:
            color: 前景色
            
        Returns:
            适合当前主题的轻量背景色
        """
        # 根据颜色返回对应的轻量背景
        if color == Colors.SUCCESS:
            # 绿色：rgba(34,197,94,0.15) 效果
            return (Colors.SUCCESS_BG, Colors.SUCCESS_BG_DARK)
        elif color == Colors.DANGER:
            # 红色：rgba(211,47,47,0.15) 效果
            return (Colors.DANGER_BG, Colors.DANGER_BG_DARK)
        elif color == Colors.WARNING:
            # 橙色：rgba(245,124,0,0.15) 效果
            return (Colors.WARNING_BG, Colors.WARNING_BG_DARK)
        else:
            # 中性色：轻微透明
            return ((Colors.HOVER_LIGHT, Colors.HOVER_DARK))
    
    def stop_monitoring(self):
        """停止监控"""
        self.is_monitoring = False
    
    def update_config(self, new_config):
        """更新配置"""
        self.config = new_config
        self.last_status = {"service": "LOADING", "process": "LOADING"}
        if self.winfo_exists():
            self._animate_loading()
