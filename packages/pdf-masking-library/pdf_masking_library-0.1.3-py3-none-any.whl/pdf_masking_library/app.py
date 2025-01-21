import time
import base64
from io import BytesIO
from pdf2image import convert_from_bytes
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from pdfrw import PdfReader, PdfWriter, PageMerge
import logging
from concurrent.futures import ThreadPoolExecutor

from .logger_config import setup_logger
from .pdf_processing import process_page

logger = setup_logger(log_file="masking_app.log", log_level=logging.DEBUG)

def process_pdf(base64_pdf_input, custom_pattern=None):
    """
    Process a PDF from a Base64 input and mask sensitive information.

    Args:
        base64_pdf_input (str): The Base64-encoded PDF string to be processed.
        custom_pattern (list, optional): List of custom regex patterns for masking. Defaults to None.

    Returns:
        str: Base64-encoded processed PDF.
    """
    start_time = time.time()

    try:
        if not base64_pdf_input:
            raise ValueError("No Base64 input provided")

        # Decode the Base64-encoded PDF
        pdf_bytes_old = base64.b64decode(base64_pdf_input)
        images = convert_from_bytes(pdf_bytes_old, fmt='jpeg', dpi=100)

        # Create a new PDF buffer
        pdf_buffer = BytesIO()
        pdf_canvas = canvas.Canvas(pdf_buffer, pagesize=letter)

        # Convert images to PDF
        for img in images:
            img_buffer = BytesIO()
            img.save(img_buffer, format="JPEG")
            img_buffer.seek(0)

            img_reader = ImageReader(img_buffer)
            pdf_canvas.drawImage(img_reader, 0, 0, width=letter[0], height=letter[1])
            pdf_canvas.showPage()

        pdf_canvas.save()
        pdf_buffer.seek(0)

        # Re-encode the PDF
        new_pdf_bytes = pdf_buffer.read()
        base64_pdf = base64.b64encode(new_pdf_bytes).decode('utf-8')
        pdf_bytes = base64.b64decode(base64_pdf)

        # Read the PDF and process pages
        try:
            pdf_reader = PdfReader(BytesIO(pdf_bytes))
        except Exception as e:
            logger.error(f"Error reading original PDF: {e}")
            raise e

        num_pages = len(pdf_reader.pages)
        writer = PdfWriter()

        with ThreadPoolExecutor() as executor:
            futures = [
                executor.submit(process_page, i + 1, pdf_bytes, pdf_reader, custom_pattern=custom_pattern)
                for i in range(num_pages)
            ]
            for future in futures:
                page_num, new_page = future.result()
                original_page = pdf_reader.pages[page_num - 1]
                if new_page:
                    PageMerge(original_page).add(new_page).render()
                writer.addpage(original_page)

        # Encode the final PDF as Base64
        output_buffer = BytesIO()
        writer.write(output_buffer)
        output_buffer.seek(0)
        encode_bytes = output_buffer.read()
        encode_pdf_bytes = base64.b64encode(encode_bytes).decode('utf-8')

        execution_time = time.time() - start_time
        logger.info(f"Total execution time: {execution_time:.2f} seconds")

        return encode_pdf_bytes

    except Exception as e:
        logger.error(f"Error in processing PDF: {e}")
        raise e

