# Dockerfile for ubuntu with python3 and numpy

##### Base Image
FROM ubuntu


##### Turn off Interactive apt-get to avoid problems with tzone
ENV DEBIAN_FRONTEND noninteractive

############################################################
##### Install packages including python3
############################################################
RUN apt-get update
RUN apt-get install -y python3
RUN apt-get install -y python3-pip

##### Install utilities
RUN apt-get install -y vim

##### Install MQTT messaging and testing clients
RUN apt-get install -y mosquitto-clients
# RUN apt-get install -y mosquitto

############################################################
##### Copy needed files to the image
############################################################

COPY py/imgproc.py /bin/imgproc.py

run mkdir .bluemix

COPY cos_credentials .bluemix/cos_credentials

############################################################
##### Install needed python3 libraries
############################################################
RUN pip3 install --upgrade pip

##### math and arrays
# RUN pip3 install scipy
RUN pip3 install numpy
# RUN pip3 install pandas

##### Python image handling
# RUN pip3 install Pillow
# RUN pip3 install pypng

##### Python Messaging
RUN pip3 install paho-mqtt

##### IBM Cloud Object Storage
RUN pip3 install ibm-cos-sdk

############################################################
##### Default Program to Run
############################################################
# CMD bash
CMD python3 /bin/imgproc.py
