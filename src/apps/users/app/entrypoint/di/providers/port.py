from dishka import Provider, Scope

from app.domain.common.id_generator import IdGenerator
from app.infrastructure.adapters.id_generator import IdGeneratorImpl


def provide_domain_ports(provider: Provider) -> None:
    """Внедрение доменных портов к их адаптерам."""
    provider.provide(IdGeneratorImpl, scope=Scope.REQUEST, provides=IdGenerator)
