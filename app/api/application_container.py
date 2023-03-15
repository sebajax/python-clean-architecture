"""
application container dependency injection
"""
from dependency_injector import containers, providers

from app.core.core_container import CoreContainer
from app.infrastructure.infrastructure_container import InfrastructureContainer
from app.services.service_container import ServiceContainer


class ApplicationContainer(containers.DeclarativeContainer):
    # core
    core_container = providers.Container(
        CoreContainer
    )

    # infrastructure
    infrastructure_container = providers.Container(
        InfrastructureContainer,
        core_container=core_container
    )

    # services
    service_container = providers.Container(
        ServiceContainer,
        infrastructure_container=infrastructure_container
    )
