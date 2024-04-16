# kics-scan disable=ae9c56a6-3ed1-4ac0-9b54-31267f51151d,0008c003-79aa-42d8-95b8-1c2fe37dbfe6,4b410d24-1cbe-4430-a632-62c9a931cf1c,d3499f6d-1651-41bb-a9a7-de925fea487b,9513a694-aa0d-41d8-be61-3271e056f36b,f2f903fb-b977-461e-98d7-b3e2185c6118
ARG ALPINE_VERSION="3.19"

FROM alpine:${ALPINE_VERSION} AS builder
COPY --link apk_build_packages apk_packages pip_packages ansible_collections /tmp/
# checkov:skip=CKV_DOCKER_4
# hadolint ignore=DL3018
RUN --mount=type=cache,id=builder_apk_cache,target=/var/cache/apk \
    apk add gettext-envsubst

FROM alpine:${ALPINE_VERSION}
ENV ANSIBLE_CORE_VERSION="2.16.6"
ENV ANSIBLE_LINT_VERSION="24.2.2"
LABEL maintainer="Thomas GUIRRIEC <thomas@guirriec.fr>"
ENV ANSIBLE_FORCE_COLOR=true
ENV ANSIBLE_COLLECTIONS_PATH="/usr/share/ansible/collections"
ENV ANSIBLE_EXPORTER_PORT=8123
ENV ANSIBLE_EXPORTER_LOGLEVEL='INFO'
ENV ANSIBLE_EXPORTER_NAME='ansible-exporter'
ENV SCRIPT='ansible_exporter.py'
ENV USERNAME="ansible"
ENV UID="1000"
ENV VIRTUAL_ENV="/venv"
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
# hadolint ignore=DL3013,DL3018,DL3042,SC2006
RUN --mount=type=bind,from=builder,source=/usr/bin/envsubst,target=/usr/bin/envsubst \
    --mount=type=bind,from=builder,source=/usr/lib/libintl.so.8,target=/usr/lib/libintl.so.8 \
    --mount=type=bind,from=builder,source=/tmp,target=/tmp \
    --mount=type=cache,id=apk_cache,target=/var/cache/apk \
    --mount=type=cache,id=pip_cache,target=/root/.cache \
    --mount=type=cache,id=collections_cache,target=/root/.ansible \
    apk --update add --virtual .build-deps `envsubst < /tmp/apk_build_packages` \
    && apk --update add `envsubst < /tmp/apk_packages` \
    && python3 -m venv "${VIRTUAL_ENV}" \
    && pip install `envsubst < /tmp/pip_packages` \
    && pip uninstall -y setuptools \
    && ansible-galaxy collection install `envsubst < /tmp/ansible_collections` -p "${ANSIBLE_COLLECTIONS_PATH}" \
    && useradd -l -u "${UID}" -U -s /bin/bash -m "${USERNAME}" \
    && apk del .build-deps
COPY --link --chmod=755 ${SCRIPT} ${VIRTUAL_ENV}
COPY --link --chmod=755 entrypoint.sh /
USER ${USERNAME}
WORKDIR /home/${USERNAME}
EXPOSE ${ANSIBLE_EXPORTER_PORT}
HEALTHCHECK CMD ansible --version || exit 1 # nosemgrep
ENTRYPOINT ["/entrypoint.sh"]
