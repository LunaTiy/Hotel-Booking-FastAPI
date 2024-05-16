import datetime
import logging
from logging import LogRecord
from typing import Any

from pythonjsonlogger import jsonlogger

from app.config import settings

logger = logging.getLogger()
log_handler = logging.StreamHandler()


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record: dict[str, Any], record: LogRecord, message_dict: dict[str, Any]) -> None:
        super().add_fields(log_record, record, message_dict)

        if not log_record.get("timestamp"):
            now = datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
            log_record["timestamp"] = now

        if log_record.get("level"):
            log_record["level"] = log_record["level"].upper()
        else:
            log_record["level"] = record.levelname


formatter = CustomJsonFormatter(
    "%(timestamp)s %(level)s %(message)s %(module)s %(funcName)s"
)

log_handler.setFormatter(formatter)
logger.addHandler(log_handler)
logger.setLevel(settings.log_level)
