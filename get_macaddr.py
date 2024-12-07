import subprocess

command = "powershell -Command \"Get-NetAdapter\""
try:
    # cmd_result = subprocess.run("ipconfig", capture_output=True, text=True, shell=True)
    cmd_result = subprocess.run(command, capture_output=True, text=True, shell=True)

    output_file_path = "NetInfo.txt"
    with open(output_file_path, "w", encoding="utf-8") as file:
        file.write(cmd_result.stdout)
    
    macaddr = ''
    with open(output_file_path, "r", encoding="utf-8") as file:
        line = file.readline()
        while line:
            info = line.split("  ")
            if(info[0] == '乙太網路'):
                for inf in info:
                    inf = inf.lstrip()
                    
                    if len(inf) == 17 and inf[2] == '-' and inf[5] == '-' and inf[8] == '-' and inf[11] == '-' and inf[14] == '-':
                        print("你的Mac Address為：")
                        print(inf)
                        macaddr = ''.join(inf.split('-'))
                        print(macaddr)
            line = file.readline()
    with open(output_file_path, "w", encoding="utf-8") as file:
        file.write(macaddr)
except Exception as e:
    print(f"An error occurred: {e}")
