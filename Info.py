import os,sys
Version="2.0"
LastDetectedTraffic='尚未開始偵測'

def resource_path(relative_path):
    """取得打包後的資源文件路徑"""
    if hasattr(sys, '_MEIPASS'):
        # PyInstaller 打包後的臨時目錄
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

def GetPath():
    if getattr(sys, 'frozen', False):
        # 如果程式是通過 PyInstaller 打包的
        return os.path.dirname(sys.executable)
    else:
        # 如果是在開發環境中執行
        return os.path.dirname(os.path.abspath(__file__))

def GetInternalPath():
    if getattr(sys, 'frozen', False):
        # 如果程式是通過 PyInstaller 打包的
        return os.path.join(os.path.dirname(sys.executable),"_internal")
    else:
        # 如果是在開發環境中執行
        return os.path.dirname(os.path.abspath(__file__))

def GetIconpath():
    # 返回圖示檔案的路徑
    return(resource_path("NcuNetLimiter.ico"))

def GetConfigspath():
    # 返回配置檔案的路徑
    return(resource_path("Configs.txt"))

def GetExeclsivepath():
    # 返回主程式執行檔案的路徑
    return os.path.join(GetPath(),"NcuNetLimiter.exe")

def GetHelperTxT():
    # 返回說明檔案的路徑
    return(resource_path("helper.txt"))