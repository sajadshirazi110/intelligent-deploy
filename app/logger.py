import logging
import json
from datetime import datetime


class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "message": record.getMessage(),
            "service": "intelligent-deploy",
            "logger": record.name,
        }

        # capture extra fields
        for key, value in record.__dict__.items():
            if key not in (
                "msg", "args", "levelname", "levelno",
                "pathname", "filename", "module",
                "exc_info", "exc_text", "stack_info",
                "lineno", "funcName", "created",
                "msecs", "relativeCreated", "thread",
                "threadName", "processName", "process",
                "name"
            ):
                log_record[key] = value

        return json.dumps(log_record)


def get_logger(name: str = "app") -> logging.Logger:
    logger = logging.getLogger(name)

    # جلوگیری از duplicate handler
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    handler = logging.StreamHandler()
    handler.setFormatter(JsonFormatter())

    logger.addHandler(handler)
    logger.propagate = False

    return logger
