from lib2to3.pgen2.token import OP
import os
import sys
import shutil
import signal
import subprocess

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from utils.utils import save_json
from lines import *
from configs import weight_path, NAS_weight_path, wight_type

class Wcmd(QThread):
    textSignal = pyqtSignal(str)
    def __init__(self, parent=None):
        super().__init__(parent)
        self.stop = False     

    def kill(self):
        self.stop = True

    def run(self):
        self.textSignal.emit(LINE_checking_weight)
        r = subprocess.Popen([f"ls {NAS_weight_path}"], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        lines = r.stdout.readlines()
        files = [line.decode("UTF8").rstrip() for line in lines]
        weights = [file for file in files if file.split('.')[-1] in wight_type]
        weight_count = len(weights)
        if weight_count == 0:
            msg = LINE_NO_weight_found    
            self.textSignal.emit(msg)
            return
        elif weight_count < 2:
            msg = f"Found weight: {weights}. Start to download.\n"            
        elif weight_count < 10:
            msg = f"Found weights: {weights}. Start to download.\n"
        self.textSignal.emit(msg)
        
        for w in weights:
            Opath = os.path.join(NAS_weight_path, w)
            Tpath = os.path.join(weight_path, w)
            self.textSignal.emit(f"Downloading {w}... ")
            r = subprocess.Popen([f"mv -v '{Opath}' '{Tpath}'"], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            while not self.stop:
                line = r.stdout.read(1)
                try:
                    text = line.decode("UTF8")
                except:
                    continue
                if text == "r":
                    break
            self.textSignal.emit(f"done\n")