from PIL import Image
from pathlib import Path

def convert():
    """从 icon.png 生成 icon.ico（活动状态图标）"""
    assets_dir = Path(__file__).parent.parent / "assets"
    png_path = assets_dir / "icon.png"
    ico_path = assets_dir / "icon.ico"
    
    if not png_path.exists():
        print(f"错误: {png_path} 不存在。")
        return
    
    try:
        img = Image.open(png_path)
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        
        # 使用多尺寸保存，确保在不同 DPI 下清晰显示
        sizes = [(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)]
        img.save(ico_path, format='ICO', sizes=sizes)
        print(f"✅ 成功生成: {ico_path}")
        print(f"   包含尺寸: {', '.join([f'{s[0]}x{s[1]}' for s in sizes])}")
    except Exception as e:
        print(f"❌ 生成失败: {e}")

if __name__ == "__main__":
    convert()
