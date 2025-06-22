# metadata_utils.py

import fitz
import docx
import pytesseract
from pdf2image import convert_from_path
import spacy
from rake_nltk import Rake
import nltk

nltk.download("punkt")
nltk.download("stopwords")
nlp = spacy.load("en_core_web_sm")

def extract_text_from_pdf(path):
    with fitz.open(path) as doc:
        return "".join(page.get_text() for page in doc)

def extract_text_from_docx(path):
    return "\n".join(para.text for para in docx.Document(path).paragraphs)

def extract_text_from_txt(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def extract_text_with_ocr(path):
    images = convert_from_path(path)
    return "".join(pytesseract.image_to_string(img) for img in images)

def extract_text(file_path, ext):
    if ext == ".pdf":
        text = extract_text_from_pdf(file_path)
        if not text.strip():
            text = extract_text_with_ocr(file_path)
    elif ext == ".docx":
        text = extract_text_from_docx(file_path)
    elif ext == ".txt":
        text = extract_text_from_txt(file_path)
    else:
        raise ValueError("Unsupported file type")
    return text

def generate_metadata(text):
    rake = Rake()
    rake.extract_keywords_from_text(text)
    keywords = rake.get_ranked_phrases()[:10]
    summary = " ".join(nltk.sent_tokenize(text)[:3])
    entities = list({ent.text for ent in nlp(text).ents if ent.label_ in ['PERSON', 'ORG', 'GPE', 'PRODUCT']})
    title = text.strip().split("\n")[0]
    return {
        "title": title,
        "summary": summary,
        "keywords": keywords,
        "entities": entities,
        "length": len(text)
    }
