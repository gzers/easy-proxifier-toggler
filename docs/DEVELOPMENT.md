# 开发指南

## 开发环境设置

### 1. 克隆/下载项目
```bash
git clone <repository-url>
cd easy-proxifier-toggle
```

### 2. 安装依赖
```bash
pip install -r requirements.txt
```

### 3. 配置开发环境
首次运行会自动创建配置文件 `config/config.json`

---

## 运行项目

### 🔧 开发模式（推荐用于开发调试）

**使用开发模式启动脚本**：
```bash
python run_dev.py
```

**特点**：
- ✅ 跳过管理员权限检查
- ✅ 显示详细的启动信息
- ✅ 更好的错误提示
- ✅ 不会弹出 UAC 对话框
- ⚠️ 某些功能（服务控制）可能无法使用

**适用场景**：
- 开发和调试 GUI 界面
- 测试配置管理功能
- 修改代码后快速验证
- 查看错误堆栈信息

---

### 🚀 生产模式（完整功能）

**使用生产模式启动脚本**：
```bash
python run.py
```

**特点**：
- ✅ 自动请求管理员权限
- ✅ 所有功能完整可用
- ✅ 可以控制 Windows 服务
- ⚠️ 会弹出 UAC 对话框
- ⚠️ 程序会重启（命令行窗口会关闭）

**适用场景**：
- 测试完整功能
- 验证服务控制功能
- 最终测试和发布前验证

---

## 两种模式的区别

| 特性 | 开发模式 (`run_dev.py`) | 生产模式 (`run.py`) |
|------|------------------------|---------------------|
| 管理员权限 | ❌ 不需要 | ✅ 自动请求 |
| UAC 对话框 | ❌ 不弹出 | ✅ 会弹出 |
| 程序重启 | ❌ 不会 | ✅ 会重启 |
| 命令行输出 | ✅ 保持 | ❌ 关闭 |
| 错误提示 | ✅ 详细 | ⚠️ 简单 |
| 服务控制 | ❌ 不可用 | ✅ 可用 |
| GUI 功能 | ✅ 可用 | ✅ 可用 |
| 配置管理 | ✅ 可用 | ✅ 可用 |

---

## 开发工作流

### 1. 日常开发
```bash
# 1. 修改代码
# 2. 使用开发模式测试
python run_dev.py

# 3. 测试 GUI 和配置功能
# 4. 修复问题，重复步骤 2-3
```

### 2. 功能测试
```bash
# 测试需要管理员权限的功能
python run.py
```

### 3. 单元测试
```bash
# 测试项目结构
python test_structure.py

# 测试配置功能
python scripts/check_config.py
```

---

## 调试技巧

### 1. 查看详细错误信息
开发模式会显示完整的错误堆栈：
```bash
python run_dev.py
```

### 2. 测试特定模块
```python
# 测试配置管理
python -c "from src.config import manager; print(manager.load_config())"

# 测试服务状态（需要管理员权限）
python -c "from src.core import service; print(service.get_service_status('proxifierdrv'))"
```

### 3. 使用 Python 调试器
```bash
# 使用 pdb 调试
python -m pdb run_dev.py

# 或在代码中添加断点
import pdb; pdb.set_trace()
```

### 4. 查看配置文件
```bash
# Windows
type config\config.json

# 或使用文本编辑器打开
notepad config\config.json
```

---

## 常见问题

### Q: 为什么运行 `python run.py` 后命令行窗口关闭了？
**A**: 这是正常行为。程序请求管理员权限后会重启，原来的命令行窗口会关闭。程序会在系统托盘中运行。

**解决方案**：
- 开发时使用 `python run_dev.py`
- 查看托盘图标确认程序是否运行

### Q: 开发模式下为什么某些功能不可用？
**A**: 开发模式跳过了管理员权限检查，因此无法控制 Windows 服务。

**解决方案**：
- GUI 和配置功能可以在开发模式下测试
- 服务控制功能需要使用生产模式测试

### Q: 如何在开发模式下测试服务控制功能？
**A**: 以管理员身份运行命令提示符，然后运行 `python run_dev.py`

```bash
# 1. 右键点击"命令提示符"
# 2. 选择"以管理员身份运行"
# 3. 切换到项目目录
cd d:\Users\15119\工作区\Code\tools\easy-proxifier-toggle
# 4. 运行开发模式
python run_dev.py
```

### Q: 如何查看程序日志？
**A**: 当前版本没有日志系统。可以在代码中添加 `print()` 语句，然后使用开发模式查看输出。

---

## 代码结构

### 添加新功能的步骤

1. **确定功能位置**
   ```
   src/
   ├── core/      # 核心功能（服务、进程管理）
   ├── gui/       # GUI 相关（托盘、设置窗口）
   ├── config/    # 配置管理
   └── utils/     # 工具函数
   ```

2. **创建新模块**
   ```python
   # src/core/new_feature.py
   """新功能模块"""
   
   def new_function():
       """新功能函数"""
       pass
   ```

3. **导入并使用**
   ```python
   # src/main.py 或其他文件
   from src.core.new_feature import new_function
   ```

4. **测试**
   ```bash
   python run_dev.py
   ```

---

## 打包发布

### 1. 测试
```bash
# 完整功能测试
python run.py

# 结构测试
python test_structure.py
```

### 2. 打包
```bash
cd scripts
build.bat
```

### 3. 测试打包后的程序
```bash
dist\ProxifierToggler.exe
```

---

## 版本发布指南

### 1. 更新版本号

我们提供了一个自动化脚本来同步更新项目中的版本号（包括 `src/__init__.py`、`README.md` 和 `PROJECT_SUMMARY.md`）。

**使用方法**:
```bash
# 在项目根目录下运行
# 格式: python scripts/update_version.py <新版本号>
python scripts/update_version.py 2.3.1
```

**脚本会自动更新**:
- `src/__init__.py`: 更新 `__version__` 变量
- `README.md`: 更新 Version Badge 链接
- `PROJECT_SUMMARY.md`: 更新版本号字段

### 2. 更新更新日志

**必须手动**编辑 `docs/CHANGELOG.md` 文件，添加详细的更新记录：

```markdown
## [2.3.1] - 2026-01-18

### 新增
- ...

### 修复
- ...
```

### 3. 打包发布

执行打包脚本生成新的可执行文件：

```bash
cd scripts
build.bat
```

---

## 推荐的 IDE 配置

### VS Code

**launch.json** 配置：
```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "开发模式",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/run_dev.py",
            "console": "integratedTerminal"
        },
        {
            "name": "生产模式",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/run.py",
            "console": "integratedTerminal"
        }
    ]
}
```

### PyCharm

1. 创建运行配置
2. Script path: `run_dev.py` 或 `run.py`
3. Working directory: 项目根目录

---

## 贡献指南

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

---

## 技术栈

- **语言**: Python 3.8+
- **GUI**: tkinter (内置), pystray
- **图像处理**: Pillow
- **打包**: PyInstaller

---

## 联系方式

如有问题，请：
- 查看 [README.md](../README.md)
- 查看 [docs/](.) 目录下的其他文档
- 提交 Issue
