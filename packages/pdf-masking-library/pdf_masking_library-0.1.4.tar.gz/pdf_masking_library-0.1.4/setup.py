from setuptools import setup, find_packages

setup(
    name='pdf-masking-library',
    version='0.1.4',
    author='Demo',
    author_email='demo@example.com',
    description='A library for processing PDFs with OCR and masking sensitive information',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    # url='https://github.com/yourusername/pdf-processor-library',
    packages=find_packages(),
    install_requires=[
        'pytesseract',
        'pdf2image',
        'pdfrw',
        'lxml',
        'reportlab',
        'Pillow',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3',
)
