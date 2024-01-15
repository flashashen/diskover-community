ARG DISKOVER_BASE_VERSION=1.5
ARG ALPINE_VERSION=3.18

# Copy default S6 setup
FROM diskoverdata/diskover-base:$DISKOVER_BASE_VERSION as base
FROM php:8.3-fpm-alpine${ALPINE_VERSION} as final


RUN apk add nginx openldap-dev python3 && \
    docker-php-ext-configure ldap && \
    docker-php-ext-install ldap && \
    cp /usr/local/etc/php/php.ini-production /usr/local/etc/php/php.ini


ENV PATH="/opt/venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1
#RUN apk add --update --no-cache python3 && ln -sf python3 /usr/bin/python
#RUN python3 -m ensurepip
RUN python3 -m venv /opt/venv && \
    pip install --upgrade pip && \
    pip install jinja2 j2cli


ARG S6_OVERLAY_VERSION="3.1.5.0"
ARG S6_OVERLAY_ARCH="x86_64"

# Diskover images use S6 for initialization that waits on user actions which take an
# indefinite amount of time. So, by default, have S6-overlay wait as long as it takes
ENV S6_CMD_WAIT_FOR_SERVICES_MAXTIME=0

# S6 warnings and errors only
ENV S6_VERBOSITY=1

# Copy S6 staged container start (configure, template, unpack)
COPY --from=base /etc/s6-overlay /etc/s6-overlay

# add s6 overlay
ADD https://github.com/just-containers/s6-overlay/releases/download/v${S6_OVERLAY_VERSION}/s6-overlay-noarch.tar.xz /tmp
RUN tar -C / -Jxpf /tmp/s6-overlay-noarch.tar.xz
ADD https://github.com/just-containers/s6-overlay/releases/download/v${S6_OVERLAY_VERSION}/s6-overlay-x86_64.tar.xz /tmp
RUN tar -C / -Jxpf /tmp/s6-overlay-x86_64.tar.xz && rm /tmp/s6*.xz

# add local files
COPY docker/web/root/ /
RUN chmod 777 /tmp

# add application source
COPY diskover-web/ /var/www

WORKDIR /var/www

## ports and volumes
#EXPOSE 9000

ENTRYPOINT ["/init"]
#CMD ["/usr/local/sbin/php-fpm", "-F"]