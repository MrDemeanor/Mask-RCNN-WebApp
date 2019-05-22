from app import app 
from flask import render_template, request, send_file, make_response
import numpy as np
import cv2 
import io
import os
from app.IMA import IMA
import json

basedir = os.path.dirname(os.path.abspath(__file__))

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/inference_json', methods=['GET', 'POST'])
def inference_json():

    cfg = json.load(open("configs/IMA_config.json"))
    ima = IMA(cfg)

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

    response = make_response(str(json_results))
    response.headers.set('Content-Type', 'application/json')
    response.headers.set( 'Content-Disposition', 'attachment', filename="inference.json")

    
    return response