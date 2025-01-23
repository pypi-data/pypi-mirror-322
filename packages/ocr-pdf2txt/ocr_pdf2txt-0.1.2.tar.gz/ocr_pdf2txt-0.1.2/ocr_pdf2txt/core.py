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
from typing import List, Dict, Optional
import webbrowser
import subprocess
import concurrent.futures
import tabula
from transformers import pipeline
from googletrans import Translator

tesseract_path = shutil.which("tesseract")
if not tesseract_path:
    raise EnvironmentError("Tesseract is not installed or not in PATH.")
pytesseract.pytesseract_cmd = tesseract_path

try:
    nlp = spacy.load('en_core_web_sm')
except OSError:
    subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
    nlp = spacy.load('en_core_web_sm')

nltk.download('punkt', quiet=True)

def check_poppler():
    if not shutil.which("pdftoppm"):
        raise EnvironmentError("Poppler-utils (pdftoppm) is not installed.")

check_poppler()

def pdf_to_text_only(pdf_path: str) -> str:
    images = convert_from_path(pdf_path)
    text_parts = []
    for image in images:
        text_parts.append(pytesseract.image_to_string(image))
    return "\n".join(text_parts)

def ocr_pdf_to_text(pdf_path: str, output_folder: str):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    base_name = os.path.splitext(os.path.basename(pdf_path))[0]
    text_output_path = os.path.join(output_folder, f"{base_name}_extracted.txt")
    audio_output_path = os.path.join(output_folder, f"{base_name}.mp3")
    images = convert_from_path(pdf_path)
    text_data = []

    for i, image in enumerate(images):
        print(f"Processing page {i+1}/{len(images)} of {pdf_path}")
        raw_text = pytesseract.image_to_string(image)
        text_data.append(raw_text)
        visualize_ocr(image, raw_text, output_folder, base_name, i+1)

    full_text = "\n".join(text_data)
    with open(text_output_path, "w") as f:
        f.write(full_text)
    print(f"Text saved to {text_output_path}")

    generate_audio(full_text, audio_output_path)

    topics = detect_topics(full_text)
    print("Detected topics:", ", ".join(topics))

    summarized = advanced_summarize(full_text)
    summary_path = os.path.join(output_folder, f"{base_name}_advanced_summary.txt")
    with open(summary_path, "w") as sum_file:
        sum_file.write(summarized)
    print(f"Advanced summary saved to {summary_path}")

    translated_text = translate_text(full_text, "es")
    translation_path = os.path.join(output_folder, f"{base_name}_translated.txt")
    with open(translation_path, "w") as trans_file:
        trans_file.write(translated_text)
    print(f"Translated text saved to {translation_path}")

def visualize_ocr(image: Image.Image, text: str, output_folder: str, base_name: str, page_num: int):
    hocr_data = pytesseract.image_to_pdf_or_hocr(image, extension="hocr")
    html_output_path = os.path.join(output_folder, f"{base_name}_page{page_num}.html")
    with open(html_output_path, "wb") as f:
        f.write(hocr_data)
    print(f"Visualization saved to {html_output_path}")
    webbrowser.open(f"file://{os.path.abspath(html_output_path)}")

def generate_audio(text: str, output_path: str):
    tts = gTTS(text)
    tts.save(output_path)
    print(f"Audio saved to {output_path}")

def detect_topics(text: str) -> List[str]:
    doc = nlp(text)
    return list(set(ent.label_ for ent in doc.ents))

def advanced_summarize(long_text: str, max_length: int = 300) -> str:
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    max_chunk_size = 2000
    words = long_text.split()
    chunks = []
    while words:
        part = " ".join(words[:max_chunk_size])
        words = words[max_chunk_size:]
        summary_out = summarizer(part, max_length=max_length, min_length=50, do_sample=False)
        chunks.append(summary_out[0]["summary_text"])
    return "\n".join(chunks)

def translate_text(text: str, language: str) -> str:
    translator = Translator()
    result = translator.translate(text, dest=language)
    return result.text

def extract_tables_from_pdf(pdf_path: str, output_csv_path: str, pages: str = "all"):
    tabula.convert_into(pdf_path, output_csv_path, pages=pages)
    print(f"Extracted tables saved to {output_csv_path}")

def ocr_batch_pdfs_to_text(
    pdf_paths: List[str],
    output_folder: str,
    max_workers: int = 4
):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []
        for pdf_path in pdf_paths:
            futures.append(executor.submit(ocr_pdf_to_text, pdf_path, output_folder))
        concurrent.futures.wait(futures)
    print("Batch OCR complete.")
    