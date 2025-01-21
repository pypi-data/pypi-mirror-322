# src/setlogging/__init__.py
from .logger import setup_logging, get_logger, CustomFormatter

__version__ = "0.3.0"
__all__ = ["setup_logging", "get_logger", "CustomFormatter"]
