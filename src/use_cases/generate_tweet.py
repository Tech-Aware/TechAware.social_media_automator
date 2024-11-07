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
            guidelines = """
                        Here are the guidelines for this X (formerly Twitter) post with a maximum of 250 characters, leveraging a premium subscription:

                        1. **Catchy start**: Begin with a short, impactful sentence that quickly grabs attention.
                        2. **Value and relevance**: Share an insight, fact, or tip to engage the audience immediately.
                        3. **Conciseness**: Keep the message concise and easy to digest, using the extended character limit only if necessary.
                        4. **Call to action**: End with a prompt to reply, retweet, or follow.
                        5. **Hashtags and tags**: Add up to 3 relevant hashtags for discoverability, and tag any relevant accounts to increase reach.
                        6. **Professional yet authentic tone**: Use a tone that’s professional but personal, possibly with a personal insight or experience.

                        The post should be written in French, with appropriate emojis to enhance readability. No special formatting is required for links, such as https://www.webpage.net.
                        """

            logger.debug("Generating X publication")
            x_prompt = (
                "Generate a 250-character X (formerly Twitter) post following these guidelines. "
                "The post should be engaging, conversational, and suitable for a general audience, written in French. "
                "Include relevant emojis if suitable. "
                f"{guidelines}"
                "Example output : 🚀 Découvrez comment Kevin a transformé sa carrière grâce à notre étude de cas! Des insights précieux pour tout professionnel tech. 🌟 Lisez l'intégralité ici: https://techaware.net/etude-de-cas #Tech #Carrière #Innovation"
            )
            generated_publication = self.openai_gateway.generate(x_prompt)
            logger.debug(f"X publication generated: {generated_publication}")

            if len(generated_publication) > 250:
                logger.warning("Tweet length invalid ! must be 250 char max ! Trying again")
                self.execute()
            else:
                return generated_publication
        except OpenAIError as e:
            logger.error(f"Erreur OpenAI dans GenerateTweetUseCase : {str(e)}")
            raise TweetGenerationError(f"Erreur lors de la génération du tweet : {str(e)}")
        except Exception as e:
            logger.error(f"Erreur inattendue dans GenerateTweetUseCase : {str(e)}")
            raise TweetGenerationError(f"Erreur inattendue lors de la génération du tweet : {str(e)}")