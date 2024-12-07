from tkinter import filedialog, messagebox
import winreg
import os
 
# 取得當前使用者的啟動項註冊表路徑
startup_reg_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
startup_reg_key = winreg.HKEY_CURRENT_USER

def add_startup_item(file_path):
    try:
        filename = os.path.basename(file_path)
        key = winreg.OpenKey(startup_reg_key, startup_reg_path, 0, winreg.KEY_WRITE)
        winreg.SetValueEx(key, filename, 0, winreg.REG_SZ, file_path)
        winreg.CloseKey(key)
        messagebox.showinfo("添加啟動項", f"已成功添加啟動項: {filename}")
    except Exception as e:
        messagebox.showerror("添加啟動項", f"添加啟動項失敗: {str(e)}")
 
def remove_startup_item(item_name):
    try:
        key = winreg.OpenKey(startup_reg_key, startup_reg_path, 0, winreg.KEY_WRITE)
        winreg.DeleteValue(key, item_name)
        winreg.CloseKey(key)
        messagebox.showinfo("删除啟動項", f"已成功刪除啟動項: {item_name}")
    except FileNotFoundError:
        messagebox.showwarning("删除啟動項", f"啟動項 '{item_name}' 不存在")
    except Exception as e:
        messagebox.showerror("删除啟動項失敗", f"删除啟動項時失敗: {str(e)}")