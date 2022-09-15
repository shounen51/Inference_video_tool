import os
import sys
import shutil
import subprocess
import random
import json

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import cv2
for k, v in os.environ.items():
    if k.startswith("QT_") and "cv2" in v:
        del os.environ[k]

from utils.utils import save_json, load_json


def add_in_data(data_json, _data):
    with open(data_json, "w") as _j:
        _str = json.dumps(_data, ensure_ascii=False)
        _j.write(_str)

def label2int(label, _LIST):
    if label in _LIST:
        return _LIST.index(label)
    else:
        return -1

class data_maker(QThread):
    textSignal = pyqtSignal(str)
    doneSignal = pyqtSignal()
    def __init__(self, parent=None):
        super().__init__(parent)
        self.model_name = ""
        self.train_set = 1
        self.all_labels = {}
        self.train_list = []
        self.test_list = []
        self._LIST = []

    def set_config(self, model_name, train_set, classes):
#'faster_rcnn_R_50_FPN_3x','faster_rcnn_R_101_FPN_3x','faster_rcnn_X_101_32x8d_FPN_3x','retinanet_R_50_FPN_3x','retinanet_R_101_FPN_3x'
        self.model_name = model_name     
        self.train_set = train_set
        self._LIST = classes

    def run(self):
        self.textSignal.emit('start making dataset.\n')
        self.model_dir = os.path.join('detectron2/', self.model_name)
        if not os.path.isdir(self.model_dir):
            os.mkdir(self.model_dir)
        self.model_images_dir = os.path.join(self.model_dir, "images")
        if not os.path.isdir(self.model_images_dir):
            os.mkdir(self.model_images_dir)
        rootDir = os.path.join("./dataset", self.model_name)
        for _file in os.listdir(rootDir):
            _dir = os.path.join(rootDir,_file)
            if os.path.isdir(_dir):
                for path in os.listdir(_dir):
                    if path.split('.')[-1]=='json':
                        jsonPath = os.path.join(_dir,path)
                        ok, _json = load_json(jsonPath)
                        if ok:
                            keys = _json.keys()
                            for pic in keys:
                                self.all_labels[pic] = _json[pic]
                                picPath = os.path.join(_dir,pic)
                                shutil.copyfile(picPath, os.path.join(self.model_images_dir, _json[pic]["filename"]))

        keys = self.all_labels.keys()
        nAll = len(keys)
        nTrain = nAll*self.train_set
        nTset = nAll-nTrain
        for pic in keys:
            _rand = random.randint(1, nTrain+nTset)
            if _rand > nTrain:
                nTset-=1
                self.test_list.append(pic)
            else:
                nTrain-=1
                self.train_list.append(pic)
        self._detectron_data()
        self.textSignal.emit('data is ready.\n')
        self.doneSignal.emit()

    def _detectron_data(self):
        keys = self.all_labels.keys()
        train_list = []
        test_list = []
        number_dict = {}
        
        for key in self._LIST:
            number_dict[key] = 0
        for pic in keys:
            if pic in self.test_list:
                _set = test_list
            else:
                _set = train_list

            _dict = {}
            picPath = os.path.join(self.model_images_dir, pic)
            frame = cv2.imread(picPath)
            _dict['width'] = frame.shape[1]
            _dict['height'] = frame.shape[0]
            _dict["file_name"] = pic
            _dict["id"] = pic
            areas = self.all_labels[pic]['regions'].keys()
            objs = []
            for i, area in enumerate(areas):
                obj = {}
                color = (int(random.random()*205+50), int(random.random()*205+50), int(random.random()*205+50))
                xs = self.all_labels[pic]['regions'][area]['shape_attributes']['all_points_x']
                ys = self.all_labels[pic]['regions'][area]['shape_attributes']['all_points_y']
                label = self.all_labels[pic]['regions'][area]['region_attributes']['label']
                xs = [int(x) for x in xs]
                ys = [int(y) for y in ys]
                bbox = [min(xs), min(ys), max(xs), max(ys)]
                obj["bbox"] = bbox
                segmentation = []
                for i, x in enumerate(xs):
                    segmentation.append(x)
                    segmentation.append(ys[i])
                obj["segmentation"] = [segmentation]
                obj['bbox_mode'] = 0
                obj["category_id"] = label2int(label, self._LIST)
                number_dict[label] += 1
                objs.append(obj)
            _dict["annotations"] = objs
            _set.append(_dict)
        add_in_data(os.path.join(self.model_dir, "train.json"), train_list)
        add_in_data(os.path.join(self.model_dir, "test.json"), test_list)
        for key in number_dict:
            self.textSignal.emit(key + ":" + str(number_dict[key]) + "\n")