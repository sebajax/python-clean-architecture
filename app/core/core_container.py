"""
core dependency injection
"""
from dependency_injector import containers, providers

from app.core.cache import Cache
from app.core.config import get_settings
from app.core.database import Database


class CoreContainer(containers.DeclarativeContainer):
    # database connection
    db_provider = providers.Singleton(
        Database,
        db_url=get_settings().assemble_db_connection()
    )
    # cache connection
    cache_provider = providers.Singleton(
        Cache,
        cache_host=get_settings().CACHE_HOST,
        cache_password=get_settings().CACHE_PASSWORD
    )
