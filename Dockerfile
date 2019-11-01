FROM alpine:3.10
MAINTAINER Thomas GUIRRIEC
RUN apk add --update --no-cache \
    curl \
    gcc \
    git \
    libffi-dev \
    musl-dev \
    openssl-dev \
    python3 \
    python3-dev \
    sshpass
RUN curl -O https://bootstrap.pypa.io/get-pip.py && python3 get-pip.py && rm get-pip.py
RUN pip3 --no-cache-dir install ansible-lint && rm -rf /tmp/*
