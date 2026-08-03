# LiteLLM

## Setup

1. Install and start the add-on.
2. On first start the add-on writes a default `litellm.yaml` to the config folder
   and stops with instructions.
3. Edit `/addon_configs/a1fb5371_litellm/litellm.yaml` — at minimum set:
   - `general_settings.master_key` — a strong key starting with `sk-` (clients use this to authenticate).
   - `api_key` on each model entry — your [OpenRouter API key](https://openrouter.ai/keys).
4. Restart the add-on.

For Claude Code, set `ANTHROPIC_BASE_URL` to `http://HOME_ASSISTANT_IP:4000`
and `ANTHROPIC_API_KEY` to your configured `master_key`.

## Configuration

All configuration lives in a single file:

```
/addon_configs/a1fb5371_litellm/litellm.yaml
```

Edit this file directly and restart the add-on to apply changes. It is a
standard [LiteLLM proxy configuration](https://docs.litellm.ai/docs/proxy/configs).

The default file includes commented-out sections for PostgreSQL, Redis, SearXNG,
and NVIDIA NIM — uncomment and fill in the values to enable them.

## PostgreSQL (optional)

Required for the admin UI, virtual keys, and spend tracking.

1. Install the **[PostgreSQL](https://github.com/hassio-addons/addon-postgres)**
   community add-on and start it.
2. Create a database for LiteLLM:
   ```sql
   CREATE USER litellm WITH PASSWORD 'choose-a-password';
   CREATE DATABASE litellm OWNER litellm;
   ```
3. In `litellm.yaml` uncomment and fill in `general_settings.database_url`:
   ```yaml
   database_url: postgresql://litellm:choose-a-password@core-mariadb:5432/litellm
   store_model_in_db: true
   ```

LiteLLM starts without a database, but the admin UI login and key management
will not work.

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
