import json
import logging
import os
import re
from logging import LogRecord
from typing import Union, TypeAlias, Any

import yaml

LoadData: TypeAlias = dict[
    str, Union[int, bool, dict[str, dict[str, Union[str, None, bool]]]],
]


class LoggerConfig:
    """
    Класс для конфигурирования логирования.
    Этот класс загружает настройки логирования из YAML-файла и проверяет
    существование необходимой директории и файлов
    для логов, создавая их при необходимости.
    """
    @staticmethod
    def __load_config() -> LoadData:
        """Загрузить конфиги для логирования из yml-файла."""
        with open("core/log_config.yml", "r") as config:
            return yaml.load(config, Loader=yaml.FullLoader)

    @classmethod
    def execute_config(cls) -> LoadData:
        """
        Устанавливаем конфигурацию для логирования.
        Помимо этого, проверяем существует ли директория с файлом,
        куда будет записываться все логи.
        Если этой директории и файла нет, то создадим их.
        """
        # Повышаем уровень логирования для watchfiles.main, чтобы не было спама в логах,
        # и не нагружал из-за этого систему.
        logger = logging.getLogger('watchfiles.main')
        logger.setLevel(logging.WARNING)

        if os.path.exists("logs/app.log"):
            return cls.__load_config()
        # Это проверка связана с Докером. В Докере при развёртывании приложения
        # создается директория logs, это связано с названием volume-а,
        # соответственно нам нужно будет только создать файл.
        elif os.path.exists("logs/"):
            open("logs/app.log", "w").close()
            return cls.__load_config()
        else:
            os.mkdir("logs")
            open("logs/app.log", "w").close()
            return cls.__load_config()


class JSONFormatter(logging.Formatter):
    """
    Класс форматтера для логирования,
    который преобразует лог-сообщения в формат JSON.
    Этот класс используется для структурирования логов в формате JSON,
    с поддержкой специальной обработки логов от httpx и uvicorn.
    """
    @staticmethod
    def __httpx_logs(message: str) -> Union[dict[str, str], dict]:
        """Конвертировать данные из строки в словарь для логов httpx."""
        log_pattern = re.compile(
            r"HTTP Request: (?P<http_method>\w+) (?P<http_protocol>https?)://"
            r"(?P<http_path>\S+) \"(?P<http_version>HTTP/\d\.\d) "
            r"(?P<http_status>\d+) (?P<http_status_message>.+)\""
        )

        match = log_pattern.match(message)
        if match:
            return match.groupdict()
        return {}

    @staticmethod
    def __uvicorn_access_logs(message: str) -> Union[dict[str, str], dict]:
        """Конвертировать данные из строки в словарь для логов uvicorn."""
        log_pattern = re.compile(
            r"(?P<client_ip>[\d.]+):(?P<client_port>\d+) - \"(?P<http_method>\w+) "
            r"(?P<http_path>\S+) (?P<http_version>HTTP/\d\.\d)\" (?P<http_status>\d+)"
        )
        match = log_pattern.match(message)
        if match:
            return match.groupdict()
        return {}

    @staticmethod
    def __convert_to_dict_if_str_is_json_type(message: str) -> Union[dict[str, Any], str]:
        """Конвертировать строку в словарь, если она является типом json."""
        try:
            return json.loads(message)
        except json.JSONDecodeError:
            return ""

    def format(self, record: LogRecord) -> str:
        """Отформатировать записи журнала."""
        if record.name.__eq__("httpx"):
            message = self.__httpx_logs(record.getMessage())
        elif record.name.__eq__("uvicorn.access"):
            message = self.__uvicorn_access_logs(record.getMessage())
        else:
            message = record.getMessage()

        if isinstance(message, str):
            message = self.__convert_to_dict_if_str_is_json_type(message)
        log_record = {
            'timestamp': self.formatTime(record, self.datefmt),
            'level': record.levelname,
            'message': message,
            'name': record.name,
            'app': "users",
            'module': record.module,
            'file': record.pathname,
            'line': record.lineno,
            'func': record.funcName,
            'process': record.processName,
            'thread': record.threadName
        }
        return json.dumps(log_record, ensure_ascii=False)


class LoggingFilter(logging.Filter):
    """
    Класс фильтра для логирования.
    Этот класс позволяет фильтровать логи по определенным условиям.
    """
    def filter(self, record: logging.LogRecord) -> bool:
        """Отфильтровать все сообщения, которые не являются словарём."""
        return bool(record.name in ("root", "uvicorn.access", "httpx"))
