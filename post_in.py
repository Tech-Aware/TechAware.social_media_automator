# post_in.py

import os
import sys
from dotenv import load_dotenv, find_dotenv
from pathlib import Path
import argparse
from src.infrastructure.logging.logger import get_logger
from src.domain.exceptions import ConfigurationError, AutomatorError
from src.presentation.post_command import PostCommand

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


def setup_parser():
    """Configure l'analyseur d'arguments en ligne de commande"""
    parser = argparse.ArgumentParser(description='Post content to social media platforms')

    parser.add_argument('platform',
                        choices=['facebook', 'linkedin', 'twitter'],
                        help='The platform to post to')

    parser.add_argument('--debug',
                        action='store_true',
                        help='Enable debug logging')

    parser.add_argument('--dry-run',
                        action='store_true',
                        help='Generate content without posting')

    parser.add_argument('--topic',
                        choices=['business', 'developer', 'slides'],
                        help='Specify the topic category')

    return parser


def main():
    try:
        # Parser les arguments
        parser = setup_parser()
        args = parser.parse_args()

        # Configuration de l'environnement
        if not setup_environment():
            raise ConfigurationError("Failed to setup environment")

        # Exécuter la commande
        command = PostCommand()
        result = command.execute(
            platform=args.platform,
            dry_run=args.dry_run,
            topic=args.topic
        )

        # Afficher le résultat
        if args.dry_run:
            print("\nGenerated content:")
            print("-" * 40)
            print(result)
            print("-" * 40)
        else:
            print(f"Successfully posted to {args.platform}!")

    except ConfigurationError as e:
        logger.error(f"Configuration error: {str(e)}")
        print(f"Configuration error: {str(e)}")
        sys.exit(1)
    except AutomatorError as e:
        logger.error(f"Automator error: {str(e)}")
        print(f"An error occurred: {str(e)}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"An unexpected error occurred: {str(e)}", exc_info=True)
        print(f"An unexpected error occurred. Please check the logs for more details.")
        sys.exit(1)


if __name__ == "__main__":
    main()