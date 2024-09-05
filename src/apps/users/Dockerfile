# Базовый образ.
FROM python:3.11-alpine

ENV LANG=C.UTF-8 \
    LC_ALL=C.UTF-8 \
    # python
    # Предотвращает копирование файлов pyc в контейнер.
    PYTHONDONTWRITEBYTECODE=1 \
    # Гарантирует, что выходные данные python регистрируются в терминале контейнера.
    PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    # pip
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    PIP_ROOT_USER_ACTION=ignore \
    # poetry
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_VIRTUALENVS_IN_PROJECT=false \
    POETRY_NO_INTERACTION=1 \
    POETRY_VERSION=1.8.0

ENV PATH="$PATH:$POETRY_HOME/bin"


RUN apk update && \
    apk add --upgrade --no-cache expat curl && \
    pip install --upgrade pip setuptools && \
    curl -sSL https://install.python-poetry.org | python3 - && \
    apk del curl expat && \
    rm -rf ~/.cache/pip /var/cache/apk/*

# Указываем рабочий каталог
WORKDIR /usr/src/app

# Установка зависимостей проекта с помощью Poetry.
COPY pyproject.toml poetry.lock ./

# Настройка poetry
RUN poetry config virtualenvs.create false && \
    poetry install \
    --only main \
    --no-root \
    --no-interaction \
    --no-ansi \
    --without test && \
    rm -rf ~/.cache/pypoetry && \
    # Устанавливаем adduser
    adduser -D user

# Переключаемся на пользователя
USER user

# Копирование кода в контейнер.
COPY --chown=user:user . .

# Команда для запуска сервера с помощью Uvicorn для main.py.
ENTRYPOINT ["/bin/sh", "-c", "alembic upgrade head && python main.py"]
