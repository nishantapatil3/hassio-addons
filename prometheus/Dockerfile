FROM prom/prometheus:v3.13.2

ARG BUILD_ARCH
ARG BUILD_VERSION

# The launcher reads add-on options and writes the generated configuration.
USER root
COPY rootfs /

RUN chmod 0755 /usr/local/bin/prometheus-addon

EXPOSE 9090

HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
    CMD ["wget", "-q", "-O", "/dev/null", "http://127.0.0.1:9090/-/ready"]

LABEL \
    io.hass.arch="${BUILD_ARCH}" \
    io.hass.description="Prometheus monitoring and time-series database" \
    io.hass.name="Prometheus" \
    io.hass.type="app" \
    io.hass.version="${BUILD_VERSION}" \
    org.opencontainers.image.source="https://github.com/nishantapatil3/hassio-addons"

ENTRYPOINT ["/usr/local/bin/prometheus-addon"]
