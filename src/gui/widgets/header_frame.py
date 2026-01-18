import tkinter as tk
from PIL import Image, ImageTk, ImageSequence
from ..styles import FONTS, COLORS

class HeaderFrame(tk.Frame):
    """页眉组件 - 支持动态 GIF Logo 和标题"""
    def __init__(self, master, title, logo_path, **kwargs):
        super().__init__(master, **kwargs)
        self.title_text = title
        self.logo_path = logo_path
        self.frames = []
        self._curr_frame_idx = 0
        self._setup_ui()

    def _setup_ui(self):
        # 容器
        self.logo_label = tk.Label(self, bg=self["bg"])
        self.logo_label.pack(side=tk.LEFT, padx=(0, 10))

        # 加载 GIF 序列并缩放
        try:
            if self.logo_path.exists():
                img = Image.open(self.logo_path)
                
                # 遍历所有帧
                for frame in ImageSequence.Iterator(img):
                    # 关键：先转换为 RGBA 确保缩放时 alpha 通道处理正确，减少锯齿感
                    frame = frame.convert("RGBA")
                    
                    h = 36 # 稍微放大一点点
                    w = int(frame.width * (h / frame.height))
                    # 使用高质量滤镜
                    frame = frame.resize((w, h), Image.Resampling.LANCZOS)
                    
                    self.frames.append(ImageTk.PhotoImage(frame))
                
                if self.frames:
                    self._animate()
        except Exception as e:
            print(f"Error loading animated header logo: {e}")

        # 标题文字
        tk.Label(
            self, 
            text=self.title_text, 
            font=FONTS["caption"], 
            fg=COLORS["primary"], 
            bg=self["bg"]
        ).pack(side=tk.LEFT)

    def _animate(self):
        """循环更新 GIF 帧"""
        if not self.frames:
            return
            
        frame = self.frames[self._curr_frame_idx]
        self.logo_label.config(image=frame)
        
        self._curr_frame_idx = (self._curr_frame_idx + 1) % len(self.frames)
        
        # 约 50ms 一帧 (20fps)，可根据实际 GIF 调整
        self.after(50, self._animate)
