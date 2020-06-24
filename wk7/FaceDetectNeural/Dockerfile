# Dockerfile for face recognition with neural network
# includes python script to capture and recognize
# HAD TO CONVERT TO PYTHON3 TO USE TENSORRT

# FROM nvcr.io/nvidia/l4t-base:r32.3.1
FROM w251/tensorflow:dev-tx2-4.3_b132-tf1



# Set timezone so install does not request it interactively
# which doesnt work from docker build
ENV DEBIAN_FRONTEND noninteractive

# Change link so "python" links to "python3"
# RUN cd /usr/bin && rm python && ln -s python3 python

# Install the detection script
COPY ./py/detectneural.py /bin/
COPY ./data/frozen_inference_graph_face.pb /bin/
COPY ./data/warriors.jpg /bin/
COPY ./tf_trt_models /tmp/tf_trt_models
COPY ./paho.mqtt.python /tmp/paho.mqtt.python
RUN chmod +x /bin/detectneural.py


# Install the numpy library needed by the script
RUN apt-get update 
RUN apt-get install -y python-pip 
RUN apt-get install -y python-matplotlib 
RUN apt-get install -y python-numpy 
RUN apt-get install -y wget 
RUN apt-get install -y cheese 
RUN apt-get install -y python-opencv 
RUN pip install numpy 
RUN pip install pycuda 
RUN apt-get install python-libnvinfer-dev
RUN pip install python-tensorrt 
RUN pip install pycocotools 
RUN apt-get install -y mosquitto-clients 
RUN apt-get install -y git-all


RUN cd /tmp/tf_trt_models/ && ls -la && bash install.sh 
# RUN cd /tmp/tf_trt_models/ && ls -la && bash install.sh python3
RUN cd /tmp/paho.mqtt.python/ && ls -la && python setup.py install


CMD /bin/bash
# CMD python2 bin/detectneural.py
