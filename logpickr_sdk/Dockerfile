FROM python:3-slim

MAINTAINER Fabrice Baranski <fabrice.baranski@igrafx.com>

ADD logpickr_sdk /tmp/logpickr_sdk
ADD ./setup.py /tmp/setup.py

RUN cd /tmp/ && \
    pip install .

RUN find -type d -name __pycache__ -prune -exec rm -rf {} \; && \
    rm -rf ~/.cache/pip