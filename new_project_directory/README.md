# 自动空格按键工具 (Auto Space Presser)

这是一个基于Tauri的桌面应用程序，可以按设定的时间间隔自动按下空格键。特别适用于需要保持屏幕活动或需要定时按键的场景。

## 功能特点

- 可自定义按键时间间隔（毫秒级）
- 简洁直观的用户界面
- 支持Windows系统（主要目标平台）
- 应用程序最小化后仍能继续在后台工作
- 轻量级，资源占用少

## 开发技术

- 前端：React + TypeScript
- 后端：Rust + Tauri
- 构建工具：PNPM + Vite

## 安装方法

### 下载预构建版本

从[GitHub Releases](https://github.com/sliverkeigo/auto-space-presser/releases)页面下载最新版本。

- Windows用户: 下载 `.exe` 或 `.msi` 文件
- macOS用户: 下载 `.dmg` 文件

### 从源码构建

1. 克隆仓库
```bash
git clone https://github.com/sliverkeigo/auto-space-presser.git
cd auto-space-presser
```

2. 安装依赖
```bash
pnpm install
```

3. 开发模式运行
```bash
pnpm tauri dev
```

4. 构建可执行文件
```bash
pnpm tauri build
```

## 使用说明

1. 启动应用程序
2. 在输入框中设置按键间隔时间（毫秒）
3. 点击"开始"按钮启动自动按键
4. 应用可以最小化，会继续在后台工作
5. 需要停止时，点击"停止"按钮

## 贡献指南

欢迎提交问题报告或功能建议！如果您想贡献代码，请fork本仓库并提交拉取请求。

## 许可证

MIT
