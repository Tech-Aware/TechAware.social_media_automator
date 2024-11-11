# main.py

import os
import sys
from pathlib import Path
from dotenv import load_dotenv, find_dotenv
from src.presentation.cli import CLI
from src.infrastructure.logging.logger import get_logger
from src.domain.exceptions import ConfigurationError, AutomatorError

logger = get_logger(__name__)


def setup_environment():
    """Configure l'environnement d'exécution"""
    try:
        # Obtenir les chemins absolus
        current_dir = os.getcwd()
        script_dir = os.path.dirname(os.path.abspath(__file__))

        # Log des chemins pour debug
        logger.debug(f"Current working directory: {current_dir}")
        logger.debug(f"Script directory: {script_dir}")

        # Chercher le fichier .env
        dotenv_path = find_dotenv(usecwd=True)
        logger.debug(f"Found .env at: {dotenv_path}")

        # Charger le .env
        loaded = load_dotenv(dotenv_path, override=True)
        logger.debug(f"Loading .env result: {loaded}")

        # Vérifier la clé OpenAI
        openai_key = os.getenv('OPENAI_API_KEY')
        logger.debug(f"OpenAI key loaded: {'Yes' if openai_key else 'No'}")
        if openai_key:
            logger.debug(f"Key type: {'Project key' if openai_key.startswith('sk-proj-') else 'Standard key'}")

        return True
    except Exception as e:
        logger.error(f"Error setting up environment: {str(e)}")
        return False


def main():
    try:
        # Configuration initiale
        logger.info("Starting Automator application")
        if not setup_environment():
            raise ConfigurationError("Failed to setup environment")

        cli = CLI()
        cli.menu()
        logger.info("Automator application completed successfully")
    except ConfigurationError as e:
        logger.error(f"Configuration error: {str(e)}")
        print(f"Configuration error: {str(e)}")
    except AutomatorError as e:
        logger.error(f"Automator error: {str(e)}")
        print(f"An error occurred: {str(e)}")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {str(e)}", exc_info=True)
        print(f"An unexpected error occurred. Please check the logs for more details.")


if __name__ == "__main__":
    main()