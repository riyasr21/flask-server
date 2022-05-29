
from sys import stdout
import logging
from flask import Flask, render_template, Response
from flask_socketio import SocketIO, emit
from flask_cors import CORS, cross_origin
import numpy as np
import cv2
import imutils
import PIL.Image
import io
from io import BytesIO,StringIO
import base64
import cv2
import time
import os
from fastai.vision import *
from fastai.vision import Image as ImageF
import dlib
from imutils import face_utils
import numpy as np
from scipy.spatial import distance as dist

    
app = Flask(__name__)
app.logger.addHandler(logging.StreamHandler(stdout))
app.config['SECRET_KEY'] = 'secret!'
app.config['DEBUG'] = True
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'





socketio = SocketIO(app,cors_allowed_origins='*')
data = []
time_value = 0
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
EYE_AR_THRESH = 0.20
EYE_AR_CONSEC_FRAMES = 10
COUNTER = 0
start = time.perf_counter()
path = Path()
learn = load_learner(path)
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]



@app.route('/', methods=['POST', 'GET'])
def index():
    print("Welcome")
def eye_aspect_ratio(eye):
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])
    C = dist.euclidean(eye[0], eye[3])
    ear = (A + B) / (2.0 * C)
    return ear



def data_time(time_value, prediction, probability, ear):
    current_time = int(time.perf_counter()-start)
    if current_time != time_value:
        data.append([current_time, prediction, probability, ear])
        time_value = current_time
    return time_value
@socketio.on('image')
def image(data_image):
    
    global time_value,COUNTER
    sbuf = StringIO()
    sbuf.write(data_image)

    # decode and convert into image
    b = io.BytesIO(base64.b64decode(data_image))
    pimg = PIL.Image.open(b)
    frame = cv2.cvtColor(np.array(pimg), cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    face_coord = face_cascade.detectMultiScale(gray, 1.1, 5, minSize=(30, 30))

    for coords in face_coord:
        X, Y, w, h = coords
        H, W, _ = frame.shape
        X_1, X_2 = (max(0, X - int(w * 0.3)), min(X + int(1.3 * w), W))
        Y_1, Y_2 = (max(0, Y - int(0.3 * h)), min(Y + int(1.3 * h), H))
        img_cp = gray[Y_1:Y_2, X_1:X_2].copy()
        prediction, idx, probability = learn.predict(ImageF(pil2tensor(img_cp, np.float32).div_(225)))

        cv2.rectangle(
                img=frame,
                pt1=(X_1, Y_1),
                pt2=(X_2, Y_2),
                color=(128, 128, 0),
                thickness=2,
            )
        
        rect = dlib.rectangle(X, Y, X+w, Y+h)

        cv2.putText(frame, str(prediction), (10, frame.shape[0] - 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (225, 255, 255), 2)

        shape = predictor(gray, rect)
        shape = face_utils.shape_to_np(shape)
        leftEye = shape[lStart:lEnd]
        rightEye = shape[rStart:rEnd]
        leftEAR = eye_aspect_ratio(leftEye)
        rightEAR = eye_aspect_ratio(rightEye)
        ear = (leftEAR + rightEAR) / 2.0
        leftEyeHull = cv2.convexHull(leftEye)
        rightEyeHull = cv2.convexHull(rightEye)
        cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
        cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)
        if ear < EYE_AR_THRESH:
            COUNTER += 1
            if COUNTER >= EYE_AR_CONSEC_FRAMES:
                cv2.putText(frame, "Distracted", (35, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        else:
            COUNTER = 0
        cv2.putText(frame, "Eye Ratio: {:.2f}".format(ear), (250, frame.shape[0] - 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        time_value = data_time(time_value, prediction, probability, ear)
        
    imgencode = cv2.imencode('.jpeg', frame,[cv2.IMWRITE_JPEG_QUALITY,40])[1]

    # base64 encode
    stringData = base64.b64encode(imgencode).decode('utf-8')
    b64_src = 'data:image/jpeg;base64,'
    
    stringData = b64_src + stringData
    

    # emit the frame back
    emit('response_back', stringData)

@socketio.on('connect')
def test_connect():
    app.logger.info("client connected")
   

    
if __name__ == '__main__':
    socketio.run(app,port=80,)
