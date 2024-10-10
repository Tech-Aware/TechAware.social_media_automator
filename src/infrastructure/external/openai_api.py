# src/infrastructure/external/openai_api.py

from openai import OpenAI
from src.interfaces.openai_gateway import OpenAIGateway
from src.infrastructure.logging.logger import logger, log_method
from src.infrastructure.config.environment import get_openai_credentials
from src.domain.exceptions import OpenAIError, ConfigurationError, TweetGenerationError


class OpenAIAPI(OpenAIGateway):
    @log_method(logger)
    def __init__(self):
        try:
            logger.debug("Chargement des identifiants OpenAI")
            credentials = get_openai_credentials()
            self.client = OpenAI(api_key=credentials['api_key'])
            logger.debug("Client OpenAI initialisé avec succès")
        except ConfigurationError as e:
            logger.error(f"Échec de l'initialisation de l'API OpenAI : {str(e)}")
            raise

    @log_method(logger)
    def generate_tweet(self, prompt: str) -> str:
        try:
            logger.debug(f"Génération d'un tweet avec le prompt : {prompt}")
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Vous êtes un assistant utile qui génère du contenu pour des tweets."},
                    {"role": "user", "content": f"Générez un tweet basé sur ce prompt : {prompt}"}
                ]
            )
            generated_tweet = response.choices[0].message.content.strip('')
            generated_tweet = generated_tweet[1:-1]  # Supprime le premier et le dernier caractère
            logger.debug(f"Tweet généré : {generated_tweet}")
            return generated_tweet
        except Exception as e:
            logger.error(f"Échec de la génération du tweet : {str(e)}")
            raise TweetGenerationError(f"Échec de la génération du tweet : {str(e)}")