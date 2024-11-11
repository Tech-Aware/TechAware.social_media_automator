# post_in.py

import sys
import os
from dotenv import load_dotenv, find_dotenv
from pathlib import Path
import argparse
from src.infrastructure.logging.logger import get_logger
from src.domain.exceptions import ConfigurationError, AutomatorError
from src.use_cases.generate_facebook_publication import GenerateFacebookPublicationUseCase
from src.use_cases.generate_linkedin_post import GenerateLinkedInPostUseCase
from src.use_cases.generate_tweet import GenerateTweetUseCase
from src.use_cases.post_facebook import PostFacebookUseCase
from src.use_cases.post_linkedin import PostLinkedInUseCase
from src.use_cases.post_tweet import PostTweetUseCase
from src.infrastructure.external.facebook_api import FacebookAPI
from src.infrastructure.external.linkedin_api import LinkedInAPI
from src.infrastructure.external.twitter_api import TwitterAPI
from src.infrastructure.external.openai_api import OpenAIAPI

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


def post_to_platform(platform: str):
    """
    Génère et poste du contenu sur une plateforme spécifique.

    Args:
        platform (str): La plateforme cible ('facebook', 'linkedin', ou 'twitter')
    """
    try:
        # Initialiser OpenAI pour la génération
        openai_gateway = OpenAIAPI()

        if platform == 'facebook':
            # Facebook
            facebook_gateway = FacebookAPI()
            generate_use_case = GenerateFacebookPublicationUseCase(openai_gateway)
            post_use_case = PostFacebookUseCase(facebook_gateway)

            # Génération et post
            logger.info("Generating Facebook content")
            content = generate_use_case.execute()
            logger.info("Posting to Facebook")
            result = post_use_case.execute(content)
            print("Successfully posted to Facebook!")

        elif platform == 'linkedin':
            # LinkedIn
            linkedin_gateway = LinkedInAPI()
            generate_use_case = GenerateLinkedInPostUseCase(openai_gateway)
            post_use_case = PostLinkedInUseCase(linkedin_gateway)

            # Génération et post
            logger.info("Generating LinkedIn content")
            content = generate_use_case.execute()
            logger.info("Posting to LinkedIn")
            result = post_use_case.execute(content)
            print("Successfully posted to LinkedIn!")

        elif platform == 'twitter':
            # Twitter
            twitter_gateway = TwitterAPI()
            generate_use_case = GenerateTweetUseCase(openai_gateway)
            post_use_case = PostTweetUseCase(twitter_gateway)

            # Génération et post
            logger.info("Generating tweet")
            content = generate_use_case.execute()
            logger.info("Posting to Twitter")
            result = post_use_case.execute(content)
            print("Successfully posted to Twitter!")

        else:
            raise ValueError(f"Unsupported platform: {platform}")

    except Exception as e:
        logger.error(f"Error posting to {platform}: {str(e)}")
        raise


def main():
    try:
        # Configurer l'analyseur d'arguments
        parser = argparse.ArgumentParser(description='Post content to social media platforms')
        parser.add_argument('platform', choices=['facebook', 'linkedin', 'twitter'],
                            help='The platform to post to')

        # Parser les arguments
        args = parser.parse_args()

        # Configuration de l'environnement
        if not setup_environment():
            raise ConfigurationError("Failed to setup environment")

        # Poster sur la plateforme sélectionnée
        post_to_platform(args.platform)

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