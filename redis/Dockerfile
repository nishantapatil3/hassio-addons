FROM redis:7-alpine

ARG BUILD_ARCH
ARG BUILD_VERSION

RUN apk add --no-cache jq

COPY rootfs /

RUN chmod 0755 /usr/local/bin/redis-addon

EXPOSE 6379

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["redis-cli", "-p", "6379", "ping"]

LABEL \
    io.hass.arch="${BUILD_ARCH}" \
    io.hass.description="Redis in-memory data store" \
    io.hass.name="Redis" \
    io.hass.type="app" \
    io.hass.version="${BUILD_VERSION}" \
    org.opencontainers.image.source="https://github.com/nishantapatil3/hassio-addons"

ENTRYPOINT ["/usr/local/bin/redis-addon"]
