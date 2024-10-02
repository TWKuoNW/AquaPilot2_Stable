# 測試用，未來會刪掉
import socket
import threading
import time
import re

class Connector(): # 建立一個連接器的class
    def __init__(self, host, port):  # 初始化Thread的設定，接收兩個參數(ip, port)
        super().__init__()
        self.host = host 
        self.port = port 
        # 創建一個socket物件，其中 socket.AF_INET 代表使用 IPv4 地址族；SOCK_STREAM 則代表使用 TCP 傳輸，若想使用 UDP 則宣告成 SOCK_DGRAM。
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.settimeout(3) # 判定十秒為超時連線
        self.client_socket.setblocking(1)
        self.client_socket.connect((host, port)) # 連接伺服器
       
        # 初始化水質參數
        self.air_temp = 0.0 
        self.air_hum = 0.0 
        self.water_temp = 0.0
        self.water_DO = 0.0
        self.water_pH = 0.0

        threading.Thread(target = self.listener, daemon = True).start()


    def transmitter(self, msg): # 執行續啟動後會啟動該function
        self.client_socket.send(str(msg).encode('utf-8'))
    
    def listener(self): # 監聽器
        try:
            while(True):
                msg = self.client_socket.recv(1024).decode('utf-8') # 接收客戶端發來的訊息
                
                if(self.is_valid_format(msg)):
                    msg_list = [str(i) for i in msg.split()]
                    if(msg_list[0] == "01"):
                        if(msg_list[1] == "00"):
                            self.water_temp = float(msg_list[2])
                        if(msg_list[1] == "01"):
                            self.water_DO = float(msg_list[2])
                    elif(msg_list[1] == 1):
                        pass
                    elif(msg_list[2] == 2):
                        pass
                elif(msg != ""):
                    print("收到:", msg)
                
                time.sleep(1)
        except Exception as e:
            print(f"接收區 發生錯誤:{e}")
            print("關閉客戶端連線")
            self.client_socket.close()
            print("連線結束")

    def getAirTemp(self):
        return self.air_temp
    
    def getAirHum(self):
        return self.air_hum
    
    def getWaterTemp(self):
        return self.water_temp
    
    def getWaterDO(self):   
        return self.water_DO
    
    def getWaterPH(self):    
        return self.water_pH
    
    def is_valid_format(self, check_string):
        pattern = r'^(\b\d+(\.\d+)?\b\s*)+$'
        return re.match(pattern, check_string) is not None


# 使用示例
if __name__ == "__main__":
    host = "100.81.241.109"
    port = 9999
    connector = Connector(host, port)
    
    while(True):
        msg = input("請輸入要傳送的訊息: ")
        if(msg == "EXIT"):
            break
        connector.transmitter(msg)
        
    
    print("Done.")
    
