#!/usr/bin/env python2

import paho.mqtt.client as mqtt
import time

LOCAL_MQTT_HOST="tx2broker"
LOCAL_MQTT_PORT=1883
LOCAL_MQTT_TOPIC="/facedetect/local/faces"
CLOUD_MQTT_HOST="52.117.94.104"
CLOUD_MQTT_PORT=1883
CLOUD_MQTT_TOPIC="/facedetect/cloud/faces"

# allows us to get information about errors inside callbacks
def on_log(client, userdata, level, buf):
    # print("on_log:",level,buf)
    if (level == MQTT_LOG_WARNING):
        print("MQTT_WARNING:",buf)
    elif (level == MQTT_LOG_ERR):
        print("MQTT_ERROR:",buf)
        print("Exiting.")
        exit(-1)

def local_on_connect(client, userdata, flags, rc):
    print("Connected to local mqtt broker with result code "+str(rc))
    print("Subscribing...")
    client.subscribe(LOCAL_MQTT_TOPIC)
    print("Completed subscription to " + LOCAL_MQTT_TOPIC)

def cloud_on_connect(client, userdata, flags, rc):
    print("Connected to cloud mqtt broker with result code "+str(rc))

def cloud_on_publish(client,userdata,rc):
    print("Published to cloud mqtt broker with result code "+str(rc))

def on_message(client, userdata, msg):
    print("Received a message - payload: " + str(msg.payload)[:30] + "...")
    # do not need to decode the message, just pass as is,
    # the image processor module will convert back to dataframe
    # and from then to JPG.
    cloud_mqttclient.publish(CLOUD_MQTT_TOPIC, payload=msg.payload, qos=0, retain=False)

print("Setting up Client objects")
local_mqttclient = mqtt.Client(client_id="forwarder_local")
cloud_mqttclient = mqtt.Client(client_id="forwarder_cloud")

print("Adding Callbacks")

local_mqttclient.on_connect = local_on_connect
local_mqttclient.on_message = on_message
local_mqttclient.on_log = on_log

cloud_mqttclient.on_connect = cloud_on_connect
cloud_mqttclient.on_publish = cloud_on_publish
cloud_mqttclient.on_log = on_log

# set up connection to MQTT broker on the cloud VSI
print("Connecting to cloud broker")
cloud_mqttclient.connect(CLOUD_MQTT_HOST, CLOUD_MQTT_PORT)

# set up connection to MQTT broker on the TX2
print("Connecting to local broker")
local_mqttclient.connect(LOCAL_MQTT_HOST, LOCAL_MQTT_PORT)

print("Starting loop...")

while True:
    local_mqttclient.loop(0.1)
    cloud_mqttclient.loop(0.1)

