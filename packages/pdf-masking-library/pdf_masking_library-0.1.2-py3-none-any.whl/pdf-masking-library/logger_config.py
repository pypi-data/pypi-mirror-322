import logging
from logging.handlers import RotatingFileHandler

def setup_logger(name=None, log_file="app.log", log_level=logging.INFO, max_bytes=5 * 1024 * 1024, backup_count=5):
    """
    Sets up a logger with file and console handlers.
    
    :param name: Logger name. If None, the root logger is configured.
    :param log_file: File to log messages to.
    :param log_level: Logging level (e.g., logging.DEBUG, logging.INFO).
    :param max_bytes: Maximum size of the log file before rotation (in bytes).
    :param backup_count: Number of backup files to retain.
    :return: Configured logger instance.
    """
    # Create a logger instance
    logger = logging.getLogger(name)
    logger.setLevel(log_level)

    # Check if handlers are already added to avoid duplication
    if not logger.handlers:
        # File handler with rotation
        file_handler = RotatingFileHandler(
            log_file, maxBytes=max_bytes, backupCount=backup_count
        )
        file_handler.setLevel(log_level)
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(file_formatter)

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)
        console_formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s'
        )
        console_handler.setFormatter(console_formatter)

        # Add handlers to logger
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger

# # Example of usage
# if __name__ == "__main__":
#     # Setup logger
#     logger = setup_logger(name="MaskingApp", log_file="masking_app.log", log_level=logging.DEBUG)
    
#     # Example log messages
#     logger.debug("Debug message")
#     logger.info("Info message")
#     logger.warning("Warning message")
#     logger.error("Error message")
#     logger.critical("Critical message")
