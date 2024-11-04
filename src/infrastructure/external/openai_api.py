import openai
import re
import random
import PyPDF2
import os
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

    def read_pdf(self, file_path):
        """Fonction utilitaire pour lire un fichier PDF"""
        content = ""
        with open(file_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                content += page.extract_text() + "\n"
        return content

    @log_method(logger)
    def generate(self, prompt: str) -> str:
        try:
            # Définir le chemin vers les fichiers knowledge
            knowledge_path = "resources/knowledge/"
            guideline_files = []
            topic_files = []
            relevant_link = {}

            # Charger les fichiers selon leur type
            for file_name in os.listdir(knowledge_path):
                if file_name.endswith(".pdf"):
                    # Fichiers de directives (premier mot en majuscule)
                    if file_name[0:3].isupper():
                        guideline_files.append(file_name)
                    # Fichiers de sujets (commencent par "page")
                    elif file_name.startswith("page"):
                        if "Entreprise" in file_name:
                            topic_files.append(file_name)
                            relevant_link[file_name] = "https://www.techaware.net/pour-les-entreprises "
                        elif "Temoignage" in file_name:
                            topic_files.append(file_name)
                            relevant_link[file_name] = "https://www.techaware.net/temoignage-satochip "
                        elif "Developpeur" in file_name:
                            relevant_link[file_name] = "https://www.techaware.net/pour-les-developpeurs "
                            topic_files.append(file_name)
                        elif "EtudeCasKevin" in file_name:
                            topic_files.append(file_name)
                            relevant_link[file_name] = "https://www.techaware.net/pour-les-https://www.techaware.net/etude-de-cas "
                        elif "accueil" in file_name:
                            topic_files.append(file_name)
                            relevant_link[file_name] = "https://www.techaware.net/bienvenue "

            # Lire le contenu des fichiers de directives (guidelines)
            guideline_content = ""
            for file in guideline_files:
                guideline_content += self.read_pdf(os.path.join(knowledge_path, file))

            # Lire le contenu des fichiers de sujets (topics)
            topic_content = ""
            for file in topic_files:
                topic_content += self.read_pdf(os.path.join(knowledge_path, file))

            # Créer le prompt système avec le contenu chargé
            system_prompt = f"""
            You are an automation assistant specialized in social media marketing and SEO. Your task is to create, optimize, schedule, and publish posts on X (formerly Twitter), LinkedIn, and Facebook using the provided content from Tech Aware.

            Provide the final social media post enclosed within a <social_media_post> tag.

            You have access to various files that contain important information to create social media posts. The files are classified into two main categories:

            1. **Guidelines for Creating the Publication**: {guideline_content}

            2. **Topics for the Publication**: {random.choices([link for link in relevant_link])} where dict key are topics and value are the relevant link to include in the final publication

            Your task is to choose an appropriate topic from the relevant "page" files, and use the information in the "Guideline" files to ensure that the content is optimized and suitable for the platform. Always include a link to the corresponding page in the generated post to direct the audience towards more information. The link can be found in the content of the topic file itself.

            Provide the final social media post enclosed within a <social_media_post> tag.

            Make sure each post is tailored to the specific platform to maximize engagement, SEO-friendly, relevant, and effective for driving user interaction and brand visibility.

            Example output format:

            Automator assistant

            Vous avez raison, je m'excuse pour cet oubli. Voici la publication Facebook encadrée par la balise <social_media_post> comme demandé :

            <social_media_post> 🌟 Améliorez vos Projets Tech avec l'Aide de Tech Aware ! 🚀

            Chez Satochip, notre collaboration avec Tech Aware nous a permis de franchir des étapes cruciales en intégrant des talents comme Kevin, dont les compétences ont transformé notre façon de travailler. Grâce à Tech Aware, nous avons accès à des développeurs qualifiés et prêts à nous aider à atteindre nos objectifs.

            🔍 Pourquoi choisir Tech Aware ?

            Sélection Rigoureuse : Nous vous connectons uniquement avec des développeurs qualifiés qui correspondent à vos besoins spécifiques.
            Mentorat Expert : Chaque professionnel est soutenu par un mentorat de qualité pour assurer son intégration et sa performance au sein de votre équipe.
            Adaptation aux Projets : Les compétences des développeurs sont constamment alignées avec les exigences de vos projets grâce à une formation continue.
            ✨ Rejoignez les rangs des entreprises qui réalisent des projets innovants avec l’aide de Tech Aware. Découvrez plus sur nos services et comment nous pouvons vous aider à transformer votre équipe tech ici : {relevant_link} </social_media_post>

            Cette balise permet de délimiter clairement le contenu destiné à être publié sur les réseaux sociaux.
            
            FULL OUTPUT IN FRENCH INCLUDING pageTopic source link
            """

            # Appel à l'API OpenAI pour générer la publication
            logger.debug(f"Génération d'une publication avec le prompt donné")
            response = self.client.chat.completions.create(
                model="gpt-4-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ]
            )
            generated_content = response.choices[0].message.content.strip()

            # Vérifier si le contenu a été généré
            if generated_content:
                logger.debug(f"Contenu généré : {generated_content}")
                # Utiliser une expression régulière pour extraire le texte entre <social_media_post> et </social_media_post>
                match = re.search(r"<social_media_post>(.*?)</social_media_post>", generated_content, re.DOTALL)
                if match:
                    # Extraire le contenu entre les balises et supprimer les '**'
                    generated_content = match.group(1).strip()
                    generated_content = re.sub(r"\*\*", "", generated_content)
                    generated_content.strip('.')
                    logger.debug(f"Contenu extrait entre les balises (sans '**') : {generated_content}")
                else:
                    logger.error("Impossible de trouver le contenu entre les balises <social_media_post>")
                    raise ValueError("Le contenu généré ne contient pas les balises <social_media_post>.")
                return generated_content
            else:
                raise OpenAIError("Le contenu généré est vide.")
        except Exception as e:
            logger.error(f"Échec de la génération de la publication : {str(e)}")
            raise OpenAIError(f"Échec de la génération de la publication : {str(e)}")
