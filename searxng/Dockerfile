FROM docker.io/searxng/searxng:2026.8.4-c63835bd2@sha256:f4c8e59de166ed71f6380c0847c312ca51f0d41996e31d0559163b6b09ecde52

ARG BUILD_ARCH
ARG BUILD_VERSION

USER root
COPY rootfs /

RUN chmod 0755 /usr/local/bin/searxng-addon

# Keep the cache in Home Assistant's persistent app data volume.
ENV __SEARXNG_DATA_PATH="/data/searxng-cache"

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD ["wget", "-q", "-O", "/dev/null", "http://127.0.0.1:8080/"]

LABEL \
    io.hass.arch="${BUILD_ARCH}" \
    io.hass.description="Privacy-respecting metasearch engine" \
    io.hass.name="SearXNG" \
    io.hass.type="app" \
    io.hass.version="${BUILD_VERSION}" \
    org.opencontainers.image.source="https://github.com/nishantapatil3/hassio-addons"

ENTRYPOINT ["/usr/local/bin/searxng-addon"]
