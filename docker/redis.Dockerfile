# Первый этап: установка OpenSSL и генерация сертификатов
FROM debian:stable-slim AS cert-builder

# Установка OpenSSL
RUN apt-get update && apt-get install -y openssl && rm -rf /var/lib/apt/lists/*

# Копирование скрипта для генерации сертификатов
COPY scripts/gen-certs-redis.sh /gen-certs-redis.sh

# Выдача прав на выполнение скрипта
RUN chmod +x /gen-certs-redis.sh

# Запуск скрипта для генерации сертификатов
RUN /gen-certs-redis.sh

# Второй этап: чистый образ Redis с копированием сертификатов
FROM redis:7.4.1-alpine

# Установка переменной для пути сертификатов
ARG CERTS_DIR=/certs

# Копирование сертификатов из предыдущего этапа
COPY --from=cert-builder "$CERTS_DIR" "$CERTS_DIR"

COPY scripts/init-overcommit-memory.sh /init-overcommit-memory.sh

RUN chmod +x /init-overcommit-memory.sh && \
    # Меняем права на этот ключ, чтобы клиент смог его прочитать
    chmod 644 /certs/client.key


# Настройка команд для запуска Redis
CMD ["/bin/sh", "-c", "/init-overcommit-memory.sh && redis-server /usr/local/etc/redis/redis.conf"]