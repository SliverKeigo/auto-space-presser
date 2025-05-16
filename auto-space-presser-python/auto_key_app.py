import tkinter as tk
import threading
import time
import sys
import platform
from tkinter import messagebox, ttk
import customtkinter as ctk

# 根据系统选择键盘控制库
SYSTEM = platform.system()
if SYSTEM == "Windows":
    import keyboard
else:
    import pyautogui

class KeyPresser:
    def __init__(self):
        self.running = False
        self.interval = 0.5  # 默认500ms
        self.key = "space"   # 默认空格键
        self.thread = None
        self.system = SYSTEM

    def start(self):
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self._press_key_loop)
            self.thread.daemon = True
            self.thread.start()
            return True
        return False

    def stop(self):
        if self.running:
            self.running = False
            if self.thread:
                self.thread.join(timeout=1.0)
                self.thread = None
            return True
        return False

    def set_interval(self, interval):
        try:
            interval_val = float(interval)
            if interval_val > 0:
                self.interval = interval_val
                return True
        except ValueError:
            pass
        return False

    def set_key(self, key):
        self.key = key
        return True

    def _press_key_loop(self):
        """不同平台的按键循环实现"""
        while self.running:
            try:
                if self.system == "Windows":
                    keyboard.press_and_release(self.key)
                else:
                    pyautogui.press(self.key)
                time.sleep(self.interval)
            except Exception as e:
                print(f"按键错误: {e}")
                time.sleep(self.interval)


class AutoKeyApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # 设置应用主题
        ctk.set_appearance_mode("System")  # 系统主题
        ctk.set_default_color_theme("blue")
        
        self.key_presser = KeyPresser()
        self.title("自动按键工具")
        self.geometry("450x400")
        self.minsize(450, 400)
        
        # 创建UI组件
        self.setup_ui()
        
        # 状态更新计时器
        self.after(1000, self.update_status)
        
        # 关闭窗口时的处理
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def setup_ui(self):
        # 创建主框架
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # 标题
        title_label = ctk.CTkLabel(
            main_frame, 
            text="自动按键工具", 
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=(0, 20))
        
        # 按键选择区域
        key_frame = ctk.CTkFrame(main_frame)
        key_frame.pack(fill="x", padx=10, pady=10)
        
        key_label = ctk.CTkLabel(key_frame, text="选择按键:")
        key_label.pack(side="left", padx=10)
        
        # 创建下拉选择框
        self.key_var = tk.StringVar(value="空格键")
        key_options = ["空格键", "回车键", "Tab键", "Esc键", "左箭头", "右箭头", "上箭头", "下箭头"]
        
        self.key_menu = ctk.CTkOptionMenu(
            key_frame,
            values=key_options,
            variable=self.key_var,
            command=self.on_key_changed
        )
        self.key_menu.pack(side="left", padx=10, fill="x", expand=True)
        
        # 间隔设置区域
        interval_frame = ctk.CTkFrame(main_frame)
        interval_frame.pack(fill="x", padx=10, pady=10)
        
        interval_label = ctk.CTkLabel(interval_frame, text="按键间隔(秒):")
        interval_label.pack(side="left", padx=10)
        
        self.interval_var = tk.DoubleVar(value=0.5)
        
        # 自定义滑块
        self.interval_slider = ctk.CTkSlider(
            interval_frame,
            from_=0.1,
            to=5.0,
            number_of_steps=49,
            variable=self.interval_var,
            command=self.on_slider_changed
        )
        self.interval_slider.pack(side="left", padx=10, fill="x", expand=True)
        
        # 显示具体数值
        self.interval_value_label = ctk.CTkLabel(interval_frame, text="0.5")
        self.interval_value_label.pack(side="left", padx=10)
        
        # 精确输入区域
        precise_frame = ctk.CTkFrame(main_frame)
        precise_frame.pack(fill="x", padx=10, pady=10)
        
        precise_label = ctk.CTkLabel(precise_frame, text="精确设置(秒):")
        precise_label.pack(side="left", padx=10)
        
        self.precise_entry = ctk.CTkEntry(precise_frame, width=80)
        self.precise_entry.insert(0, "0.5")
        self.precise_entry.pack(side="left", padx=10)
        
        apply_button = ctk.CTkButton(
            precise_frame, 
            text="应用", 
            command=self.on_apply_precise,
            width=60
        )
        apply_button.pack(side="left", padx=10)
        
        # 控制按钮区域
        button_frame = ctk.CTkFrame(main_frame)
        button_frame.pack(fill="x", padx=10, pady=(20, 10))
        
        self.start_button = ctk.CTkButton(
            button_frame, 
            text="开始", 
            command=self.on_start,
            fg_color="#28a745",
            hover_color="#218838",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.start_button.pack(side="left", padx=10, fill="x", expand=True)
        
        self.stop_button = ctk.CTkButton(
            button_frame, 
            text="停止", 
            command=self.on_stop,
            fg_color="#dc3545",
            hover_color="#c82333",
            font=ctk.CTkFont(size=16, weight="bold"),
            state="disabled"
        )
        self.stop_button.pack(side="left", padx=10, fill="x", expand=True)
        
        # 状态区域
        status_frame = ctk.CTkFrame(main_frame)
        status_frame.pack(fill="x", padx=10, pady=10)
        
        self.status_label = ctk.CTkLabel(
            status_frame, 
            text="状态: 已停止",
            font=ctk.CTkFont(weight="bold")
        )
        self.status_label.pack(pady=10)
        
        # 系统信息
        system_info = ctk.CTkLabel(
            main_frame, 
            text=f"运行环境: {platform.system()} {platform.release()}",
            font=ctk.CTkFont(size=12)
        )
        system_info.pack(pady=(20, 0))
        
    def on_key_changed(self, choice):
        key_map = {
            "空格键": "space",
            "回车键": "enter",
            "Tab键": "tab",
            "Esc键": "esc",
            "左箭头": "left",
            "右箭头": "right",
            "上箭头": "up",
            "下箭头": "down"
        }
        self.key_presser.set_key(key_map.get(choice, "space"))
        
    def on_slider_changed(self, value):
        self.interval_var.set(value)
        self.interval_value_label.configure(text=f"{value:.1f}")
        self.precise_entry.delete(0, tk.END)
        self.precise_entry.insert(0, f"{value:.1f}")
        self.key_presser.set_interval(value)
        
    def on_apply_precise(self):
        try:
            value = float(self.precise_entry.get())
            if 0.1 <= value <= 5.0:
                self.interval_var.set(value)
                self.interval_slider.set(value)
                self.interval_value_label.configure(text=f"{value:.1f}")
                self.key_presser.set_interval(value)
            else:
                messagebox.showwarning("输入范围错误", "请输入0.1到5.0之间的数值")
        except ValueError:
            messagebox.showwarning("输入错误", "请输入有效的数字")
            
    def on_start(self):
        if self.key_presser.start():
            self.start_button.configure(state="disabled")
            self.stop_button.configure(state="normal")
            self.status_label.configure(text="状态: 运行中")
            
    def on_stop(self):
        if self.key_presser.stop():
            self.start_button.configure(state="normal")
            self.stop_button.configure(state="disabled")
            self.status_label.configure(text="状态: 已停止")
            
    def update_status(self):
        if self.key_presser.running:
            key_name_map = {
                "space": "空格键",
                "enter": "回车键",
                "tab": "Tab键",
                "esc": "Esc键",
                "left": "左箭头",
                "right": "右箭头",
                "up": "上箭头", 
                "down": "下箭头"
            }
            key_display = key_name_map.get(self.key_presser.key, self.key_presser.key)
            self.status_label.configure(
                text=f"状态: 运行中 - 每{self.key_presser.interval:.1f}秒按下{key_display}"
            )
        self.after(1000, self.update_status)
        
    def on_closing(self):
        if self.key_presser.running:
            if messagebox.askyesno("确认", "程序正在运行中，确定要退出吗?"):
                self.key_presser.stop()
                self.destroy()
        else:
            self.destroy()


def main():
    try:
        app = AutoKeyApp()
        app.mainloop()
    except Exception as e:
        error_msg = str(e)
        print(f"程序发生错误: {error_msg}")
        # 在tkinter界面显示错误
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("错误", f"程序发生错误:\n{error_msg}")
        sys.exit(1)

if __name__ == "__main__":
    main()
