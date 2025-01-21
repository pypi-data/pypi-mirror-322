import re
import logging
from .logger_config import setup_logger

custom_pattern = []
# custom_pattern.append(re.compile(r"\b\d{2}\b"))

logger = setup_logger(log_file="masking_app.log", log_level=logging.DEBUG)

def add_custom_patterns(name, pattern):
    try:
        custom_pattern.append(re.compile(pattern))
        logger.info(f"Custom pattern {name} added successfully. ")
    except re.error as e:
        logger.error(f"Failed to compile custom pattern {name} : {e}")
        
def get_custom_pattern():
    return custom_pattern

# add_custom_pattern("credit_card", r'\d{16}')  # 16-digit credit card numbers
# add_custom_pattern("license_plate", r'[A-Z]{2}\d{2}[A-Z]{2}\d{4}')  # License plate pattern