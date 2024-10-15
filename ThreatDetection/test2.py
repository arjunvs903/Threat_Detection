from flask import Flask, request, render_template, jsonify, Response, send_file
import numpy as np
from pickle import load, dump

import cv2
import numpy as np
from time import time, sleep
import os
import base64
import shutil
import tqdm
import threading

import torch
from super_gradients.training import models

# print(torch.cuda.is_available())

model = models.get('yolo_nas_l', num_classes=3, checkpoint_path=r"model.pth")



model.predict(r"C:\Users\majma\Downloads\g002.mp4").save(r'Processed\output.mp4') 