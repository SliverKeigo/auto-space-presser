import PyInstaller.__main__
import os

# 应用名称
app_name = "自动按键工具"
main_script = "auto_key_app.py"

# 创建临时目录(如果不存在)
if not os.path.exists("build"):
    os.makedirs("build")
if not os.path.exists("dist"):
    os.makedirs("dist")

# 优化参数（减小文件体积）
PyInstaller.__main__.run([
    main_script,
    "--name=%s" % app_name,
    "--onefile",                 # 打包成单个exe文件
    "--windowed",                # 使用窗口界面(不显示控制台)
    "--icon=NONE",               # 如果有图标可以替换此处
    "--noupx",                   # 不使用UPX压缩（避免被杀毒软件误报）
    "--clean",                   # 清理缓存
    "--noconfirm",               # 不要询问确认
    "--log-level=WARN",          # 日志级别
    # 以下是优化参数
    "--strip",                   # 减小二进制文件体积
    "--exclude-module=matplotlib",  # 排除不需要的大型模块
    "--exclude-module=scipy",
    "--exclude-module=pandas",
    "--exclude-module=numpy",
    "--exclude-module=PyQt5",
    "--exclude-module=PySide2",
    "--exclude-module=PIL.ImageQt",
    # 仅包含所需的tkinter模块
    # "--exclude-module=tkinter.test",
    # "--exclude-module=tkinter.tix",
    # "--exclude-module=tk.demos",
])

print(f"\n优化打包完成！可执行文件位于: dist/{app_name}.exe")
print("文件体积已经过优化，应该比之前的版本小很多。")
