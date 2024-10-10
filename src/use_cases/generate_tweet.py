# src/use_cases/generate_tweet.py

from src.interfaces.openai_gateway import OpenAIGateway
from src.infrastructure.logging.logger import logger, log_method
from src.domain.exceptions import AutomatorError, OpenAIError, TweetGenerationError

class GenerateTweetUseCase:
    @log_method(logger)
    def __init__(self, openai_gateway: OpenAIGateway):
        self.openai_gateway = openai_gateway
        logger.debug(f"GenerateTweetUseCase initialisé avec {openai_gateway.__class__.__name__}")

    @log_method(logger)
    def execute(self, prompt: str) -> str:
        try:
            logger.debug(f"Génération d'un tweet avec le prompt : {prompt}")
            generated_tweet = self.openai_gateway.generate_tweet(prompt)
            logger.debug(f"Tweet généré : {generated_tweet}")
            return generated_tweet
        except OpenAIError as e:
            logger.error(f"Erreur OpenAI dans GenerateTweetUseCase : {str(e)}")
            raise TweetGenerationError(f"Erreur lors de la génération du tweet : {str(e)}")
        except Exception as e:
            logger.error(f"Erreur inattendue dans GenerateTweetUseCase : {str(e)}")
            raise TweetGenerationError(f"Erreur inattendue lors de la génération du tweet : {str(e)}")