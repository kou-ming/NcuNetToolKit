import tkinter as tk
from tkinter import messagebox
import Crwal
import webbrowser
import re
import AutoStart
import os, sys
import Iconify, Info
import Helper

Scanning = False  # 全域變數，判斷是否正在掃描

# 儲存並退出程式
def SaveQuit():
    UpdateConfig()  # 更新設定檔
    window.destroy()  # 關閉主視窗

# 驗證使用者輸入值的正確性
def SettingsValueCheck():
    # 檢查流量閾值是否為數字
    if not re.match(r'\d+', TrafficMaxValue.get().strip()):
        messagebox.showerror("錯誤", "請輸入數字")
        return False
    # 檢查 IP 格式是否正確
    elif not re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', YourIp.get().strip()):
        messagebox.showerror("錯誤", "請輸入正確IP位置格式")
        return False
    return True

# 更新設定檔案內容，將 IP、自動啟動、最小化選項及流量閾值儲存到 `Configs.txt`
def UpdateConfig():
    Configs = open(Info.GetConfigspath(), "w")
    Configs.write(YourIp.get().strip() + '\n' + str(IsAutoStart.get()) + '\n' +
                  str(MinimizeWhenScanning.get()) + '\n' + TrafficMaxValue.get().strip())
    Configs.close()

# 停止掃描
def StopScanning():
    global Scanning
    Scanning = False
    Crwal.StopScanning()  # 停止後端的掃描程式
    # 重設按鈕狀態
    StopScanButton['state'] = tk.DISABLED
    ScanButton['state'] = tk.ACTIVE
    YourIp['state'] = tk.NORMAL
    TrafficMaxValue['state'] = tk.NORMAL
    HelperButton['state'] = tk.NORMAL

# 開始檢測流量
def StartScanning():
    global Scanning
    if SettingsValueCheck():  # 確認輸入的設定是否正確
        Scanning = True

        # 如果勾選了最小化到托盤
        if MinimizeWhenScanning.get():
            Iconify.minimize_to_tray(window, SaveQuit)
        UpdateConfig()  # 儲存最新的設定
        # 鎖定相關輸入框與按鈕
        YourIp['state'] = tk.DISABLED
        TrafficMaxValue['state'] = tk.DISABLED
        StopScanButton['state'] = tk.ACTIVE
        ScanButton['state'] = tk.DISABLED
        HelperButton['state'] = tk.DISABLED
        # 啟動流量檢測
        Crwal.StartDetect(Log, '1.0', YourIp.get(), TrafficMaxValue.get(), window.wm_state)
    else:
        Scanning = False
        window.deiconify()  # 如果有錯誤，恢復視窗
        messagebox.showerror("無法啟動自動掃描", "設定參數有誤")

# 當視窗最小化時的回呼函數
def IconifyCallBack(event):
    if MinimizeWhenScanning.get() and Scanning and window.state() == 'iconic':
        Iconify.minimize_to_tray(window, SaveQuit)

# 當視窗恢復時的回呼函數
def DeIconifyCallBack(event):
    pass

# 開機自動掃描的選項
def AutoStartCheck():
    UpdateConfig()  # 更新設定檔
    if IsAutoStart.get():
        AutoStart.add_startup_item(Info.GetExeclsivepath())  # 新增到開機自動執行
    else:
        AutoStart.remove_startup_item("NcuNetToolKit.exe")  # 從開機自動執行中移除

# 讀取之前的設定檔Configs.txt
def ReadConfigs():
    try:
        with open(Info.GetConfigspath(), 'r') as file:
            content = file.read().split()
            Ip = content[0]
            IsAutoStart.set(content[1])
            MinimizeWhenScanning.set(content[2])
            Limit = content[3]
            return Ip, Limit
    except:
        # 若無設定檔，初始化預設值
        with open(Info.GetConfigspath(), 'w') as file:
            file.write("111.111.111.111\n0\n0\n2.5")
            Ip = "111.111.111.111"
            IsAutoStart.set(0)
            MinimizeWhenScanning.set(0)
            Limit = "2.5"
            return Ip, Limit

# 打開「宿網小幫手」功能
def Open_helper():
    # 創建新視窗
    new_window = Helper.Create_new_window(window)
    ScanButton['state'] = tk.DISABLED  # 暫時禁用主視窗的掃描按鈕
    new_window.transient(window)
    new_window.grab_set()
    window.wait_window(new_window)  # 等待子視窗關閉
    ScanButton['state'] = tk.ACTIVE

# 主視窗初始化
window = tk.Tk()
window.title('NcuNetToolKit')
window.iconbitmap(Info.GetIconpath())
window.geometry('455x260')

# 設定選單欄
menubar = tk.Menu()
help_ = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label='Help', menu=help_)
help_.add_command(label='版本號:%s' % Info.Version)
window.config(menu=menubar)

# 設定框架
Setting = tk.LabelFrame(window, text='設定')
label = tk.Label(Setting, text="輸入你的IP")
YourIp = tk.Entry(Setting, width=15)
Log = tk.Text(window, height=15, width=30, state=tk.DISABLED)
ScanButton = tk.Button(window, text="開始偵測", command=StartScanning)
StopScanButton = tk.Button(window, text="停止偵測", command=StopScanning)
label2 = tk.Label(Setting, text="報警閥值(GB)")

# 小幫手按鈕
HelperButton = tk.Button(window, text="宿網小幫手", command=Open_helper)

# 設定變數
IsAutoStart = tk.IntVar()  # 開機自動掃描
MinimizeWhenScanning = tk.IntVar()  # 最小化到托盤

# 讀取先前設定
Ip, Limit = ReadConfigs()

# 綁定選項
AutoStartScanButton = tk.Checkbutton(Setting, text='開機自動掃描', command=AutoStartCheck, variable=IsAutoStart)
MinimizeWhenScanningButton = tk.Checkbutton(Setting, text='掃描時最小化到托盤', command=UpdateConfig, variable=MinimizeWhenScanning)

# 設定文字輸入框
TrafficMaxValue = tk.Entry(Setting, width=15)

# 按鈕狀態初始化
StopScanButton['state'] = tk.DISABLED
ScanButton['state'] = tk.ACTIVE

# 自動填入之前的設定
YourIp.insert(0, Ip)
TrafficMaxValue.insert(0, Limit)

# GUI布局
Log.grid(column=0, row=0, columnspan=2, rowspan=2, padx=10, pady=10)
Setting.grid(column=2, row=0)
label.grid(column=0, row=0, pady=10, padx=5)
YourIp.grid(column=1, row=0, pady=10, padx=5)
label2.grid(column=0, row=1, pady=10, padx=5)
TrafficMaxValue.grid(column=1, row=1, pady=10, padx=5)
AutoStartScanButton.grid(column=0, row=2, pady=5, columnspan=2)
MinimizeWhenScanningButton.grid(column=0, row=4, pady=5, columnspan=2)
ScanButton.grid(column=1, row=2)
StopScanButton.grid(column=0, row=2)
HelperButton.grid(column=2, row=2)

# 自動開始掃描
if IsAutoStart.get():
    StartScanning()
window.bind("<Unmap>", IconifyCallBack)
window.bind("<Map>", DeIconifyCallBack)
window.resizable(False, False)
window.mainloop()