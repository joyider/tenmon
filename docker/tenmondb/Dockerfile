FROM timescale/timescaledb:latest-pg11

LABEL maintainer="andre@tenforward.io"

EXPOSE 5432

RUN apk add --no-cache \
    bash \
    postgresql-plpython3 \
    postgresql-contrib \
    mosquitto-clients

COPY docker/tenmondb/docker-entrypoint-initdb.d/* ./docker-entrypoint-initdb.d/

COPY docker/tenmondb/healthcheck.sh /usr/local/bin/docker-healthcheck

HEALTHCHECK --interval=15s CMD docker-healthcheck
