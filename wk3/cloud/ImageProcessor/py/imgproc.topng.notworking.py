#!/usr/bin/env python2

import paho.mqtt.client as mqtt
import numpy as np
# import scipy.misc as misc
import json
import time
import sys
import traceback
import png
# from PIL import Image
from datetime import datetime

CLOUD_MQTT_HOST="cloudbroker"
CLOUD_MQTT_PORT=1883
CLOUD_MQTT_TOPIC="/facedetect/cloud/faces"

def on_connect(client, userdata, flags, rc):
    print("Connected to cloud mqtt broker with result code "+str(rc))
    print("Subscribing...")
    client.subscribe(CLOUD_MQTT_TOPIC)
    print("Completed subscription to " + CLOUD_MQTT_TOPIC)


# allows us to get information about errors inside callbacks
def on_log(client, userdata, level, buf):
    print("on_log:",level,buf)
#     if (level == MQTT_LOG_WARNING):
#             print("MQTT_WARNING:",buf)
#     elif (level == MQTT_LOG_ERR):
#             print("MQTT_ERROR:",buf)
#             print("Exiting.")
#             exit(-1)


# Note the try-except block to get around paho-mqtt from
# killing error messages.  Doesnt work. need to look at
# on-log.
def on_message(client, userdata, msg):
    try:
        print("Received a message, payload: " + str(msg.payload)[:30] + "...")

        # create save filename based on time of message
        now = datetime.now()
        file_name = now.strftime("%y%m%d-%H%M%S.%f") + ".png"

        # convert back to array from json formatted string
        m_decode=str(msg.payload.decode("utf-8","ignore"))
        data = json.loads(m_decode)
        img_array = np.array(data[1], np.uint16)
        print(img_array[0])

        # create image file using Pillow
        # image = Image.fromarray(img_array, mode="L")
        # image.save("images/" + file_name, format="JPEG")

        # create image using scipy imsave - creates png files
        # cmin and cmax stop the image levels being renormalized
        # between the max and minimum values.
        # misc.toimage(img_array, cmin=0.0, cmax=0.0).save("images/" + file_name)
        # Create image file using pypng
        png.from_array(img_array, "L").save("images/" + file_name)



    except:
        traceback.print_exc()
        quit(0)

print("Setting up Client object")
client = mqtt.Client(client_id="imgproc")

print("Adding Callbacks")
client.on_connect = on_connect
client.on_message = on_message
client.on_log = on_log

# set up connection to MQTT broker on the cloud VSI
print("Connecting to cloud broker")
client.connect(CLOUD_MQTT_HOST, CLOUD_MQTT_PORT)

print("Starting loop...")

while True:
    client.loop(0.1)


