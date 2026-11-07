# HereSphere 简体中文补丁

适用于 **Windows / Steam 版 HereSphere 0.11.4（UE4.25）特定构建**的非官方简体中文补丁。安装器会校验原始 EXE 和 PAK 的 SHA-256；即使版本号相同，构建文件不匹配也会拒绝安装。

## 下载与安装

**[下载完整汉化安装包](https://github.com/Roryzhou233/HereSphere-Chinese/raw/refs/heads/main/downloads/HereSphere_Chinese_Update.zip)** · [SHA-256 校验文件](downloads/SHA256SUMS.txt)

1. 完全退出 HereSphere，解压整个安装包。
2. 打开解压后的 `HereSphere_Chinese` 文件夹，双击 `Install.cmd`。
3. 安装器自动查找 Steam 游戏库；有多个安装时选择编号，未找到时粘贴包含 `HereSphere.exe` 的游戏根目录。
4. 提示校验成功后，从 Steam 正常启动。遇到访问被拒绝时，以管理员身份运行安装器。

双击 `Uninstall.cmd` 可卸载并恢复备份的原程序。**需要完整安装包；仅复制 PAK 无法汉化动态下拉菜单。** 下载上方 ZIP 即可，无需 Python，也无需下载整个源码仓库。

支持自定义安装位置、中文路径和带空格的路径：

```cmd
Install.cmd -GameDir "D:\我的游戏\SteamLibrary\steamapps\common\HereSphere"
Uninstall.cmd -GameDir "D:\我的游戏\SteamLibrary\steamapps\common\HereSphere"
```

完整安装、升级、卸载和编码说明见 [使用说明](release/使用说明.md)。更新 HereSphere 前建议先卸载补丁。

## 汉化范围

- 113 个 UI 资源中的 2379 处文字，以及 359 条说明表内容。
- 投影、立体模式、宽高比、屏幕朝向、背景及遮罩等下拉菜单常用选项。
- 字幕弹窗、设置项、提示和用户指南。
- 体感控制器、游戏手柄、键盘、鼠标的按键绑定操作名称及常用按键显示名称。
- 1091 条动态显示翻译，保留内部选项值、按键标识和存档格式。

产品名、第三方版权声明、用户文件名、字母键及部分技术缩写保留原文，仍可能有未覆盖的英文。具体资源数量和校验值见 [构建报告](release/build-report.json)。

## 源码与构建

仓库提供翻译表、PAK 读写与资源修改脚本、程序显示补丁生成脚本、安装器及验证脚本。原始游戏资源、完整游戏 EXE、测试副本和第三方工具依赖不随源码分发。安装包包含运行所需的 PAK 与补丁数据。

维护者需要合法安装匹配的原版软件，并使用 Python 3.11 或更高版本：

```powershell
python -m pip install -r requirements.txt
```

当前构建脚本沿用制作时的本机路径。若游戏不在默认 Steam 目录，先修改 `pak_tool.py` 的 `GAME`、`inspect_native.py` 的 `EXE` 以及相关验证脚本的游戏路径。已安装汉化时，`inspect_native.py` 优先读取 `.cn-original` 备份。发行安装器本身支持自动发现目录。

在项目根目录依次运行：

```powershell
python pak_tool.py
python build_patch.py
python build_native_patch.py
python verify_native_patch.py
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\verify_discovery.ps1
python verify_cmd_encoding.py
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\verify_installer.ps1
```

`pak_tool.py` 将本机原始资源解包至被 Git 忽略的 `original/`；两个构建脚本生成 `release/` 下的 PAK、程序补丁数据及报告。验证脚本使用本地游戏或隔离测试目录；安装器验证需要有效的原程序 `.cn-original` 备份。编译出的测试 EXE 不会上传。

主要维护入口：`translate_catalog.py`（界面）、`translate_help.py`（说明）、`translate_bindings.py`（按键显示）。

## 反馈与声明

发现遗漏或问题时，可在 [Issues](https://github.com/Roryzhou233/HereSphere-Chinese/issues) 提交软件版本、界面位置及截图。

本项目为非官方汉化，与 HereSphere 开发者无隶属关系。HereSphere 及原始资源的权利归原权利人所有；本补丁不提供完整软件，不替代原软件授权。
