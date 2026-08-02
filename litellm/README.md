# Home Assistant app: LiteLLM

LiteLLM is an OpenAI-compatible AI gateway. This package adapts the
[litellm-compose](https://github.com/nishantapatil3/litellm-compose) setup for
Home Assistant's single-container app model.

It provides the Compose setup's Claude-compatible model aliases, OpenRouter
Nemotron routes, Prometheus metrics, and file-upload guardrail. PostgreSQL,
Redis, and SearXNG can be connected as external services through app options.

![Supports aarch64 Architecture][aarch64-shield]
![Supports amd64 Architecture][amd64-shield]

[aarch64-shield]: https://img.shields.io/badge/aarch64-yes-green.svg
[amd64-shield]: https://img.shields.io/badge/amd64-yes-green.svg
