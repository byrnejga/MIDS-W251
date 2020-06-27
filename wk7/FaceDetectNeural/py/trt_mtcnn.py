"""trt_mtcnn.py

This script demonstrates how to do real-time face detection with
Cython wrapped TensorRT optimized MTCNN engine.
"""

import sys
import time
import argparse
import json

import cv2
from utils.camera import add_camera_args, Camera
from utils.display import open_window, set_display, show_fps
from utils.mtcnn import TrtMtcnn

WINDOW_NAME = 'TrtMtcnnDemo'
WINDOW_NAME2 = 'TrtMtcnnExtracted'
BBOX_COLOR = (0, 255, 0)  # green

import paho.mqtt.client as mqtt
LOCAL_MQTT_HOST="tx2broker"
LOCAL_MQTT_PORT=1883
LOCAL_MQTT_TOPIC="/facedetect/local/faces"
keepalive=1200 #set MQTT time out to 20 minutes


def parse_args():
    """Parse input arguments."""
    desc = ('Capture and display live camera video, while doing '
            'real-time face detection with TrtMtcnn on Jetson '
            'Nano')
    parser = argparse.ArgumentParser(description=desc)
    # print(f"desc: {desc}")
    parser = add_camera_args(parser)
    parser.add_argument('--minsize', type=int, default=40,
                        help='minsize (in pixels) for detection [40]')
    args = parser.parse_args()
    # print(f"args: {args}")
    return args


def show_faces(img, boxes, landmarks):
    """Draw bounding boxes and face landmarks on image."""
    for bb, ll in zip(boxes, landmarks):
        x1, y1, x2, y2 = int(bb[0]), int(bb[1]), int(bb[2]), int(bb[3])
        cv2.rectangle(img, (x1, y1), (x2, y2), BBOX_COLOR, 2)
        send_face(img[y1:y2, x1:x2, : ])
        for j in range(5):
            cv2.circle(img, (int(ll[j]), int(ll[j+5])), 2, BBOX_COLOR, 2)
    return img

def send_face(img):
    # Display the extracted face on the window
    cv2.imshow(WINDOW_NAME2, img)

    # first member is a tuple showing the resolution of the captured face
    json_string = json.dumps( ( img.shape, img.tolist()) )
    local_mqttclient.publish(LOCAL_MQTT_TOPIC, payload=json_string, qos=0, retain=False)

    return img


def loop_and_detect(cap, mtcnn, minsize):
    """Continuously capture images from camera and do face detection."""
    full_scrn = False
    fps = 0.0
    tic = time.time()

    fps_count=10

    while True:
        if cv2.getWindowProperty(WINDOW_NAME, 0) < 0:
            break
#         img = cam.read()
        ret,img = cap.read()
        if img is not None:
            dets, landmarks = mtcnn.detect(img, minsize=minsize)
            print('{} face(s) found'.format(len(dets)))
            img = show_faces(img, dets, landmarks)
            img = show_fps(img, fps)
            cv2.imshow(WINDOW_NAME, img)
            toc = time.time()
            curr_fps = 1.0 / (toc - tic)
            # calculate an exponentially decaying average of fps number
            fps = curr_fps if fps == 0.0 else (fps*0.95 + curr_fps*0.05)
            tic = toc
        fps_count -= 1
        if fps_count == 0:
            print(f"frames: {fps}")
            fps_count = 10
        key = cv2.waitKey(1)
        if key == 27:  # ESC key: quit program
            break
        elif key == ord('F') or key == ord('f'):  # Toggle fullscreen
            full_scrn = not full_scrn
            set_display(WINDOW_NAME, full_scrn)


def main():
    args = parse_args()

    cap = cv2.VideoCapture(0)

    # Attach to messaging
    global local_mqttclient
    local_mqttclient = mqtt.Client("facedetect")
    local_mqttclient.connect(LOCAL_MQTT_HOST, LOCAL_MQTT_PORT,keepalive)


    mtcnn = TrtMtcnn()

    open_window(WINDOW_NAME, args.image_width, args.image_height,
                'Image with Identified Faces')
    open_window(WINDOW_NAME2, int(args.image_width / 4) , int(args.image_height / 4),
                'Extracted Face')
    loop_and_detect(cap, mtcnn, args.minsize)

    cv2.destroyAllWindows()

    del(mtcnn)


if __name__ == '__main__':
    main()
