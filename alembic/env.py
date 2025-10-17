import os
import sys
from logging.config import fileConfig

from sqlalchemy import create_engine, pool
from alembic import context

# Ensure your app is importable
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from app.database import Base
from app import models  # Ensure all models are imported so Alembic sees them

# Alembic config object
config = context.config

# Set the SQLAlchemy URL from environment variable (Render/GitHub Actions) or fallback
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://litebank:litebank@db:5432/litebank_db"
)
config.set_main_option("sqlalchemy.url", DATABASE_URL)

# Configure logging from Alembic config file
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Target metadata for 'autogenerate'
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode (no DB connection)."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode (connect to DB)."""
    connectable = create_engine(DATABASE_URL, poolclass=pool.NullPool)

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
