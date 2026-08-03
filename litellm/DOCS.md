# LiteLLM

## Prerequisites

The admin UI, virtual keys, and spend tracking require a PostgreSQL database.

1. Install the **[PostgreSQL](https://github.com/hassio-addons/addon-postgres)**
   community add-on and start it.
2. Connect to it and create a database and user for LiteLLM:
   ```sql
   CREATE USER litellm WITH PASSWORD 'choose-a-password';
   CREATE DATABASE litellm OWNER litellm;
   ```
3. Note the host (usually the Home Assistant IP), port (default `5432`),
   database name, username, and password — you will add these to `litellm.yaml`
   in the setup step below.

LiteLLM will start without a database, but the admin UI login and key management
will not work.

## Setup

1. In the add-on **Configuration** tab, set:
   - **Master key** — a strong key starting with `sk-` (clients use this to authenticate).
   - **OpenRouter API key** — from [openrouter.ai/keys](https://openrouter.ai/keys).
2. Start the app once — it writes a default `litellm.yaml` to the app config
   folder and exits with instructions.
3. Restart the app.

The default `litellm.yaml` reads all sensitive values from the add-on options
via `os.environ/` references, so you normally do not need to edit the file.
Edit it to add models, change routing, enable caching, or adjust any other
proxy setting.

For Claude Code, set `ANTHROPIC_BASE_URL` to `http://HOME_ASSISTANT_IP:4000`
and `ANTHROPIC_API_KEY` to your configured `master_key`.

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

## Configuration

`litellm.yaml` is a standard [LiteLLM proxy configuration](https://docs.litellm.ai/docs/proxy/configs).
Edit it to add models, change routing, enable caching, or any other proxy option.

The add-on injects these environment variables into the proxy process, which
`litellm.yaml` can reference with `os.environ/VAR_NAME`:

| Add-on option | Environment variable | Purpose |
| --- | --- | --- |
| `master_key` | `LITELLM_MASTER_KEY` | API authentication key |
| `openrouter_api_key` | `OPENROUTER_API_KEY` | OpenRouter backend |
| `nvidia_api_key` | `NVIDIA_NIM_API_KEY` | NVIDIA NIM backend |
| `database_url` | `DATABASE_URL` | PostgreSQL for admin UI / keys |
| `redis_url` | `REDIS_URL` | Redis response cache |
| `searxng_api_base` | `SEARXNG_API_BASE` | SearXNG web-search |
| `server_root_path` | `SERVER_ROOT_PATH` | Custom base path |
| `log_level` | `LITELLM_LOG` | Log verbosity |
| *(auto-generated)* | `LITELLM_SALT_KEY` | Encrypts stored secrets |

## Security

Port 4000 is exposed on the local network. Use a strong master key, keep API
keys private, and place LiteLLM behind a trusted HTTPS reverse proxy before
making it reachable from the internet.
