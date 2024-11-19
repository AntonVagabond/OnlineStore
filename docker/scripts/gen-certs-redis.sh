#!/bin/bash

# Функция для создания сертификатов
generate_cert() {
    local name=$1
    local cn="$2"
    local opts="$3"

    local keyfile=certs/${name}.key
    local certfile=certs/${name}.crt

    # Проверка на наличие приватного ключа и создание, если его нет
    [ -f $keyfile ] || openssl genrsa -out $keyfile 2048
    echo "Создание сертификата для $name..."
    openssl req \
        -new -sha256 \
        -subj "/O=Redis Test/CN=$cn" \
        -key $keyfile | \
        openssl x509 \
            -req -sha256 \
            -CA certs/ca.crt \
            -CAkey certs/ca.key \
            -CAserial certs/ca.txt \
            -CAcreateserial \
            -days 365 \
            $opts \
            -out $certfile
}

# Создание каталога для сертификатов, если его нет
mkdir -p certs
echo "Каталог сертификатов создан или уже существует."

# Проверка наличия корневого сертификата и ключа
if [ ! -f certs/ca.key ]; then
    echo "Создание корневого сертификата..."
    openssl genrsa -out certs/ca.key 4096
    openssl req \
        -x509 -new -nodes -sha256 \
        -key certs/ca.key \
        -days 3650 \
        -subj '/O=Redis Test/CN=Certificate Authority' \
        -out certs/ca.crt
else
    echo "Корневой сертификат уже существует."
fi

# Генерация конфигурации для сертификатов
cat > certs/openssl.cnf <<_END_
[ server_cert ]
keyUsage = digitalSignature, keyEncipherment
nsCertType = server

[ client_cert ]
keyUsage = digitalSignature, keyEncipherment
nsCertType = client
_END_

# Генерация сертификатов
echo "Генерация сертификатов..."
generate_cert server "redis.db" "-extfile certs/openssl.cnf -extensions server_cert"
generate_cert client "auth.api" "-extfile certs/openssl.cnf -extensions client_cert"

# Удаление серийного номера, если он не нужен после завершения
rm -f certs/ca.txt
echo "Очистка временных файлов завершена."
