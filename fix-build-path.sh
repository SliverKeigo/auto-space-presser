#!/bin/bash

# 修复Tauri 2.0路径问题的脚本

echo "开始修复Tauri构建路径问题..."

# 清理之前的构建缓存
echo "1. 清理构建缓存..."
rm -rf src-tauri/target
rm -rf src-tauri/.cargo

# 检查并修正tauri.conf.json
echo "2. 检查Tauri配置..."

# 确保正确的应用标识符格式
IDENTIFIER=$(grep -o '"identifier": "[^"]*"' src-tauri/tauri.conf.json | cut -d'"' -f4)
if [[ ! $IDENTIFIER =~ ^[a-z][a-z0-9_]*(\.[a-z0-9_]+)+[a-z0-9_]$ ]]; then
  echo "警告: 应用标识符 '$IDENTIFIER' 格式可能不正确，建议使用格式如 'com.example.app'"
fi

# 检查capabilities目录是否存在
if [ ! -d "src-tauri/capabilities" ]; then
  echo "创建capabilities目录..."
  mkdir -p src-tauri/capabilities
fi

# 检查键盘输入capabilities配置
if [ ! -f "src-tauri/capabilities/keyboard.json" ]; then
  echo "创建键盘输入capability配置..."
  cat > src-tauri/capabilities/keyboard.json << 'EOL'
{
  "$schema": "../gen/schemas/desktop-schema.json",
  "identifier": "keyboard-input",
  "description": "允许应用程序模拟键盘输入",
  "windows": ["main"],
  "permissions": [
    "keyboard:allow-input"
  ]
}
EOL
fi

# 检查默认capabilities配置
if [ ! -f "src-tauri/capabilities/default.json" ]; then
  echo "创建默认capability配置..."
  cat > src-tauri/capabilities/default.json << 'EOL'
{
  "$schema": "../gen/schemas/desktop-schema.json",
  "identifier": "default",
  "description": "自动空格按键工具的基本权限",
  "windows": ["main"],
  "permissions": [
    "core:default",
    "opener:default"
  ]
}
EOL
fi

# 确保tauri.conf.json引用了正确的capabilities
if ! grep -q '"capabilities"' src-tauri/tauri.conf.json; then
  echo "警告: tauri.conf.json中缺少capabilities配置，这可能会导致应用权限问题"
fi

echo "3. 准备重新构建..."
# 设置TAURI_PATH_SEPARATOR环境变量以避免Windows路径问题
export TAURI_PATH_SEPARATOR="/"

echo "修复完成！请尝试重新构建应用："
echo "pnpm tauri build" 