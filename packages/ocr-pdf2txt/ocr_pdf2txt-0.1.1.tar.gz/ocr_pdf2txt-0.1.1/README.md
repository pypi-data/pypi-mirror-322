# ocr_pdf2txt

This library extracts text from PDF files using OCR, automatically discovers poppler and Tesseract dependencies, and even allows you to visualize recognized text, generate audio, and detect broad semantic topics. 

## Features
- Cross-platform (Mac, Windows, Linux) with automatic detection of Tesseract.
- HTML visualization of recognized text on each page.
- Audio file generation for reading PDF content aloud.
- Semantic topic detection leveraging spaCy’s named entity recognition.

## Installation

```bash
pip install ocr_pdf2txt
```

## Usage

```python
from ocr_pdf2txt import ocr_pdf_to_text

pdf_path = "sample.pdf"
output_folder = "output_dir"

ocr_pdf_to_text(
    pdf_path=pdf_path,
    output_folder=output_folder,
    visualize=True,      # Show OCR overlay in HTML
    audio_output=True,   # Generate an MP3 of recognized text
    semantic_topics=True # Print out recognized semantic topics
)
```

Make sure you have Tesseract and Poppler installed on your machine. Check documentation for your operating system if you run into issues.

## License

MIT. See [LICENSE](LICENSE) for more information.
