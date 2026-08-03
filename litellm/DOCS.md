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

Prometheus metrics are exposed at `/metrics/`. Point an external Prometheus
server at `http://HOME_ASSISTANT_IP:4000/metrics/`.

## Security

Port 4000 is exposed on the local network. Use a strong master key, keep API
keys private, and place LiteLLM behind a trusted HTTPS reverse proxy before
making it reachable from the internet.
