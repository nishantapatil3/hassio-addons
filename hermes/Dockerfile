FROM docker.io/nousresearch/hermes-agent:v2026.8.3@sha256:16788311e2fa3035456bdc1bafb8ec2b1777db64ebf020af9bb7eb73c3712c9e

ARG BUILD_ARCH
ARG BUILD_VERSION

USER root
COPY rootfs /

RUN chmod 0755 /usr/local/bin/hermes-addon

EXPOSE 8642 9119

LABEL \
    io.hass.arch="${BUILD_ARCH}" \
    io.hass.description="Self-improving AI agent with Home Assistant integration" \
    io.hass.name="Hermes Agent" \
    io.hass.type="app" \
    io.hass.version="${BUILD_VERSION}" \
    org.opencontainers.image.source="https://github.com/nishantapatil3/hassio-addons"

# The wrapper configures Home Assistant options and then execs the upstream
# dispatcher, keeping Hermes' s6-overlay process supervisor as PID 1.
ENTRYPOINT ["/usr/local/bin/hermes-addon"]
