"""
services dependency injection
"""
from dependency_injector import containers, providers

from app.services.create_user_service import CreateUserService


class ServiceContainer(containers.DeclarativeContainer):
    # infrastructure container wiring
    infrastructure_container = providers.DependenciesContainer()

    # services
    create_user_service_provider = providers.Factory(
        CreateUserService,
        auth=infrastructure_container.auth_provider,
        user_repository=infrastructure_container.user_repository_provider
    )
