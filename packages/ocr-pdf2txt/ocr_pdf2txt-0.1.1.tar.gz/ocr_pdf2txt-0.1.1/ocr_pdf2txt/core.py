import os
import re
import shutil
import pytesseract
import spacy
import nltk
from nltk import tokenize
from pdf2image import convert_from_path
from PIL import Image, ImageDraw
from gtts import gTTS
from typing import List, Dict
import webbrowser

# Auto-detect Tesseract executable
tesseract_path = shutil.which("tesseract")
if not tesseract_path:
    raise EnvironmentError("Tesseract is not installed or not in PATH. Please install it.")

pytesseract.pytesseract.tesseract_cmd = tesseract_path

# Ensure required NLP models are loaded
try:
    nlp = spacy.load('en_core_web_sm')
except OSError:
    import subprocess
    subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
    nlp = spacy.load('en_core_web_sm')

nltk.download('punkt', quiet=True)

def check_poppler():
    """
    Ensure `pdftoppm` (poppler-utils) is installed for pdf2image.
    Raises an error if not found. 
    """
    if not shutil.which("pdftoppm"):
        raise EnvironmentError("Poppler-utils not found. Please install it to use pdf2image.")

check_poppler()

def ocr_pdf_to_text(
    pdf_path: str,
    output_folder: str,
    visualize: bool = False,
    audio_output: bool = False,
    semantic_topics: bool = False
):
    """
    Extract text from a single PDF file, optionally generate 
    an HTML visualization of OCR, produce an audio output, 
    and detect high-level semantic topics.

    Args:
        pdf_path (str): Path to the input PDF file.
        output_folder (str): Folder to store output text, HTML, and audio files.
        visualize (bool): If True, creates an HTML overlay visualization for each page.
        audio_output (bool): If True, generates an MP3 file of the extracted text.
        semantic_topics (bool): If True, prints recognized topics from the text.

    Raises:
        EnvironmentError: If an external dependency is not available.
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    base_name = os.path.splitext(os.path.basename(pdf_path))[0]
    text_output_path = os.path.join(output_folder, f"{base_name}_extracted.txt")
    audio_output_path = os.path.join(output_folder, f"{base_name}.mp3")
    images = convert_from_path(pdf_path)

    text_data = []

    for i, image in enumerate(images):
        print(f"Processing page {i+1}/{len(images)}...")
        text = pytesseract.image_to_string(image)
        text_data.append(text)

        if visualize:
            visualize_ocr(image, text, output_folder, base_name, i+1)

    with open(text_output_path, "w") as f:
        for page_num, page_text in enumerate(text_data, 1):
            f.write(f"--- Page {page_num} ---\n{page_text}\n")
    print(f"Text saved to {text_output_path}")

    if audio_output:
        generate_audio("\n".join(text_data), audio_output_path)

    if semantic_topics:
        topics = detect_topics("\n".join(text_data))
        print(f"Detected Topics: {', '.join(topics)}")

def visualize_ocr(image: Image.Image, text: str, output_folder: str, base_name: str, page_num: int):
    """
    Create an HTML visualization of OCR output using HOCR data. 
    Opens the result in the default web browser. 
    """
    hocr = pytesseract.image_to_pdf_or_hocr(image, extension="hocr")
    html_output_path = os.path.join(output_folder, f"{base_name}_page{page_num}.html")

    with open(html_output_path, "wb") as f:
        f.write(hocr)
    print(f"Visualization saved to {html_output_path}")

    webbrowser.open(f"file://{os.path.abspath(html_output_path)}")

def generate_audio(text: str, output_path: str):
    """
    Convert text to speech and save as an MP3 file using gTTS.
    """
    tts = gTTS(text)
    tts.save(output_path)
    print(f"Audio saved to {output_path}")

def detect_topics(text: str) -> List[str]:
    """
    Detect high-level semantic topics via spaCy’s named entity recognition.
    Returns a list of distinct entity labels from the extracted text.
    """
    doc = nlp(text)
    topics = set(ent.label_ for ent in doc.ents)
    return list(topics)

# Example usage - demonstration only.
# In a real library, users can call these functions directly from their code.
if __name__ == "__main__":
    pdf_path = "/path/to/your/input.pdf"  # Replace with real path
    output_folder = "/path/to/output_folder"  # Replace with real folder
    ocr_pdf_to_text(
        pdf_path=pdf_path,
        output_folder=output_folder,
        visualize=True,
        audio_output=True,
        semantic_topics=True
    )