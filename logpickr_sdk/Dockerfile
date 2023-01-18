FROM python:3.6.8-slim

MAINTAINER Fabrice Baranski <fabrice.baranski@igrafx.com>

RUN apt-get update && \
	pip install --upgrade pip

ADD logpickr_sdk /tmp/logpickr_sdk
ADD ./setup.py /tmp/setup.py

RUN cd /tmp/ && \
    pip install .

RUN find -type d -name __pycache__ -prune -exec rm -rf {} \; && \
    rm -rf ~/.cache/pip