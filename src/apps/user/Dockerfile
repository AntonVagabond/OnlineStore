# Базовый образ.
FROM python:3.11-alpine

WORKDIR /usr/src/app

# Настройка env.
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
# Предотвращает копирование файлов pyc в контейнер.
ENV PYTHONDONTWRITEBYTECODE 1
# Гарантирует, что выходные данные python регистрируются в терминале контейнера.
ENV PYTHONFAULTHANDLER 1

# Обновление пакета pip и установка Poetry.
RUN pip install --upgrade pip \
    && pip install poetry \
    && rm -rf ~/.cache/pip


# Установка зависимостей проекта с помощью Poetry.
COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi \
    && rm -rf ~/.cache/pip ~/.cache/pypoetry

# Копирование кода в контейнер.
COPY . .

# Команда для запуска сервера с помощью Uvicorn для main.py.
ENTRYPOINT alembic upgrade head && python main.py
