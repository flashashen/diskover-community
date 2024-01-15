ARG DISKOVER_BASE_VERSION=1.5
FROM diskoverdata/diskover-builder:$DISKOVER_BASE_VERSION as builder

# Install required python3 pip modules
RUN source /opt/venv/bin/activate && pip install --no-cache-dir \
    elasticsearch==7.13.4 \
    confuse==1.6.0 \
    rsa==4.7.2 \
    requests==2.31.0 \
    croniter==1.0.15  \
    boto3==1.18.63


FROM diskoverdata/diskover-base:$DISKOVER_BASE_VERSION as base

## copy the installed libs and activate the virtual env
COPY --from=builder /opt/venv /opt/venv

# add local files - s6 overlay scripts, templates etc.
COPY docker/worker/root/ /

# add application source
COPY diskover/ /opt/diskover

ENV DISKOVERDIR=/root/.config/diskover
WORKDIR /opt/diskover

