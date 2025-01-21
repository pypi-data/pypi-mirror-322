import unittest
from flask import json
import base64
from ..pdf_masking_library import process_pdf

class TestPDFMasking(unittest.TestCase):
    def setUp(self):
        """Set up the test client and other necessary variables."""
        self.app = process_pdf.test_client()
        self.app.testing = True

    def test_process_pdf_success(self):
        """Test processing a valid PDF."""
        with open('test_files/sample.pdf', 'rb') as f:
            base64_pdf = base64.b64encode(f.read()).decode('utf-8')
        
        response = self.app.post('/process_pdf', json={'Base64': base64_pdf})
        self.assertEqual(response.status_code, 200)
        self.assertIn('pdfBase64', json.loads(response.data))

    def test_process_pdf_no_file(self):
        """Test processing when no file is provided."""
        response = self.app.post('/process_pdf', json={})
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', json.loads(response.data))

    def test_process_pdf_invalid_base64(self):
        """Test processing with invalid base64 data."""
        response = self.app.post('/process_pdf', json={'Base64': 'invalid_base64'})
        self.assertEqual(response.status_code, 500)
        self.assertIn('error', json.loads(response.data))

    def test_process_pdf_empty_file(self):
        """Test processing an empty PDF file."""
        empty_pdf_base64 = base64.b64encode(b'').decode('utf-8')
        response = self.app.post('/process_pdf', json={'Base64': empty_pdf_base64})
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', json.loads(response.data))

    def test_process_pdf_with_invalid_json(self):
        """Test processing with invalid JSON structure."""
        response = self.app.post('/process_pdf', data='not_json')
        self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main()
