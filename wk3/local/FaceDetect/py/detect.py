#!/usr/bin/env python2

import numpy as np
import cv2 as cv
import time
import paho.mqtt.client as mqtt
import json

LOCAL_MQTT_HOST="tx2broker"
LOCAL_MQTT_PORT=1883
LOCAL_MQTT_TOPIC="/facedetect/local/faces"

keepalive=1200 #set MQTT time out to 20 minutes

# 1 should correspond to /dev/video1 , your USB camera. The 0 is reserved
# for the TX2 onboard camera
# ^^^ Apparently this is not always the case, depending on the order
# of recognition
cap = cv.VideoCapture(0)
face_cascade = cv.CascadeClassifier('/usr/share/opencv4/haarcascades/haarcascade_frontalface_default.xml')


# set up connection to MQTT broker on the TX2

local_mqttclient = mqtt.Client("facedetect")
local_mqttclient.connect(LOCAL_MQTT_HOST, LOCAL_MQTT_PORT,keepalive)


t = True

while(True):
# while(t == True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # We don't use the color information, so might as well save space
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    # face detection and other logic goes here

    print(gray)
    print(gray.shape)

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    print(faces) 
    for (x,y,w,h) in faces:
        gray_cropped = gray[y:y+h, x:x+w].copy()
        print("faces: ",faces)
        print(gray_cropped)
        print(gray_cropped.shape)

        # Publish the captured greyscale face to MQTT in JSON format
        print (gray_cropped.shape)

        # first member is a tuple showing the resolution of the captured face
        json_string = json.dumps( ( gray_cropped.shape, gray_cropped.tolist()) )
        print(json_string)
        local_mqttclient.publish(LOCAL_MQTT_TOPIC, payload=json_string, qos=0, retain=False)


    # Slow the capture rate down a bit
    time.sleep(1);
    
#    t = False
