import json
import shutil
import time
import sys
from datetime import datetime
import random
import subprocess
import os

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import requests

from configs import *
from utils.utils import *
from utils.cmd import cmd
from utils.cmd_nvidia import Ncmd
from utils.cmd_video import Vcmd
from utils.cmd_weight import Wcmd
from lines import *

class btn_events():
    def __init__(self, main_window):
        self.main = main_window
        self.weight_checker = Wcmd()
        self.weight_checker.textSignal.connect(self.update_TB)
        self.weight_checker.finished.connect(self._start_checkGPU)
        self.GPU_checker = Ncmd()
        self.GPU_checker.textSignal.connect(self.update_TB)
        self.GPU_checker.doneSignal.connect(self._GPU_OK)
        self.GPU_checker.finished.connect(self._copy_NAS)
        self.NAS_copyer = Vcmd()
        self.NAS_copyer.textSignal.connect(self.update_TB)
        self.NAS_copyer.doneSignal.connect(self._video_count)
        self.NAS_copyer.finished.connect(self._start_inference)
        self.cmdThread = cmd(args)
        self.cmdThread.textSignal.connect(self.update_TB)
        self.cmdThread.finished.connect(self._thread_end)

        # self.cmdThread.doneSignal.connect(self._thread_end)

        self.GPU_OK = 0
        self.video_count = 0
        self.THREAD_DONE = False
        self.pw = ""

    def start(self):
        self._thread_on()
        self.weight_checker.start()

    def _start_checkGPU(self):
        self.GPU_checker.set_force(self.main.ui.cb_force_run.isChecked())
        self.GPU_checker.start()

    def _copy_NAS(self):
        if self.GPU_OK:
            self.NAS_copyer.start()

    # def _copy_result(self):
        

    def _start_inference(self):
        if self.video_count == 0:
            self._thread_end()
            return
        HL = self.main.ui.cb_hide_labels.isChecked()
        HC = self.main.ui.cb_hide_conf.isChecked()
        fonc = self.main.ui.cbb_moudle_name.currentText()
        self.cmdThread.set_args(fonc, functions[fonc], HL, HC)
        self.cmdThread.start()

    def update_TB(self, text):
        self.main.ui.console.insertPlainText(text)
        self.main.ui.console.moveCursor(self.main.ui.console.textCursor().End)

    def _thread_on(self):
        self.GPU_OK = 0
        self.video_count = 0
        self.THREAD_DONE = False
        self.main.ui.console.clear()
        shutil.rmtree(video_path)
        os.makedirs(video_path, exist_ok=True)
        self._disable_btn()

    def _thread_end(self):
        self.THREAD_DONE = True
        self.update_TB(LINE_end)
        self._enable_btn()

    def _GPU_OK(self, s):            
        self.GPU_OK = s

    def _video_count(self, i):
        self.video_count = i

    def _enable_btn(self):        
        self.main.ui.btn_start.setEnabled(True)

    def _disable_btn(self):
        self.main.ui.btn_start.setEnabled(False)

    def SCL_click(self):
        self.pw += "0"
        if "10" == self.pw:
            self.main.set_visible(True)
        elif not "10".startswith(self.pw):
            self.pw = ""

    def SCR_click(self):
        self.pw += "1"
        if "10" == self.pw:
            self.main.set_visible(True)
        elif not "10".startswith(self.pw):
            self.pw = ""
            
    # def editting_train(self):
    #     try:
    #         train = float(self.main.ui.edit_train.text())
    #         if train <= 1 and train >= 0:
    #             val = 1-train
    #             self.main.ui.edit_val.setText(str(round(val,3)))
    #             self.main.ui.btn_start.setEnabled(True)
    #         else:
    #             self.main.ui.btn_start.setEnabled(False)
    #     except:
    #         self.main.ui.btn_start.setEnabled(False)

    # def editting_val(self):
    #     try:
    #         val = float(self.main.ui.edit_val.text())
    #         if val <= 1 and val >= 0:
    #             train = 1-val
    #             self.main.ui.edit_train.setText(str(round(train,3)))
    #             self.main.ui.btn_start.setEnabled(True)
    #         else:
    #             self.main.ui.btn_start.setEnabled(False)
    #     except:
    #         self.main.ui.btn_start.setEnabled(False)
