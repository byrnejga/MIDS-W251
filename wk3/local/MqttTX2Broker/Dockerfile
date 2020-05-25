# Dockerfile for alpine-based Mosquitto broker
# includes python script to capture and recognize

FROM alpine

# install mosquitto broker, libraries and clients
RUN apk update && \
    apk add --no-cache --purge -uU mosquitto mosquitto-libs mosquitto-clients

EXPOSE 1883

CMD /usr/sbin/mosquitto
