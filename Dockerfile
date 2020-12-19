FROM alpine:3.12
LABEL maintainer="Thomas GUIRRIEC <thomas@guirriec.fr>"
ARG ANSIBLE_VERSION=2.10.4
ARG ANSIBLE_LINT_VERSION=4.3.7
ENV ANSIBLE_COLLECTIONS_PATH=/usr/share/ansible/collections
COPY requirements.txt /
RUN apk add --no-cache --update --virtual \
      build-dependencies \
        gcc \
        libffi-dev \
        musl-dev \
        openssl-dev \
        python3-dev \
    && apk add --no-cache --update \
         git \
         openssh-client \
         python3 \
         sshpass \
         rsync \
    && wget -O get-pip.py https://bootstrap.pypa.io/get-pip.py \
    && python3 get-pip.py \
    && rm get-pip.py \
    && pip install --no-cache-dir --no-dependencies --no-binary :all: -r requirements.txt \
    && pip install --no-cache-dir --no-dependencies --no-binary :all: \
         ansible-base==$ANSIBLE_VERSION \
         ansible-lint==$ANSIBLE_LINT_VERSION \
    && apk del build-dependencies \
    && pip uninstall -y wheel pip \
    && rm -rf \
        /root/.ansible \
        /root/.cache \
        /tmp/* \
        /var/cache/* \
    && ansible-galaxy collection install -p $ANSIBLE_COLLECTIONS_PATH ansible.posix \
    && ansible-galaxy collection install -p $ANSIBLE_COLLECTIONS_PATH community.general \
    && addgroup -g 1000 ansible \
    && adduser -u 1000 -D -h /etc/ansible -s /bin/sh -G ansible ansible
USER ansible
WORKDIR /etc/ansible
HEALTHCHECK CMD ansible --version || exit 1
CMD ["/usr/bin/ansible", "--version"]
