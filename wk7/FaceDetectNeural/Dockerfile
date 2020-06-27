# Dockerfile for alpine-based face recognition with OpenCV
# includes python script to capture and recognize

FROM tensorrtlab05

# Set timezone so install does not request it interactively
# which doesnt work from docker build
ENV DEBIAN_FRONTEND noninteractive


# Copy over the pre-compiled tensorrt_demos tree
RUN mkdir /tmp/tensorrt_demos
COPY ./tensorrt_demos /tmp/tensorrt_demos

# replace script with updated version
RUN cd /tmp/tensorrt_demos && mv trt_mtcnn.py trt_mtcnn.py.bak
COPY ./py/trt_mtcnn.py /tmp/tensorrt_demos/


# Install the numpy library needed by the script
RUN apt-get update
RUN apt-get install -y tzdata
RUN apt-get install -y python3-opencv
RUN apt-get install -y mosquitto-clients
RUN pip3 install paho-mqtt
RUN apt-get install -y git-all 

# CMD /bin/bash
CMD cd /tmp/tensorrt_demos && python3 trt_mtcnn.py --usb --vid 0 --width 1280 --height 720
