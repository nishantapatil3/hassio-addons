# PostgreSQL 18 Add-on Documentation

PostgreSQL 18 relational database, packaged as a Home Assistant add-on.
Data is stored in the HA persistent data volume (`/data/postgresql`) and survives add-on updates.

## Configuration

### `POSTGRES_PASSWORD` (required)

Password for the superuser account. Set this before first start — it cannot be changed via
options after the database has been initialized. To change it later, connect and run
`ALTER USER postgres PASSWORD 'newpassword';`.

### `POSTGRES_USER`

Superuser account name. Default: `postgres`.

### `POSTGRES_DB` (optional)

Name of the default database created on first start. Defaults to the value of `POSTGRES_USER`.

## Connecting

Connect using your Home Assistant IP and port `5432`:

```
postgresql://postgres:yourpassword@homeassistant.local:5432/postgres
```

## Notes

- Data is initialized on first start. Changing `POSTGRES_USER` or `POSTGRES_DB` after
  initialization has no effect — the database already exists.
- For pgvector or other extensions, connect and run `CREATE EXTENSION vector;` after install.
