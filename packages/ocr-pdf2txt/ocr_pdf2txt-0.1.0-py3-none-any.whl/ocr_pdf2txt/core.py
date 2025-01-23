import os
import re
import pytesseract
import spacy
import nltk
from nltk import tokenize
from pdf2image import convert_from_path
from PIL import Image
from typing import List

pytesseract.pytesseract.tesseract_cmd = r'/opt/homebrew/bin/tesseract'  # Adjust this for your system

try:
    nlp = spacy.load('en_core_web_sm')
except OSError:
    import subprocess
    subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
    nlp = spacy.load('en_core_web_sm')

nltk.download('punkt', quiet=True)

def ocr_batch_pdfs_to_text(
    pdf_paths: List[str],
    output_folder: str,
    reconstruct_layout: bool = True,
    anonymize: bool = False,
    anonymize_mask: str = "[REDACTED]",
    ephemeral_index: bool = False,
    summary: bool = False
):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    ephemeral_data_index = {}

    for pdf_path in pdf_paths:
        try:
            base_name = os.path.splitext(os.path.basename(pdf_path))[0]
            ocr_text_path = os.path.join(output_folder, f"{base_name}_extracted.txt")
            layout_output_path = os.path.join(output_folder, f"{base_name}_reconstructed.txt")
            summary_output_path = os.path.join(output_folder, f"{base_name}_summary.txt")

            images = convert_from_path(pdf_path)
            raw_pages = []

            for i, image in enumerate(images):
                print(f"Processing {pdf_path}, page {i+1}/{len(images)}...")
                page_text = pytesseract.image_to_string(image)
                if anonymize:
                    page_text = anonymize_text(page_text, anonymize_mask)
                raw_pages.append(page_text)

            with open(ocr_text_path, 'w') as f:
                for page_num, txt in enumerate(raw_pages, 1):
                    f.write(f"--- Page {page_num} ---\n{txt}\n")
            print(f"Saved raw OCR to {ocr_text_path}")

            if reconstruct_layout:
                reconstructed_text = reconstruct_document(images, raw_pages)
                with open(layout_output_path, 'w') as f2:
                    f2.write(reconstructed_text)
                print(f"Saved layout reconstruction to {layout_output_path}")

            if ephemeral_index:
                ephemeral_data_index[pdf_path] = "\n".join(raw_pages)

            if summary:
                summary_text = generate_dynamic_summary("\n".join(raw_pages))
                with open(summary_output_path, 'w') as sum_file:
                    sum_file.write(summary_text)
                print(f"Saved summary to {summary_output_path}")
        
        except Exception as e:
            print(f"Error processing {pdf_path}: {e}")
    
    if ephemeral_index:
        print("\nEphemeral indexing is complete. Try searching for a keyword:")
        search_keyword = input("Enter a keyword (or press Enter to skip): ").strip()
        if search_keyword:
            for doc_name, content in ephemeral_data_index.items():
                if search_keyword.lower() in content.lower():
                    print(f"Keyword found in {doc_name}")
                else:
                    print(f"Keyword not found in {doc_name}")
        print("Ephemeral index will now be discarded. Done.")

def anonymize_text(text, mask="[REDACTED]"):
    text = re.sub(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]+', mask, text)
    text = re.sub(r'\b(\+?\d{1,3}[\s.-]?)?\(?\d{2,3}\)?[\s.-]?\d{3,4}[\s.-]?\d{4}\b', mask, text)
    text = re.sub(r'\d{1,5}\s+\w+\s+(Street|St\.|Rd\.|Road|Ave\.|Avenue|Boulevard|Blvd\.|Lane|Ln\.)', mask, text, flags=re.IGNORECASE)
    return text

def reconstruct_document(images: List[Image.Image], page_texts: List[str]) -> str:
    reconstructed = []
    for index, page_text in enumerate(page_texts):
        reconstructed.append(f"--- Page {index+1}: Attempted Layout Reconstruction ---\n")
        lines = page_text.split("\n")
        for line in lines:
            reconstructed.append(line)
        reconstructed.append("\n")
    return "\n".join(reconstructed)

def generate_dynamic_summary(text):
    cleaned_text = re.sub(r'\s+', ' ', text.strip())
    doc = nlp(cleaned_text)

    entity_dict = {}
    for ent in doc.ents:
        entity_dict[ent.text] = entity_dict.get(ent.text, 0) + 1

    sentences = tokenize.sent_tokenize(cleaned_text)
    sentence_scores = {}
    for sentence in sentences:
        for entity_text, count in entity_dict.items():
            if entity_text in sentence:
                sentence_scores[sentence] = sentence_scores.get(sentence, 0) + count

    if not sentence_scores:
        return "No significant summary could be generated."

    ranked_sentences = sorted(sentence_scores, key=sentence_scores.get, reverse=True)
    summary_sentence_count = min(5, len(ranked_sentences))
    top_sentences = ranked_sentences[:summary_sentence_count]
    summary_text = " ".join(top_sentences)

    return f"DYNAMIC SUMMARY:\n\n{summary_text}\n\nEND OF SUMMARY."