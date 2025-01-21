import logging

from .logger_config import setup_logger

logger = setup_logger(log_file="masking_app.log", log_level=logging.DEBUG)

# def configure_logging(log_file="app.log", log_level=logging.INFO):
#     """
#     Configures logging for the application.
#     :param log_file: The file to store logs.
#     :param log_level: Logging level (e.g., logging.INFO, logging.DEBUG).
#     """
#     logging.basicConfig(
#         filename=log_file,
#         filemode='a',
#         format='%(asctime)s - %(levelname)s - %(message)s',
#         datefmt='%Y-%m-%d %H:%M:%S',
#         level=log_level,
#     )
#     console = logging.StreamHandler()
#     console.setLevel(log_level)
#     formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
#     console.setFormatter(formatter)
#     logging.getLogger('').addHandler(console)
    
def get_pdf_dimensions(pdf, page_num):
    """Get the width and height of the PDF."""
    try:
        page = pdf.pages[page_num]
        width = float(page.MediaBox[2])
        height = float(page.MediaBox[3])
    except Exception as e:
        logger.error(f"Error getting PDF dimensions: {e}")
        width, height = 0, 0
    return width, height

def polyval(poly, x):
    """Evaluate a polynomial at a given value of x."""
    return x * poly[0] + poly[1]