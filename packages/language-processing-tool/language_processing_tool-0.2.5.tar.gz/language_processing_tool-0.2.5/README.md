# Language Processing Tool

This Python package provides functionality to process PDFs and detect languages in the documents.

## Installation

You can install the package using pip:


## Usage

For batch processing:

process-pdfs /path/to/input/ /path/to/csv_file.csv /path/to/output/



For single PDF processing:

process-pdfs path.pdf

```
language_processing_tool
├─ LICENSE
├─ MANIFEST.in
├─ README.md
├─ build
│  ├─ bdist.linux-x86_64
│  └─ lib
│     └─ language_processing_tool
│        ├─ __init__.py
│        ├─ process_pdfs.py
│        └─ sourcecode.py
├─ dist
│  ├─ language-processing-tool-0.2.4.tar.gz
│  └─ language_processing_tool-0.2.4-py3-none-any.whl
├─ language_processing_tool
│  ├─ __init__.py
│  └─ process_pdfs.py
├─ language_processing_tool.egg-info
│  ├─ PKG-INFO
│  ├─ SOURCES.txt
│  ├─ dependency_links.txt
│  ├─ entry_points.txt
│  ├─ requires.txt
│  └─ top_level.txt
├─ pyproject.toml
├─ requirements.txt
├─ setup.py
└─ tests
   └─ test.py

```