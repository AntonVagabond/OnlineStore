#!/bin/bash

# Укажите путь к каталогу сертификатов
CERTS_DIR="/certs"

# Создание каталога сертификатов, если он не существует
echo "Создание каталога сертификатов..."
mkdir -p "$CERTS_DIR"

# Проверьте, существуют ли корневой сертификат и закрытый ключ для Redis
if [ ! -f "$CERTS_DIR/ca.crt" ] || [ ! -f "$CERTS_DIR/redis.key" ]; then
  echo "Генерация сертификатов и ключей для Redis..."

  # Генерация корневого сертификата (CA), если он не существует
  if [ ! -f "$CERTS_DIR/ca.key" ]; then
    echo "Создаем корневой сертификат (CA)..."
    openssl genpkey -algorithm RSA -out "$CERTS_DIR/ca.key"
    openssl req -x509 -new -nodes -key "$CERTS_DIR/ca.key" -sha256 -days 3650 -out "$CERTS_DIR/ca.crt" -subj "/CN=MyRedisRootCA"
  else
    echo "Корневой сертификат (CA) уже существует."
  fi

  # Генерация закрытого ключа для Redis
  if [ ! -f "$CERTS_DIR/redis.key" ]; then
    echo "Создаем закрытый ключ для Redis..."
    openssl genpkey -algorithm RSA -out "$CERTS_DIR/redis.key"
    chmod 644 "$CERTS_DIR/redis.key"
  else
    echo "Закрытый ключ для Redis уже существует."
  fi

  # Создание запроса на сертификат для Redis
  if [ ! -f "$CERTS_DIR/redis.crt" ]; then
    echo "Создаем запрос на сертификат для Redis..."
    openssl req -new -key "$CERTS_DIR/redis.key" -out "$CERTS_DIR/redis.csr" -subj "/CN=localhost"

    # Подписываем запрос Redis с корневым сертификатом (CA)
    echo "Подписываем сертификат Redis корневым сертификатом (CA)..."
    openssl x509 -req -in "$CERTS_DIR/redis.csr" -CA "$CERTS_DIR/ca.crt" -CAkey "$CERTS_DIR/ca.key" -CAcreateserial -out "$CERTS_DIR/redis.crt" -days 365 -sha256
  else
    echo "Сертификат Redis уже существует."
  fi

  echo "Сертификаты и ключи созданы в каталоге $CERTS_DIR:"
  ls -l "$CERTS_DIR"
else
  echo "Сертификаты и ключи для Redis уже существуют. Генерация сертификатов пропускается."
fi

echo "Настройка завершена!"