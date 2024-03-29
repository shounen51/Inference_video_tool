import json
import os
import time
import random

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import numpy as np
from PIL import Image, ImageDraw, ImageFont

def load_json(path):
    _dict={}
    try:
        with open(path,encoding="utf-8") as file:
            _dict = json.load(file)
        return True, _dict
    except:
        return False, _dict

def save_json(path, _dict):
    try:
        with open(path, "w", encoding="utf-8") as file:
            json.dump(_dict, file, indent=4, ensure_ascii=False)
        return True
    except:
        return False

def load_class(txtPath):
    classes = []
    with open(txtPath,'r') as f:
        classes = f.readlines()
    classes = [cl.rstrip() for cl in classes]
    return classes


