"""
一键生成所有图标文件
从 PNG 文件生成对应的 ICO 文件
"""
from PIL import Image
from pathlib import Path

def convert_png_to_ico(png_filename, ico_filename, description):
    """将 PNG 转换为多尺寸 ICO"""
    assets_dir = Path(__file__).parent.parent / "assets"
    png_path = assets_dir / png_filename
    ico_path = assets_dir / ico_filename
    
    if not png_path.exists():
        print(f"⚠️  跳过 {description}: {png_path} 不存在")
        return False
    
    try:
        img = Image.open(png_path)
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        
        # 使用多尺寸保存，确保在不同 DPI 下清晰显示
        sizes = [(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)]
        img.save(ico_path, format='ICO', sizes=sizes)
        print(f"✅ {description}: {ico_filename}")
        print(f"   包含尺寸: {', '.join([f'{s[0]}x{s[1]}' for s in sizes])}")
        return True
    except Exception as e:
        print(f"❌ {description} 生成失败: {e}")
        return False

def main():
    print("=" * 60)
    print("图标生成工具 - Easy Proxifier Toggler")
    print("=" * 60)
    print()
    
    success_count = 0
    total_count = 0
    
    # 生成活动状态图标
    total_count += 1
    if convert_png_to_ico("icon.png", "icon.ico", "活动状态图标"):
        success_count += 1
    print()
    
    # 生成非活动状态图标
    total_count += 1
    if convert_png_to_ico("icon_inactive.png", "icon_inactive.ico", "非活动状态图标"):
        success_count += 1
    print()
    
    print("=" * 60)
    print(f"完成! 成功生成 {success_count}/{total_count} 个图标文件")
    print("=" * 60)

if __name__ == "__main__":
    main()
