import subprocess

def get_MacAddr():
    # 使用powershell查詢網路卡資訊的指令
    command = "powershell -Command \"Get-NetAdapter\""

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
            line = file.readline()
            while line:
                # 利用兩個空格做分隔，因為可能會有"乙太網路"、"乙太網路 2"，所以不能只用一個空格
                info = line.split("  ")
                if(info[0] == '乙太網路'):
                    for inf in info:
                        # MacAddress再切時前面可能會有空格，因此把左側空格全清除
                        inf = inf.lstrip()
                        # 判斷是否何格式XX-XX-XX-XX-XX-XX
                        if len(inf) == 17 and inf[2] == '-' and inf[5] == '-' and inf[8] == '-' and inf[11] == '-' and inf[14] == '-':
                            # print("你的Mac Address為：")
                            # print(inf)
                            macaddr = ''.join(inf.split('-')) # 將"-"都去除，方便資料填寫
                            # print(macaddr)
                line = file.readline()
        # 將其記錄丟回NetInfo.txt
        with open(output_file_path, "w", encoding="utf-8") as file:
            file.write(macaddr)
        return macaddr
    except Exception as e:
        print(f"An error occurred: {e}")
