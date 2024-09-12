#!/bin/bash

echo "Создание каталога сертификатов..."
[[ -d config/certs ]] || mkdir config/certs

# Проверьте, существует ли сертификат центра сертификации
if [ ! -f config/certs/ca/ca.crt ]; then
  echo "Генерирование подстановочных SSL-сертификатов для ES (в формате PEM)..."
  bin/elasticsearch-certutil ca --pem --days 3650 --out config/certs/elkstack-ca.zip
  unzip -d config/certs config/certs/elkstack-ca.zip
  bin/elasticsearch-certutil cert \
    --name elkstack-certs \
    --ca-cert config/certs/ca/ca.crt \
    --ca-key config/certs/ca/ca.key \
    --pem \
    --dns "*.localhost,es01,logstash" \
    --days 3650 \
    --out config/certs/elkstack-certs.zip
  echo "Разархивировать SSL-сертификаты из zip-файла..."
  unzip -d config/certs config/certs/elkstack-certs.zip
else
  echo "Сертификат центра сертификации уже существует. Генерация сертификатов пропускается."
fi

echo "Проверка готовности Elasticsearch..."
until curl -s --cacert config/certs/ca/ca.crt -u "elastic:elastic_store" https://es01:9200 | grep -q "elk"; do sleep 10; done

echo "Установить пароль для kibana_system..."
if curl -sk -XGET --cacert config/certs/ca/ca.crt "https://es01:9200" -u "kibana_system:kibana_store" | grep -q "elk"; then
  echo "Пароль для kibana_system работает. Продолжаем настройку Elasticsearch для kibana_system."
else
  echo "Не удалось авторизоваться с помощью пароля kibana_system. Пытаюсь установить пароль для kibana_system."
  until curl -s -XPOST --cacert config/certs/ca/ca.crt -u "elastic:elastic_store" -H "Content-Type: application/json" https://es01:9200/_security/user/kibana_system/_password -d "{\"password\":\"kibana_store\"}" | grep -q "^{}"; do sleep 10; done
fi

echo "Настройка завершена!"