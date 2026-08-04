# Redis Add-on Documentation

Redis is an in-memory data structure store used as a database, cache, and message broker.

## Configuration

### `password` (optional)

A password that Redis clients must provide via `AUTH` before executing commands.
Leave empty to run without authentication (suitable for a trusted home network).

### `loglevel`

Controls the verbosity of Redis output. Options: `debug`, `verbose`, `notice`, `warning`.
Default: `notice`.

### `appendonly`

When `true`, enables Redis AOF (Append Only File) persistence so data survives restarts.
Default: `false` (in-memory only).

## Connecting

Connect using the hostname of your Home Assistant instance and port `6379`:

```
redis://homeassistant.local:6379
```

With a password:

```
redis://:yourpassword@homeassistant.local:6379
```
