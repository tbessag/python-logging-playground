"""
logging_basics.py
A minimal example showing the correct way to start using the
logging module:
* always create a module-level logger with logging.getLogger(__name__)
* avoid the root logger
* attach a StreamHandler to stdout
* set a simple formatter with timestamp, name, level and message
"""

import logging
import sys

# 1. Create a logger for this module
logger = logging.getLogger('test_logger')
logger.setLevel(logging.DEBUG)  # temporarily set to DEBUG to show all levels

# 2. Create a StreamHandler that writes to stdout
stream_handler = logging.StreamHandler(stream=sys.stdout)
stream_handler.setLevel(logging.DEBUG)  # pass everything through the handler

# 3. Define a simple formatter and add it to the handler
formatter = logging.Formatter(
    fmt="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
stream_handler.setFormatter(formatter)

# 4. Attach the handler to the logger (do it once!)
logger.addHandler(stream_handler)

# 5. Emit some log records with different severities
logger.debug("This is DEBUG – useful while developing")
logger.info("This is INFO – standard operational messages")
logger.warning("This is WARNING – something unexpected happened")
logger.error("This is ERROR – the operation failed but the program is still running")
logger.critical("This is CRITICAL – the program might not be able to continue")

"""
Expected output (timestamps will differ):

2025-07-04 12:00:00 | __main__ | DEBUG | This is DEBUG – useful while developing
2025-07-04 12:00:00 | __main__ | INFO | This is INFO – standard operational messages
2025-07-04 12:00:00 | __main__ | WARNING | This is WARNING – something unexpected happened
2025-07-04 12:00:00 | __main__ | ERROR | This is ERROR – the operation failed but the program is still running
2025-07-04 12:00:00 | __main__ | CRITICAL | This is CRITICAL – the program might not be able to continue
"""
