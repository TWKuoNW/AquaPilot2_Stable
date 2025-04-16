# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'FeederManagerUI.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *


class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(962, 582)
        self.verticalLayout_3 = QVBoxLayout(Form)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.labCurrentTime = QLabel(Form)
        self.labCurrentTime.setObjectName(u"labCurrentTime")
        font = QFont()
        font.setFamily(u"Arial")
        font.setPointSize(20)
        self.labCurrentTime.setFont(font)

        self.horizontalLayout.addWidget(self.labCurrentTime)


        self.verticalLayout_3.addLayout(self.horizontalLayout)

        self.line = QFrame(Form)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_3.addWidget(self.line)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.labAutoFeeder = QLabel(Form)
        self.labAutoFeeder.setObjectName(u"labAutoFeeder")
        self.labAutoFeeder.setMinimumSize(QSize(110, 30))

        self.horizontalLayout_2.addWidget(self.labAutoFeeder, 0, Qt.AlignHCenter)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_3)

        self.cbAutoFeederStart = QCheckBox(Form)
        self.cbAutoFeederStart.setObjectName(u"cbAutoFeederStart")

        self.horizontalLayout_2.addWidget(self.cbAutoFeederStart)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)

        self.horizontalLayout_2.setStretch(0, 1)
        self.horizontalLayout_2.setStretch(2, 1)
        self.horizontalLayout_2.setStretch(3, 5)

        self.verticalLayout_3.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.labAIFunction = QLabel(Form)
        self.labAIFunction.setObjectName(u"labAIFunction")
        self.labAIFunction.setMinimumSize(QSize(110, 30))

        self.horizontalLayout_4.addWidget(self.labAIFunction, 0, Qt.AlignHCenter)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_4)

        self.cbAIFunctionStart = QCheckBox(Form)
        self.cbAIFunctionStart.setObjectName(u"cbAIFunctionStart")

        self.horizontalLayout_4.addWidget(self.cbAIFunctionStart)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_5)

        self.btnSubmit = QPushButton(Form)
        self.btnSubmit.setObjectName(u"btnSubmit")

        self.horizontalLayout_4.addWidget(self.btnSubmit)

        self.horizontalLayout_4.setStretch(0, 1)
        self.horizontalLayout_4.setStretch(2, 1)
        self.horizontalLayout_4.setStretch(3, 4)
        self.horizontalLayout_4.setStretch(4, 1)

        self.verticalLayout_3.addLayout(self.horizontalLayout_4)

        self.line_2 = QFrame(Form)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.HLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_3.addWidget(self.line_2)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.label_4 = QLabel(Form)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setMinimumSize(QSize(110, 30))
        self.label_4.setLayoutDirection(Qt.LeftToRight)
        self.label_4.setAutoFillBackground(False)

        self.horizontalLayout_6.addWidget(self.label_4)

        self.labTimer = QLabel(Form)
        self.labTimer.setObjectName(u"labTimer")
        self.labTimer.setMinimumSize(QSize(110, 30))

        self.horizontalLayout_6.addWidget(self.labTimer)


        self.verticalLayout_4.addLayout(self.horizontalLayout_6)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.label_6 = QLabel(Form)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setMinimumSize(QSize(110, 30))

        self.horizontalLayout_7.addWidget(self.label_6)

        self.labAmount = QLabel(Form)
        self.labAmount.setObjectName(u"labAmount")
        self.labAmount.setMinimumSize(QSize(110, 30))

        self.horizontalLayout_7.addWidget(self.labAmount)


        self.verticalLayout_4.addLayout(self.horizontalLayout_7)


        self.horizontalLayout_5.addLayout(self.verticalLayout_4)

        self.pteStatus = QPlainTextEdit(Form)
        self.pteStatus.setObjectName(u"pteStatus")

        self.horizontalLayout_5.addWidget(self.pteStatus)


        self.verticalLayout_3.addLayout(self.horizontalLayout_5)

        self.verticalLayout_3.setStretch(0, 1)
        self.verticalLayout_3.setStretch(2, 1)
        self.verticalLayout_3.setStretch(3, 1)
        self.verticalLayout_3.setStretch(5, 10)

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.labCurrentTime.setText(QCoreApplication.translate("Form", u"2024-01-01 00:00:00", None))
        self.labAutoFeeder.setText(QCoreApplication.translate("Form", u"\u555f\u52d5\u81ea\u52d5\u9935\u98df\u5668", None))
        self.cbAutoFeederStart.setText(QCoreApplication.translate("Form", u"\u555f\u52d5", None))
        self.labAIFunction.setText(QCoreApplication.translate("Form", u"\u555f\u52d5AI\u8fa8\u8b58", None))
        self.cbAIFunctionStart.setText(QCoreApplication.translate("Form", u"\u555f\u52d5", None))
        self.btnSubmit.setText(QCoreApplication.translate("Form", u"\u9001\u51fa", None))
        self.label_4.setText(QCoreApplication.translate("Form", u"\u5012\u6578\u6642\u9593\uff1a", None))
        self.labTimer.setText(QCoreApplication.translate("Form", u"00\u664200\u520600\u79d2", None))
        self.label_6.setText(QCoreApplication.translate("Form", u"\u9935\u98df\u91cf", None))
        self.labAmount.setText(QCoreApplication.translate("Form", u"1\u5708", None))
    # retranslateUi

