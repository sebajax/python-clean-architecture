"""
api dependency injection
"""

from dependency_injector import containers, providers

from app.core.cache import Cache
from app.core.config import get_settings
from app.core.database import Database
from app.infrastructure.auth.auth import Auth
from app.infrastructure.cache.redis import CacheClient
from app.infrastructure.repositories.user_repository import UserRepository
from app.services.create_user_service import CreateUserService


class Container(containers.DeclarativeContainer):
    # wiring configuration
    wiring_config = containers.WiringConfiguration(modules=["app.api.routes.users_route"])

    # core
    db_provider = providers.Singleton(
        Database,
        db_url=get_settings().assemble_db_connection()
    )
    cache_provider = providers.Singleton(
        Cache,
        cache_host=get_settings().CACHE_HOST,
        cache_password=get_settings().CACHE_PASSWORD
    )

    # infrastructure
    redis_provider = providers.Factory(
        CacheClient,
        redis=cache_provider,
        cache_default_ttl=get_settings().CACHE_DEFAULT_TTL
    )
    auth_provider = providers.Singleton(Auth)
    user_repository_provider = providers.Factory(
        UserRepository,
        session_factory=db_provider.provided.session
    )

    # services
    create_user_service_provider = providers.Factory(
        CreateUserService,
        auth=auth_provider,
        user_repository=user_repository_provider
    )
