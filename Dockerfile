FROM alpine:3.16
LABEL maintainer="Thomas GUIRRIEC <thomas@guirriec.fr>"
ENV ANSIBLE_FORCE_COLOR=true
ARG USER="ansible"
ARG UID="1000"
ARG GID="1000"
COPY apk_packages /
COPY pip_packages /
COPY ansible_collections /
RUN xargs -a /apk_packages apk add --no-cache --update \
    && pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r pip_packages \
    && xargs -a /ansible_collections ansible-galaxy collection install -p /usr/share/ansible/collections \
    && useradd -u ${UID} -U -s /bin/bash ${USER} \
    && mkdir /home/${USER} \
    && chown -R ${USER}:${USER} /home/${USER} \
    && pip uninstall -y pip \
    && rm -rf \
         /root/.ansible \
         /root/.cache \
         /tmp/* \
         /var/cache/* 
USER ${USER}
WORKDIR /home/${USER}
HEALTHCHECK CMD ansible --version || exit 1
ENTRYPOINT ["/bin/sh", "-c", "sleep infinity"]
