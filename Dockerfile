FROM alpine:3.17
LABEL maintainer="Thomas GUIRRIEC <thomas@guirriec.fr>"
ENV ANSIBLE_FORCE_COLOR=true
ENV USERNAME="ansible"
ENV UID="1000"
COPY apk_packages /
COPY pip_packages /
COPY ansible_collections /
RUN xargs -a /apk_packages apk add --no-cache --update \
    && pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r pip_packages \
    && xargs -a /ansible_collections ansible-galaxy collection install -p /usr/share/ansible/collections \
    && useradd -l -u ${UID} -U -s /bin/bash -m ${USERNAME} \
    && pip uninstall -y pip \
    && rm -rf \
         /root/.ansible \
         /root/.cache \
         /tmp/* \
         /var/cache/* 
USER ${USERNAME}
WORKDIR /home/${USERNAME}
HEALTHCHECK CMD ansible --version || exit 1
ENTRYPOINT ["/bin/sh", "-c", "sleep infinity"]
