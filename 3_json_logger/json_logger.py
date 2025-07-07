"""
logging_json_logger.py
-------------------------------------------------
Emit log records in **JSON** so they can be parsed by log aggregators
(Elastic, Loki, Datadog, CloudWatch, …).

Requires::

    pip install python-json-logger

Highlights
~~~~~~~~~~
* Uses **python-json-logger** to serialise records as one‑line JSON.
* Adds extra context (hostname, pid, ISO8601 timestamp) via a custom
  *filter* so every log entry has identical keys.
* Still demonstrates multiple handlers: JSON to stdout **and** DEBUG
  plaintext to a rotating file.

Run::

    python logging_json_logger.py

Then inspect ``logs/json_demo.log`` and standard output.
"""

from __future__ import annotations

import json
import logging
import logging.handlers as handlers
import os
import pathlib
import socket
import sys
from datetime import datetime, timezone

from pythonjsonlogger import jsonlogger

# ---------------------------------------------------------------------------
# Paths & constant context
# ---------------------------------------------------------------------------
LOGGER_NAME = __name__
LOG_DIR = pathlib.Path(__file__).with_name("logs")
LOG_DIR.mkdir(exist_ok=True)
LOG_PATH = LOG_DIR / "json_demo.log"

HOSTNAME = socket.gethostname()
PID = os.getpid()

# ---------------------------------------------------------------------------
# Custom filter: inject hostname & pid into every record
# ---------------------------------------------------------------------------
class ContextFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:  # noqa: D401
        record.hostname = HOSTNAME  # type: ignore[attr-defined]
        record.pid = PID            # type: ignore[attr-defined]
        return True


# ---------------------------------------------------------------------------
# JSON formatter (stdout)
# ---------------------------------------------------------------------------
json_fmt = jsonlogger.JsonFormatter(
    fmt="%(asctime)s %(levelname)s %(name)s %(message)s %(hostname)s %(pid)s",
    datefmt="%Y-%m-%dT%H:%M:%S%z",
    rename_fields={
        "asctime": "timestamp",
        "levelname": "level",
    },
    json_default=str,
)


# ---------------------------------------------------------------------------
# Plaintext formatter (file)
# ---------------------------------------------------------------------------
plain_fmt = logging.Formatter(
    fmt="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# ---------------------------------------------------------------------------
# Logger & handlers
# ---------------------------------------------------------------------------
logger = logging.getLogger(LOGGER_NAME)
logger.setLevel(logging.DEBUG)
logger.addFilter(ContextFilter())

# 1. JSON to stdout (INFO+)
json_handler = logging.StreamHandler(stream=sys.stdout)
json_handler.setLevel(logging.INFO)
json_handler.setFormatter(json_fmt)
logger.addHandler(json_handler)

# 2. Rotating plaintext file (DEBUG+)
file_handler = handlers.RotatingFileHandler(
    filename=LOG_PATH,
    maxBytes=1_000_000,
    backupCount=3,
    encoding="utf-8",
)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(plain_fmt)
logger.addHandler(file_handler)

# ---------------------------------------------------------------------------
# Demo payload
# ---------------------------------------------------------------------------

def expensive_operation(x: int) -> int:  # dummy fn
    if x == 13:
        raise ValueError("Bad luck!")
    return x * x


def main() -> None:  # noqa: D401
    logger.info("🚀 Starting JSON logger demo", extra={"stage": "startup"})

    for i in range(15):
        try:
            result = expensive_operation(i)
            logger.debug("%d squared is %d", i, result, extra={"iter": i})
        except ValueError as err:
            logger.error("Computation failed", exc_info=err, extra={"iter": i})

    logger.info("✅ Finished demo run", extra={"records": 15})


if __name__ == "__main__":
    main()
