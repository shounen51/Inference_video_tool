import os
import sys
import shutil
import signal
import subprocess
import time

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from utils.utils import save_json
from lines import *

class Ncmd(QThread):
    textSignal = pyqtSignal(str)
    doneSignal = pyqtSignal(int)
    def __init__(self, parent=None):
        super().__init__(parent)
        self.stop = False 
        self.FORCE = False

    def kill(self):
        self.stop = True

    def set_force(self, FORCE):
        self.FORCE = FORCE

    def run(self):
        if self.FORCE:
            self.textSignal.emit(LINE_force_run)
            self.doneSignal.emit(1)
            return
        self.textSignal.emit(LINE_checking_GPU)         
        for _ in range(3):
            time.sleep(2)
            r = subprocess.Popen(['nvidia-smi | grep MiB'], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            text = r.stdout.readline()
            text = text.decode("UTF8")
            Muse = int(text.split("|")[2].split("/")[0][:-4])
            Guse = int(text.split("|")[3].split("%")[0])
            text = f"Memory use now is: {Muse} MiB, usage: {Guse} %\n"
            self.textSignal.emit(text) 
            if Muse > 200 or Guse > 10:
                time.sleep(0.5)
                self.textSignal.emit(LINE_GPU_busy)
                self.doneSignal.emit(0)
                return
        time.sleep(0.5)
        self.textSignal.emit(LINE_GPU_ready)
        self.doneSignal.emit(1)