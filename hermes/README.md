# Home Assistant app: Hermes Agent

Hermes Agent is the self-improving AI agent from [Nous Research][upstream].
This package runs the official multi-architecture container in gateway mode so
it can persist conversations, memories, skills, and schedules on Home Assistant.

## Features

- Official Hermes Agent container for aarch64 and amd64
- Persistent Hermes state in the Home Assistant app configuration directory
- Home Assistant API and event gateway support through the Supervisor proxy
- Optional Telegram and Discord gateway configuration
- Optional OpenAI-compatible API and authenticated web dashboard
- Upstream s6-overlay supervision retained inside the app container

## Installation

Add this repository to Home Assistant and install the Hermes Agent app.
Configure at least one model provider key, then start the app.

See [DOCS.md](DOCS.md) for setup and security details.

[upstream]: https://github.com/nousresearch/hermes-agent
