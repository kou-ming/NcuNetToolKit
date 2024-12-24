import tkinter as tk
from pystray import Icon, MenuItem, Menu
from PIL import Image, ImageDraw
import threading
import sys
import Info, Crwal

# 顯示窗口
def show_window():
    print("P")
    global ico, win
    ico.stop()  # 停止系統托盤圖標
    win.deiconify()  # 恢復 Tkinter 窗口
    print("i")

# 最小化到托盤
def minimize_to_tray(window, SaveQuit):
    print("p")
    global win
    win = window
    win.withdraw()  # 隱藏窗口
    # Notify.notify("通知", "正在後台運作")
    threading.Thread(target=show_tray_icon).start()  # 開啟一個線程來顯示托盤圖標

# 顯示托盤圖標
def show_tray_icon():
    global win, ico
    icon = Icon(
        "test_icon",
        Image.open(Info.GetIconpath()),  # 設置托盤圖標
        f"當前上傳量:%s" % Crwal.GetLastDetectedTraffic(),  # 顯示托盤提示文字
        menu=Menu(
            MenuItem(text="show window", action=show_window, default=True)  # 設置菜單項目
        )
    )
    ico = icon
    icon.run()  # 啟動托盤圖標

# 退出程式
def quit_app(icon=None, item=None):
    if icon:
        icon.stop()  # 停止托盤圖標
    # 停止 Tkinter 主循環
    sys.exit()