FROM alpine:3.16
LABEL maintainer="Thomas GUIRRIEC <thomas@guirriec.fr>"
COPY apk_packages /
COPY pip_packages /
COPY ansible_collections /
RUN xargs -a /apk_packages apk add --no-cache --update \
    && pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r pip_packages \
    && xargs -a /ansible_collections ansible-galaxy collection install -p /usr/share/ansible/collections \
    && addgroup -g 1000 ansible \
    && adduser -u 1000 -D -h /etc/ansible -s /bin/sh -G ansible ansible \
    && pip uninstall -y pip \
    && rm -rf \
         /root/.ansible \
         /root/.cache \
         /tmp/* \
         /var/cache/* 
USER ansible
WORKDIR /etc/ansible
HEALTHCHECK CMD ansible --version || exit 1
ENTRYPOINT ["/bin/sh", "-c", "sleep infinity"]
