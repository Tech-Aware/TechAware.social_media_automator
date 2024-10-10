from src.presentation.cli import CLI
from src.infrastructure.logging.logger import get_logger
from src.domain.exceptions import ConfigurationError, AutomatorError

logger = get_logger(__name__)

def main():
    try:
        logger.info("Starting Automator application")
        cli = CLI()
        cli.run()
        logger.info("Automator application completed successfully")
    except ConfigurationError as e:
        logger.error(f"Configuration error: {str(e)}")
        print(f"Configuration error: {str(e)}")
    except AutomatorError as e:
        logger.error(f"Automator error: {str(e)}")
        print(f"An error occurred: {str(e)}")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {str(e)}", exc_info=True)
        print(f"An unexpected error occurred. Please check the logs for more details.")

if __name__ == "__main__":
    main()