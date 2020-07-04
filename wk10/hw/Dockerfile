# Dockerfile for alpine-based face recognition with OpenCV
# includes python script to capture and recognize

# FROM w251/tensorflow:dev-tx2-4.3_b132-tf1
FROM w251-tx2-hw9

COPY ./1_dqn_tutorial.ipynb /tmp


# Install the numpy library needed by the script
RUN apt-get update && \
    apt-get install -y jupyter-notebook && \
    apt-get install -y xvfb ffmpeg && \
    python3 -m pip install 'gym==0.10.11' && \
    python3 -m pip install 'imageio==2.4.0' &&\
    python3 -m pip install 'pyglet==1.3.2' &&\
    python3 -m pip install pyvirtualdisplay &&\
    python3 -m pip install tf-agents



# Already in the HW9 image
#RUN  python3 -m pip install PILLOW &&\

RUN rm /usr/bin/python
RUN cd /usr/bin/ && ln -s python3 python

# CMD jupyter notebook --ip=0.0.0.0 --no-browser --allow-root
CMD /bin/bash
