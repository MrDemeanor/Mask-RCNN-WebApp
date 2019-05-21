from app import app 
from flask import render_template, request
import numpy as np
import cv2 
import io
import os
from app.IMA import IMA
import json

cfg = json.load(open("configs/IMA_config.json"))
ima = IMA(cfg)

# json_results = ima.save_inference_json("/home/brentredmon/Documents/IMA/IMA_Web_App/app/uploaded_images/boat.jpg")
# with open("anothertest.json", "w") as outfile:
#     json.dump(json_results, outfile)

basedir = os.path.dirname(os.path.abspath(__file__))

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/inference_json', methods=['GET', 'POST'])
def inference_json():

    global ima

    target = os.path.join(basedir, 'uploaded_images/')
    destination = ''
    print(target)

    if not os.path.isdir(target):
        os.mkdir(target)

    img = request.files["file"]
    filename = img.filename
    destination = target + filename
    img.save(destination)
    
    json_results = ima.save_inference_json(destination)

    
    return str(json_results)