#!/usr/bin/env python3

from PIL import Image
import os
import numpy as np
import cv2 as cv
import time
import paho.mqtt.client as mqtt
import json
from tensorflow.contrib import tensorrt as trt
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import tensorflow as tf
import numpy as np
import time
from tf_trt_models.detection import download_detection_model, build_detection_graph

print("\n\n##### Starting...")

LOCAL_MQTT_HOST="tx2broker"
LOCAL_MQTT_PORT=1883
LOCAL_MQTT_TOPIC="/facedetect/local/faces"


# 1 should correspond to /dev/video1 , your USB camera. The 0 is reserved
# for the TX2 onboard camera
# ^^^ Apparently this is not always the case, depending on the order
# of recognition
cap = cv.VideoCapture(1)


# set up connection to MQTT broker on the TX2
print("\n\n##### Connecting to MQTT...")
keepalive=1200  # avoid continuous dropouts when no active data
local_mqttclient = mqtt.Client("facedetect")
local_mqttclient.connect(LOCAL_MQTT_HOST, LOCAL_MQTT_PORT,keepalive)


# Set up variables
DATA_LOC = "~/W251/MIDS-W251/wk7/FaceDetectNeural/data"

# Set up the neural network
print("\n\n##### Setting up network...")
FROZEN_GRAPH_NAME = '/bin/frozen_inference_graph_face.pb'
output_dir=''
frozen_graph = tf.compat.v1.GraphDef()
print("\n\n##### Load pre-trained parameters....")
with open(os.path.join(output_dir, FROZEN_GRAPH_NAME), 'rb') as f:
  frozen_graph.ParseFromString(f.read())


INPUT_NAME='image_tensor'
BOXES_NAME='detection_boxes'
CLASSES_NAME='detection_classes'
SCORES_NAME='detection_scores'
MASKS_NAME='detection_masks'
NUM_DETECTIONS_NAME='num_detections'

input_names = [INPUT_NAME]
output_names = [BOXES_NAME, CLASSES_NAME, SCORES_NAME, NUM_DETECTIONS_NAME]

print("\n\n##### Optimizing frozen graph....")
trt_graph = trt.create_inference_graph(
    input_graph_def=frozen_graph,
    outputs=output_names,
    max_batch_size=1,
    max_workspace_size_bytes=1 << 25,
    precision_mode='FP16',
    minimum_segment_size=50
)


print("\n\n##### Create Session and load the graph....")
tf_config = tf.ConfigProto()
tf_config.gpu_options.allow_growth = True

tf_sess = tf.Session(config=tf_config)

# use this if you want to try on the optimized TensorRT graph
# Note that this will take a while
# tf.import_graph_def(trt_graph, name='')

# use this if you want to try directly on the frozen TF graph
# this is much faster
tf.import_graph_def(frozen_graph, name='')

tf_input = tf_sess.graph.get_tensor_by_name(input_names[0] + ':0')
tf_scores = tf_sess.graph.get_tensor_by_name('detection_scores:0')
tf_boxes = tf_sess.graph.get_tensor_by_name('detection_boxes:0')
tf_classes = tf_sess.graph.get_tensor_by_name('detection_classes:0')
tf_num_detections = tf_sess.graph.get_tensor_by_name('num_detections:0')


###### LOAD AND PREPROCESS - THIS IS WHERE WE REPLACE WITH CAPTURED FRAMES

while(t == True):
    print("\n\n##### Loading Image")
    ret, frame = cap.read()
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    print(gray)
    print(gray.shape)


    image = Image.open(IMAGE_PATH)
    plt.imshow(image)
    image_resized = np.array(image.resize((300, 300)))
    image = np.array(image)

    print("\n\n##### Running Network on Image...")
    scores, boxes, classes, num_detections = tf_sess.run([tf_scores, tf_boxes, tf_classes, tf_num_detections], feed_dict={
        tf_input: image_resized[None, ...]
    })

    boxes = boxes[0] # index by 0 to remove batch dimension
    scores = scores[0]
    classes = classes[0]
    num_detections = num_detections[0]

    print("boxes:", boxes)
    print("scores", scores)
    print("classes:", classes)
    print("num_detections:", num_detections)

    print("\n\n##### Sleeping...")
    time.sleep(100000);

    t = True

# while(True):
# while(t == True):
    # Capture frame-by-frame
#    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
#    print(faces) 
##    for (x,y,w,h) in faces:
#        gray_cropped = gray[y:y+h, x:x+w].copy()
#        print("faces: ",faces)
#        print(gray_cropped)
#        print(gray_cropped.shape)
#
#        # Publish the captured greyscale face to MQTT in JSON format
#        print (gray_cropped.shape)
#
#        # first member is a tuple showing the resolution of the captured face
#        json_string = json.dumps( ( gray_cropped.shape, gray_cropped.tolist()) )
#        print(json_string)
#        local_mqttclient.publish(LOCAL_MQTT_TOPIC, payload=json_string, qos=0, retain=False)
#
#
#    # Slow the capture rate down a bit
#    time.sleep(1);
#    
#    t = False
