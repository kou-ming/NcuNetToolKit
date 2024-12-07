import get_macaddr
import tkinter as tk
from tkinter import ttk
from threading import Thread
import queue
import time
from PIL import Image, ImageTk
import os

def _on_mouse_wheel(event):
    chat_canvas.yview_scroll(-1 * int(event.delta / 120), "units")  # 滾動速度調整為 120 單位

def add_message(text, image_path=None, button_text=None):
    frame = tk.Frame(chat_frame)

    # 顯示文字訊息
    msg_label = tk.Label(frame, text=text, wraplength=300, anchor='w')
    msg_label.pack(side='top', anchor='w', padx=5, pady=5)

    
    if image_path:
        image_path = os.path.join(image_path)
        img = Image.open(image_path)
        img.thumbnail((200, 200))
        img = ImageTk.PhotoImage(img)
        img_label = tk.Label(frame, image=img)
        img_label.image = img  # 保持對圖片的引用
        img_label.pack(side='top', anchor='w', padx=5, pady=5)

    # 如果有按鈕文字，則添加按鈕
    if button_text:
        button = tk.Button(frame, text=button_text, command=lambda: on_button_click(button_text))
        button.pack(side='top', anchor='w', padx=5, pady=5)

    frame.pack(fill='x', padx=5, pady=5)  # 將框架添加到聊天區塊
    chat_canvas.update_idletasks()
    chat_canvas.yview_moveto(1)  # 自動向下滾動到最新消息

def send_message():
    add_message("Hello, this is a chat message!", button_text="按鈕1")

def Create_new_window(main_window):
    window = tk.Toplevel(main_window)
    window.title("宿網解惑小幫手")
    window.geometry("500x600")

    global chat_canvas
    chat_canvas = tk.Canvas(window, height=350, width=400)
    global chat_frame
    chat_frame = tk.Frame(chat_canvas)
    scrollbar = ttk.Scrollbar(window, orient="vertical", command=chat_canvas.yview)
    chat_canvas.configure(yscrollcommand=scrollbar.set)

    scrollbar.pack(side='right', fill='y')
    chat_canvas.pack(side='left', fill='both', expand=False)
    chat_canvas.create_window((0, 0), window=chat_frame, anchor='nw')
    

    chat_canvas.bind("<MouseWheel>", _on_mouse_wheel)  # Windows 和 Linux
    chat_canvas.bind("<Button-4>", lambda e: chat_canvas.yview_scroll(-1, "units"))  # macOS 向上
    chat_canvas.bind("<Button-5>", lambda e: chat_canvas.yview_scroll(1, "units"))

    chat_frame.bind("<Configure>", lambda e: chat_canvas.configure(scrollregion=chat_canvas.bbox("all")))
    chat_canvas.configure(scrollregion=(0, 0, 400, 350))  # 固定大小為 400x350

    send_button = tk.Button(window, text="發送", command=lambda: add_message("test\ntest\n", "img/image.png"))
    send_button.pack(side='left', padx=5, pady=5)

    return window
