# Changelog

## 1.0.16

- Add `server_root_path` HA UI option — sets the `SERVER_ROOT_PATH` env var
  for running LiteLLM behind a reverse proxy sub-path (e.g. `/litellm`).

## 1.0.15

- Remove NVIDIA NIM direct section from bundled litellm.yaml.

## 1.0.14

- Add `openrouter_api_key` HA UI option — set your OpenRouter API key in the
  add-on configuration panel without editing litellm.yaml directly.
- Bundled litellm.yaml model entries use `os.environ/OPENROUTER_API_KEY`.

## 1.0.13

- Add `master_key` HA UI option — set your LiteLLM master key in the add-on
  configuration panel without editing litellm.yaml directly.
- Bundled litellm.yaml uses `os.environ/LITELLM_MASTER_KEY`; the HA UI value
  overrides it when set, otherwise the file's own value is used.

## 1.0.12

- Remove HA UI options and schema — litellm.yaml is now the single configuration
  point. Edit /addon_configs/a1fb5371_litellm/litellm.yaml directly.
- Bundled default litellm.yaml uses inline placeholder values instead of
  os.environ/ references; users replace them in the file.
- Launcher no longer reads options.json or injects environment variables.
- Docs rewritten to reflect single-file configuration flow.

## 1.0.11

- Move default litellm.yaml out of the launcher script into a standalone file
  bundled in the image at /etc/litellm-addon/litellm.yaml.
- On first start the launcher copies the bundled file to the config directory
  instead of writing an embedded Python string.

## 1.0.10

- Add-on options now map to environment variables matching the litellm-compose
  .env.example (LITELLM_MASTER_KEY, OPENROUTER_API_KEY, NVIDIA_NIM_API_KEY,
  DATABASE_URL, REDIS_URL, SEARXNG_API_BASE, SERVER_ROOT_PATH, LITELLM_LOG).
- Default litellm.yaml uses os.environ/ references for all sensitive values so
  users only need to fill in the add-on options panel, not edit the yaml file.
- Add server_root_path option (SERVER_ROOT_PATH).
- Add translations for all options with descriptions.
- Update docs to reflect options-driven setup flow.

## 1.0.9

- Add legacy options back to schema to silence HA supervisor warnings about
  unknown options stored from previous addon versions.

## 1.0.8

- Restore full configuration template: NVIDIA NIM model, Redis cache, SearXNG
  web-search, and store_prompts_in_spend_logs — all commented out with
  instructions so users can opt in without consulting external docs.

## 1.0.7

- Remove SQLite database default; PostgreSQL is now required for admin UI and key management.
- Default `litellm.yaml` includes a commented-out `database_url` example with instructions.
- Docs updated with PostgreSQL prerequisite steps.

## 1.0.6

- Replace HA configuration options with a `litellm.yaml` file in the app config folder.
- On first start the app writes a default `litellm.yaml` and exits with instructions.
- Users now edit the file directly for full LiteLLM proxy configuration flexibility.

## 1.0.5

- Set hostname to `litellm` instead of the auto-generated hash-prefixed value.

## 1.0.4

- Fix admin UI "Not connected to DB" error by defaulting to a local SQLite database stored in the app data directory.

## 1.0.3

- Replace legacy `addon_config` map type with `app_config`.

## 1.0.2

- Remove experimental stage tag.

## 1.0.1

- Simplify configuration to `master_key` and `openrouter_api_key` only.
- Prometheus metrics and file/document input guardrail are always enabled.
- Remove optional PostgreSQL, Redis, SearXNG, NVIDIA NIM, and custom config options.
- Use native amd64 and arm64 build runners (no QEMU emulation).

## 1.0.0

- Initial Home Assistant package.
- Package LiteLLM 1.95.0 from the upstream multi-architecture image.
- Add the OpenRouter/Nemotron model mappings from `litellm-compose`.
- Add the file and document input guardrail.
- Add optional external PostgreSQL, Redis, and SearXNG connections.
- Add Prometheus metrics and multi-architecture builds.
