import os
import sys
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add app folder to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import your Base and models
from app.database import Base
from app import models

# Alembic Config object
config = context.config

# Interpret the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Set up metadata for 'autogenerate'
target_metadata = Base.metadata   # ✅ this line is key

# Database URL (from .env or default)
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://litebank:litebank@db:5432/litebank_db")
config.set_main_option("sqlalchemy.url", DATABASE_URL)


def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,  # ✅ must be passed here
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
