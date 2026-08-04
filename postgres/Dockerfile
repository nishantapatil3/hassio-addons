FROM postgres:18-alpine

ARG BUILD_ARCH
ARG BUILD_VERSION

RUN apk add --no-cache jq

COPY rootfs /

RUN chmod 0755 /usr/local/bin/postgres-addon

EXPOSE 5432

HEALTHCHECK --interval=15s --timeout=5s --start-period=30s --retries=5 \
    CMD ["pg_isready", "-U", "postgres"]

LABEL \
    io.hass.arch="${BUILD_ARCH}" \
    io.hass.description="PostgreSQL 18 database" \
    io.hass.name="PostgreSQL 18" \
    io.hass.type="app" \
    io.hass.version="${BUILD_VERSION}" \
    org.opencontainers.image.source="https://github.com/nishantapatil3/hassio-addons"

ENTRYPOINT ["/usr/local/bin/postgres-addon"]
