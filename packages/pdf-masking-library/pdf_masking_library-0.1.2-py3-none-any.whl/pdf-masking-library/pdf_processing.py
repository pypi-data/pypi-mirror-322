from pdf2image import convert_from_bytes
import pytesseract
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from pdfrw import PdfReader
import logging
import re

from .logger_config import setup_logger
from .ocr_extraction import extract_coordinates_from_hocr
from .utils import get_pdf_dimensions, polyval

logger = setup_logger(log_file="masking_app.log", log_level=logging.DEBUG)

def process_page(page_num, pdf_bytes, pdf_reader, custom_pattern=None):
    """ Process each page to get its sensitive information to mask in the PDF """
    try:
        if custom_pattern:
            # If custom_pattern is a string, compile it into a list
            if isinstance(custom_pattern, str):
                custom_pattern = [re.compile(custom_pattern)]
            # If custom_pattern is a list, ensure all elements are compiled regex patterns
            elif isinstance(custom_pattern, list):
                custom_pattern = [re.compile(pattern) if isinstance(pattern, str) else pattern for pattern in custom_pattern]
            else:
                # If custom_pattern is not a valid type, raise an error
                raise ValueError("custom_pattern must be a string or a list of compiled patterns.")
        else:
            # Default behavior if no custom pattern is provided
            custom_pattern = []
        image = convert_from_bytes(pdf_bytes,  first_page=page_num, last_page=page_num)[0]
        dpi = image.info.get('dpi', (200,))[0]
        hocr_data = pytesseract.image_to_pdf_or_hocr(image, extension='hocr',lang='eng+kan', config='--psm 6').decode('utf-8')
        aadhaar_coords, pan_coords, thumb_coords, custom_coords = extract_coordinates_from_hocr(hocr_data, page_num, custom_pattern = custom_pattern)
        sensitive_positions = aadhaar_coords + pan_coords + thumb_coords + custom_coords

        if not sensitive_positions:
            return page_num, None

        packet = BytesIO()
        c = canvas.Canvas(packet, pagesize=letter)
        scale_factor = 72 / dpi
        width, height = get_pdf_dimensions(pdf_reader, page_num - 1)

        for position in sensitive_positions:
            if len(position) == 3:
                (x0, y0, x1, y1), b,  page = position
                
                x0 *= scale_factor
                y0 *= scale_factor
                x1 *= scale_factor
                y1 *= scale_factor
                
                c.setFillColorRGB(0, 0, 0)
                rect_width = x1 - x0
                rect_height = y1 - y0
                c.roundRect(x0, height - b - 3, rect_width + 5, rect_height + 5, 0, fill=1)
            else:
                (x0, y0, x1, y1), page = position
                baseline = [0, 0]
                
                x0 *= scale_factor
                y0 *= scale_factor
                x1 *= scale_factor
                y1 *= scale_factor
                
                b = (polyval(baseline, (x0 + x1) / 2) + y1)
                
                if thumb_coords :
                    
                    c.setFillColorRGB(0, 0, 0)
                    rect_width = 65
                    rect_height = 65
                    c.roundRect(x0 - 30, height - b + 10, rect_width , rect_height , 0, fill=1)
                    
                else:
                    c.setFillColorRGB(0, 0, 0)
                    rect_width = x1 - x0
                    rect_height = y1 - y0
                    c.roundRect(x0, height - b - 3, rect_width + 5, rect_height + 5, 0, fill=1)

        c.save()
        packet.seek(0)
        return page_num, PdfReader(packet).pages[0]
    except Exception as e:
        logger.error(f"Error processing page {page_num}: {e}")
        return page_num, None