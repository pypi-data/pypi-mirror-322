from setuptools import setup, find_packages

setup(
    name="language_processing_tool",  # The name of your package
    version="0.1.0",                 # The version of your package
    description="A tool to detect languages in PDF documents",
    author="Harish Kumar",
    author_email="harishkumar56278@gmail.com",
    packages=find_packages(),        # Automatically find the packages
    install_requires=[               # List of external dependencies
        'pymupdf',
        'pytesseract',
        'langdetect',
        'pandas',
        'pillow',
        'icecream',
    ],
    classifiers=[                    # Classify your package
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',          # Specify minimum Python version
)
