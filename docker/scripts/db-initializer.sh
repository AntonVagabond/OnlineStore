#!/bin/bash

# Параметры подключения к PostgreSQL
DB_NAME_CORE="UserStoreDB"
DB_USER="postgres"

# Функция для проверки существования базы данных и создания её при необходимости
check_and_create_db() {
  local db_name="$1"

  # Проверяем, существует ли база данных
  DB_EXISTS=$(psql -U $DB_USER -tc "SELECT 1 FROM pg_database WHERE datname = '$db_name';" | tr -d '[:space:]')

  # Если база данных не существует, создаем ее
  if [ "$DB_EXISTS" != "1" ]; then
    echo "Database $db_name does not exist. Creating..."
    psql -U $DB_USER -c "CREATE DATABASE \"$db_name\";"
    if [ $? -eq 0 ]; then
      echo "Database $db_name created successfully."
    else
      echo "Error creating database $db_name."
      exit 1
    fi
  else
    echo "Database $db_name initialized successfully."
  fi
}

# Вызываем функцию для каждой базы данных
check_and_create_db "$DB_NAME_CORE"