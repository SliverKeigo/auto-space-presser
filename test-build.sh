#!/bin/bash

# 测试Tauri构建修复的脚本

echo "测试Tauri构建修复..."

# 运行修复脚本
echo "1. 运行修复脚本..."
chmod +x ./fix-build-path.sh
./fix-build-path.sh

# 尝试构建（仅编译，不打包）
echo "2. 测试编译..."
TAURI_PATH_SEPARATOR="/" pnpm tauri build --debug

# 检查构建结果
if [ $? -eq 0 ]; then
  echo "✅ 测试成功！修复有效。"
  echo "您现在可以运行 'pnpm build-clean' 进行完整构建。"
else
  echo "❌ 测试失败。修复可能不完整。"
  echo "请检查错误消息并修改fix-build-path.sh脚本。"
fi 