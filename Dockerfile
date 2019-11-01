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
      sshpass \
    && curl -O https://bootstrap.pypa.io/get-pip.py \
    && python3 get-pip.py \
    && rm get-pip.py \
    && pip3 --no-cache-dir install ansible-lint \
    && apk del \
      curl \
      gcc \
      libffi-dev \
      musl-dev \
      openssl-dev \
      python3-dev \
    && rm -rf /tmp/*