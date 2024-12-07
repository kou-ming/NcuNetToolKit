import subprocess

def get_MacAddr():
    # 利用ps指令查詢網路卡資料
    command = "powershell -Command \"Get-NetAdapter | Format-List\""

    try:
        # 使用subporcess.run跑這項指令，取得網路卡資訊
        cmd_result = subprocess.run(command, capture_output=True, text=True, shell=True)

        # 將網路卡資訊寫入NetInfo.txt，作為暫時記錄
        output_file_path = "NetInfo.txt"
        with open(output_file_path, "w", encoding="utf-8") as file:
            file.write(cmd_result.stdout)
        
        # 取得這台電腦的Mac Address
        macaddr = ''
        with open(output_file_path, "r", encoding="utf-8") as file:
            # line = file.readline()
            data_list = file.read().split("\n\n")
            for data in data_list:
                info_list = data.split('\n')
                if(info_list[0][29:] == "乙太網路"):
                    print(info_list[3][29:])
                    macaddr = ''.join(info_list[3][29:].split('-'))
        with open(output_file_path, "w", encoding="utf-8") as file:
            file.write(macaddr)
        return macaddr
    except Exception as e:
        print(f"An error occurred: {e}")
    return "Cannot find Mac Address"
