# LiteLLM

## Setup

Before starting the app, configure these required options:

- `master_key`: a new secret beginning with `sk-`; clients use this key.
- `openrouter_api_key`: your OpenRouter API key.

Generate a master key on another trusted computer with:

```shell
openssl rand -hex 32 | sed 's/^/sk-/'
```

Start the app, then use:

- API base: `http://HOME_ASSISTANT_IP:4000`
- Admin UI: `http://HOME_ASSISTANT_IP:4000/ui`
- Health: `http://HOME_ASSISTANT_IP:4000/health/liveliness`
- Metrics: `http://HOME_ASSISTANT_IP:4000/metrics/`

For Claude Code, set `ANTHROPIC_BASE_URL` to the API base and
`ANTHROPIC_API_KEY` to the configured `master_key`.

## Default models

| Client model alias | OpenRouter model |
| --- | --- |
| `claude-haiku-4-5-20251001` | `nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free` |
| `claude-sonnet-4-6` | `nvidia/nemotron-3-super-120b-a12b:free` |
| `claude-opus-4-8` | `nvidia/nemotron-3-ultra-550b-a55b:free` |

The default guardrail rejects file and document content blocks before a model
call. Image content is allowed and routed to the Haiku alias.

## Optional services

The original Compose project runs several neighboring containers. Home
Assistant manages one container per app, so this package accepts connection
URLs for external instances instead:

- `database_url`: PostgreSQL URL. Required for the admin UI, virtual keys,
  budgets, and persistent spend data. Example:
  `postgresql://user:password@database-host:5432/litellm`.
- `redis_url`: Redis URL for the ten-minute response cache. Example:
  `redis://:password@redis-host:6379/0`.
- `searxng_api_base`: SearXNG base URL for the `searxng-search` tool. Example:
  `http://searxng-host:8080`.
- `nvidia_api_key`: enables the direct `nemotron-3-ultra-550b-a55b` NVIDIA NIM
  route.

Prometheus does not need to run in this container. Point an external
Prometheus server at `http://HOME_ASSISTANT_IP:4000/metrics/`.

## Custom LiteLLM configuration

To replace the generated model configuration:

1. Map or open the app configuration folder.
2. Create a file such as `litellm-custom.yaml` there.
3. Set `custom_config` to `litellm-custom.yaml`.
4. Restart the app.

The app still exports keys and service URLs from its options as these
environment variables: `LITELLM_MASTER_KEY`, `LITELLM_SALT_KEY`,
`OPENROUTER_API_KEY`, `NVIDIA_NIM_API_KEY`, `DATABASE_URL`, `REDIS_URL`, and
`SEARXNG_API_BASE`.

The salt key is generated once and persisted in the app data directory. Do not
delete it after storing encrypted values in PostgreSQL.

## Security

Port 4000 is exposed on the local network. Use a strong master key, keep API
keys private, and place LiteLLM behind a trusted HTTPS reverse proxy before
making it reachable from the internet.
