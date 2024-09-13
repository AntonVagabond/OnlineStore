# Этап 1: Сборка зависимостей и приложения
FROM python:3.11-alpine AS builder

# Установка переменных окружения
ENV LANG=C.UTF-8 \
    LC_ALL=C.UTF-8 \
    # python
    PYTHONDONTWRITEBYTECODE=1 \
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

# Обновление пакетов и установка необходимых инструментов
RUN apk update && \
    apk add --no-cache expat curl && \
    pip install --upgrade pip setuptools && \
    curl -sSL https://install.python-poetry.org | python3 - && \
    apk del curl expat && \
    rm -rf ~/.cache/pip /var/cache/apk/*

# Указываем рабочий каталог
WORKDIR /usr/src/app

# Копируем зависимости проекта и устанавливаем их
COPY pyproject.toml poetry.lock ./
RUN poetry install \
    --only main \
    --no-root \
    --no-interaction \
    --no-ansi \
    --without dev && \
    rm -rf ~/.cache/pypoetry

# Этап 2: Финальный образ
FROM builder as production

# Указываем рабочий каталог
WORKDIR /usr/src/app

# Копируем установленные зависимости из этапа сборки
COPY --from=builder /usr/src/app /usr/src/app

# Создаем нового пользователя
RUN adduser -D user

# Переключаемся на пользователя
USER user

# Копирование кода в контейнер
COPY --chown=user:user . .

# Команда для запуска сервера с помощью Uvicorn для main.py.
ENTRYPOINT ["/bin/sh", "-c", "python main.py"]
