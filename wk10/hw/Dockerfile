# DOCKER FILE - FOR X86_64 ONLY.  Required tensorflow 2.2
# apparently not available apparently for aarch64 on the Jetson
# uses tensorflow base image, not the W251 version.
# Loads the version of the image both Nvdida GPU ready and
# including a jupyter server already set up.

# FROM w251/tensorflow:dev-tx2-4.3_b132-tf1
# FROM w251-tx2-hw9
FROM tensorflow/tensorflow:latest-gpu-jupyter

COPY ./1_dqn_tutorial.ipynb /tf
COPY .bash_aliases ~

RUN apt-get update 
RUN apt-get install python-opengl
RUN pip3 uninstall cloudpickle && \
    pip3 install cloudpickle==1.3.0


# RUN apt-get install -y jupyter-notebook 
RUN apt-get install -y xvfb ffmpeg 
RUN apt install -y libgl1-mesa-dev
RUN apt-get install -y libglu1-mesa-dev 
# RUN apt-get install -y python3-pip 
# RUN apt-get install -y build-essential
# RUN apt-get install -y libatlas-base-dev
# RUN apt-get install -y libblas-dev
# RUN apt-get install -y liblapack-dev
# RUN apt-get install -y libatlas-base-dev
# RUN apt-get install -y gfortran
RUN python3 -m pip install --no-cache-dir 'gym==0.10.11' 
RUN python3 -m pip install --no-cache-dir JSAnimation
# RUN python3 -m pip install --no-cache-dir 'imageio==2.4.0' 
# RUN python3 -m pip install --no-cache-dir 'pyglet==1.3.2' 
# RUN python3 -m pip install --no-cache-dir pyvirtualdisplay 
# RUN python3 -m pip install --no-cache-dir 'scipy==1.4.1'
# RUN echo python3 -m pip install --no-cache-dir --extra-index-url https://developer.download.nvidia.com/compute/redist/jp/v43 tensorflow | bash
# RUN python3 -m pip install --no-cache-dir tf-agents==0.4.0



RUN rm -f /usr/bin/python
RUN cd /usr/bin/ && ln -s python3 python

# CMD jupyter notebook --ip=0.0.0.0 --no-browser --allow-root
CMD /bin/bash
