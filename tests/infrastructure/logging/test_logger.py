# tests/infrastructure/logging/test_logger.py

"""
Ce module contient les tests unitaires pour le logger personnalisé
défini dans src.infrastructure.logging.logger.
"""

import sys
import os
import pytest
from unittest.mock import patch, MagicMock
import logging


# Ajoute le répertoire racine du projet au sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
sys.path.insert(0, project_root)


from src.infrastructure.logging.logger import CustomLogger, ColoredFormatter, get_logger, log_method


def test_custom_logger_creation():
    logger = CustomLogger("test_logger")
    assert isinstance(logger, logging.Logger)
    assert logger.name == "test_logger"


def test_custom_logger_levels():
    logger = CustomLogger("test_logger")
    assert hasattr(logger, 'success')
    assert hasattr(logger, 'entering')
    assert hasattr(logger, 'exiting')


@patch('sys.stdout', new_callable=MagicMock)
def test_colored_formatter(mock_stdout):
    formatter = ColoredFormatter()
    record = logging.LogRecord("test_logger", logging.INFO, "test.py", 10, "Test message", (), None)
    formatted = formatter.format(record)
    assert "INFO" in formatted
    assert "Test message" in formatted


@patch('logging.Logger.addHandler')
@patch('logging.StreamHandler')
def test_get_logger(mock_handler, mock_add_handler):
    logger = get_logger("test_logger")
    assert isinstance(logger, CustomLogger)
    assert mock_add_handler.called  # Vérifie si la méthode a été appelée au moins une fois


@patch('src.infrastructure.logging.logger.CustomLogger')
def test_log_method_decorator(mock_logger):
    mock_logger_instance = MagicMock()
    mock_logger.return_value = mock_logger_instance

    @log_method(mock_logger_instance)
    def test_function(arg1, arg2):
        return arg1 + arg2

    result = test_function(1, 2)

    assert result == 3
    mock_logger_instance.entering.assert_called_once()
    mock_logger_instance.info.assert_called_once()
    mock_logger_instance.debug.assert_called()
    mock_logger_instance.success.assert_called_once()
    mock_logger_instance.exiting.assert_called_once()


@patch('src.infrastructure.logging.logger.CustomLogger')
def test_log_method_decorator_exception(mock_logger):
    mock_logger_instance = MagicMock()
    mock_logger.return_value = mock_logger_instance

    @log_method(mock_logger_instance)
    def test_function():
        raise ValueError("Test exception")

    with pytest.raises(ValueError):
        test_function()

    mock_logger_instance.entering.assert_called_once()
    mock_logger_instance.info.assert_called_once()
    mock_logger_instance.error.assert_called_once_with("Exception in test_function: Test exception")
    mock_logger_instance.exiting.assert_called_once()


if __name__ == "__main__":
    pytest.main([__file__, '-v'])
