from PySide6.QtCore import QThread, Signal
from PySide6.QtGui import QImage
import cv2

class VideoThread(QThread):
    change_pixmap_signal = Signal(QImage)  # 定義影像更新 signal

    def __init__(self, video_url):
        super().__init__()
        self.video_url = video_url
        self._run_flag = True  # 控制開關
        self.cap = None

    def run(self):
        self.cap = cv2.VideoCapture(self.video_url)
        while self._run_flag:
            ret, frame = self.cap.read()
            if ret:
                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgb.shape
                bytes_per_line = ch * w
                qt_img = QImage(rgb.data, w, h, bytes_per_line, QImage.Format_RGB888)
                self.change_pixmap_signal.emit(qt_img)  # 傳送圖片

        self.cap.release()

    def stop(self):
        self._run_flag = False
        self.wait()

