# src/infrastructure/logging/logger.py

"""
This module provides a custom logging setup for the application. It includes
a ColoredFormatter for console output, a CustomLogger class with additional
logging levels, and utility functions for creating loggers and decorating
methods with logging capabilities.
"""

import logging
import sys
from functools import wraps
import inspect
import os

class ColoredFormatter(logging.Formatter):
    COLORS = {
        'INFO': '\033[94m',  # Bleu
        'DEBUG': '\033[97m',  # Blanc
        'WARNING': '\033[93m',  # Orange
        'ERROR': '\033[91m',  # Rouge
        'CRITICAL': '\033[91m',  # Rouge
        'SUCCESS': '\033[92m',  # Vert
        'ENTERING': '\033[96m',  # Cyan
        'EXITING': '\033[95m'  # Magenta
    }
    RESET = '\033[0m'

    def format(self, record):
        caller = self.get_caller_info()
        log_type = record.levelname
        prefix = ""
        if hasattr(record, 'custom_level'):
            if record.custom_level == 'ENTERING':
                log_type = 'ENTERING'
                prefix = "↓ ↓ ↓ "
            elif record.custom_level == 'EXITING':
                log_type = 'EXITING'
                prefix = "↑ ↑ ↑ "
            elif record.custom_level == 'SUCCESS':
                log_type = 'SUCCESS'
                prefix = "★ ★ ★ "

        log_message = f"{prefix}{caller['file'].upper()} - {caller['function']} - line {caller['line']} - {record.getMessage()}"

        if log_type == 'SUCCESS':
            log_message += " ★ ★ ★"
        elif log_type == 'ENTERING':
            log_message += " ↓ ↓ ↓"
        elif log_type == 'EXITING':
            log_message += " ↑ ↑ ↑"

        level_color = self.COLORS.get(log_type, self.RESET)
        colored_message = f"{level_color}{self.formatTime(record, '%Y-%m-%d %H:%M:%S')} - {log_type} - {log_message}{self.RESET}"

        return colored_message

    def get_caller_info(self):
        frame = inspect.currentframe()
        while frame and (frame.f_code.co_filename == __file__ or 'logging' in frame.f_code.co_filename):
            frame = frame.f_back

        if frame:
            filename = os.path.basename(frame.f_code.co_filename)
            return {
                'file': filename,
                'function': frame.f_code.co_name,
                'line': frame.f_lineno
            }
        else:
            return {'file': 'unknown', 'function': 'unknown', 'line': 0}

class CustomLogger(logging.Logger):
    def __init__(self, name, level=logging.NOTSET):
        super().__init__(name, level)
        self.success = self._success
        self.entering = self._entering
        self.exiting = self._exiting

    def _log_with_custom_level(self, level, msg, custom_level, *args, **kwargs):
        if self.isEnabledFor(level):
            extra = kwargs.get('extra', {})
            extra['custom_level'] = custom_level
            kwargs['extra'] = extra
            self._log(level, msg, args, **kwargs)

    def _success(self, msg, *args, **kwargs):
        self._log_with_custom_level(logging.INFO, msg, 'SUCCESS', *args, **kwargs)

    def _entering(self, msg, *args, **kwargs):
        self._log_with_custom_level(logging.DEBUG, msg, 'ENTERING', *args, **kwargs)

    def _exiting(self, msg, *args, **kwargs):
        self._log_with_custom_level(logging.DEBUG, msg, 'EXITING', *args, **kwargs)

def get_logger(name):
    logging.setLoggerClass(CustomLogger)
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)  # Set to DEBUG to capture all levels

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)  # Set handler to DEBUG as well

    formatter = ColoredFormatter()
    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)

    # Ajouter un handler non formaté pour les erreurs
    error_handler = logging.StreamHandler(sys.stderr)
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s:\n%(pathname)s:%(lineno)d'))
    logger.addHandler(error_handler)

    return logger

def log_method(logger):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            logger.entering(f"Entering {func.__name__}")
            logger.info(f"Executing {func.__name__}")
            try:
                logger.debug(f"Arguments: {args}, {kwargs}")
                result = func(*args, **kwargs)
                logger.debug(f"Result: {result}")
                logger.success(f"Successfully executed {func.__name__}")
                return result
            except Exception as e:
                logger.error(f"Exception in {func.__name__}: {str(e)}")
                raise
            finally:
                logger.exiting(f"Exiting {func.__name__}")
        return wrapper
    return decorator

logger = get_logger(__name__)