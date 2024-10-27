# Location: src/infrastructure/utils/file_reader.py

"""
This module provides utilities for reading prompt files from the resources directory.
It includes functions to safely read files with proper error handling and logging.
"""

import os
from src.infrastructure.logging.logger import logger, log_method

# todo: possibly deprecated by better openai_api integration in prompting
@log_method(logger)
def read_prompt_file(platform: str) -> str:
    """
    Read a platform-specific prompt file from the resources directory.

    Args:
        platform (str): The platform or filename to read the prompt for

    Returns:
        str: The content of the prompt file

    Raises:
        FileNotFoundError: If the prompt file doesn't exist
        IOError: If there's an error reading the file
    """
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    file_path = os.path.join(project_root, 'resources', 'prompts', f"techaware_pro_prompt_for_{platform}.txt")

    logger.debug(f"Attempting to read prompt file for {platform}: {file_path}")

    try:
        with open(file_path, 'r') as file:
            content = file.read().strip()
            logger.debug(f"Successfully read prompt file for {platform}")
            return content
    except FileNotFoundError:
        logger.error(f"Prompt file not found for {platform}: {file_path}")
        raise FileNotFoundError(f"Prompt file not found for {platform}: {file_path}")
    except IOError as e:
        logger.error(f"Error reading prompt file for {platform}: {str(e)}")
        raise IOError(f"Failed to read prompt file for {platform}: {str(e)}")