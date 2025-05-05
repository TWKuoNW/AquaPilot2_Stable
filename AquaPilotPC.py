from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QTimer, Slot
from PySide6.QtGui import QImage, QPixmap, QIcon
from PySide6 import QtCore

from Connector import Connector
from AquaPilotPC_UI.AquaPilotUI_V2_t1 import Ui_AquaPlayer
from SensorDataPlotWidget import Form as sensorDataPlot
from DeviceManagerWidget import Form as DeviceManagerWidget
from ProbioticManagerWidget import Form as ProbioticManagerWidget
from FeederManagerWidget import Form as FeederManagerWidget
from VideoThread import VideoThread

import cv2
import threading
import serial

class QMainWindow(QMainWindow): # 覆寫QMainWindow
    def __init__(self):
        super().__init__() # 呼叫父類別的建構函式
        self.setWindowIcon(QIcon('img\\Logo3_fix.png')) # 設定視窗icon
    
    @Slot()
    def closeEvent(self, event):  # 關閉視窗事件
        print("關閉AquaPilot")    # 顯示關閉事件
        QApplication.instance().quit() # 關閉視窗
    

class MyApp():
    def __init__(self):
        self.app = QApplication([]) # 創建應用程式
        self.window = QMainWindow() # 創建視窗
        self.ui = Ui_AquaPlayer()   # 創建UI
        self.ui.setupUi(self.window) # 設定UI
        # ------------------------------------- #
        #          是否開啟debug模式             #
        # ------------------------------------- #
        self.debug = False 

        self.ui.txtName.setText("養殖場 01")
        self.ui.txtIP.setText("192.168.51.120")

        self.connector = None # 初始化connector為None

        # 影像變數
        self.isCapturingVideo0 = False # 初始化isCapturing為False
        self.isCapturingVideo1 = False # 初始化isCapturing為False
        self.isCapturingVideo2 = False # 初始化isCapturing為False
        self.cap0 = None # 初始化cap0為None
        self.cap1 = None # 初始化cap1為None
        self.cap2 = None # 初始化cap1為None
        
        # 連接button與函數
        self.ui.btnStrVideo0.clicked.connect(self.on_video0_button_clicked) 
        self.ui.btnStrVideo1.clicked.connect(self.on_video1_button_clicked) 
        self.ui.btnConn.clicked.connect(self.on_connMod_button_clicked) 
        self.ui.btnClear.clicked.connect(self.on_btnClear_button_clicked)
        self.ui.btnSend.clicked.connect(self.on_btnSend_button_clicked)

        # 連接功能列的button
        self.ui.sensorFunPushButton.clicked.connect(self.on_sensor_button_clicked)
        self.ui.probioticFunPushButton.clicked.connect(self.on_probiotic_button_clicked)
        self.ui.feederFunPushButton.clicked.connect(self.on_feeder_button_clicked)
        self.ui.deviceFunPushButton.clicked.connect(self.on_device_button_clicked)
        self.ui.mapFunPushButton.clicked.connect(self.on_map_button_clicked)
        
        self.ui.btnAutoFeeder.clicked.connect(self.on_btnAutoFeeder_clicked)
        self.ui.btnProbioticSprayer.clicked.connect(self.on_btnAutoFeeder_clicked)

        self.ui.btnVideo2TurnRight.clicked.connect(self.on_btnVideo2TurnRight_button_clicked)
        self.ui.btnVideo2TurnLeft.clicked.connect(self.on_btnVideo2TurnLeft_button_clicked)

        # 初始化video0
        self.video0 = QTimer()
        self.video0.timeout.connect(self.updateFrame0)
        
        # 初始化video1
        self.video1 = QTimer()
        self.video1.timeout.connect(self.updateFrame1)
       
        # 初始化感測器讀取
        self.update_sensorvalue = QTimer()
        self.update_sensorvalue.timeout.connect(self.updateSensorValue)
        
        # open com
        if(not self.debug):
            print("open com...")
            self.af_ser = serial.Serial(port='COM4', baudrate=9600, timeout=1) 
            print("comport is opened.")

        self.ui.pteComm.setPlainText("-------------------命令視窗-------------------")
    
    def run(self): # 執行應用程式，於程式啟動時執行
        self.window.show()
        self.app.exec_()

    def on_connMod_button_clicked(self): # 連接模式
        self.ui.pteComm.appendPlainText("連接養殖場伺服器...")
        port = 9999
        name = self.ui.txtName.text()
        ip = self.ui.txtIP.text()
        try:
            self.connector = Connector(ip, port)
            self.ui.labStatus.setText("已連接")
            self.ui.pteComm.appendPlainText("成功連接伺服器")            
            self.ui.labName.setText(str(name))
            self.ui.labIP.setText(str(ip))
            video0_url = 'http://' + str(ip) + ':8000/video'
            video1_url = 'http://' + str(ip) + ':8001/video'
            self.cap0 = cv2.VideoCapture(video0_url)
            self.cap1 = cv2.VideoCapture(video1_url)
            self.update_sensorvalue.start(1000) # 啟動updateSensorValue，並每秒更新一次感測器數值
        except ConnectionRefusedError:
            self.ui.pteComm.appendPlainText("無法連線，因為目標電腦拒絕連線")
        except OSError:
            self.ui.pteComm.appendPlainText("內容中所要求的位址不正確。")
        except Exception as e:
            self.ui.pteComm.appendPlainText(f"發生異常: {e}")

    def updateSensorValue(self): # 更新感測器數值
        air_temp = self.connector.getAirTemp()
        air_hum = self.connector.getAirHum()
        water_temp = self.connector.getWaterTemp()
        water_DO = self.connector.getWaterDO()
        water_pH = self.connector.getWaterPH()
        
        self.ui.labTempValue.setText(str(air_temp)) 
        self.ui.labHumValue.setText(str(air_hum))
        self.ui.labORPValue.setText(str(water_temp))
        self.ui.labDOValue.setText(str(water_DO))
        self.ui.labPHValue.setText(str(water_pH))

    def updateFrame0(self): # 更新相機畫面
        ret, frame = self.cap0.read()  
        
        if ret:
            rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgbImage.shape # 高、寬、通道數
            bytesPerLine = ch * w # 每行的字節數
            convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888) # 轉換成QImage格式
            quality = self.ui.cbxQuality.currentText() # 取得解析度

            if(quality == "1920*1080"):
                w = 1920
                h = 1080
            elif(quality == "1280*1024"):
                w = 1152
                h = 922
            elif(quality == "640*480"):
                w = 640
                h = 480
            elif(quality == "320*240"):
                w = 320
                h = 240
            
            p = convertToQtFormat.scaled(w, h, QtCore.Qt.KeepAspectRatio) # 保持長寬比
            self.ui.labVideo0.setPixmap(QPixmap.fromImage(p)) # 顯示畫面

    def updateFrame1(self): # 更新相機畫面
        ret, frame = self.cap1.read()  
        if ret:
            rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgbImage.shape # 高、寬、通道數
            bytesPerLine = ch * w # 每行的字節數
            convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888) # 轉換成QImage格式
            
            p = convertToQtFormat.scaled(320, 240, aspectRatioMode=QtCore.Qt.KeepAspectRatio) # 保持長寬比
            self.ui.labVideo1.setPixmap(QPixmap.fromImage(p)) # 顯示畫面

    def on_video0_button_clicked(self): # 開啟/關閉相機
        if(self.cap0 != None):
            if(self.isCapturingVideo0):
                self.video0.stop()
                self.isCapturingVideo0 = False
                self.ui.labVideo0.setText("video0")
                self.ui.btnStrVideo0.setText("開始")
                self.ui.pteComm.appendPlainText("Video0相機 關閉")
            else:
                self.video0.start(20)
                self.isCapturingVideo0 = True
                self.ui.btnStrVideo0.setText("關閉")
                self.ui.pteComm.appendPlainText("Video0相機 開啟")
                
                quality = self.ui.cbxQuality.currentText()
                
                if(quality == "1920*1080"):
                    self.ui.pteComm.appendPlainText("相機解析度設定1920*1080")
                elif(quality == "1280*1024"):
                    self.ui.pteComm.appendPlainText("相機解析度設定1280*1024")
                elif(quality == "640*480"):
                    self.ui.pteComm.appendPlainText("相機解析度設定640*480")
                elif(quality == "320*240"):
                    self.ui.pteComm.appendPlainText("相機解析度設定320*240")
            
    def on_video1_button_clicked(self): # 開啟/關閉相機
        if(not self.cap1 == None):
            if self.isCapturingVideo1:
                self.video1.stop()
                self.isCapturingVideo1 = False
                self.ui.labVideo1.setText("video1")
                self.ui.btnStrVideo1.setText("開始")
                self.ui.pteComm.appendPlainText("Video1相機 關閉")
            else:
                self.video1.start(20)
                self.isCapturingVideo1 = True
                self.ui.btnStrVideo1.setText("關閉")
                self.ui.pteComm.appendPlainText("Video1相機 開啟")
    
    def send_autoFeeder_command_to_connector(self, command): # 向Connector發送自動餵食器命令
        if(command == 0):
            self.connector.transmitter("02 00 00 00")
        elif(command == 1):
            self.connector.transmitter("02 01 00 00")

    def on_btnAutoFeeder_clicked(self):
        try:
            if(self.af_ser.is_open):
                self.af_ser.write(b'1')
            threading.Thread(target=self.send_autoFeeder_command_to_connector, daemon = True, args=(1,)).start()    
            self.ui.pteComm.appendPlainText("啟動自動餵食器")
        except AttributeError:
            self.ui.pteComm.appendPlainText("尚未開啟連線")


    def send_probioticSprayer_command_to_connector(self, command): # 向Connector發送益生菌噴灑器命令
        if(command == 0):
            self.connector.transmitter("03 00 00 00")
        elif(command == 1):
            self.connector.transmitter("03 01 00 00")

    def on_btnProbioticSprayer_clicked(self):
        try:
            self.ui.pteComm.appendPlainText("啟動益生菌噴灑器")
            threading.Thread(target=self.send_probioticSprayer_command_to_connector, daemon = True, args=(1,)).start()
        except AttributeError:
            self.ui.pteComm.appendPlainText("尚未開啟連線")
    
    def on_btnSend_button_clicked(self): # 發送命令
        self.connector.transmitter(self.ui.lineEditSend.text())
        printSendCommand = "向伺服器發送->" + self.ui.lineEditSend.text()
        self.ui.pteComm.appendPlainText(printSendCommand)        
        self.ui.lineEditSend.clear()

    def on_btnClear_button_clicked(self): # 清除命令視窗
        self.ui.pteComm.clear()

    def on_sensor_button_clicked(self):
        self.sensorDataPlot = sensorDataPlot()
        self.sensorDataPlot.show()
    
    def on_probiotic_button_clicked(self):
        self.ProbioticManagerWidget = ProbioticManagerWidget()
        self.ProbioticManagerWidget.show()
        print("probioticWidget")

    def on_feeder_button_clicked(self):
        self.FeederManagerWidget = FeederManagerWidget(self.af_ser)
        self.FeederManagerWidget.show()
        print("feederWidget")

    def on_device_button_clicked(self):
        self.DeviceManagerWidget = DeviceManagerWidget()
        self.DeviceManagerWidget.show()
        print("diveceWidget")

    def on_map_button_clicked(self):
        print("mapWidget")

    def on_btnVideo2TurnRight_button_clicked(self): # 當按下R
        self.connector.transmitter("04 00 10") # 向養殖端主機發送
        # print("04 00 10")
        
    def on_btnVideo2TurnLeft_button_clicked(self): # 當按下L
        self.connector.transmitter("04 01 10")
        # print("04 01 10")
        

if __name__ == "__main__":
    my_app = MyApp()
    my_app.run()