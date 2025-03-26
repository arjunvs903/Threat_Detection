from flask import Flask, request, render_template, jsonify, Response, send_file
import numpy as np
from pickle import load, dump
from dotenv import load_dotenv
import cv2
import numpy as np
from time import time, sleep
import os
import base64
import shutil
import tqdm
import threading
# import pygame
from twilio.rest import Client
from moviepy.editor import VideoFileClip

import torch
from super_gradients.training import models

model = models.get('yolo_nas_l', num_classes=3, checkpoint_path=r"model/model.pth")

app = Flask(__name__)

start  = time()
cnt = True



def generate(phone):
    global start
    global cnt

    # Load environment variables from .env
    load_dotenv()
    
    # Get Twilio credentials and phone number
    account_sid = os.getenv('TWILIO_ACCOUNT_SID')
    auth_token = os.getenv('TWILIO_AUTH_TOKEN')
    twilio_number = os.getenv('TWILIO_PHONE_NUMBER')  # Load Twilio phone number

    # create Twilio client
    client = Client(account_sid, auth_token)

    # send SMS message containing OTP
    end = time()
    print(np.round(end-start, 0))
    if (np.round(end-start, 0) > 30) or cnt:
        message = client.messages.create(
            body=f'Threat Detected!!!',
            from_=twilio_number,
            to="+91"+phone
        )
        start = time()
        cnt = False


cam_stat = False

# def play_sound():
#     pygame.init()
#     sound = pygame.mixer.Sound('beep.wav')
#     sound.play()
#     pygame.time.wait(int(sound.get_length() * 750))
#     pygame.quit()

def gen_frames(cap, conf, phoneno, alarm, sms):  
    lab = {0: "Person", 1: "Knife", 2: "Gun"}

    cols = {0: (255, 165, 18), 1: (0, 68, 172), 2: (12, 69, 188)}
    while cam_stat:
        success, frame = cap.read()
        if not success:
            break
        else:
            results = model.to(0 if torch.cuda.is_available() else "cpu").predict(frame)
            # print(results[0].prediction.labels)
            col = (255, 255, 0)
                
            for box in results[0].prediction.bboxes_xyxy:
                x1, y1, x2, y2 = map(int, box)
                cv2.rectangle(frame, (x1, y1), (x2, y2), col, 3)
                c = 0
                for label in results[0].prediction.labels:

                    if label == 1 or label == 2:
                        # if alarm == 'true':
                        #     sound_thread = threading.Thread(target=play_sound)
                        #     sound_thread.start()
                        if sms == 'true':
                            generate(phoneno)

                    confidence = 0
                    try:
                         confidence = results[0].prediction.confidence[c]
                    except:
                         pass
                    cv2.putText(frame, f"{lab[label]}: {confidence:.2f}", (x1, y1-15), cv2.FONT_HERSHEY_SIMPLEX, 1.1, cols[label], 2)
                    c+= 1
            
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

        
@app.route("/", methods=["GET", "POST"])
def index():
    try:
        with open("settings.pkl", "rb") as file:
            data = load(file)
        if len(data) != 5:
            return render_template("index.html", error=True)
        else:
            return render_template("index.html")
    except:
        return render_template("index.html", error=True)

@app.route("/settings", methods=["GET", "POST"])
def settings():
    conf = float(request.form['confidence'])/100
    phone = request.form['phoneno']
    src = request.form['camera']
    alarm = request.form['alarm']
    sms = request.form['sms']
    ls = [conf, phone, src, alarm, sms]
    with open("settings.pkl", "wb") as file:
        dump(ls, file)
    
    return "Settings Saved!"

@app.route("/video_feed")
def video_feed():
        with open("settings.pkl", "rb") as file:
            data = load(file)
        conf, phoneno, cam, alarm, sms = data
        vidcap = cv2.VideoCapture(int(cam))
        return Response(gen_frames(vidcap, conf, phoneno, alarm, sms), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/control_cam", methods=["GET", "POST"])
def control():
    global cam_stat
    print(type(request.form['status']))
    if request.form['status'] == 'true':
        cam_stat = True
    else:
        cam_stat = False
    video_feed()
    return "status_good"

@app.route("/analyze_data", methods=["GET", "POST"])
def process_file():

    directory_path = r"Uploads"

    # Iterate through the files in the directory
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
                print(f"Deleted: {file_path}")
        except Exception as e:
            print(f"Error deleting {file_path}: {e}")

    img = ""
    with open("settings.pkl", "rb") as file:
        data = load(file)
    conf, phoneno, cam, alarm, sms = data
    file = request.files['uploadfiledata']
    ftype = request.form['filetype']
    fname = f'Uploads/{file.filename}'
    file.save(fname)
    if ftype == 'video':
        res =  model.to(0 if torch.cuda.is_available() else "cpu").predict(fname).save(r"Processed\output.mp4")  
        video_clip = VideoFileClip(r"Processed\output.mp4")
        video_clip = video_clip.set_fps(24)
        video_clip.write_videofile(r"Processed\output.mp4", codec="libx264")
        video_file_path = 'Processed/output.mp4'  # Update with the correct path

        # # Read video file
        # with open(video_file_path, 'rb') as video_file:
        #     video_data = video_file.read()

        # # Encode as Base64
        # encoded_data = base64.b64encode(video_data).decode('utf-8')

        # # Construct Data URL
        # data_url = f'data:video/mp4;base64,{encoded_data}'

        # return Response(data_url, content_type='text/plain')
        if os.path.exists(r"Processed\output.mp4"):
            return "true"
        else:
            return "false"

    elif ftype == 'image':
        image = cv2.imread(fname)
        image = cv2.resize(image, (640, 640))
        cv2.imwrite(fname, image)
        res = model.to(0 if torch.cuda.is_available() else "cpu").predict(fname).save(r'Processed')   
        print(res)
        if os.path.exists(r"".join(fname)):
            img = cv2.imread(r'Processed\pred_0.jpg')
            ret, buf = cv2.imencode('.jpg', img)
            img = buf.tobytes()
            img = f"data:image/jpeg;base64,{base64.b64encode(img).decode('utf-8')}"
            
        return img
    
@app.route("/video_data")
def send_vdata():
    return send_file(r"Processed\output2.mp4", mimetype='video/mp4', as_attachment=False)

if __name__ == "__main__":
    app.run(debug=True)