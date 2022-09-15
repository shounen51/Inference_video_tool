'''
⠄⠄⠈⣿⠄⠄⠄⢙⢞⢿⣿⢹⢿⣦⢏⣱⢿⠘⣿⣝⠹⢿⣿⡽⣿⣿⣏⣆⢿⣿⡞⠁
⠄⠄⠄⢻⡀⠄⠄⠈⣾⡸⡏⢸⡾⣴⣿⣿⣶⣼⣎⢵⢀⡛⣿⣷⡙⡻⢻⡴⠨⠨⠖⠃
⠄⠄⠄⠈⣧⢀⡴⠊⢹⠁⡇⠈⢣⣿⣿⣿⣿⣦⣿⣷⣜⡳⣝⢧⢃⢣⣼⢁⠘⠆⠄⠄
⠄⠄⠄⠄⢹⡇⠄⣠⠔⠚⣅⠄⢰⣶⣦⣭⣿⣿⣿⡿⠟⠿⣷⡧⠄⣘⣟⣸⠄⠄⠄⠄
⠄⠄⠄⠄⠄⢷⠎⠄⠄⠄⣼⣦⠻⣿⣿⡟⠛⠻⢿⣿⣿⣿⡾⢱⣿⡏⠸⡏⠄⠄⠄⠄
⠄⠄⠄⠄⠄⠸⡄⠄⡄⠄⣿⢧⢗⠌⠻⣇⠿⠿⣸⣿⣿⡟⡐⣿⠟⢰⣇⠇⠄⠄⠄⠄
⠄⠄⠄⠄⠄⣠⡆⠄⠃⢠⠏⣤⢀⢢⡰⣭⣛⡉⠩⠭⡅⣾⢳⡴⡀⢸⣿⡆⠄⠄⠄⠄
⠄⠄⠄⢀⣶⡟⣽⠼⢀⡕⢀⠘⠸⢮⡳⡻⡍⡷⡆⠤⠤⠭⢸⢳⣷⢸⡟⣷⠄⠄⠄⠄
'''

import os
import sys
import time

import numpy as np
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import *

from ui.A import A_form
from ui_controller.button_event import btn_events
from utils.utils import load_class
from configs import functions
from lines import *

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.btn_events = btn_events(self)
        self.ui = A_form(self, self, self.btn_events)
        self._listmodel()
        self.set_visible(False)

    def _listmodel(self):
        for func_name in functions:
            self.ui.cbb_moudle_name.addItem(func_name)

    def closeEvent(self,event):
        result = QMessageBox.question(self,
                      LINE_try_exit_title,
                      LINE_try_exit,
                      QMessageBox.Yes| QMessageBox.No)
        event.ignore()
        if result == QMessageBox.Yes:
            self.btn_events.update_TB("\nNow closing....\n")
            self.btn_events.weight_checker.kill()
            self.btn_events.GPU_checker.kill()
            self.btn_events.NAS_copyer.kill()
            self.btn_events.cmdThread.kill()
            self.btn_events.weight_checker.wait(2000)
            self.btn_events.GPU_checker.wait(2000)
            self.btn_events.NAS_copyer.wait(2000)
            self.btn_events.cmdThread.wait()
            event.accept()

    def set_visible(self, v = False):
        self.ui.cb_force_run.setVisible(v)
        self.ui.lab_6.setVisible(v)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())

    