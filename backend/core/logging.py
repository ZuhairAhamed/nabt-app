"""
Logging configuration for Nabt application.
"""

import logging
import sys
from typing import Optional


def setup_logging(log_level: str = "INFO") -> None:
    # Setup application-wide logging configuration with specified level
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )


def get_logger(name: str, log_level: Optional[str] = None) -> logging.Logger:
    # Get a logger instance with optional log level override
    logger = logging.getLogger(name)
    if log_level:
        logger.setLevel(getattr(logging, log_level.upper()))
    return logger

