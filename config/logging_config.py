import logging
import sys
from pathlib import Path
from typing import Optional
from .settings import settings

def configure_logging():
    """Configure logging based on settings."""
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    debug_format = "%(asctime)s - %(name)s - %(levelname)s - %(pathname)s:%(lineno)d - %(funcName)s - %(message)s"
    
    formatter = logging.Formatter(debug_format if settings.LOG_LEVEL == "DEBUG" else log_format)
    
    handlers = []
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    handlers.append(console_handler)
    
    # File handler if specified
    if settings.LOG_FILE:
        settings.LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(settings.LOG_FILE)
        file_handler.setFormatter(formatter)
        handlers.append(file_handler)
    
    # Configure root logger
    logging.basicConfig(
        level=settings.LOG_LEVEL,
        handlers=handlers
    )
    
    # Set specific log levels for noisy libraries
    logging.getLogger("chromadb").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)