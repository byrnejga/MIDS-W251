# Dockerfile for alpine-based forwarder

FROM alpine

ENV localbroker=tx2broker

# install mosquitto broker, libraries and clients
RUN apk update
RUN apk add python2
RUN apk add py-pip
RUN apk add --no-cache --purge -uU mosquitto mosquitto-libs mosquitto-clients

COPY py/mqttforwarder.py /bin/mqttforwarder.py

RUN pip install paho-mqtt

# CMD ash
CMD python2 /bin/mqttforwarder.py
