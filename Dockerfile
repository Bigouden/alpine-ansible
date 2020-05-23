FROM registry.gitlab.com/bigouden/alpine-base:3.11.6
LABEL maintainer="Thomas GUIRRIEC <thomas@guirriec.fr>"
ARG ANSIBLE_VERSION=2.9.9
RUN apk add --no-cache --update --virtual \
      build-dependencies \
        curl \
        gcc \
        libffi-dev \
        musl-dev \
        openssl-dev \
        python3-dev \
    && apk add --no-cache --update \
         git \
         openssh \
         python3 \
         sshpass \
         rsync \
    && curl -O https://bootstrap.pypa.io/get-pip.py \
    && python3 get-pip.py \
    && rm get-pip.py \
    && pip --no-cache-dir install \
         ansible==$ANSIBLE_VERSION \
         ansible-lint \
         bcrypt \
         passlib \
    && apk del build-dependencies \
    && pip uninstall -y pip \
    && rm -rf \
        /lib/apk/db/* \
        /tmp/* \
        /root/.cache \
        /var/cache/* \
    && addgroup -g 1000 ansible \
    && adduser -u 1000 -D -h /etc/ansible -s /bin/sh -G ansible ansible
USER ansible
WORKDIR /etc/ansible
HEALTHCHECK CMD ansible --version || exit 1
CMD ["/usr/bin/ansible", "--version"]
