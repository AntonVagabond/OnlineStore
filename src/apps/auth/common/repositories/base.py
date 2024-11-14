from redis.asyncio import Redis


class BaseRepository:
    """Базовый класс репозитория."""

    def __init__(self, session: Redis) -> None:
        self.session = session
