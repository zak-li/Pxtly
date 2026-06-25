<br>

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="../../.github/assets/logos/logo-dark.svg">
    <img src="../../.github/assets/logos/logo.svg" alt="Pxtly" width="300">
  </picture>
</p>

<br>

# DB

Schema migrations for the Pxtly PostgreSQL application database, managed via Alembic.

## Initial Setup

Apply the base SQL seeds to an empty database, then initialize the Alembic revision tree:
```bash
alembic stamp head
```

## Creating Migrations

When you modify SQLAlchemy models in the `core/features` directories, generate a new migration automatically:
```bash
alembic revision --autogenerate -m "description of change"
```

Apply the migration to update the schema:
```bash
alembic upgrade head
```

## Configuration

Database connections are handled securely via the `DATABASE_URL` environment variable. Alembic reads the configuration directly from `core.config.settings` to prevent exposing credentials in `alembic.ini`.
