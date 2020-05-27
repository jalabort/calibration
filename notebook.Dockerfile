ARG CUDA_VERSION=10.2
ARG CUDNN_VERSION=7
ARG UBUNTU_VERSION=18.04
FROM nvidia/cuda:${CUDA_VERSION}-cudnn${CUDNN_VERSION}-runtime-ubuntu${UBUNTU_VERSION}
 
# Dockerfile info
LABEL maintainer="Wyscout"
LABEL version="0.0.1"
LABEL description="Base GPU docker image for experimenting with camera calibation."
 
# Update and install packages
RUN apt-get update -y && \
    apt-get install -y --no-install-recommends wget bzip2 build-essential vim htop && \
    rm -rf /var/lib/apt/lists/*
 
# Set up CUPTI (CUDA Performance Tool Interface)
ENV LD_LIBRARY_PATH /usr/local/cuda/extras/CUPTI/lib64:$LD_LIBRARY_PATH
 
# Configure Quilt
ENV QUILT_PRIMARY_PACKAGE_DIR /root/output/quilt_packages
ENV QUILT_BASE /root/.local/share/QuiltCli
RUN mkdir -p $QUILT_BASE && echo '{"registry_url": "http://52.70.18.116"}' > $QUILT_BASE/config.json
 
# Install Miniconda
ARG MINICONDA_VERSION=4.6.14
RUN wget https://repo.continuum.io/miniconda/Miniconda3-${MINICONDA_VERSION}-Linux-x86_64.sh \
    --quiet -O miniconda.sh && bash ./miniconda.sh -b && rm miniconda.sh
ENV PATH $PATH:/root/miniconda3/bin/
 
# Install Python 3.7 and PIP
ENV PYTHONDONTWRITEBYTECODE=true
RUN conda install python=3.7 && conda install pip -y
 
# Point PIP to Huld PyPI
RUN mkdir -p /root/.pip/ && echo '[global]\n\
index-url = https://pypi.python.org/simple/\n\
extra-index-url = http://54.161.171.57/simple/\n\
trusted-host = 54.161.171.57' >> /root/.pip/pip.conf

# Install Python Packages
RUN pip install jupyter black
RUN jupyter nbextension install https://github.com/drillan/jupyter-black/archive/master.zip \
    && jupyter nbextension enable jupyter-black-master/jupyter-black
RUN pip install fastai
RUN pip install opencv-python

# Clean conda env
RUN conda clean -afy \
    && find /root/miniconda3/ -follow -type f -name '*.a' -delete \
    && find /root/miniconda3/ -follow -type f -name '*.pyc' -delete \
