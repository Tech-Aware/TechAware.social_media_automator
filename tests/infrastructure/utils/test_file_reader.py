# tests/infrastructure/utils/test_file_reader.py

"""
This module contains unit tests for the file_reader module.

It tests the read_prompt_file function to ensure it correctly reads
prompt files, handles file not found errors, and manages IO errors.
"""

import os
import sys
import pytest
from unittest.mock import patch, mock_open

# Ajoute le répertoire racine du projet au sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
sys.path.insert(0, project_root)

from src.infrastructure.utils.file_reader import read_prompt_file


def test_read_prompt_file():
    mock_content = "This is a mock prompt content"
    mock_file_path = os.path.join('resources', 'prompts', 'test_prompt.txt')

    with patch('builtins.open', mock_open(read_data=mock_content)) as mock_file:
        with patch('os.path.dirname') as mock_dirname:
            mock_dirname.return_value = '/fake/path'
            result = read_prompt_file('test_prompt.txt')

    assert result == mock_content.strip()
    mock_file.assert_called_once_with(os.path.join('/fake/path', 'resources', 'prompts', 'test_prompt.txt'), 'r')


def test_read_prompt_file_file_not_found():
    with pytest.raises(FileNotFoundError):
        with patch('builtins.open', mock_open()) as mock_file:
            mock_file.side_effect = FileNotFoundError()
            read_prompt_file('non_existent_file.txt')


def test_read_prompt_file_io_error():
    with pytest.raises(IOError):
        with patch('builtins.open', mock_open()) as mock_file:
            mock_file.side_effect = IOError()
            read_prompt_file('error_file.txt')