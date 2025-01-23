# This file makes Python treat the ocr_pdf2txt folder as a package.
# You can import symbols from core.py here to simplify user imports.

from .core import (
    ocr_pdf_to_text,
    visualize_ocr,
    generate_audio,
    detect_topics,
    check_poppler
)