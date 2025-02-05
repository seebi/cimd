FROM registry.access.redhat.com/ubi9/ubi-minimal

LABEL maintainer="Sebastian Tramp"
LABEL vendor="Sebastian Tramp"
LABEL url="https://github.com/seebi/cimd"
ENV OC_IMAGE_VENDOR="Sebastian Tramp"
ENV OC_IMAGE_TITLE="cimd"
ENV OC_IMAGE_DESCRIPTION="Collect and share metadata of CI/CD processes."
ENV OC_IMAGE_URL="https://github.com/seebi/cimd"
ENV OC_IMAGE_DOCUMENTATION="https://github.com/seebi/cimd"

ARG TARGETARCH
COPY dist /tmp/dist
ENV PATH=/app/bin:$PATH

RUN echo "I'm building for $TARGETARCH" && \
    microdnf update -y && \
    microdnf upgrade -y && \
    microdnf install -y python3.11 python3.11-pip && \
    ln -s /usr/bin/python3.11 /usr/bin/python && \
    ln -s /usr/bin/pip3.11 /usr/bin/pip && \
    python -m venv /app && \
    source /app/bin/activate && \
    pip install --upgrade pip setuptools

RUN pip install -r /tmp/dist/requirements.txt && \
    pip install --no-deps /tmp/dist/cimd*.tar.gz

RUN microdnf clean all && \
    rm -rf /root/.cache && \
    rm -rf /usr/lib/python3.11/site-packages/*
WORKDIR /data
VOLUME /data
ENTRYPOINT [ "/app/bin/cimd" ]

