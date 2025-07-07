"""yaml_loader_demo.py

Bootstrap a logger using the stand‑alone ``logging_config.yaml`` that
lives *right next to this file*, no matter where you launch the script
from.

Usage::

    python 4_config_file/yaml_loader_demo.py

Dependencies::

    pip install pyyaml python-json-logger
"""

from __future__ import annotations

import logging.config
import pathlib
import sys
from typing import Any

import pathlib
pathlib.Path("logs").mkdir(exist_ok=True)

try:
    import yaml  # type: ignore
except ImportError as exc:
    print("✖️  Missing dependency: pyyaml. Run 'pip install pyyaml'", file=sys.stderr)
    raise

# ---------------------------------------------------------------------------
# Locate the YAML file *relative to this script*, not to the CWD.
# ---------------------------------------------------------------------------
CONFIG_PATH = pathlib.Path(__file__).with_name("logging_config.yaml")
if not CONFIG_PATH.exists():
    raise FileNotFoundError(f"Cannot find {CONFIG_PATH!s}")

with CONFIG_PATH.open("r", encoding="utf-8") as fh:
    cfg: dict[str, Any] = yaml.safe_load(fh)

# ---------------------------------------------------------------------------
# Activate and test
# ---------------------------------------------------------------------------
logging.config.dictConfig(cfg)
logger = logging.getLogger(__name__)
logger.info("🎉 YAML logging active via %s", CONFIG_PATH)
