# SearXNG Add-on Documentation

SearXNG is a privacy-respecting metasearch engine. It queries multiple search
services without tracking users or building a personal profile.

## Configuration

### `base_url`

The public URL of this SearXNG instance, including a trailing slash. SearXNG
uses it to generate links and redirects. The default is suitable for direct
access on a Home Assistant installation at `homeassistant.local:8080`.

Change it if you use a different hostname, port, or reverse proxy path.

### `image_proxy`

When enabled, SearXNG proxies images through the instance. This improves
privacy but uses additional memory and bandwidth. Default: `true`.

## Custom settings

The add-on creates and persists SearXNG's configuration in the add-on config
directory. Edit `settings.yml` there to configure search engines, themes, and
advanced SearXNG settings, including the instance name, then restart the add-on.

The generated `secret_key` is stored in this file and survives updates. Do not
share it publicly.

## Connecting

Open the SearXNG web interface at:

```text
http://homeassistant.local:8080
```

The search API is available from SearXNG's normal `/search` endpoint. Enable
the desired response format in `settings.yml` before using API clients.
