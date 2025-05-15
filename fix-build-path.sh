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

# 检查capabilities配置
if ! grep -q '"capabilities"' src-tauri/tauri.conf.json; then
  echo "警告: 缺少capabilities配置，这可能会导致应用权限问题"
fi

echo "3. 准备重新构建..."
# 设置TAURI_PATH_SEPARATOR环境变量以避免Windows路径问题
export TAURI_PATH_SEPARATOR="/"

echo "修复完成！请尝试重新构建应用："
echo "pnpm tauri build" 