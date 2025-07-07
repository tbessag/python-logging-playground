"""
logging_file_handler.py
---------------------------------
Write logs to **both** standard output *and* a rotating log file.

Key points
~~~~~~~~~~
* **RotatingFileHandler** ‒ keeps each logfile under ``maxBytes`` and
  automatically renames old files (``filename.1``, ``filename.2`` …).
* Re‑uses the same simple formatter so console and file entries look identical.
* Demonstrates that you can attach *multiple* handlers to one logger.

Run directly to generate ~10 KB of dummy log traffic so you can watch the
files roll over.

Usage::

    python logging_file_handler.py

Look for files ``logs/app.log``, ``app.log.1`` etc. afterwards.
"""

from __future__ import annotations

import logging
import logging.handlers as handlers
import pathlib
import random
import string
import sys
from datetime import datetime

# ---------------------------------------------------------------------------
# Logger & formatter setup
# ---------------------------------------------------------------------------
LOGGER_NAME = __name__  # => 'logging_file_handler' when executed directly
LOG_DIR = pathlib.Path(__file__).with_name("logs")
LOG_DIR.mkdir(exist_ok=True)
LOG_PATH = LOG_DIR / "app.log"

# 1. Create (or get) a module‑level logger
logger = logging.getLogger(LOGGER_NAME)
logger.setLevel(logging.DEBUG)

# 2. Shared formatter
fmt = "%(asctime)s | %(name)s | %(levelname)s | %(message)s"
formatter = logging.Formatter(fmt=fmt, datefmt="%Y-%m-%d %H:%M:%S")

# 3a. Console handler (stdout)
console_handler = logging.StreamHandler(stream=sys.stdout)
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)

# 3b. Rotating file handler (1 MB, keep 3 backups)
file_handler = handlers.RotatingFileHandler(
    filename=LOG_PATH,
    maxBytes=1_000_000,  # 1 MB
    backupCount=3,
    encoding="utf-8",
)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

# 4. Attach handlers once (avoid duplicates if script is re‑imported)
if not logger.handlers:
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

# ---------------------------------------------------------------------------
# Demo payload – generate some noise so we can test rotation
# ---------------------------------------------------------------------------
LOREM = string.ascii_letters + string.digits


def _random_line(length: int = 60) -> str:
    return "".join(random.choice(LOREM) for _ in range(length))


if __name__ == "__main__":
    logger.info("✨ Starting demo run at %s", datetime.now().isoformat())

    for i in range(2000):
        logger.debug("%04d | %s", i, _random_line())
        if i % 250 == 0:
            logger.warning("Reached %d lines", i)

    logger.info("✅ Demo run complete; check %s and rotated backups", LOG_PATH)
