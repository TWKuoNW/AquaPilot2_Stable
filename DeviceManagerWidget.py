from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from DeviceManager_UI.DeviceManagerUI import Ui_Form

import sys

class Form(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.setWindowTitle("設備管理器")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = Form()
    form.show()
    sys.exit(app.exec_())