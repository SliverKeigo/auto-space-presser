# 自动按键工具 (Auto Key Presser)

一个现代化的跨平台自动按键工具，使用 Python 和 CustomTkinter 开发。能在全屏应用中定时自动按下指定的按键。

## 功能特点

- **美观的现代界面**：使用 CustomTkinter 构建的界面美观易用
- **多按键支持**：支持空格、回车、Tab、Esc 以及方向键
- **灵活的时间设置**：通过滑块或精确输入设置按键间隔
- **全屏应用支持**：在全屏应用和游戏中也能正常工作
- **跨平台兼容**：
  - Windows 使用 keyboard 库
  - Mac 和 Linux 使用 pyautogui 库

## 系统要求

- Python 3.6+
- Windows/Mac/Linux 操作系统

## 安装方法

1. 确保已安装 Python
2. 运行以下命令安装依赖：

```bash
pip install -r requirements.txt
```

## 运行方法

```bash
python auto_key_app.py
```

## 使用说明

1. 从下拉菜单中选择要自动按下的按键
2. 使用滑块调整按键间隔时间，或在精确设置框中输入具体数值
3. 点击"开始"按钮启动自动按键
4. 点击"停止"按钮停止自动按键

## 注意事项

- 在 Mac 和 Linux 系统上，可能需要额外的系统权限来允许按键模拟
- 在 Windows 系统上，某些游戏可能有反作弊机制，可能会检测到自动按键

## 技术信息

本工具使用以下技术：

- CustomTkinter - 用于现代化的 GUI 界面
- keyboard - 用于 Windows 系统的键盘模拟
- pyautogui - 用于 Mac 和 Linux 系统的键盘模拟
