# Prometheus Add-on Documentation

Prometheus stores time-series metrics and provides a web UI and HTTP API on port `9090`.
Data is stored in the Home Assistant persistent data volume and survives add-on updates.

## Configuration

### `scrape_interval`

How often Prometheus scrapes targets. Default: `15s`.

### `evaluation_interval`

How often recording and alerting rules are evaluated. Default: `15s`.

### `retention_time`

How long time-series data is retained. Default: `15d`.

### `scrape_litellm`

When `true`, scrape the bundled LiteLLM add-on's `/metrics/` endpoint. Default: `true`.

### `litellm_target`

The LiteLLM host and port to scrape. Default: `db21ed7f-litellm:4000`.

### `scrape_homeassistant`

When `true`, scrape Home Assistant's Prometheus integration at `/api/prometheus`.
Enable the Prometheus integration in Home Assistant first. Default: `false`.

### `homeassistant_target`

The Home Assistant host and port to scrape. Default: `homeassistant.local:8123`.

### `homeassistant_token`

Optional Home Assistant long-lived access token. A token is required when the Home
Assistant Prometheus endpoint requires authentication.

## Connecting

Open the Prometheus web UI at:

```text
http://homeassistant.local:9090
```

The HTTP API is available under `/api/v1`.
