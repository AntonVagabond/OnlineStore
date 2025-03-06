from dishka import Provider, Scope, provide

from app.entrypoint.config import AppConfig


class AppConfigProvider(Provider):
    """Провайдер для приложения."""

    @provide(scope=Scope.APP)
    def provide_config(self) -> AppConfig:
        """Получение конфигурации приложения."""
        return AppConfig()
