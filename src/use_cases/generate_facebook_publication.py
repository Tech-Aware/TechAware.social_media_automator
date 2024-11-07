# Location: src/use_cases/generate_facebook_publication.py

"""
This module implements the GenerateFacebookPublicationUseCase class, which encapsulates
the business logic for generating Facebook publications using OpenAI. It handles
the coordination between the OpenAI gateway and publication generation process.
"""

from src.interfaces.openai_gateway import OpenAIGateway
from src.infrastructure.logging.logger import logger, log_method
from src.domain.exceptions import AutomatorError, OpenAIError, FacebookGenerationError


class GenerateFacebookPublicationUseCase:
    @log_method(logger)
    def __init__(self, openai_gateway: OpenAIGateway):
        """
        Initialize the use case with an OpenAI gateway.

        Args:
            openai_gateway (OpenAIGateway): The gateway to interact with OpenAI
        """
        self.openai_gateway = openai_gateway
        logger.debug(f"GenerateFacebookPublicationUseCase initialized with {openai_gateway.__class__.__name__}")

    @log_method(logger)
    def execute(self) -> str:
        """
        Execute the use case to generate Facebook publication content.

        Args:
            prompt (str): The prompt for publication generation

        Returns:
            str: The generated Facebook publication content

        Raises:
            TweetGenerationError: If publication generation fails
        """
        try:
            guidelines = """
                        Here are the guidelines for this Facebook post:

                        1. **Engaging opener**: Start with an interesting or emotional sentence to immediately capture attention.
                        2. **Clarity and conciseness**: Use clear sentences and short paragraphs for easy readability.
                        3. **Value for the reader**: Share helpful information, tips, or insights relevant to the audience.
                        4. **Call to action**: End with a prompt encouraging readers to like, comment, share, or tag friends.
                        5. **Relevant hashtags**: Add a few relevant hashtags, but keep it natural and avoid overloading with tags.
                        6. **Friendly and authentic tone**: Keep a professional yet friendly tone, with a personal touch or experience if relevant.

                        The post should be written in French, with appropriate emojis to enhance readability. No special formatting is required for links, such as https://www.webpage.net.
                        """

            logger.debug("Generating Facebook publication")

            facebook_prompt = (
                "Generate a Facebook post following these guidelines. "
                "The post should be engaging, conversational, and suitable for a general audience, written in French. "
                "Include relevant emojis if suitable. "
                f"{guidelines}"
                f"""Example output :  🚀 À la recherche d'une évolution professionnelle? Tech Aware est votre partenaire idéal! 🌟
Nous comprenons que le chemin vers le succès professionnel est souvent semé d'embûches. C'est pourquoi chez Tech Aware, nous nous engageons à vous fournir des ressources et des conseils précieux pour propulser votre carrière. 🌐 Découvrez comment nous pouvons vous aider à atteindre vos objectifs professionnels sur notre page dédiée:  https://www.techaware.net/pour-les-entreprises 
🔍 Que trouverez-vous chez Tech Aware ?
- Des conseils d'experts sur les tendances du marché
- Des outils pour améliorer vos compétences techniques
- Une communauté de professionnels comme vous
👍 Aimez-vous les nouvelles opportunités ? Commentez avec vos attentes professionnelles ou partagez ce post avec vos amis qui pourraient être intéressés! 📢
#Carrière #Innovation #TechAware #EmploiTech"""
            )
            generated_publication = self.openai_gateway.generate(facebook_prompt)
            logger.debug(f"Facebook publication generated: {generated_publication}")
            return generated_publication

        except OpenAIError as e:
            logger.error(f"OpenAI error in GenerateFacebookPublicationUseCase: {str(e)}")
            raise FacebookGenerationError(f"Error generating Facebook publication: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error in GenerateFacebookPublicationUseCase: {str(e)}")
            raise FacebookGenerationError(f"Unexpected error generating Facebook publication: {str(e)}")