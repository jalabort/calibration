FROM continuumio/miniconda3

# Configure quilt
ENV QUILT_PRIMARY_PACKAGE_DIR /root/output/quilt_packages
ENV QUILT_BASE /root/.local/share/QuiltCli
RUN mkdir -p $QUILT_BASE

# Configure pip
RUN echo '{"registry_url": "http://52.70.18.116"}' > $QUILT_BASE/config.json
RUN mkdir -p /root/.pip/ && printf "[global]\nextra-index-url = http://54.161.171.57/simple/\ntrusted-host = 54.161.171.57\n"

# Install Python Packages
ENV PYTHONDONTWRITEBYTECODE=true
RUN pip install jupyter black
RUN jupyter nbextension install https://github.com/drillan/jupyter-black/archive/master.zip \
    && jupyter nbextension enable jupyter-black-master/jupyter-black
RUN pip install fastai 
RUN conda clean -afy \
    && find /opt/conda/ -follow -type f -name '*.a' -delete \
    && find /opt/conda/ -follow -type f -name '*.pyc' -delete \
