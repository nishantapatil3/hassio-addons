# LiteLLM

## Setup

1. Install and start the add-on.
2. Install and start the PostgreSQL, Redis, and Prometheus add-ons from this repository.
   The defaults use the internal Home Assistant hostnames for these add-ons.
3. On first start the add-on writes a default `litellm.yaml` to the config folder
   and stops with instructions.
4. In the add-on Configuration page, set:
   - `master_key` — a strong key starting with `sk-` (clients use this to authenticate).
   - `openrouter_api_key` — your [OpenRouter API key](https://openrouter.ai/keys).
   - `database_url` — the PostgreSQL connection URL, defaulting to the bundled database.
   - `redis_url` — the Redis connection URL, defaulting to the bundled cache.
5. Restart the add-on.

For Claude Code, set `ANTHROPIC_BASE_URL` to `http://HOME_ASSISTANT_IP:4000`
and `ANTHROPIC_API_KEY` to your configured `master_key`.

## Configuration

Most connection settings are available in the add-on Configuration page. Advanced
LiteLLM settings live in:

```
/addon_configs/a1fb5371_litellm/litellm.yaml
```

Edit this file directly and restart the add-on to apply advanced changes. It is
a standard [LiteLLM proxy configuration](https://docs.litellm.ai/docs/proxy/configs).

The default file enables Redis response caching and Prometheus metrics. The
SearXNG and NVIDIA NIM sections remain optional advanced configuration.

## PostgreSQL (bundled default)

PostgreSQL is used for the admin UI, virtual keys, and spend tracking.

The PostgreSQL add-on in this repository creates the `litellm` database on its
first start. Its default connection URL is:

```text
postgresql://postgres:homeassistant@db21ed7f-postgres:5432/litellm
```

Changing PostgreSQL options after initialization does not change an existing
database; update `database_url` if you use different credentials or a different host.

## Redis (bundled default)

Redis response caching is enabled by default with:

```text
redis://db21ed7f-redis:6379/0
```

If Redis authentication is enabled, update `redis_url` to include the password.

## Prometheus (bundled default)

LiteLLM exposes metrics at `/metrics/`. The Prometheus add-on scrapes this
endpoint by default at `db21ed7f-litellm:4000`.

## Endpoints

| Path | Purpose |
| --- | --- |
| `http://HOME_ASSISTANT_IP:4000` | API base |
| `http://HOME_ASSISTANT_IP:4000/ui` | Admin UI (login: `admin` / `master_key`) |
| `http://HOME_ASSISTANT_IP:4000/health/liveliness` | Health check |
| `http://HOME_ASSISTANT_IP:4000/metrics/` | Prometheus metrics |

## Default models

| Alias | OpenRouter model |
| --- | --- |
| `claude-haiku-4-5-20251001` | `nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free` |
| `claude-sonnet-4-6` | `nvidia/nemotron-3-super-120b-a12b:free` |
| `claude-opus-4-8` | `nvidia/nemotron-3-ultra-550b-a55b:free` |

The file guardrail rejects file and document content blocks before a model call.

## Security

Port 4000 is exposed on the local network. Use a strong master key, keep API
keys private, and place LiteLLM behind a trusted HTTPS reverse proxy before
making it reachable from the internet.
