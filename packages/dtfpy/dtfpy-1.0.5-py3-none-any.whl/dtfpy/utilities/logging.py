import json
import os
import requests
import logging
from time import sleep
from uuid import UUID
from dataclasses import dataclass
from logging.handlers import RotatingFileHandler
from fastapi.encoders import jsonable_encoder


@dataclass
class DTLog:
    log_type: str | None = None
    subject: str | None = None
    controller: str | None = None
    message: str | None = None
    user_id: str | UUID | None = None
    dealer_id: str | UUID | None = None
    payload: dict | list = None

    def __post_init__(self):
        if self.log_type not in ['warning', 'info', 'error']:
            self.log_type = 'info'

        self.user_id = self._convert_to_uuid(self.user_id)
        self.dealer_id = self._convert_to_uuid(self.dealer_id)

    @staticmethod
    def _convert_to_uuid(value):
        if isinstance(value, str):
            try:
                return UUID(value)
            except ValueError:
                raise ValueError(f"Invalid UUID string: {value}")
        return value

    def __str__(self):
        return f'{self.subject} - {self.controller} - {self.message}' + (f" - {json.dumps(self.payload, default=str)}" if self.payload else "")


class CustomFormatter(logging.Formatter):
    def __init__(self):
        super().__init__(None, '%Y-%m-%d %H:%M:%S')

    def format(self, record):
        if hasattr(record, 'details'):
            self._style._fmt = '%(asctime)s - %(levelname)s - %(details)s'
        else:
            self._style._fmt = '%(asctime)s - %(levelname)s - %(message)s'
        return super().format(record)


class DTLogger:
    def __init__(self, service_name, logging_api_url, logging_api_key):
        self.api_url = logging_api_url
        self.api_key = logging_api_key
        self.service_name = service_name

        self.headers = {
            "Authorization": f"{self.api_key}",
            "Content-Type": "application/json"
        }

    def log(
            self,
            log_type: str = "info",
            controller: str | None = None,
            subject: str | None = None,
            message: str | None = None,
            user_id: str | None = None,
            dealer_id: str | None = None,
            payload: dict | list = None
    ):
        max_retries = 5
        backoff_seconds = 3
        for attempt in range(1, max_retries + 1):
            try:
                response = requests.post(
                    url=f'{self.api_url}/{self.service_name}/log',
                    json=jsonable_encoder({
                        'log_type': log_type,
                        'controller': controller,
                        'subject': subject,
                        'message': message,
                        'user_id': user_id,
                        'dealer_id': dealer_id,
                        'payload': payload
                    }),
                    headers=self.headers
                )
                response.raise_for_status()
                return True
            except requests.exceptions.RequestException as e:
                if attempt < max_retries:
                    sleep(backoff_seconds)
                else:
                    logging.error(f"Failed to send log to API: {e}")
                    raise


class DTLoggerHandler(logging.Handler):
    def __init__(self, service_name, logging_api_url, logging_api_key):
        super().__init__()
        self.logger = DTLogger(
            service_name=service_name,
            logging_api_url=logging_api_url,
            logging_api_key=logging_api_key,
        )

    def emit(self, record):
        log_entry = self.format(record)
        log_type = record.levelname.lower()
        details: DTLog = record.__dict__.get('details')
        if details is not None:
            self.logger.log(
                log_type=details.log_type or log_type,
                subject=details.subject or log_entry.split("-", 1)[0].strip(),
                controller=details.controller or record.funcName,
                message=details.message or log_entry,
                user_id=details.user_id or None,
                dealer_id=details.dealer_id or None,
                payload=details.payload or None,
            )
        elif log_type in ['error']:
            self.logger.log(
                log_type=log_type,
                subject='System Log',
                controller=record.funcName,
                message=log_entry,
                user_id=None,
                dealer_id=None,
                payload=None,
            )


def get_handlers_data():
    formatter = CustomFormatter()

    service_name = os.getenv("SERVICE_NAME")
    logging_api_url = os.getenv("LOGGING_MS_URL")
    logging_api_key = os.getenv("LOGGING_MS_KEY")

    log_print = bool(os.getenv("LOG_PRINT", False))
    log_store = bool(os.getenv("LOG_STORE", False))
    log_level = getattr(logging, str(os.getenv("LOG_LEVEL", 'error')).upper())

    handlers = []

    if logging_api_url and logging_api_key and service_name:
        api_handler = DTLoggerHandler(
            service_name=service_name,
            logging_api_url=logging_api_url,
            logging_api_key=logging_api_key,
        )
        api_handler.setLevel(log_level)
        api_handler.setFormatter(formatter)
        handlers.append(api_handler)

    if log_print:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)
        console_handler.setFormatter(formatter)
        handlers.append(console_handler)

    if log_store:
        rotating_handler = RotatingFileHandler('app.log', maxBytes=5 * 1024 * 1024, backupCount=10)
        rotating_handler.setLevel(log_level)
        rotating_handler.setFormatter(formatter)
        handlers.append(rotating_handler)

    return handlers, log_level


def configure_dt_logging():
    handlers, log_level = get_handlers_data()
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)

    celery_logger = logging.getLogger('celery')
    celery_logger.setLevel(log_level)

    for handle in handlers:
        root_logger.addHandler(handle)
        celery_logger.addHandler(handle)


def create_celery_logger_handler(logger, propagate):
    handlers, log_level = get_handlers_data()
    logger.logLevel = log_level
    logger.propagate = propagate
    for handle in handlers:
        logger.addHandler(handle)


def leave_a_footprint(
        log_type: str,
        controller: str,
        subject: str | None = None,
        message: str | None = None,
        dealer_id: UUID | None = None,
        user_id: str | None = None,
        payload: dict | list | None = None,
):
    logger = logging.getLogger()

    data = dict(
        msg=message,
        extra={
            'details': DTLog(
                log_type=log_type,
                controller=controller,
                subject=subject,
                message=message,
                user_id=user_id,
                dealer_id=dealer_id,
                payload=payload,
            ),
        }
    )

    if log_type.lower() == "warning":
        logger.warning(**data)
    elif log_type.lower() == "error":
        logger.error(**data)
    else:
        logger.info(**data)
