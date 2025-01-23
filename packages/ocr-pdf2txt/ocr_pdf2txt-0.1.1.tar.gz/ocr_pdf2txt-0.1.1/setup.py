import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ocr_pdf2txt",
    version="0.1.1",
    author="Piyush Acharya",
    author_email="hey@piyushacharya.com",
    description="OCR library with advanced PDF to text, layout visuals, and audio generation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/VerisimilitudeX/ocr_pdf2txt",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "pytesseract",
        "pdf2image",
        "spacy",
        "nltk",
        "Pillow",
        "gTTS",
    ],
)