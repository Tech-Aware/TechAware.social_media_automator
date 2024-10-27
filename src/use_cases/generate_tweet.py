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
    def execute(self) -> str:
        try:
            logger.debug(f"Generating X publication")
            x_prompt = (
                "Generate a X (ex twitter) publication of a maximum of 250 char. The publication should be engaging, "
                "conversational, and suitable for a general audience. "
                "Respecting the length limit of character for X platform at 250 character maximum"
                "Include relevant emojis where appropriate. "
            )
            generated_publication = self.openai_gateway.generate(x_prompt)
            logger.debug(f"X publication generated: {generated_publication}")
            return generated_publication
        except OpenAIError as e:
            logger.error(f"Erreur OpenAI dans GenerateTweetUseCase : {str(e)}")
            raise TweetGenerationError(f"Erreur lors de la génération du tweet : {str(e)}")
        except Exception as e:
            logger.error(f"Erreur inattendue dans GenerateTweetUseCase : {str(e)}")
            raise TweetGenerationError(f"Erreur inattendue lors de la génération du tweet : {str(e)}")