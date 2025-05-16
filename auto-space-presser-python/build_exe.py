import PyInstaller.__main__
import os
import sys
import shutil

# 构建参数
app_name = "自动按键工具"
main_script = "auto_key_app.py"

# 创建临时目录(如果不存在)
if not os.path.exists("build"):
    os.makedirs("build")
if not os.path.exists("dist"):
    os.makedirs("dist")

# 使用PyInstaller打包
PyInstaller.__main__.run([
    main_script,
    "--name=%s" % app_name,
    "--onefile",  # 打包成单个exe文件
    "--windowed",  # 使用窗口界面(不显示控制台)
    "--icon=NONE",  # 如果有图标可以替换此处
    "--add-data=README.md;.",  # 添加额外文件
    "--clean",  # 清理缓存
    "--noconfirm",  # 不要询问确认
    "--log-level=WARN",  # 日志级别
])

# 打印完成信息
print(f"\n打包完成！可执行文件位于: dist/{app_name}.exe")
print("你可以在任何没有安装Python的Windows电脑上运行此文件。")
