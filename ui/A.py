# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Joseph\git\Taipei_MOT_UI\test\A.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from ui.color import *
from ui_controller.my_widgets import *

class A_form(QtWidgets.QWidget):
    def __init__(self, Form, main, event):
        QtWidgets.QWidget.__init__(self)
        # Form.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        Form.setObjectName("Form")
        Form.resize(1460, 920)
        Form.setMinimumSize(QtCore.QSize(956, 584))
        Form.setMaximumSize(QtCore.QSize(956, 584))
        Form.setAutoFillBackground(True)
        Form.setPalette(back_plt)

        # Form.setStyleSheet("background-image: url(./src/0000_mv.jpg);")

        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(12)

        self.btn_start = my_btn(Form)
        self.btn_start.setFont(font)
        self.btn_start.setGeometry(QtCore.QRect(810, 100, 131, 21))
        self.btn_start.setObjectName("pushButton")

        # self.lab_1.setAlignment(QtCore.Qt.AlignCenter)]
        self.lab_1 = my_label(Form)
        self.lab_1.setFont(font)
        self.lab_1.setGeometry(QtCore.QRect(20, 20, 121, 21))
        self.cb_hide_labels = my_cb(Form)
        self.cb_hide_labels.setFont(font)
        self.cb_hide_labels.setGeometry(QtCore.QRect(20, 50, 120, 21))
        self.cb_hide_conf = my_cb(Form)
        self.cb_hide_conf.setFont(font)
        self.cb_hide_conf.setGeometry(QtCore.QRect(20, 80, 120, 21))
        self.cb_force_run = my_cb(Form)
        self.cb_force_run.setFont(font)
        self.cb_force_run.setGeometry(QtCore.QRect(20, 110, 120, 21))
        self.lab_4 = my_label(Form)
        self.lab_4.setFont(font)
        self.lab_4.setGeometry(QtCore.QRect(45, 50, 121, 21))
        self.lab_5 = my_label(Form)
        self.lab_5.setFont(font)
        self.lab_5.setGeometry(QtCore.QRect(45, 80, 121, 21))
        self.lab_6 = my_label(Form)
        self.lab_6.setFont(font)
        self.lab_6.setGeometry(QtCore.QRect(45, 110, 421, 21))

        self.cbb_moudle_name = my_cbb(Form)
        self.cbb_moudle_name.setFont(font)
        self.cbb_moudle_name.setGeometry(QtCore.QRect(150, 20, 171, 21))
        self.cbb_moudle_name.setObjectName("lineEdit")

        self.lab_logo = clickable_label(Form, event)
        self.lab_logo.setGeometry(QtCore.QRect(791, 10, 150, 40))
        self.lab_logo.setStyleSheet("background-image: url(./src/BeseyeLOGO.png);")

        self.console = my_text_browser(Form)
        self.console.setFont(font)
        self.console.setGeometry(QtCore.QRect(20, 140, 921, 431))
        self.console.setObjectName("console")
        


        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)
        self.event_connect(event)

    def event_connect(self, event):
        self.btn_start.clicked.connect(event.start)
        
    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Auto run"))
        self.lab_1.setText(_translate("Form", "Model Name:"))
        self.cb_hide_labels.setText(_translate("Form", ""))
        self.cb_hide_conf.setText(_translate("Form", ""))
        self.cb_force_run.setText(_translate("Form", ""))
        self.lab_4.setText(_translate("Form", "Hide labels"))
        self.lab_5.setText(_translate("Form", "Hide conf"))
        self.lab_6.setText(_translate("Form", "Force run (Don't check if you don't know what it means.)"))
        self.btn_start.setText(_translate("Form", "start"))
        


