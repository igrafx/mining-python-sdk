FROM python:3.6.8-slim

MAINTAINER iGrafx <support@igrafx.com>

RUN apt-get update && \
	apt-get install ffmpeg libsm6 libxext6  -y && \
	pip install --upgrade pip && \
	pip install Pillow pandas anonympy dask && \
	pip install --no-deps cape-privacy==0.3.0 && \
	pip install toml

ADD igrafx_mining_sdk /tmp/igrafx_mining_sdk
ADD ./setup.py /tmp/setup.py

RUN cd /tmp/ && \
    pip install .

RUN find -type d -name __pycache__ -prune -exec rm -rf {} \; && \
    rm -rf ~/.cache/pip