"""
Logging configuration for Nabt application.
"""

import logging
import sys
from typing import Optional


def setup_logging(log_level: str = "INFO") -> None:
    """
    Setup application-wide logging configuration.
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    """
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )


def get_logger(name: str, log_level: Optional[str] = None) -> logging.Logger:
    """
    Get a logger instance.
    
    Args:
        name: Logger name (typically __name__)
        log_level: Optional log level override
        
    Returns:
        logging.Logger: Configured logger instance
    """
    logger = logging.getLogger(name)
    if log_level:
        logger.setLevel(getattr(logging, log_level.upper()))
    return logger

