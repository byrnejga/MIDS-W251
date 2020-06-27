#!/usr/bin/env python3

import ibm_boto3
from ibm_botocore.client import Config, ClientError

COS_BUCKET_NAME="byrnej-object-storage-wk3"
COS_ENDPOINT= "https://s3.private.us-east.cloud-object-storage.appdomain.cloud"

#### IBM CLOUD OBJECT STORAGE CREDENTIALS
cred = {
  "apikey": "_z-feA5w0JcgHtbHEAasGXMt17LgpDcjoeJypEXwPil1",
  "endpoints": "https://control.cloud-object-storage.cloud.ibm.com/v2/endpoints",
  "iam_apikey_description": "Auto-generated for key 83a7c37f-905c-46c7-bafc-0f59c424ea67",
  "iam_apikey_name": "byrnej-object-storage-wk3",
  "iam_role_crn": "crn:v1:bluemix:public:iam::::serviceRole:Writer",
  "iam_serviceid_crn": "crn:v1:bluemix:public:iam-identity::a/eda6b7edc8514da3814170714bcfa440::serviceid:ServiceId-de319b19-d7a6-44ef-935b-5209ae611718",
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

##### List all buckets and contents of specified bucket above
print("trying to list buckets")
for bucket in cos.buckets.all():
    print("Bucket Name: {0}".format(bucket.name))
print("trying to list contents")
files = cos.Bucket(COS_BUCKET_NAME).objects.all()
for file in files:
    print(f"Item: {file.key} ({file.size} bytes).")
