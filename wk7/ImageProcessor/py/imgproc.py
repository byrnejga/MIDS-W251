#!/usr/bin/env python2

import paho.mqtt.client as mqtt
import numpy as np
# import scipy.misc as misc
import json
import time
import sys
import traceback
# import png
# from PIL import Image
from datetime import datetime

import ibm_boto3
from ibm_botocore.client import Config, ClientError

CLOUD_MQTT_HOST="cloudbroker"
CLOUD_MQTT_PORT=1883
CLOUD_MQTT_TOPIC="/facedetect/cloud/faces"

COS_BUCKET_NAME="byrnej-object-storage-wk3"
COS_ENDPOINT= "https://s3.private.us-east.cloud-object-storage.appdomain.cloud"


#### IBM CLOUD OBJECT STORAGE CREDENTIALS
cred = {
  "apikey": "rqhlDqUlhZaIUoxNoqbezz2384MRydk-h0he1wkUzIiM",
  "endpoints": "https://control.cloud-object-storage.cloud.ibm.com/v2/endpoints",
  "iam_apikey_description": "Auto-generated for key a0578150-577f-4895-9a2b-3a66d8038bfb",
  "iam_apikey_name": "byrnej-object-storage-wk7",
  "iam_role_crn": "crn:v1:bluemix:public:iam::::serviceRole:Writer",
  "iam_serviceid_crn": "crn:v1:bluemix:public:iam-identity::a/eda6b7edc8514da3814170714bcfa440::serviceid:ServiceId-f76673fa-73ac-4342-b7bd-f4c088e8791b",
  "resource_instance_id": "crn:v1:bluemix:public:cloud-object-storage:global:a/eda6b7edc8514da3814170714bcfa440:d4248333-b19f-4e17-9662-66a57ce4df55::"
}


##### Create resource for COS:
cos = ibm_boto3.resource("s3",
      ibm_api_key_id=cred["apikey"],
      ibm_service_instance_id=cred["resource_instance_id"],
      ibm_auth_endpoint="https://iam.bluemix.net/oidc/token",
      config=Config(signature_version="oauth"),
      endpoint_url=COS_ENDPOINT
)

##### Test commands for successful connection to COS
print("trying to list buckets")
for bucket in cos.buckets.all():
    print("Bucket Name: {0}".format(bucket.name))
print("trying to list contents")
files = cos.Bucket(COS_BUCKET_NAME).objects.all()
for file in files:
    print(f"Item: {file.key} ({file.size} bytes).")

def on_connect(client, userdata, flags, rc):
    print("Connected to cloud mqtt broker with result code "+str(rc))
    print("Subscribing...")
    client.subscribe(CLOUD_MQTT_TOPIC)
    print("Completed subscription to " + CLOUD_MQTT_TOPIC)


# allows us to get information about errors inside callbacks
def on_log(client, userdata, level, buf):
    # print("on_log:",level,buf)
    if (level == MQTT_LOG_WARNING):
        print("MQTT_WARNING:",buf)
    elif (level == MQTT_LOG_ERR):
        print("MQTT_ERROR:",buf)
        print("Exiting.")
        exit(-1)

# Error in callbacks are not printed, nor exceptions thrown
# outside the mqtt. Uses on_log to print out the results
def on_message(client, userdata, msg):
    try:
        print("Received a message, payload: " + str(msg.payload)[:30] + "...")

        # create save filename based on time of message
        now = datetime.now()
        file_name = now.strftime("%y%m%d-%H%M%S.%f") + ".json"

        # convert back to array from json formatted string
        m_decode=str(msg.payload.decode("utf-8","ignore"))
        data = json.loads(m_decode)
        print(data[0])

        print(f"Adding json text as '{file_name}' to COS")
        cos.Object(COS_BUCKET_NAME, file_name).put(Body=m_decode)

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


