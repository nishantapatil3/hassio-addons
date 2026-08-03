# LiteLLM

## Setup

1. Start the app once — it will exit after writing a default configuration to
   `litellm.yaml` in this app's configuration folder.
2. Open the file and replace `sk-your-openrouter-api-key` with your
   [OpenRouter API key](https://openrouter.ai/keys) and `sk-change-me` with a
   strong master key starting with `sk-`.
3. Restart the app.

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

The app automatically sets these environment variables that the config file can
reference with `os.environ/VAR_NAME`:

| Variable | Value |
| --- | --- |
| `DATABASE_URL` | SQLite database stored in the app data directory |
| `LITELLM_SALT_KEY` | Stable per-installation key for encrypting stored values |

## Security

Port 4000 is exposed on the local network. Use a strong master key, keep API
keys private, and place LiteLLM behind a trusted HTTPS reverse proxy before
making it reachable from the internet.
