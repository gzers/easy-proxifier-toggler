"""
版本更新工具
用于自动同步 src/__init__.py, README.md, PROJECT_SUMMARY.md 中的版本号
使用方法: python scripts/update_version.py 2.3.1
"""
import re
import os
import argparse
from pathlib import Path

# 获取项目根目录 (scripts 目录的上一级)
PROJECT_ROOT = Path(__file__).parent.parent

def update_src_init(new_version):
    """更新源代码中的版本号"""
    path = PROJECT_ROOT / "src" / "__init__.py"
    if not path.exists():
        print(f"❌ 未找到文件: {path}")
        return

    content = path.read_text(encoding="utf-8")
    # 匹配 __version__ = "x.y.z"
    pattern = r'__version__ = "[^"]+"'
    replacement = f'__version__ = "{new_version}"'
    
    if re.search(pattern, content):
        new_content = re.sub(pattern, replacement, content)
        path.write_text(new_content, encoding="utf-8")
        print(f"✅ 已更新 src/__init__.py: {new_version}")
    else:
        print(f"⚠️  在 src/__init__.py 中未找到版本号定义")

def update_readme(new_version):
    """更新 README 中的徽章版本"""
    path = PROJECT_ROOT / "README.md"
    if not path.exists():
        print(f"❌ 未找到文件: {path}")
        return

    content = path.read_text(encoding="utf-8")
    # 匹配 Shield Badge: version-x.y.z-blue.svg
    pattern = r'version-[\d\.]+(-[a-zA-Z]+)?\.svg'
    replacement = f'version-{new_version}-blue.svg'
    
    if re.search(pattern, content):
        new_content = re.sub(pattern, replacement, content)
        path.write_text(new_content, encoding="utf-8")
        print(f"✅ 已更新 README.md Badge: {new_version}")
    else:
        print(f"⚠️  在 README.md 中未找到版本徽章链接")

def update_project_summary(new_version):
    """更新项目概要中的版本号"""
    path = PROJECT_ROOT / "PROJECT_SUMMARY.md"
    if not path.exists():
        # 这个文件可能不存在，不是必须的
        return

    content = path.read_text(encoding="utf-8")
    # 匹配 **版本**: 2.3.0
    pattern = r'\*\*版本\*\*: [\d\.]+'
    replacement = f'**版本**: {new_version}'
    
    if re.search(pattern, content):
        new_content = re.sub(pattern, replacement, content)
        path.write_text(new_content, encoding="utf-8")
        print(f"✅ 已更新 PROJECT_SUMMARY.md: {new_version}")
    else:
        print(f"⚠️  在 PROJECT_SUMMARY.md 中未找到版本号字段")

def get_current_version():
    """读取当前版本"""
    path = PROJECT_ROOT / "src" / "__init__.py"
    if not path.exists():
        return "Unknown"
        
    content = path.read_text(encoding="utf-8")
    match = re.search(r'__version__ = "([^"]+)"', content)
    if match:
        return match.group(1)
    return "Unknown"

def main():
    parser = argparse.ArgumentParser(description="版本号同步工具")
    parser.add_argument("version", help="新版本号 (例如 2.3.1)")
    args = parser.parse_args()
    
    current = get_current_version()
    print(f"当前版本: {current}")
    print(f"目标版本: {args.version}")
    print("-" * 40)
    
    update_src_init(args.version)
    update_readme(args.version)
    update_project_summary(args.version)
    
    print("-" * 40)
    print("⚠️  请记得手动更新 docs/CHANGELOG.md 添加详细更新日志！")

if __name__ == "__main__":
    main()
