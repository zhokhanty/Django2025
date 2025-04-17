import fitz
import docx
import re
from collections import Counter


def extract_text_from_pdf(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def extract_text_from_docx(file):
    doc = docx.Document(file)
    return "\n".join([para.text for para in doc.paragraphs])

def parse_resume(file):
    filename = file.name.lower()
    if filename.endswith(".pdf"):
        text = extract_text_from_pdf(file)
    elif filename.endswith(".docx"):
        text = extract_text_from_docx(file)
    else:
        raise ValueError("Unsupported file type")

    return {
        "name": extract_name(text),
        "email": extract_email(text),
        "skills": extract_skills(text),
        "education": extract_education(text),
        "experience": extract_experience(text),
    }

def extract_email(text):
    match = re.search(r'[\w\.-]+@[\w\.-]+', text)
    return match.group(0) if match else None

def extract_name(text):
    return text.split('\n')[0]

def extract_skills(text):
    keywords = ["Python", "Django", "JavaScript", "SQL", "React"]
    return [kw for kw in keywords if kw.lower() in text.lower()]

def extract_education(text):
    return "Bachelor's in Computer Science" if "bachelor" in text.lower() else None

def extract_experience(text):
    return "2+ years experience" if "experience" in text.lower() else None

import json

with open('resume/market_skills.json') as f:
    MARKET_SKILLS = json.load(f)

def compute_skill_gaps(resume_skills):
    return [skill for skill in MARKET_SKILLS if skill not in resume_skills]

def formatting_suggestions(parsed_text):
    suggestions = []
    if 'Summary' not in parsed_text:
        suggestions.append("Добавьте раздел `Summary` в начале резюме.")
    if len(parsed_text.split()) > 800:
        suggestions.append("Сократите общее количество слов (рекомендуется ≤ 800).")
    return suggestions

def keyword_recommendations(resume_text, job):
    # берём skills и ключевые слова из описания
    keywords = set(job.required_skills + re.findall(r'\b[A-Z][a-zA-Z]+\b', job.description))
    word_counts = Counter(re.findall(r'\w+', resume_text.lower()))
    recs = [kw for kw in keywords if word_counts[kw.lower()] < 1]
    return recs
