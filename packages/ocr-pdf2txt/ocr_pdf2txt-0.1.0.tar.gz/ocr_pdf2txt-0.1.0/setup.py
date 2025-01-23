from setuptools import setup, find_packages

setup(
    name="ocr_pdf2txt",
    version="0.1.0",
    author="Piyush Acharya",
    author_email="hey@piyushacharya.com",
    description="OCR library with layout reconstruction, anonymization, and summarization",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/ocr_pdf2txt",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=["pytesseract", "pdf2image", "spacy", "nltk", "Pillow"],
)