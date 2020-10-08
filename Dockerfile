FROM alpine:3.12
LABEL maintainer="Thomas GUIRRIEC <thomas@guirriec.fr>"
ARG ANSIBLE_VERSION=2.10.2
ENV ANSIBLE_COLLECTIONS_PATH=/usr/share/ansible/collections
ADD requirements.txt /
RUN apk add --no-cache --update --virtual \
      build-dependencies \
        curl \
        gcc \
        libffi-dev \
        musl-dev \
        openssl-dev \
        python3-dev \
        py3-setuptools \
    && apk add --no-cache --update \
         git \
         openssh \
         py3-cryptography \
         python3 \
         sshpass \
         rsync \
    && curl -O https://bootstrap.pypa.io/get-pip.py \
    && python3 get-pip.py \
    && rm get-pip.py \
    && pip install --no-cache-dir --no-dependencies -r requirements.txt \
    && pip install --no-cache-dir --no-dependencies \
         ansible-base==$ANSIBLE_VERSION \
         ansible-lint \
    && apk del build-dependencies \
    && pip --no-cache-dir install packaging \
    && pip uninstall -y pip \
    && rm -rf \
        /root/.cache \
        /tmp/* \
        /var/cache/* \
    && ansible-galaxy collection install -p /usr/share/ansible/collections community.general \
    && addgroup -g 1000 ansible \
    && adduser -u 1000 -D -h /etc/ansible -s /bin/sh -G ansible ansible
USER ansible
WORKDIR /etc/ansible
HEALTHCHECK CMD ansible --version || exit 1
CMD ["/usr/bin/ansible", "--version"]
