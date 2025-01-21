# PDF Masking Library

**pdf-masking-library** is a Python library designed to process PDF files by masking sensitive information using Optical Character Recognition (OCR). It supports masking predefined patterns such as Aadhaar numbers, PAN numbers, and custom patterns provided by the user.

## A Simple Example

```python
import base64
from pdf_masking_library import process_pdf

base64_pdf_input = "Your base64 here"
custom_pattern = [r"\b\d{2}\b"]

base64_pdf_output = process_pdf(base64_pdf_input, custom_pattern=custom_pattern)

# Save the masked PDF to a file
with open("masked_output.pdf", "wb") as output_file:
    output_file.write(base64.b64decode(base64_pdf_output))
```

### Masking Information
The library automatically detects and masks the following sensitive information:

-   Aadhaar Numbers: 12-digit Indian identification numbers.
-   PAN Numbers: 10-character alphanumeric Permanent Account Numbers.
-    Custom Patterns: User-defined patterns using regular expressions.

When providing a custom pattern, use the custom_pattern parameter, as shown above.


## Command-Line Interface (CLI)
The library includes a CLI tool for easy integration into scripts and workflows.
> python -m pdf_masking_library input.pdf output.pdf --custom-pattern "\\b\\d{2}\\b"

- Mask Aadhaar and PAN Numbers (Default Behavior):
    > python -m pdf_masking_library input.pdf output.pdf 

If you do not provide a **custom pattern**, the library will automatically mask Aadhaar numbers and PAN numbers in the PDF.