import argparse
import base64
import logging
from .app import process_pdf
from .logger_config import setup_logger

# Set up the logger
logger = setup_logger(log_file="masking_app.log", log_level=logging.INFO)

def main():
    # Argument parser for command-line usage
    parser = argparse.ArgumentParser(description="PDF Masking Library CLI")
    parser.add_argument("input_pdf", help="Path to the input PDF file")
    parser.add_argument("output_pdf", help="Path to save the output masked PDF file")
    parser.add_argument("--custom-pattern", nargs="*", help="Custom regex patterns for masking", default=None) 

    args = parser.parse_args()

    try:
        # Read the input PDF as Base64
        with open(args.input_pdf, "rb") as f:
            base64_pdf_input = base64.b64encode(f.read()).decode("utf-8")

        # Process the PDF
        logger.info(f"Processing file: {args.input_pdf}")
        processed_pdf_base64 = process_pdf(base64_pdf_input, custom_pattern=args.custom_pattern)

        # Decode and save the output PDF
        output_pdf_bytes = base64.b64decode(processed_pdf_base64)
        with open(args.output_pdf, "wb") as f:
            f.write(output_pdf_bytes)

        logger.info(f"Masked PDF saved to: {args.output_pdf}")
        print(f"Masked PDF saved to: {args.output_pdf}")

    except Exception as e:
        logger.error(f"Error processing PDF: {e}")
        print(f"Error processing PDF: {e}")

if __name__ == "__main__":
    main()

#CLI command example
# python -m pdfProcessor input.pdf output.pdf --custom-pattern "\\b\\d{2}\\b"
# python -m pdfProcessor "C:\Users\USER\Downloads\CC Search.pdf" "C:\Users\USER\Documents\ghostscript\Image_processing\masked_output.pdf"
# python -m pdfProcessor "C:\Users\USER\Downloads\CC Search.pdf" "C:\Users\USER\Documents\ghostscript\Image_processing\masked_output.pdf" --custom-pattern "\b\d{4}\b"