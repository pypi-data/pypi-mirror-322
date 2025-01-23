# ocr_pdf2txt

A comprehensive Python library for extracting text from PDF files using OCR with advanced features such as layout visualization, audio generation, table extraction, summarization, and translation.

## Features

- **Text Extraction:** Extracts text from PDF files using Tesseract OCR.
- **Layout Visualization:** Generates HTML files with OCR overlays to visualize recognized text regions.
- **Audio Output:** Converts extracted text into audio files using gTTS.
- **Semantic Topic Detection:** Identifies high-level semantic topics from the extracted text using spaCy.
- **Advanced Summarization:** Summarizes the extracted text using Hugging Face transformers.
- **Translation:** Translates extracted text into specified languages using googletrans.
- **Table Extraction:** Extracts tables from PDFs into CSV files using tabula-py.
- **Batch Processing:** Processes multiple PDFs concurrently for efficient workflows.

## Installation

### Prerequisites

- **Python 3.7+**
- **Tesseract OCR:** 
  - **macOS:** `brew install tesseract`
  - **Windows:** Download from [Tesseract at UB Mannheim](https://github.com/UB-Mannheim/tesseract/wiki)
  - **Linux:** Install via package manager, e.g., `sudo apt-get install tesseract-ocr`
- **Poppler:** Required by `pdf2image`
  - **macOS:** `brew install poppler`
  - **Windows:** Download from [Poppler for Windows](http://blog.alivate.com.au/poppler-windows/)
  - **Linux:** Install via package manager, e.g., `sudo apt-get install poppler-utils`
- **Java:** Required by `tabula-py`
  - **All OS:** Download and install from [Java Downloads](https://www.java.com/en/download/)

### Install the Library

```bash
pip install ocr_pdf2txt
```

## Usage

### Single PDF Processing

```python
from ocr_pdf2txt import ocr_pdf_to_text

pdf_path = "path/to/your/input.pdf"
output_folder = "path/to/output_folder"

ocr_pdf_to_text(
    pdf_path=pdf_path,
    output_folder=output_folder
)
```

### Batch PDF Processing

```python
from ocr_pdf2txt import ocr_batch_pdfs_to_text

pdf_list = [
    "path/to/your/first.pdf",
    "path/to/your/second.pdf",
    # Add more PDF paths
]
output_folder = "path/to/output_directory"

ocr_batch_pdfs_to_text(
    pdf_paths=pdf_list,
    output_folder=output_folder,
    max_workers=4
)
```

### Extract Text Only

```python
from ocr_pdf2txt import pdf_to_text_only

pdf_path = "path/to/your/input.pdf"
text = pdf_to_text_only(pdf_path)
print(text)
```

### Extract Tables

```python
from ocr_pdf2txt import extract_tables_from_pdf

pdf_path = "path/to/your/input.pdf"
output_csv = "path/to/output.csv"

extract_tables_from_pdf(pdf_path, output_csv, pages="all")
```

## API

### ocr_pdf_to_text

Extracts text from a PDF file using OCR and saves the output to a text file.

```python
def ocr_pdf_to_text(
    pdf_path: str,
    output_folder: str
):
```

Extracts text from a single PDF file and performs the following:

- **Layout Visualization:** Creates HTML overlays of OCR results
- **Audio Output:** Generates an MP3 file of the extracted text
- **Semantic Topic Detection:** Prints detected named entity labels
- **Advanced Summarization:** Summarizes the extracted text
- **Translation:** Translates the extracted text into Spanish

### pdf_to_text_only

```python
def pdf_to_text_only(pdf_path: str) -> str:
```

Extracts text from a single PDF and returns it as a string.

### extract_tables_from_pdf

```python
def extract_tables_from_pdf(pdf_path: str, output_csv_path: str, pages: str = "all"):
```

Extracts tables from a PDF and saves them as a CSV file.

### ocr_batch_pdfs_to_text

```python
def ocr_batch_pdfs_to_text(
    pdf_paths: List[str],
    output_folder: str,
    max_workers: int = 4
):
```

Processes multiple PDFs concurrently, performing all OCR operations on each.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
