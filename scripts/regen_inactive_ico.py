from PIL import Image
import os
from pathlib import Path

def convert():
    assets_dir = Path(r"d:\Users\15119\工作区\Code\tools\easy-proxifier-toggle\assets")
    png_path = assets_dir / "icon_inactive.png"
    ico_path = assets_dir / "icon_inactive.ico"
    
    if not png_path.exists():
        print(f"Error: {png_path} not found.")
        return

    try:
        img = Image.open(png_path)
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
            
        # 使用多尺寸保存，确保清晰度
        sizes = [(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)]
        img.save(ico_path, format='ICO', sizes=sizes)
        print(f"Successfully regenerated: {ico_path}")
    except Exception as e:
        print(f"Failed: {e}")

if __name__ == "__main__":
    convert()
