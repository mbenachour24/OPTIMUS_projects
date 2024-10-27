# logging_config.py
import logging

def configure_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # Clear existing handlers
    if logger.hasHandlers():
        logger.handlers.clear()

    # File handler
    file_handler = logging.FileHandler('optimodular.log', 'a')
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter('%(message)s')
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_formatter = logging.Formatter('%(message)s')
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    logger.info("Logger configuration complete.")

# Additional specific file handler
def add_specific_file_handler(filename='OFFICIALJOURNAL2.log'):
    specific_handler = logging.FileHandler(filename, 'a')
    specific_handler.setLevel(logging.DEBUG)
    specific_formatter = logging.Formatter('%(message)s')
    specific_handler.setFormatter(specific_formatter)
    logger = logging.getLogger()
    logger.addHandler(specific_handler)