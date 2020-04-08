FROM alpine:3.11
LABEL maintainer="Thomas GUIRRIEC <thomas@guirriec.fr>"
RUN apk add --update --no-cache \
      curl \
      gcc \
      git \
      libffi-dev \
      musl-dev \
      openssh \
      openssl-dev \
      python3 \
      python3-dev \
      sshpass \
      rsync \
    && curl -O https://bootstrap.pypa.io/get-pip.py \
    && python3 get-pip.py \
    && rm get-pip.py \
    && pip --no-cache-dir install \
         ansible-lint \
         bcrypt \
         passlib \
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
        /root/.cache/* \
    && addgroup -g 1000 ansible \
    && adduser -u 1000 -D -h /etc/ansible -s /bin/sh -G ansible ansible
USER ansible
WORKDIR /etc/ansible
CMD ["/usr/bin/ansible", "--version"]
