import asyncio
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context

import sys
import os
# 1. Импортируем dotenv
from dotenv import load_dotenv

# 2. Загружаем переменные из .env
load_dotenv()  # <--- !!! ДОБАВИЛИ

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from app.core.database import Base
from app.models.user import User
from app.models.shared_track import SharedTrack
from app.models.track import Track
from app.models.reactions import Reaction

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


# 3. Функция для подмены URL
def get_url():
    # Берем из переменной окружения
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        # Если в .env пусто, пробуем взять из alembic.ini (как запасной вариант)
        return config.get_main_option("sqlalchemy.url")
    return db_url


def run_migrations_offline() -> None:
    # Используем нашу функцию get_url() вместо config.get_main_option
    url = get_url()  # <--- !!! ИЗМЕНИЛИ
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    # Создаем конфигурацию вручную
    configuration = config.get_section(config.config_ini_section, {})

    # 4. Подменяем URL в конфигурации перед созданием движка
    configuration["sqlalchemy.url"] = get_url()  # <--- !!! ДОБАВИЛИ

    connectable = async_engine_from_config(
        configuration,  # Передаем обновленную конфигурацию
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()