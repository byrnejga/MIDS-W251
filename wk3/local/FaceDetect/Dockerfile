# Dockerfile for alpine-based face recognition with OpenCV
# includes python script to capture and recognize

FROM nvcr.io/nvidia/l4t-base:r32.3.1

# Set timezone so install does not request it interactively
# which doesnt work from docker build
ENV DEBIAN_FRONTEND noninteractive


# Install the detection script
COPY ./py/detect.py bin/
RUN chmod +x bin/detect.py


# Install the numpy library needed by the script
RUN apt-get update && \
	apt-get install -y python-pip && \
	apt-get install -y tzdata && \
	python2 -m pip install numpy && \
	apt-get install -y python-opencv && \
	apt-get install -y mosquitto-clients && \
	apt-get install -y git-all

# RUN git clone https://github.com/eclipse/paho.mqtt.python

# RUN cd paho.mqtt.python/ && python2 setup.py install

RUN pip install paho-mqtt

# Needed as it includes the cascade files we need to do
# the face detect
ADD ./opencv4.tar /

# CMD /bin/bash
CMD python2 bin/detect.py
