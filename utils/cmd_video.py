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
from configs import video_path, NAS_path, video_type

class Vcmd(QThread):
    textSignal = pyqtSignal(str)
    doneSignal = pyqtSignal(int)
    def __init__(self, parent=None):
        super().__init__(parent)
        self.stop = False     

    def kill(self):
        self.stop = True

    def run(self):
        self.textSignal.emit(LINE_checking_video)
        r = subprocess.Popen([f"ls {NAS_path}"], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        lines = r.stdout.readlines()
        files = [line.decode("UTF8").rstrip() for line in lines]
        videos = [file for file in files if file.split('.')[-1] in video_type]
        video_count = len(videos)
        if video_count == 0:
            msg = LINE_NO_video_found    
            self.textSignal.emit(msg)        
            self.doneSignal.emit(video_count)
            return
        elif video_count < 2:
            msg = f"Find video:  {', '.join(videos)} . Start to download.\n"  
        elif video_count < 10:
            msg = f"Find videos:  {', '.join(videos)} . Start to download.\n"
        else:
            msg = f"Find videos:  {', '.join(videos[:9])}  .... Start to download.\n"
        self.textSignal.emit(msg)
        
        for v in videos:
            Opath = os.path.join(NAS_path, v)
            Tpath = os.path.join(video_path, v)
            self.textSignal.emit(f"Downloading {v}... ")
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
        self.doneSignal.emit(video_count)