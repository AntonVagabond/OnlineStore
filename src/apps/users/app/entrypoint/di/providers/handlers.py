from dishka import Provider, Scope, provide

from app.application.user.commands.create_user import CreateUserHandler


class HandlersProvider(Provider):
    """Провайдер для Обработчиков."""

    scope = Scope.REQUEST

    create_user = provide(CreateUserHandler)
