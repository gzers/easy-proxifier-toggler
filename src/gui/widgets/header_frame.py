import tkinter as tk
from PIL import Image, ImageTk, ImageSequence
from ..styles import FONTS, COLORS

class HeaderFrame(tk.Frame):
    """页眉组件 - 支持动态 GIF Logo (包含缓存优化)"""
    _frames_cache = {} # 类级别缓存，避免重复解码

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

        # 优先从缓存读取
        cache_key = str(self.logo_path)
        if cache_key in HeaderFrame._frames_cache:
            self.frames = HeaderFrame._frames_cache[cache_key]
        else:
            # 异步处理或至少在第一次加载时优化
            try:
                if self.logo_path.exists():
                    img = Image.open(self.logo_path)
                    processed_frames = []
                    
                    for frame in ImageSequence.Iterator(img):
                        frame = frame.convert("RGBA")
                        h = 36 
                        w = int(frame.width * (h / frame.height))
                        frame = frame.resize((w, h), Image.Resampling.LANCZOS)
                        processed_frames.append(ImageTk.PhotoImage(frame))
                    
                    self.frames = processed_frames
                    HeaderFrame._frames_cache[cache_key] = self.frames
            except Exception as e:
                print(f"Error loading header logo: {e}")

        if self.frames:
            self._animate()

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
        if not self.winfo_exists() or not self.frames:
            return
            
        try:
            frame = self.frames[self._curr_frame_idx]
            self.logo_label.config(image=frame)
            self._curr_frame_idx = (self._curr_frame_idx + 1) % len(self.frames)
            self.after(50, self._animate)
        except:
            pass
