# Hermes Agent

Hermes Agent runs as a persistent messaging gateway inside Home Assistant.
The app starts the upstream `gateway run` command and keeps all Hermes state in
the app configuration mount at `/opt/data`.

## First start

1. Install the app and open its **Configuration** page.
2. Enter one model provider credential, such as `openrouter_api_key`.
3. Optionally enter Telegram or Discord credentials and an allowlist.
4. Start or restart the app.

The upstream image seeds these files in the app configuration directory on the
first start:

```text
/opt/data/config.yaml
/opt/data/.env
/opt/data/SOUL.md
```

Edit `config.yaml` for model selection, Home Assistant event filters, skills,
toolsets, and other advanced Hermes settings. Add provider or messaging secrets
not exposed in the app options to `.env`, then restart the app.

## Home Assistant integration

The app requests access to the Home Assistant REST and WebSocket API proxy. If
`hass_token` is empty, the app uses the Supervisor token automatically. The
default URL is:

```text
http://supervisor/core
```

For a custom long-lived token or a different Home Assistant host, set both
`hass_token` and `hass_url` in the app configuration.

With `HASS_TOKEN` set, Hermes enables its Home Assistant tools. To receive
real-time state events, add focused filters to `/opt/data/config.yaml`:

```yaml
platforms:
  homeassistant:
    enabled: true
    extra:
      watch_domains:
        - light
        - climate
        - binary_sensor
      watch_entities: []
      ignore_entities:
        - sensor.uptime
      cooldown_seconds: 30
```

No state events are forwarded until at least one of `watch_domains`,
`watch_entities`, or `watch_all` is configured. Hermes can deliver responses as
Home Assistant persistent notifications.

## Telegram and Discord

Set the bot token and an allowlist in the app Configuration page. Keep the
allowlist populated unless the gateway is isolated on a trusted network. The
gateway starts automatically after the app restarts.

Other Hermes platforms and advanced credentials can be configured in
`/opt/data/.env`. Refer to the [upstream environment variable reference][env]
and [messaging documentation][messaging].

## API server

The OpenAI-compatible API is disabled by default. To enable it:

1. Set `api_server_enabled` to `true`.
2. Set an `api_server_key` with at least 8 characters.
3. Assign a host port to internal port `8642` in the app Network settings.
4. Restart the app.

The API binds to the app network at port `8642` and requires the configured
key. Do not expose it directly to the internet.

## Web dashboard

The dashboard is disabled by default. To enable it:

1. Set `dashboard_enabled` to `true`.
2. Set `dashboard_username` and `dashboard_password`.
3. Optionally set `dashboard_secret` to keep login sessions across restarts.
4. Assign a host port to internal port `9119` in the app Network settings.
5. Restart the app and open the app Web UI.

The dashboard binds to all interfaces inside the app and always uses basic
authentication in this package. Keep the port on a trusted network or behind a
reverse proxy with additional access controls.

## Persistence and upgrades

The app configuration mount contains API credentials, OAuth state, sessions,
memories, skills, logs, cron jobs, and the Hermes YAML configuration. Back up
the app before changing versions. Never run two Hermes gateway containers
against the same configuration directory at the same time.

The bundled image is based on the pinned upstream Hermes Agent release. Update
the app when a newer package is published; the mounted Hermes state is retained
across image updates.

[env]: https://hermes-agent.nousresearch.com/docs/reference/environment-variables
[messaging]: https://hermes-agent.nousresearch.com/docs/user-guide/messaging
