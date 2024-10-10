# src/presentation/cli.py
import time

from src.use_cases.post_tweet import PostTweetUseCase
from src.use_cases.generate_tweet import GenerateTweetUseCase
from src.infrastructure.external.twitter_api import TwitterAPI
from src.infrastructure.external.openai_api import OpenAIAPI
from src.infrastructure.logging.logger import logger, log_method
from src.infrastructure.utils.file_reader import read_prompt_file
from src.domain.exceptions import AutomatorError, TwitterError, ConfigurationError, ValidationError, OpenAIError, \
    TweetGenerationError


class CLI:
    @log_method(logger)
    def __init__(self):
        try:
            logger.debug("Création de l'instance TwitterAPI")
            twitter_gateway = TwitterAPI()
            logger.debug("Instance TwitterAPI créée")

            logger.debug("Création de l'instance OpenAIAPI")
            openai_gateway = OpenAIAPI()
            logger.debug("Instance OpenAIAPI créée")

            logger.debug("Création de l'instance PostTweetUseCase")
            self.post_tweet_use_case = PostTweetUseCase(twitter_gateway)
            logger.debug("Instance PostTweetUseCase créée")

            logger.debug("Création de l'instance GenerateTweetUseCase")
            self.generate_tweet_use_case = GenerateTweetUseCase(openai_gateway)
            logger.debug("Instance GenerateTweetUseCase créée")
        except ConfigurationError as e:
            logger.error(f"Échec de l'initialisation de la CLI : {str(e)}")
            raise

    @log_method(logger)
    def run(self):
        try:
            logger.debug("Lecture du fichier prompt")
            prompt = read_prompt_file("techaware_pro_prompt_for_x.txt")
            logger.debug(f"Prompt lu depuis le fichier : {prompt[:50]}...")  # Log les 50 premiers caractères du prompt
        except FileNotFoundError as e:
            logger.error(f"Fichier prompt non trouvé : {str(e)}")
            print("Le fichier prompt n'a pas été trouvé. Utilisation d'un prompt par défaut.")
            prompt = "Générez un tweet intéressant sur la technologie."
        except IOError as e:
            logger.error(f"Erreur lors de la lecture du fichier prompt : {str(e)}")
            print("Erreur lors de la lecture du fichier prompt. Utilisation d'un prompt par défaut.")
            prompt = "Générez un tweet intéressant sur la technologie."

        try:
            if prompt:
                logger.debug("Génération d'un tweet avec OpenAI")
                generated_tweet = self.generate_tweet_use_case.execute(prompt)
                logger.debug(f"Tweet généré : {generated_tweet}")
                print(f"Tweet généré : {generated_tweet}")
                time.sleep(5)
                tweet_text = generated_tweet
            else:
                tweet_text = "Hello World !"

            logger.debug("Exécution de PostTweetUseCase")
            result = self.post_tweet_use_case.execute(tweet_text)
            logger.debug(f"Résultat de l'exécution de PostTweetUseCase : {result}")

            print(f"Tweet posté avec succès. ID du tweet : {result['data']['id']}")
            logger.success(f"Tweet posté avec succès. ID : {result['data']['id']}")
        except ValidationError as e:
            error_msg = f"Tweet invalide : {str(e)}"
            logger.warning(error_msg)
            print(error_msg)
        except TwitterError as e:
            error_msg = f"Erreur lors de la publication sur Twitter : {str(e)}"
            logger.error(error_msg)
            print(error_msg)
        except TweetGenerationError as e:
            error_msg = f"Erreur lors de la génération du tweet : {str(e)}"
            logger.error(error_msg)
            print(error_msg)
        except OpenAIError as e:
            error_msg = f"Erreur avec OpenAI : {str(e)}"
            logger.error(error_msg)
            print(error_msg)
        except AutomatorError as e:
            error_msg = f"Une erreur s'est produite : {str(e)}"
            logger.error(error_msg)
            print(error_msg)
        except Exception as e:
            error_msg = f"Une erreur inattendue s'est produite : {str(e)}"
            logger.error(error_msg, exc_info=True)
            print(error_msg)