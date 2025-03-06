#!/bin/bash

set -euo pipefail
IFS=$'\n\t'

APP_NAME="users_service_api"
LOG_DIR="logs"
LOG_FILE="${LOG_DIR}/api_$(date +%Y%m%d_%H%M%S).log"
GUNICORN_CONFIG="config/gunicorn.py"
APP_MODULE="app.entrypoint.main:app_factory"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log() {
    local level=$1
    shift
    local message=$@
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo -e "${timestamp} [${level}] ${message}" | tee -a "${LOG_FILE}"
}

get_app_pid() {
    ps aux | grep "[g]unicorn.*${APP_NAME}" | awk '{print $2}' || echo ""
}

check_if_running() {
    local pid=$(get_app_pid)
    if [ -n "${pid}" ]; then
        log "ERROR" "Приложение уже запущено с помощью PID ${pid}"
        exit 1
    fi
}

setup_directories() {
    mkdir -p "${LOG_DIR}" || {
        log "ERROR" "Не удалось создать каталог для логирования"
        exit 1
    }
}

shutdown() {
    log "INFO" "Принятый сигнал выключения"
    local pid=$(get_app_pid)
    if [ -n "${pid}" ]; then
        log "INFO" "Sending graceful shutdown signal to PID ${pid}"
        kill -TERM "${pid}" 2>/dev/null || true

        local timeout=30
        while ps -p "${pid}" >/dev/null 2>&1 && [ ${timeout} -gt 0 ]; do
            sleep 1
            timeout=$((timeout - 1))
        done

        if ps -p "${pid}" >/dev/null 2>&1; then
            log "WARNING" "Процесс завершился не корректно, принудительное завершение работы"
            kill -9 "${pid}" 2>/dev/null || true
        fi
    fi
    exit 0
}

start_application() {
    log "INFO" "Starting ${APP_NAME}..."

    export PYTHONPATH="${PYTHONPATH:+${PYTHONPATH}:}${PWD}"

    exec gunicorn --config "${GUNICORN_CONFIG}" --name "${APP_NAME}" "${APP_MODULE}"
}

main() {
    trap shutdown SIGTERM SIGINT SIGQUIT

    echo -e "${YELLOW} Создание каталога для логирования ${NC}"
    setup_directories
    echo -e "${GREEN} Каталога для логирования успешно создан ${NC}"

    echo -e "${YELLOW} Проверка на повторный запуск приложения${NC}"
    check_if_running
    echo -e "${GREEN} Приложение повторно не запущено${NC}"

    echo -e "${YELLOW} Запуск приложения${NC}"
    start_application
    echo -e "${GREEN} Приложение успешно запущено${NC}"
}

main