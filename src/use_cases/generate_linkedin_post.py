# Location: src/use_cases/generate_linkedin_post.py

"""
This module implements the GenerateLinkedInPostUseCase class, which encapsulates
the business logic for generating LinkedIn posts using OpenAI. It handles
the coordination between the OpenAI gateway and post generation process.
"""

from src.interfaces.openai_gateway import OpenAIGateway
from src.infrastructure.logging.logger import logger, log_method
from src.domain.exceptions import AutomatorError, OpenAIError, LinkedInGenerationError


class GenerateLinkedInPostUseCase:
    @log_method(logger)
    def __init__(self, openai_gateway: OpenAIGateway):
        """
        Initialize the use case with an OpenAI gateway.

        Args:
            openai_gateway (OpenAIGateway): The gateway to interact with OpenAI
        """
        self.openai_gateway = openai_gateway
        logger.debug(f"GenerateLinkedInPostUseCase initialized with {openai_gateway.__class__.__name__}")

    @log_method(logger)
    def execute(self) -> str:
        """
        Execute the use case to generate LinkedIn post content.

        Args:
            prompt (str): The prompt for post generation

        Returns:
            str: The generated LinkedIn post content

        Raises:
            TweetGenerationError: If post generation fails
        """
        try:
            guidelines = """
                        Here are the guidelines I’d like you to follow for this LinkedIn post:
                        1. **Strong hook at the beginning**: Start with an impactful sentence to grab attention.
                        2. **Clarity and conciseness**: Structure the post for easy reading, with clear and concise sentences.
                        3. **Added value**: Provide useful information and practical tips for the reader.
                        4. **Call to action**: End with a question or an invitation to comment, share, or provide feedback.
                        5. **Relevant hashtags**: Add 3 to 5 hashtags related to the topic to increase reach.
                        6. **Authenticity and professionalism**: Use a professional yet accessible tone, adding a personal touch or lived experience if relevant.
                        7. **Character limit**: Respect LinkedIn's recommended limit of 600 characters to maximize readability and engagement.

                        The post should be in French and formatted naturally, with no special formatting for links (e.g., https://www.webpage.net).
                        """

            logger.debug("Generating LinkedIn publication")

            linkedin_prompt = (
                "Generate a LinkedIn publication. The publication should be engaging, "
                "conversational, and suitable for a professional audience. "
                "Include relevant emojis where appropriate."
                "output language in french."
                "Include link without any special format, writing it as https://www.webpage.net."
                f"{guidelines}"
            )
            generated_publication = self.openai_gateway.generate(linkedin_prompt)
            logger.debug(f"LinkedIn publication generated: {generated_publication}")
            return generated_publication

        except OpenAIError as e:
            logger.error(f"OpenAI error in GenerateLinkedInPostUseCase: {str(e)}")
            raise LinkedInGenerationError(f"Error generating linkedIn publication: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error in GenerateLinkedInPostUseCase: {str(e)}")
            raise LinkedInGenerationError(f"Unexpected error generating linkedIn publication: {str(e)}")