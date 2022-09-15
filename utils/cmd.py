import os
import sys
import shutil
import signal
import subprocess

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from lines import LINE_run_end, LINE_run_start

from utils.utils import save_json
from configs import weight_path, video_path
from lines import *

class cmd(QThread):
    textSignal = pyqtSignal(str)
    def __init__(self, args, parent=None):
        super().__init__(parent)
        self.args = args
        self.stop = False
        self.founc = None

    def kill(self):
        self.stop = True

    def set_args(self, founc, command, HL, HC):
        self.founc = founc
        self.command = command
        self.args[founc]['--source'] = video_path
        
        self.args[founc]["--hide-labels"] = ""
        if not HL:
            self.args[founc].pop("--hide-labels")
        self.args[founc]["--hide-conf"] = ""
        if not HC:
            self.args[founc].pop("--hide-conf")
        
    def run(self):
        weights = [w for w in os.listdir(weight_path) if w.startswith(self.founc)]
        if len(weights) == 0:
            self.textSignal.emit(LINE_find_no_weight)
            return
        elif len(weights) == 1:
            self.args[self.founc]["--weights"] = os.path.join(weight_path, weights[0])
        else:
            weights.sort()
            for i, w in enumerate(weights):
                self.args[self.founc][f"--weights{str(i+1)}"] = os.path.join(weight_path, w)
        
        for k in self.args[self.founc]:
            self.command += " "
            self.command += str(k)
            self.command += " "
            self.command += str(self.args[self.founc][k])
        self.textSignal.emit(LINE_run_start)
                
        r = subprocess.Popen([self.command], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        text = ""
        while not self.stop:
            line = r.stdout.read(1)
            try:
                text = line.decode("UTF8")
            except:
                continue
            self.textSignal.emit(text)
            if text == ";":
                break
        if self.stop:
            os.killpg(os.getpgid(r.pid), signal.SIGTERM)
            print("subprocess has been stoped")
        else:
            self.stop = True        
        self.textSignal.emit(LINE_run_end)