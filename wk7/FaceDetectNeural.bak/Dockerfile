# Dockerfile for face recognition with neural network
# includes python script to capture and recognize

FROM nvcr.io/nvidia/l4t-base:r32.3.1
# FROM w251/tensorflow:dev-tx2-4.3_b132-tf1



# Set timezone so install does not request it interactively
# which doesnt work from docker build
ENV DEBIAN_FRONTEND noninteractive

# Change link so "python" links to "python3"
# RUN cd /usr/bin && rm python && ln -s python3 python

# Install the detection script
COPY ./py/detectneural.py /bin/
RUN  chmod +x /bin/detectneural.py
# COPY ./data/frozen_inference_graph_face.pb /bin/
# COPY ./data/warriors.jpg /bin/
# COPY ./tf_trt_models /tmp/tf_trt_models
COPY ./paho.mqtt.python /tmp/paho.mqtt.python


# Install the numpy library needed by the script
RUN apt-get update 
RUN apt-get install -y python-pip 
RUN apt-get install -y python3-pip 
RUN pip3 install -U pip testresources setuptools
RUN apt-get install -y python-matplotlib 
RUN apt-get install -y python-numpy 
RUN apt-get install -y wget 
RUN apt-get install -y cheese 
RUN apt-get install -y python-opencv 
RUN apt-get install -y mosquitto-clients 
RUN pip install numpy 
RUN pip install pycuda 

# Tensorflow and prerequisites
RUN apt-get install -y libhdf5-serial-dev
RUN apt-get install -y hdf5-tools
RUN apt-get install -y libhdf5-dev
RUN apt-get install -y zlib1g-dev
RUN apt-get install -y zip
RUN apt-get install -y libjpeg8-dev
RUN apt-get install -y liblapack-dev
RUN apt-get install -y libblas-dev
RUN apt-get install -y gfortran

RUN pip3 install -U numpy==1.16.1
RUN pip3 install -U future==0.17.1
RUN pip3 install -U mock==3.0.5
RUN pip3 install -U h5py==2.9.0
RUN pip3 install -U keras_preprocessing==1.0.5
RUN pip3 install -U keras_applications==1.0.8
RUN pip3 install -U gast==0.2.2
RUN pip3 install -U futures
RUN pip3 install -U protobuf
RUN pip3 install -U pybind11

RUN pip3 install --pre --extra-index-url https://developer.download.nvidia.com/compute/redist/jp/v44 tensorflow


# RUN apt-get install python-libnvinfer-dev
# RUN pip install python-tensorrt 
# RUN pip install pycocotools 
RUN apt-get install -y git-all


RUN cd /tmp/tf_trt_models/ && ls -la && bash install.sh 
# RUN cd /tmp/tf_trt_models/ && ls -la && bash install.sh python3
RUN cd /tmp/paho.mqtt.python/ && ls -la && python setup.py install


CMD /bin/bash
# CMD python2 bin/detectneural.py
