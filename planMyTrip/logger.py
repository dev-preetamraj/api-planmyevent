import logging
import sys

# Get logger
logger = logging.getLogger()

# Create formatter
stream_formatter = logging.Formatter(
    "\n-------------------- Log info --------------------\n"
    "1. TIME: %(asctime)s\n"
    "2. MODULE: %(module)s | FUNCTION: %(funcName)s\n"
    "3. %(levelname)s: %(message)s\n"
    "--------------------------------------------------\n"
)

file_formatter = logging.Formatter(
    "%(asctime)s - %(module)s | %(funcName)s - %(levelname)s: %(message)s\n"
)

# Create handlers
stream_handler = logging.StreamHandler(sys.stdout)
file_handler = logging.FileHandler("app.log")


stream_handler.setFormatter(stream_formatter)
file_handler.setFormatter(file_formatter)

logger.handlers = [stream_handler, file_handler]

logger.setLevel(logging.INFO)
