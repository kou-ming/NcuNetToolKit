import threading
import schedule
import time
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from tkinter import messagebox
import Info
import tkinter as tk

# 全局變數
YourIP = ''  # 用於存儲使用者的 IP 地址
stop_scanning = False  # 用於控制是否停止掃描
Traffic = '尚未開始偵測'  # 儲存最新的上傳流量數據

# 獲取最後一次檢測到的流量數據
def GetLastDetectedTraffic():
    return Traffic

# 獲取當前時間，格式為 HH:MM:SS
def GetTime():
    formatted_time = time.strftime("%H:%M:%S", time.localtime())
    return formatted_time

# 獲取網絡流量數據
def GetTraffic():
    # 打開目標網站
    driver.get("https://latias.cc.ncu.edu.tw/dormnet/index.php?section=netflow")
    print("a")

    # 等待 IP 輸入框出現並輸入 IP 地址
    FillIp = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/table/tbody/tr[2]/td/table/tbody/tr[1]/td[2]/form/table/tbody/tr/td/table/tbody/tr[3]/td/input[1]"))
    )
    FillIp.clear()  # 清除輸入框的內容
    FillIp.send_keys(YourIP)  # 填入使用者的 IP 地址

    # 點擊提交按鈕
    SendIp = driver.find_element(By.XPATH, "/html/body/table/tbody/tr[2]/td/table/tbody/tr[1]/td[2]/form/table/tbody/tr/td/table/tbody/tr[3]/td/input[2]")
    SendIp.click()
    print("b")

    # 獲取總上傳量數據
    TotoalUpload = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/table/tbody/tr[2]/td/table/tbody/tr[1]/td[2]/form/table/tbody/tr/td/table/tbody/tr[3]/td/table/tbody/tr[3]/td[2]"))
    )
    print("c")
    # 使用正則表達式提取數據中的流量值
    Traffic = re.findall(r'\d\.\d{1,2}', TotoalUpload.text)[0]
    return Traffic

# 運行爬蟲程式
def RunCrawl():
    global driver
    chrome_options = Options()
    chrome_options.add_argument("--headless=old")  # 設定瀏覽器為無頭模式
    chrome_options.add_argument("--disable-gpu")  # 禁用 GPU 加速
    driver = webdriver.Chrome(options=chrome_options)  # 啟動 Chrome 瀏覽器

    try:
        # 執行流量檢測
        global Traffic
        Traffic = GetTraffic()

        # 在文字框中顯示檢測結果
        Ins.config(state=tk.NORMAL)
        Ins.insert(End, f'上傳流量共%sGB   %s\n' % (Traffic, GetTime()))
        Ins.config(state=tk.DISABLED)

        # 如果流量超出設定值，顯示警告
        if float(Traffic) >= float(Max):
            messagebox.showerror(f"超出設定上傳流量%sGB" % Max, f'上傳流量共%sGB   %s' % (Traffic, GetTime()))
            Traffic = Traffic + 'GB'

        driver.quit()  # 關閉瀏覽器
    except Exception as e:
        messagebox.showerror("警告", str(e))  # 顯示錯誤訊息
        StopScanning()  # 停止掃描

# 定時執行爬蟲
def run_scheduler():
    scheduler = schedule.Scheduler()
    scheduler.every(10).minutes.do(RunCrawl)  # 每 10 分鐘執行一次爬蟲
    RunCrawl()  # 初次執行爬蟲
    while not stop_scanning:
        scheduler.run_pending()  # 執行所有已安排的任務
        time.sleep(30)  # 每隔 30 秒檢查一次任務，避免過高的 CPU 使用率

# 開始檢測流量
def StartDetect(TextBox, TextBoxEnd, MyIp, MaxTrafficValue, WindowState):
    global thread, YourIP, Ins, End, Max, stop_scanning, window, driver, Traffic
    Traffic = '尚未開始偵測'  # 初始化流量數據
    Ins = TextBox  # 訊息顯示框
    End = TextBoxEnd  # 插入點
    Max = MaxTrafficValue  # 流量限制值
    YourIP = MyIp  # 使用者的 IP 地址
    window = WindowState  # 窗口狀態

    # 顯示開始訊息
    Ins.config(state=tk.NORMAL)
    Ins.insert(End, "開始偵測 " + YourIP + "\n")
    Ins.config(state=tk.DISABLED)

    stop_scanning = False  # 重置停止標誌
    thread = threading.Thread(target=run_scheduler, daemon=True)  # 開啟新執行緒運行爬蟲
    thread.start()

# 停止檢測流量
def StopScanning():
    global stop_scanning
    stop_scanning = True  # 設定停止標誌
    thread.join()  # 等待執行緒結束

    # 顯示停止訊息
    Ins.config(state=tk.NORMAL)
    Ins.insert(End, "停止偵測\n")
    Ins.config(state=tk.DISABLED)