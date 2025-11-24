import os
import re
from collections import Counter
from datetime import datetime

# try optional heavy deps
try:
    from pdfminer.high_level import extract_text
except Exception:
    def extract_text(path):
        # minimal fallback: return empty
        return ""

try:
    import pytesseract
    import cv2
    def extract_text_from_image(path):
        image = cv2.imread(path)
        if image is None:
            return ""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        return pytesseract.image_to_string(cv2.medianBlur(thresh, 3))
except Exception:
    def extract_text_from_image(path):
        return ""

# spaCy optional
try:
    import spacy
    try:
        nlp = spacy.load("en_core_web_sm")
    except Exception:
        nlp = None
except Exception:
    nlp = None

# sentence-transformers optional
try:
    from sentence_transformers import SentenceTransformer, util
    model = SentenceTransformer('all-MiniLM-L6-v2')
except Exception:
    model = None

NOISY_TERMS = {
    "skill", "skills", "developer", "stack", "framework", "tools",
    "language", "technologies", "programming", "software", "web", "experience"
}

TECHNICAL_SKILLS = {
    "programming": ["python", "java", "c++", "c", "javascript", "typescript", "ruby", "go", "rust"],
    "web": ["html", "css", "react", "angular", "vue", "django", "flask", "node.js", "express"],
    "database": ["mysql", "postgresql", "mongodb", "oracle", "sql", "nosql", "sqlite"],
    "tools": ["git", "docker", "kubernetes", "aws", "azure", "gcp", "jenkins", "terraform"],
    "ml_ai": ["machine learning", "deep learning", "pytorch", "tensorflow", "scikit-learn", "nlp", "computer vision"],
    "data": ["pandas", "numpy", "matplotlib", "seaborn", "powerbi", "tableau", "data analysis"]
}

TECH_SKILL_SET = set(
    skill.lower()
    for group in TECHNICAL_SKILLS.values()
    for skill in group
    if skill.lower() not in NOISY_TERMS
)

ALL_SYNONYMS = {}

# utilities

def extract_email(text):
    match = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-z]{2,}", text)
    return match.group(0) if match else "—"


def extract_text_from_pdf_path(path):
    try:
        return extract_text(path)
    except Exception:
        return ""


def extract_section(text, section):
    text = re.sub(r'\r\n', '\n', text)
    text = re.sub(r'\n{2,}', '\n\n', text)
    headers = [
        r'skills?', r'technical\s+skills?', r'experience', r'work\s+experience',
        r'certifications?', r'education', r'projects?', r'qualifications?',
        r'work\s+history', r'professional\s+summary', r'technical\s+proficiencies'
    ]
    pattern = rf'(?i)\b{section}\b[\s:\-]*\n([\s\S]+?)(?=\n(?:{"|".join(headers)})[\s:\-]*\n|\Z)'
    match = re.search(pattern, text, re.IGNORECASE)
    return match.group(1).strip() if match else ""


def normalize_keyword(term):
    term = term.strip().lower()
    for k, syns in ALL_SYNONYMS.items():
        if term == k or term in syns:
            return k
    return term


def extract_keywords_spacy(text):
    if nlp:
        doc = nlp(text)
        keywords = set()
        for token in doc:
            if token.pos_ in {"NOUN", "PROPN", "ADJ"} and not token.is_stop and token.is_alpha:
                norm = normalize_keyword(token.lemma_.lower())
                if len(norm) >= 3 and norm not in NOISY_TERMS:
                    keywords.add(norm)
        return list(keywords)
    # fallback: simple split
    words = re.findall(r"\b[a-zA-Z]{3,}\b", text.lower())
    common = Counter(words).most_common(40)
    return [w for w,_ in common]


def is_partial_match(keyword, text, threshold=0.85):
    from difflib import SequenceMatcher
    for word in text.split():
        if SequenceMatcher(None, keyword, word).ratio() >= threshold:
            return True
    return False


def extract_technical_skills(text, job_keywords):
    text_lower = text.lower()
    expanded_keywords = set()
    for kw in job_keywords:
        expanded_keywords.add(kw)
        expanded_keywords.update(ALL_SYNONYMS.get(kw, []))
        for group in TECHNICAL_SKILLS.values():
            if kw in group:
                expanded_keywords.update(group)

    matched = []
    for kw in expanded_keywords:
        if re.search(r'\b' + re.escape(kw) + r'\b', text_lower) or is_partial_match(kw, text_lower):
            matched.append(kw)

    if len(matched) < 4:
        for tech in TECH_SKILL_SET:
            if tech not in matched and tech in text_lower:
                matched.append(tech)
                if len(matched) >= 10:
                    break

    return matched[:10]


def semantic_similarity(text, job_desc):
    try:
        if model:
            res_emb = model.encode(text, convert_to_tensor=True)
            job_emb = model.encode(job_desc, convert_to_tensor=True)
            return round(util.cos_sim(res_emb, job_emb).item() * 100, 2)
    except Exception:
        pass
    return 0.0


def keyword_density(text, keywords):
    text = text.lower()
    word_count = len(text.split()) or 1
    hits = sum(text.count(kw) for kw in keywords)
    return min(hits / word_count, 0.04)


def weighted_resume_score(text, job_keywords, job_desc):
    sections = {
        'skills': extract_section(text, "skills") or text,
        'experience': extract_section(text, "experience") or text,
        'certifications': extract_section(text, "certifications") or text,
        'education': extract_section(text, "education") or text,
        'projects': extract_section(text, "projects") or text
    }

    weights = {
        'skills': 0.3,
        'projects': 0.2,
        'experience': 0.2,
        'certifications': 0.15,
        'education': 0.1
    }

    total_keywords = len(job_keywords) or 1
    total_score = 0
    matched_all = []

    for section, weight in weights.items():
        matched = extract_technical_skills(sections[section], job_keywords)
        unique_matches = set(matched)
        matched_all.extend(unique_matches)
        section_score = len(unique_matches) / total_keywords
        total_score += section_score * weight

    # Global matches as fallback boost
    global_matches = extract_technical_skills(text, job_keywords)
    global_unique = set(global_matches) - set(matched_all)
    matched_all.extend(global_unique)

    # Semantic similarity gets slightly higher weight now
    sim = semantic_similarity(text, job_desc)
    total_score += 0.25 * (sim / 100)

    # Keyword density boost
    density_ratio = keyword_density(text, job_keywords)
    total_score += density_ratio * 0.5

    # Penalty if less than 30% of keywords matched globally
    match_ratio = len(set(matched_all)) / total_keywords
    if match_ratio < 0.3:
        total_score *= 0.85  # reduce score if very low match

    final_score = round(min(total_score * 100, 100), 2)

    tag = "Shortlisted" if final_score >= 85 else "Rejected" if final_score < 50 else "Review"
    top_skills = [s for s, _ in Counter(matched_all).most_common(10)]
    missing = list(set(job_keywords) - set(top_skills))

    return final_score, top_skills, tag, missing


if __name__ == '__main__':
    print('ai_ranker module loaded')
