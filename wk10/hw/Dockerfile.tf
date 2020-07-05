# Dockerfile for alpine-based face recognition with OpenCV
# includes python script to capture and recognize

# FROM w251/tensorflow:dev-tx2-4.3_b132-tf1
FROM tensorflow_hw10:pre_tf

RUN python3 -m pip install --no-cache-dir --extra-index-url https://developer.download.nvidia.com/compute/redist/jp/v43 tensorflow

CMD /bin/bash
