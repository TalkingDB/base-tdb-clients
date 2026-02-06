import sys
import logging
from .context import get_log_context


class ColorFormatter(logging.Formatter):
    COLORS = {
        logging.DEBUG: "\033[36m",
        logging.INFO: "\033[32m",
        logging.WARNING: "\033[33m",
        logging.ERROR: "\033[31m",
        logging.CRITICAL: "\033[41m",
    }
    RESET = "\033[0m"

    def format(self, record: logging.LogRecord) -> str:
        color = self.COLORS.get(record.levelno, "")
        record.levelname = f"{color}{record.levelname}{self.RESET}"

        log_ctx = get_log_context() or {}

        event_group_id = log_ctx.get("event_group_id")
        worker_id = log_ctx.get("worker_id")
        function_name = log_ctx.get("function")

        parts = []

        if event_group_id:
            parts.append(f"[{event_group_id}]")
        elif worker_id:
            parts.append(f"[{worker_id}]")

        if function_name:
            parts.append(f"[{function_name}]")

        record.context_prefix = " ".join(parts)

        if record.levelno == logging.INFO and record.context_prefix:
            if function_name:
                record.source = ""
            else:
                record.source = f"[{record.funcName}]"
        else:
            record.source = f"[{record.filename}::{record.funcName}:{record.lineno}]"

        return super().format(record)


def get_logger():
    formatter = ColorFormatter(
        "%(asctime)s %(levelname)-8s "
        "%(context_prefix)s "
        "%(source)s %(message)s"
    )

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)

    # Root logger (your app)
    root = logging.getLogger()
    root.setLevel(logging.INFO)
    root.handlers.clear()
    root.addHandler(handler)

    # --- Uvicorn ---
    uvicorn_error = logging.getLogger("uvicorn.error")
    uvicorn_error.handlers.clear()
    uvicorn_error.propagate = False
    uvicorn_error.addHandler(handler)

    uvicorn_access = logging.getLogger("uvicorn.access")
    uvicorn_access.handlers.clear()
    uvicorn_access.propagate = False
    uvicorn_access.addHandler(handler)

    # --- Gunicorn ---
    gunicorn_error = logging.getLogger("gunicorn.error")
    gunicorn_error.handlers.clear()
    gunicorn_error.propagate = False
    gunicorn_error.addHandler(handler)

    gunicorn_access = logging.getLogger("gunicorn.access")
    gunicorn_access.handlers.clear()
    gunicorn_access.propagate = False
    gunicorn_access.addHandler(handler)

    logging.getLogger("urllib3").setLevel(logging.ERROR)
    logging.getLogger("httpx").setLevel(logging.ERROR)

    return logging.getLogger(__name__)


logger = get_logger()


def show_error(f):
    def inner(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception:
            logger.info({"args": args, "kwargs": kwargs})
            logger.exception("Unhandled exception")
            raise

    return inner
