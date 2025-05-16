@echo off
echo 创建优化打包环境，生成更小的可执行文件...

:: 创建临时虚拟环境
echo 正在创建虚拟环境...
python -m venv temp_venv

:: 激活虚拟环境
echo 正在激活虚拟环境...
call temp_venv\Scripts\activate

:: 只安装必要的依赖
echo 正在安装必要的依赖...
pip install customtkinter==5.2.1 keyboard==0.13.5 pyinstaller==6.3.0

:: 对于非Windows系统，也安装pyautogui（但我们现在只考虑Windows）
:: pip install pyautogui==0.9.54

:: 运行PyInstaller打包（使用最小化选项）
echo 正在打包应用...
pyinstaller --onefile ^
    --windowed ^
    --clean ^
    --name="自动按键工具_精简版" ^
    --strip ^
    --exclude-module=matplotlib ^
    --exclude-module=scipy ^
    --exclude-module=pandas ^
    --exclude-module=numpy ^
    --exclude-module=PyQt5 ^
    --exclude-module=PySide2 ^
    auto_key_app.py

:: 退出虚拟环境
echo 正在清理环境...
deactivate

:: 可选：删除临时虚拟环境
:: 如果你希望保留环境以便以后使用，请注释掉下面这行
echo 是否删除临时虚拟环境? (Y/N)
set /p RESP=
if /i "%RESP%"=="Y" (
    rmdir /s /q temp_venv
    echo 已删除临时虚拟环境
) else (
    echo 已保留临时虚拟环境，如需手动删除请运行: rmdir /s /q temp_venv
)

echo.
echo 优化打包完成! 精简版可执行文件位于: dist\自动按键工具_精简版.exe
echo 文件体积应该比之前的版本小很多。
pause
