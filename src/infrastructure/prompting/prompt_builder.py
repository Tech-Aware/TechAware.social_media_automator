# src/infrastructure/prompting/prompt_builder.py

"""
This module implements the PromptBuilder class which is responsible for constructing
prompts for different social media platforms. It combines randomly selected topics
with platform-specific formatting guidelines to generate engaging content.
"""

from typing import Dict, Optional, List
import random
from src.infrastructure.logging.logger import logger, log_method
from src.domain.exceptions import ValidationError, ConfigurationError
from src.interfaces.prompt_builder_gateway import PromptBuilderGateway


class PromptBuilder(PromptBuilderGateway):
    """
    A concrete implementation of PromptBuilderGateway for creating customized prompts
    for social media content generation. Combines topic selection with platform-specific
    formatting guidelines.
    """

    # Base de données des sujets disponibles
    TOPICS_DATABASE = {
        'business': [
            {
                'subject': 'Réduction des coûts de production',
                'context': 'Les entreprises cherchent à innover sans dépasser leurs budgets. Collaborer avec des développeurs expérimentés peut être coûteux, surtout pour des projets plus restreints.',
                'problem': 'Les coûts élevés du développement freinent les petites entreprises et limitent leur capacité à réaliser des projets digitaux.',
                'solution': 'En offrant l\'opportunité de travailler avec des développeurs juniors supervisés, Tech Aware aide les entreprises à économiser jusqu\'à 70 % sur les coûts de production, sans compromis sur la qualité.',
                'link': 'https://www.techaware.net/pour-les-entreprises'
            },
            {
                'subject': 'Avantages du partenariat avec Tech Aware',
                'context': 'Les entreprises recherchent des solutions de développement flexibles, efficaces et rentables, qui leur garantissent un retour rapide sur investissement.',
                'problem': 'La méfiance envers les développeurs juniors rend difficile la collaboration, car les entreprises craignent un manque de compétences et d\'efficacité.',
                'solution': 'Le partenariat avec Tech Aware assure un retour sur investissement rapide, avec des développeurs juniors encadrés qui produisent des résultats concrets à des coûts réduits.',
                'link': 'https://www.techaware.net/pour-les-entreprises'
            },
            {
                'subject': 'Témoignages Satochip',
                'context': 'Les entreprises hésitent souvent à confier des projets à des développeurs juniors en raison de l\'incertitude concernant la qualité des livrables.',
                'problem': 'Cette réticence est souvent liée au manque de preuves concrètes montrant la réussite de collaborations similaires.',
                'solution': 'Le témoignage client de Satochip.io montre que les développeurs juniors de Tech Aware, encadrés par des mentors, sont capables de fournir des résultats de haute qualité.',
                'link': 'https://www.techaware.net/temoignage-satochip'
            },
            {
                'subject': 'Support et mentorat',
                'context': 'La qualité et l\'efficacité des projets de développement sont des priorités pour les entreprises, qui souhaitent éviter les risques liés à une mauvaise gestion de leurs projets.',
                'problem': 'Les entreprises craignent que des développeurs juniors, sans supervision, produisent des livrables de qualité inférieure.',
                'solution': 'Les développeurs juniors de Tech Aware sont encadrés par des mentors experts, assurant un soutien continu et une qualité conforme aux attentes des entreprises.',
                'link': 'https://www.techaware.net/pour-les-entreprises'
            },
            {
                'subject': 'Processus de collaboration simplifié',
                'context': 'Les entreprises, surtout les PME, recherchent des processus d\'engagement clairs et rapides pour ne pas perdre de temps et maximiser leur productivité.',
                'problem': 'Les procédures compliquées ou lentes découragent souvent les entreprises à engager de nouvelles collaborations, en particulier les petites structures avec des ressources limitées.',
                'solution': 'Tech Aware propose un processus de collaboration en trois étapes pour faciliter et accélérer la collaboration, de la demande initiale à l’intégration du partenaire dans les projets, expliqué directement sur la page entreprise.',
                'link': 'https://www.techaware.net/pour-les-entreprises'
            },
            {
                'subject': 'Solutions sur mesure',
                'context': 'Les besoins et budgets des entreprises varient considérablement, nécessitant une flexibilité dans les offres de services de développement.',
                'problem': 'Les offres de service rigides excluent les entreprises ayant des budgets limités ou des besoins spécifiques pour des projets de moindre envergure.',
                'solution': 'Tech Aware propose plusieurs options tarifaires (basique, avancée, premium), permettant aux entreprises de choisir le niveau de service le plus adapté à leurs projets et à leur budget.',
                'link': 'https://www.techaware.net/pour-les-entreprises'
            }
            # ... autres sujets business possibles
        ],
        'developer': [
            {
                'subject': 'Accès à des missions concrètes',
                'context': 'Les développeurs débutants ou en reconversion éprouvent souvent des difficultés à accéder à des projets réels pour acquérir de l\'expérience pratique.',
                'problem': 'Sans expérience concrète, il est difficile pour eux d\'améliorer leurs compétences et de constituer un portfolio convaincant.',
                'solution': 'Tech Aware propose aux développeurs des missions concrètes, leur permettant de mettre en pratique leurs compétences, d\'accumuler de l\'expérience, et de se construire un portfolio solide.',
                'link': 'https://www.techaware.net/pour-les-developpeurs'
            },
            {
                'subject': 'Opportunités de freelance',
                'context': 'Beaucoup de développeurs souhaitent travailler en freelance pour bénéficier de flexibilité et pour gérer eux-mêmes leur carrière.',
                'problem': 'Le manque d\'expérience et de réseau rend difficile la recherche de clients et la gestion d\'une activité indépendante.',
                'solution': 'Tech Aware aide les développeurs à se préparer à une activité de freelance en leur fournissant des missions pratiques et des conseils, facilitant ainsi leur transition vers une carrière indépendante.',
                'link': 'https://www.techaware.net/pour-les-developpeurs'
            },
            {
                'subject': 'Mentorat personnalisé',
                'context': 'Les développeurs en reconversion peuvent se sentir isolés et ont souvent besoin de guidance pour s’assurer qu’ils progressent efficacement dans leurs apprentissages et leurs projets.',
                'problem': 'Sans accompagnement, il est facile de stagner ou de prendre de mauvaises habitudes de travail, ce qui peut limiter leur progression.',
                'solution': 'Tech Aware offre un mentorat personnalisé avec des experts en développement, apportant un soutien régulier et des conseils adaptés pour aider chaque développeur à atteindre ses objectifs. Des exemples de mentorat réussi sont partagés dans les études de cas.',
                'link': 'https://www.techaware.net/etude-de-cas'
            },
            {
                'subject': 'Développement de la confiance en soi',
                'context': 'Les développeurs en début de carrière ou en reconversion manquent parfois de confiance en leurs compétences, ce qui peut les décourager.',
                'problem': 'Ce manque de confiance peut les freiner dans leur progression et les empêcher de postuler à des projets ou des postes pour lesquels ils seraient pourtant qualifiés.',
                'solution': 'Grâce aux missions concrètes et au mentorat offert par Tech Aware, les développeurs peuvent renforcer leur confiance en voyant leur travail valorisé et en recevant des retours positifs.',
                'link': 'https://www.techaware.net/pour-les-developpeurs'
            },
            {
                'subject': 'Formation continue',
                'context': 'Le secteur du développement évolue rapidement, et les compétences doivent être mises à jour régulièrement pour rester compétitif.',
                'problem': 'Les développeurs peuvent éprouver des difficultés à identifier les compétences importantes à acquérir et à trouver des ressources fiables pour se former.',
                'solution': 'Tech Aware propose des formations en ligne et des ressources adaptées aux besoins actuels du marché, accessibles via la page dédiée, permettant aux développeurs de continuer à se former et à se perfectionner dans les domaines les plus demandés.',
                'link': 'https://www.techaware.net/slides'
            }
            # ... autres sujets developer possibles
        ],
        'slides': [
            {
                'subject': 'Défi fondamental en 4 jours',
                'context': 'Les débutants en développement recherchent des programmes intensifs et pratiques pour acquérir rapidement les bases en algorithmique et programmation.',
                'problem': 'Il est souvent difficile de trouver des formations qui combinent théorie et pratique de manière progressive pour un apprentissage efficace en peu de temps.',
                'solution': 'Cette formation de quatre jours offre une introduction complète à l\'algorithmique, incluant des exercices pratiques sur les variables, boucles, conditions, et chaînes de caractères.',
                'link': 'https://www.techaware.net/slides/defi-fondamental-exercices-pratiques-et-maitrise-des-concepts-cles-en-4-jours-formation-en-algorithmique-et-programmation-1'
            },
            {
                'subject': 'Défi de la maîtrise : Défis algorithmiques progressifs pour développeurs débutants',
                'context': 'Pour les développeurs débutants, il est crucial de renforcer leurs compétences en algorithmique par des exercices pratiques et progressifs.',
                'problem': 'De nombreuses formations manquent d\'une progression structurée, rendant difficile l’approfondissement des concepts fondamentaux en programmation et algorithmique.',
                'solution': 'Ce programme propose des défis pratiques en Python, permettant aux débutants de maîtriser la manipulation de chaînes, la gestion des nombres, les boucles, conditions, et algorithmes de tri. Les exercices permettent une montée en compétence progressive, tout en renforçant les bases indispensables pour des projets réels.',
                'link': 'https://www.techaware.net/slides/defi-de-la-maitrise-algorithmiques-progressifs-pourdeveloppeurs-debutants-3'
            },
            {
                'subject': 'Guide essentiel du développement multi-langage : Maîtrisez Python, Java et C#',
                'context': 'La polyvalence dans plusieurs langages de programmation est un atout essentiel pour les développeurs souhaitant répondre à des exigences variées dans leurs projets.',
                'problem': 'Apprendre plusieurs langages en parallèle peut être déroutant, en particulier sans une structure claire pour comprendre les spécificités de chaque langage.',
                'solution': 'Ce guide multi-langage offre une approche structurée pour maîtriser les bases de Python, Java, et C#, permettant aux développeurs d’acquérir une compréhension pratique et appliquée de chaque langage. Cette formation aide à développer une expertise adaptable pour divers contextes de développement.',
                'link': 'https://www.techaware.net/slides/guide-essentiel-du-developpement-multi-langage-maitrisez-python-java-et-c-4'
            }
            # ... autres sujets slides possibles
        ]
    }

    # Guidelines spécifiques par plateforme
    PLATFORM_GUIDELINES = {
        'twitter': {
            'max_length': 280,
            'structure': """
    Structure pour X (anciennement Twitter):
    • Accroche forte avec emoji pertinent
    • Message direct et impactant
    • Solution Tech Aware avec bénéfice clé
    • Call-to-action + lien
    • 2-3 hashtags pertinents"""
        },
        'linkedin': {
            'max_length': 3000,
            'structure': """
    Structure pour LinkedIn:
    • Accroche professionnelle avec hook
    • Développement du contexte
    • Points clés de la solution Tech Aware
    • Exemple
    • Call-to-action professionnel + lien
    • 3-5 hashtags sectoriels"""
        },
        'facebook': {
            'max_length': 63206,
            'structure': """
    Structure pour Facebook:
    • Titre captivant avec emoji
    • Introduction engageante
    • Développement de la problématique
    • Solution Tech Aware détaillée
    • Mini cas pratique ou témoignage
    • Call-to-action + lien
    • 2-3 hashtags pertinents"""
        }
    }

    BRAND_STYLES = [
        {
            "name": "Direct et accessible",
            "description": "S'adresse à l'audience comme à des amis ou des collègues, créant une proximité naturelle. Utilise un langage simple et des exemples concrets."
        },
        {
            "name": "Pédagogique",
            "description": "Simplifie des concepts complexes, construit une progression logique avec des anecdotes et des références culturelles."
        }
    ]

    BRAND_TONES = [
        {
            "name": "Engagé et critique",
            "description": "Éveille une prise de conscience en questionnant les implications des tendances technologiques."
        },
        {
            "name": "Énergique et captivant",
            "description": "Emploie des termes marquants et un vocabulaire imagé pour captiver l'attention sur des sujets complexes."
        }
    ]

    BRAND_PERSONALITIES = [
        {
            "name": "Curieux et vigilant",
            "description": "Montre une grande curiosité et une prudence face aux nouvelles technologies."
        },
        {
            "name": "Transparent et engagé",
            "description": "Valorise la transparence et se soucie du bien-être de son audience."
        },
        {
            "name": "Visionnaire et prudent",
            "description": "Présente une vision du futur tout en avertissant des risques potentiels."
        }
    ]

    @log_method(logger)
    def _select_random_voice(self):
        """Sélectionne aléatoirement un style, un ton et une personnalité."""
        import random
        style = random.choice(self.BRAND_STYLES)
        tone = random.choice(self.BRAND_TONES)
        personality = random.choice(self.BRAND_PERSONALITIES)

        logger.debug(
            f"Selected voice elements - Style: {style['name']}, Tone: {tone['name']}, Personality: {personality['name']}")

        return {
            'style': style,
            'tone': tone,
            'personality': personality
        }

    @log_method(logger)
    def __init__(self) -> None:
        """Initialize the PromptBuilder with default values."""
        logger.debug("Initializing PromptBuilder")
        self._platform: Optional[str] = None
        self._topic_category: Optional[str] = None
        self._selected_topic: Optional[Dict] = None
        self._custom_instructions: str = ""
        logger.debug("PromptBuilder initialized successfully")

    @property
    def platform(self) -> Optional[str]:
        """Get the currently configured platform."""
        return self._platform

    @property
    def topic_category(self) -> Optional[str]:
        """Get the currently configured topic category."""
        return self._topic_category

    @property
    def selected_topic(self) -> Optional[Dict]:
        """Get the currently selected topic."""
        return self._selected_topic

    @property
    def custom_instructions(self) -> str:
        """Get the current custom instructions."""
        return self._custom_instructions

    @log_method(logger)
    def reset(self) -> None:
        """Reset the builder to its initial state."""
        logger.debug("Resetting PromptBuilder to initial state")
        self._platform = None
        self._topic_category = None
        self._selected_topic = None
        self._custom_instructions = ""
        logger.debug("PromptBuilder reset completed")

    @log_method(logger)
    def select_random_topic(self, category: str) -> Dict:
        """
        Select a random topic from the specified category.

        Args:
            category (str): The topic category to select from

        Returns:
            Dict: The selected topic information

        Raises:
            ValidationError: If category is invalid
        """
        try:
            if category not in self.TOPICS_DATABASE:
                logger.error(f"Invalid topic category: {category}")
                raise ValidationError(f"Invalid topic category: {category}")

            topics = self.TOPICS_DATABASE[category]
            selected_topic = random.choice(topics)
            logger.debug(f"Selected topic: {selected_topic['subject']}")
            return selected_topic

        except ValidationError as e:
            raise e
        except Exception as e:
            logger.error(f"Error selecting random topic: {str(e)}")
            raise ValidationError(f"Failed to select random topic: {str(e)}") from e

    @log_method(logger)
    def set_platform_and_topic_category(self, platform: str, topic_category: str) -> 'PromptBuilder':
        """
        Set the platform and topic category, and select a random topic.

        Args:
            platform (str): The target platform
            topic_category (str): The topic category to select from

        Returns:
            PromptBuilder: The builder instance

        Raises:
            ValidationError: If parameters are invalid
            ConfigurationError: If configuration fails
        """
        try:
            if not isinstance(platform, str) or not isinstance(topic_category, str):
                logger.error("Platform and topic_category must be strings")
                raise ValidationError("Platform and topic_category must be strings")

            platform = platform.lower()
            topic_category = topic_category.lower()

            if platform not in self.PLATFORM_GUIDELINES:
                logger.error(f"Unsupported platform: {platform}")
                raise ValidationError(f"Unsupported platform: {platform}")

            self._platform = platform
            self._topic_category = topic_category
            self._selected_topic = self.select_random_topic(topic_category)

            logger.debug(f"Platform set to: {platform}, topic category: {topic_category}")
            return self

        except ValidationError as e:
            logger.error(f"Validation error: {str(e)}")
            raise ValidationError(f"Invalid configuration: {str(e)}") from e
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            raise ConfigurationError(f"Configuration failed: {str(e)}") from e

    @log_method(logger)
    def add_custom_instructions(self, instructions: str) -> 'PromptBuilder':
        """Add custom instructions to the prompt."""
        try:
            if not isinstance(instructions, str):
                logger.error("Instructions must be a string")
                raise ValidationError("Instructions must be a string")

            self._custom_instructions = instructions.strip()
            logger.debug("Custom instructions added")
            return self

        except ValidationError as e:
            logger.error(f"Validation error: {str(e)}")
            raise ValidationError(f"Invalid instructions: {str(e)}") from e
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            raise ValidationError(f"Failed to add instructions: {str(e)}") from e

    @log_method(logger)
    def build(self) -> str:
        try:
            if not all([self._platform, self._topic_category, self._selected_topic]):
                logger.error("Platform and topic must be set before building prompt")
                raise ConfigurationError("Platform and topic must be set before building prompt")

            platform_info = self.PLATFORM_GUIDELINES[self._platform]
            topic = self._selected_topic
            voice = self._select_random_voice()

            brand_voice = f"""
    Voix de marque sélectionnée pour cette publication:

    Style: {voice['style']['name']}
    {voice['style']['description']}

    Ton: {voice['tone']['name']}
    {voice['tone']['description']}

    Personnalité: {voice['personality']['name']}
    {voice['personality']['description']}"""

            prompt_parts = [
                f"Générez une publication {self._platform} originale et engageante sur le sujet suivant de Tech Aware:",
                f"\nInformations sur le sujet:",
                f"Sujet: {topic['subject']}",
                f"Contexte: {topic['context']}",
                f"Problème: {topic['problem']}",
                f"Solution: {topic['solution']}",
                f"URL à inclure: {topic['link']}",
                "\nVoix de marque à adopter pour cette publication:",
                brand_voice,
                f"\nStructure pour {self._platform}:",
                platform_info['structure'],
                f"\nConsignes importantes:",
                "1. Créez un contenu UNIQUE et ORIGINAL",
                f"2. Adaptez la voix sélectionnée au format {self._platform}",
                "3. Utilisez des emojis pertinents avec modération",
                f"4. Respectez la limite de {platform_info['max_length']} caractères",
                "5. Rédigez en français avec un style naturel et engageant",
                "\nInstructions CRUCIALES pour l'URL:",
                "- Incluez l'URL en texte brut, exactement comme fournie",
                "- N'utilisez PAS de syntaxe Markdown ou de crochets",
                "- CORRECT: 'Découvrez plus sur https://www.techaware.net/pour-les-entreprises'",
                "- INCORRECT: '[Découvrez plus](https://www.techaware.net/pour-les-entreprises)'",
                "- INCORRECT: '[Tech Aware pour les Entreprises](lien)'",
                "\nFormat OBLIGATOIRE de la réponse:",
                "1. Votre réponse DOIT commencer par <social_media_post>",
                "2. Votre réponse DOIT se terminer par </social_media_post>",
                "3. La publication COMPLÈTE doit être à l'intérieur de ces balises",
                "4. Ne mettez RIEN avant ou après ces balises",
                "\nExemple de format (à ne pas copier):",
                "<social_media_post>",
                "Votre contenu ici...",
                "URL en texte brut...",
                "</social_media_post>",
            ]

            if self._custom_instructions:
                prompt_parts.append(f"\nInstructions supplémentaires:\n{self._custom_instructions}")

            final_prompt = "\n".join(prompt_parts)
            logger.success(
                f"Prompt built successfully with voice: {voice['style']['name']}, {voice['tone']['name']}, {voice['personality']['name']}")
            return final_prompt

        except ValidationError as e:
            logger.error(f"Validation error: {str(e)}")
            raise ValidationError(f"Failed to build prompt: {str(e)}") from e
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            raise ConfigurationError(f"Failed to build prompt: {str(e)}") from e