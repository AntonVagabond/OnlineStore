#!/bin/bash

set -e

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

MIGRATIONS_DIR="app/infrastructure/db/postgres/migrations"

run_migrations() {
    echo -e "${YELLOW}Запуск миграции баз данных...${NC}"
    if alembic upgrade head; then
        echo -e "${GREEN}Миграция завершилась успешно!${NC}"
        return 0
    else
        echo -e "${RED}Ошибка миграции!${NC}"
        return 1
    fi
}

show_migration_status() {
    echo -e "${YELLOW}Статус текущей миграции:${NC}"
    alembic current
    echo -e "${YELLOW}История миграций:${NC}"
    alembic history --verbose
}

main() {
    if [ ! -d "${MIGRATIONS_DIR}" ]; then
        echo -e "${RED}Ошибка: директория миграции не найдена${NC}"
        echo "Пожалуйста, запустите этот скрипт из корневого каталога приложения"
        exit 1
    fi

    if ! run_migrations; then
        exit 1
    fi

    show_migration_status
}

main