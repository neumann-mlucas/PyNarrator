import logging
import sys
from pathlib import Path

# TODO: use config options

# Configure the logger name matching your module's name
LOGGER_NAME = "pynarrator"


def setup_logging(log_file="pynarrator.log"):
    "sets up logging for the module"
    logger = logging.getLogger(LOGGER_NAME)
    logger.setLevel(logging.DEBUG)  # Adjust as needed

    # Create a file handler for outputting logs to a file
    log_file_path = Path(log_file).absolute()
    file_handler = logging.FileHandler(log_file_path)
    file_handler.setLevel(logging.DEBUG)

    # Create a console handler for outputting logs to stdout
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)  # Adjust as needed for console output

    # Define the log message format
    log_format = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(log_format)
    console_handler.setFormatter(log_format)

    # Add the handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


# Setup the logger immediately when this module is imported
logger = setup_logging()


def get_logger():
    return logger
