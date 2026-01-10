import logging
import sys
from pathlib import Path

log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)


LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def get_logger(name: str) -> logging.Logger:

    logger = logging.getLogger(name)
    
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_formatter = logging.Formatter(LOG_FORMAT, DATE_FORMAT)
        console_handler.setFormatter(console_formatter)
        
        # File handler for all logs
        file_handler = logging.FileHandler(log_dir / "app.log", encoding="utf-8")
        file_handler.setLevel(logging.INFO)
        file_formatter = logging.Formatter(LOG_FORMAT, DATE_FORMAT)
        file_handler.setFormatter(file_formatter)
        
        # Error file handler
        error_handler = logging.FileHandler(log_dir / "errors.log", encoding="utf-8")
        error_handler.setLevel(logging.ERROR)
        error_formatter = logging.Formatter(LOG_FORMAT, DATE_FORMAT)
        error_handler.setFormatter(error_formatter)
        
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)
        logger.addHandler(error_handler)
    
    return logger
