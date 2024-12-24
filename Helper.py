import get_macaddr
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from threading import Thread
import queue
import time
from PIL import Image, ImageTk
import os
import Info

text_dict = {}  # 用來存儲文字訊息的字典
img_dict = {}  # 用來存儲圖片路徑的字典
btn_dict = {}  # 用來存儲按鈕文字的字典
Macaddr = ''  # 存儲 Mac 地址
exit_button_list = []  # 存儲現有按鈕的list

# 讀取文件，將內容存成字典
def create_dict():
    # 取得helper檔案的路徑
    helper_file_path = Info.GetHelperTxT()
    with open(helper_file_path, "r", encoding="utf-8") as file:
        for line in file.read().split('}}'):    
            token_list = line.strip().split('}')
            if len(token_list) < 4:
                break
            text_dict[token_list[0]] = token_list[1]  # 文字內容
            img_dict[token_list[0]] = token_list[2].split(',')  # 圖片路徑
            btn_dict[token_list[0]] = token_list[3].split(',')  # 按鈕文字

# 發送消息，根據cmd執行相應操作
def send_message(cmd):
    print(cmd)
    # 如果cmd送過來是"自己電腦"則需要額外處理
    if cmd == "自己電腦":
        global Macaddr
        if Macaddr == '':
            Macaddr = get_macaddr.get_MacAddr()  # 取得 Mac 地址
        messagebox.showinfo("MacAddress", "你的 Mac Address 為: " + Macaddr)
        add_message(text_dict["使用注意事項"], img_dict["使用注意事項"], btn_dict["使用注意事項"])
    else:
        add_message(text_dict[cmd], img_dict[cmd], btn_dict[cmd])

# 滑鼠滾輪滾動設定
def _on_mouse_wheel(event):
    global chat_canvas
    chat_canvas.yview_scroll(-1 * int(event.delta / 120), "units")  # 滾動速度調整為 120 單位

# 計算文字輸出框需要的高度
def count_line(text, letter_num):
    text_line = (text.count("\n") + 1)  # 計算換行符號的數量
    count = 0
    # 計算每超過幾個字就要加換行
    for tx in text:
        if tx == "\n":
            count = 0
            continue
        count += 1
        if count == letter_num:
            text_line += 1
            count = 0
    return text_line

# 添加訊息到輸出框
def add_message(text, image_list=None, btn_list=None):
    global chat_frame

    # 禁用之前的按鈕
    global exit_button_list
    for butn in exit_button_list:
        butn['state'] = tk.DISABLED  # 禁用按鈕
    exit_button_list.clear()

    frame = tk.Frame(chat_frame, bg="#F7F7F7", padx=5, pady=5, relief="raised", borderwidth=1)

    # 顯示文字訊息
    text_line = count_line(text, 25)  # 計算所需高度
    msg_text = tk.Text(frame, height=text_line, width=8, wrap="word", font=("Arial", 12), bg="#CAFFFF", fg="#333333", relief="flat", padx=10, pady=10)
    msg_text.insert("1.0", text)
    msg_text.config(state="disabled")  # 禁止編輯
    msg_text.pack(fill="x", pady=5)

    # 顯示圖片
    for image_path in image_list:  
        if image_path != "None":
            script_dir = os.path.dirname(__file__)
            image_path = os.path.join(script_dir, image_path)
            img = Image.open(image_path)
            img.thumbnail((350, 350))  # 縮放圖片
            img = ImageTk.PhotoImage(img)
            img_label = tk.Label(frame, image=img, bg="#F7F7F7")
            img_label.image = img  # 保持對圖片的引用
            img_label.pack(side='top', anchor='w', padx=5, pady=5)

    # 添加按鈕
    for button_text in btn_list:
        if button_text != "None":
            button = tk.Button(
                frame, 
                text=button_text, 
                command=lambda btn_text=button_text: send_message(btn_text),
                bg="#000093", 
                fg="white", 
                font=("Arial", 10), 
                relief="flat", 
                activebackground="#000079",
                padx=5, 
                pady=3
            )
            button.pack(side='left', anchor='w', padx=5, pady=5)
            # 加進紀錄現在有什麼button的list裡
            exit_button_list.append(button)

    frame.pack(fill='x', padx=5, pady=5)  # 將框架添加到聊天區塊
    global chat_canvas
    chat_canvas.update_idletasks()
    chat_canvas.yview_moveto(1)  # 自動向下滾動到最新消息

# 創建新視窗
def Create_new_window(main_window):
    window = tk.Toplevel(main_window)
    window.title("宿網解惑小幫手")
    window.geometry("500x600")

    # 設置聊天框，可以顯示資訊
    global chat_canvas
    chat_canvas = tk.Canvas(window, height=600, width=500)
    global chat_frame
    chat_frame = tk.Frame(chat_canvas)
    scrollbar = ttk.Scrollbar(window, orient="vertical", command=chat_canvas.yview)
    chat_canvas.configure(yscrollcommand=scrollbar.set)

    scrollbar.pack(side='right', fill='y')
    chat_canvas.pack(fill='both', expand=True)
    chat_canvas.place(relx=0.6, y=0, anchor='n')
    chat_canvas.create_window((0, 0), window=chat_frame, anchor='nw')
    
    # 滑鼠滾輪綁定事件
    chat_canvas.bind("<MouseWheel>", _on_mouse_wheel)  # Windows 和 Linux
    chat_canvas.bind("<Button-4>", lambda e: chat_canvas.yview_scroll(-1, "units"))  # macOS 向上
    chat_canvas.bind("<Button-5>", lambda e: chat_canvas.yview_scroll(1, "units"))  # macOS 向下

    chat_frame.bind("<Configure>", lambda e: chat_canvas.configure(scrollregion=chat_canvas.bbox("all")))
    chat_canvas.configure(scrollregion=(0, 0, 400, 350))  # 設置固定大小為 400x350

    create_dict()  # 初始化字典
    global exit_button_list
    exit_button_list.clear()
    send_message('返回選單')  # 預設顯示返回選單

    return window