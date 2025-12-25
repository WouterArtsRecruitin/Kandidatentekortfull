"""
Structured logging configuration for V2.
"""

import logging
import sys
from datetime import datetime

# Configure root logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

def get_logger(name: str) -> logging.Logger:
    """Get a logger with the given name."""
    logger = logging.getLogger(f"v2.{name}")
    return logger


class LogContext:
    """Context manager for structured logging with context."""

    def __init__(self, logger: logging.Logger, operation: str, **context):
        self.logger = logger
        self.operation = operation
        self.context = context
        self.start_time = None

    def __enter__(self):
        self.start_time = datetime.now()
        ctx_str = " ".join(f"{k}={v}" for k, v in self.context.items())
        self.logger.info(f"[START] {self.operation} {ctx_str}")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        duration = (datetime.now() - self.start_time).total_seconds()
        if exc_type:
            self.logger.error(f"[FAIL] {self.operation} duration={duration:.2f}s error={exc_val}")
        else:
            self.logger.info(f"[OK] {self.operation} duration={duration:.2f}s")
        return False  # Don't suppress exceptions
