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
RUN curl https://bootstrap.pypa.io/get-pip.py
RUN python3 get-pip.py
RUN pip3 install ansible-lint
