"""
infrastructure dependency injection
"""
from dependency_injector import containers, providers

from app.core.config import get_settings
from app.infrastructure.auth.auth import Auth
from app.infrastructure.cache.redis import CacheClient
from app.infrastructure.repositories.user_repository import UserRepository


class InfrastructureContainer(containers.DeclarativeContainer):
    # core container wiring
    core_container = providers.DependenciesContainer()

    # cache
    redis_provider = providers.Factory(
        CacheClient,
        redis=core_container.cache_provider,
        cache_default_ttl=get_settings().CACHE_DEFAULT_TTL
    )

    # auth
    auth_provider = providers.Singleton(Auth)

    # repositories
    user_repository_provider = providers.Factory(
        UserRepository,
        session_factory=core_container.db_provider.provided.session
    )
