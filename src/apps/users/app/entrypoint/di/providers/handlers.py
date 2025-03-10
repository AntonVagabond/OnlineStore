from dishka import Provider, Scope

from app.application.user.commands.create_user import CreateUserHandler

# class HandlersProvider(Provider):
#     """Провайдер для Обработчиков."""
#
#     scope = Scope.REQUEST
#
#     create_user = provide(CreateUserHandler)


def provide_application_handlers(provider: Provider) -> None:
    """Провайдер для обработчиков приложения."""

    provider.provide(CreateUserHandler, scope=Scope.REQUEST)
