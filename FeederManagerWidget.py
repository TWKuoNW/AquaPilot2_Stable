from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from FeederManager_UI.FeederManagerUI import Ui_Form

from SITD_demo.full import AI_Fun as AI_Fun_Full
from SITD_demo.hungry import AI_Fun as AI_Fun_Hungry

from datetime import datetime

import sys
import threading
import time

class Form(QWidget):
    def __init__(self, af_ser):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.setWindowTitle("餵食器管理器")

        self.ui.btnSubmit.clicked.connect(self.on_btnSubmit_clicked)

        self.status = QTimer() # 建立一個timer
        self.status.timeout.connect(self.show_status) # 連接函數
        self.status.start(1000) # 啟動連接的函數，每X毫秒一次

        self.timer = QTimer() 
        self.timer.timeout.connect(self.fun_timer) # 連接函數

        self.init_timer_num = 30
        self.timer_num = self.init_timer_num
        self.amount = 1
        self.ai_fun = None
        self.af_ser = af_ser
        self.isHungry = True
        
    def ai_function_full(self):
        self.amount = 1
        self.ai_fun = AI_Fun_Full()
    
    def ai_function_hungry(self):
        self.amount = 2
        self.ai_fun = AI_Fun_Hungry()
        
    def show_status(self):
        formatted_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.ui.labCurrentTime.setText(str(formatted_time)) 
        self.ui.labTimer.setText(f"00時00分{self.timer_num:02}秒")
        self.ui.labAmount.setText(f"{self.amount:02}圈")
        
        if(self.ai_fun != None):
            self.red_point_length = self.ai_fun.red_point_length
            self.yellow_point_length = self.ai_fun.yellow_point_length
            self.two_point_length = self.ai_fun.two_point_length
            self.two_point_distance = self.ai_fun.two_point_distance

            info = f"{self.red_point_length}\t{self.yellow_point_length}\t{self.two_point_length}"

            if(self.two_point_distance > 12):
                info = f"{info}\t提示：檢測到投餵量不足"
            else:
                info = f"{info}\t提示：蝦腸飽滿投餵足夠"
            
            self.ui.pteStatus.appendPlainText(info) 

    def fun_timer(self):
        if(self.timer_num > 0):
            self.timer_num = self.timer_num - 1
        elif(self.timer_num == 0):
            if(self.amount == 1):
                self.af_ser.write(b'1')
            elif(self.amount == 2):
                threading.Thread(target=self.two_times_spin, daemon = True).start() # 啟動 AI function
            self.ui.pteStatus.appendPlainText("提示:自動餵食器啟動") 
            self.timer_num = self.init_timer_num
            if(self.ui.cbAIFunctionStart.isChecked()):
                if(self.isHungry):
                    self.isHungry = False
                    threading.Thread(target=self.ai_function_hungry, daemon = True).start() # 啟動 AI function
                else:
                    self.isHungry = True
                    threading.Thread(target=self.ai_function_full, daemon = True).start() # 啟動 AI function

    def on_btnSubmit_clicked(self):
        if(self.ui.cbAutoFeederStart.isChecked()):
            self.timer.start(1000)
            if(self.ui.cbAIFunctionStart.isChecked()):
                threading.Thread(target=self.ai_function_full, daemon = True).start() # 啟動 AI function
        else:
            self.timer.stop()
            self.timer_num = self.init_timer_num

    def two_times_spin(self):
        self.af_ser.write(b'1')
        time.sleep(8)
        self.af_ser.write(b'1')
        

if __name__ == "__main__":
    import serial

    app = QApplication(sys.argv)
    af_ser = serial.Serial(port='COM8', baudrate=9600, timeout=1) 
    form = Form(af_ser)
    form.show()
    sys.exit(app.exec_())

