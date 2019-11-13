FROM alpine:3.10
LABEL maintainer="Thomas GUIRRIEC <thomas@guirriec.fr>"
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
    && pip --no-cache-dir install ansible-lint \
    && apk del \
      curl \
      gcc \
      libffi-dev \
      musl-dev \
      openssl-dev \
      python3-dev \
    && pip uninstall -y pip \
    && rm -rf \
      /tmp/* \
      /root/.cache/*
CMD ["/usr/bin/ansible", "--version"]
