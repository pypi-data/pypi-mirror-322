from setuptools import setup, find_packages

setup(
    name="language-processing-tool",
    version="0.2.2",  # Updated version
    packages=find_packages(),
    install_requires=[
        "pytesseract",  # Example dependencies
        "langdetect",
        "pandas",
        "PyMuPDF",
        "icecream",
        "Pillow",
        "argparse",
        # Add other dependencies as needed
    ],
    entry_points={
        'console_scripts': [
            'process-pdfs = language_processing_tool.process_pdfs:main',  # Define your CLI entry point
        ],
    },
    description="A PDF language detection and OCR tool",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    author="Harish kumar S",
    author_email="harishkumar56278@gmail.com",
    url="https://github.com/Harish-nika/language-processing-tool-0.2.0.git",  # Update this URL
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # Specify Python version
)
