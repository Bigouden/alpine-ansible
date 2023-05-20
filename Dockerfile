FROM alpine:3.18
LABEL maintainer="Thomas GUIRRIEC <thomas@guirriec.fr>"
ENV ANSIBLE_FORCE_COLOR=true
ENV ANSIBLE_COLLECTIONS_PATHS="/usr/share/ansible/collections"
ENV ANSIBLE_EXPORTER_PORT=8123
ENV ANSIBLE_EXPORTER_LOGLEVEL='INFO'
ENV ANSIBLE_EXPORTER_NAME='ansible-exporter'
ENV SCRIPT='ansible_exporter.py'
ENV USERNAME="ansible"
ENV UID="1000"
COPY apk_packages /
#checkov:skip=CKV_DOCKER_4
ADD https://bootstrap.pypa.io/get-pip.py /
COPY pip_packages /
COPY ansible_collections /
RUN xargs -a /apk_packages apk add --no-cache --update \
    && python get-pip.py \
    && pip install --no-cache-dir -r pip_packages \
    && xargs -a /ansible_collections ansible-galaxy collection install -p ${ANSIBLE_COLLECTIONS_PATHS} \
    && useradd -l -u ${UID} -U -s /bin/bash -m ${USERNAME} \
    && pip uninstall -y pip \
    && rm -rf \
         /root/.ansible \
         /root/.cache \
         /tmp/* \
         /var/cache/* 
COPY --chown=${USERNAME}:${USERNAME} --chmod=500 ${SCRIPT} /
COPY --chown=${USERNAME}:${USERNAME} --chmod=500 entrypoint.sh /
USER ${USERNAME}
WORKDIR /home/${USERNAME}
EXPOSE ${ANSIBLE_EXPORTER_PORT}
HEALTHCHECK CMD ansible --version || exit 1 # nosemgrep
ENTRYPOINT ["/entrypoint.sh"]
