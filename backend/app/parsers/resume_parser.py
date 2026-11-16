"""
Resume parsing module for PDF, DOCX, and text formats.
Extracts candidate personal details, education, years of experience, and full text.
"""

import io
import re
from typing import Dict, Any, List, Optional
from datetime import datetime
from pypdf import PdfReader
from docx import Document

from app.nlp.taxonomy import extract_skills_from_text, get_skill_names


EMAIL_REGEX = re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+")
PHONE_REGEX = re.compile(r"(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}")
LINKEDIN_REGEX = re.compile(r"(?:https?://)?(?:www\.)?linkedin\.com/in/[a-zA-Z0-9_-]+", re.IGNORECASE)
GITHUB_REGEX = re.compile(r"(?:https?://)?(?:www\.)?github\.com/[a-zA-Z0-9_-]+", re.IGNORECASE)

EXP_EXPLICIT_REGEX = re.compile(
    r"(\d+(?:\.\d+)?)\s*\+?\s*(?:years?|yrs?)(?:\s+(?:of\s+)?(?:experience|exp|in\s+software|in\s+industry))?",
    re.IGNORECASE
)

DATE_RANGE_REGEX = re.compile(
    r"\b(Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?|\d{1,2}/)?\s*(\d{4})\s*(?:-|–|—|to)\s*(Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?|\d{1,2}/)?\s*(\d{4}|present|current|now)\b",
    re.IGNORECASE
)

EDUCATION_KEYWORDS = [
    (r"\b(?:ph\.?d|doctor\s+of\s+philosophy|doctorate)\b", "PhD"),
    (r"\b(?:m\.?s|master\s+of\s+science|m\.?tech|m\.?b\.?a|master(?:'s)?)\b", "Master's Degree"),
    (r"\b(?:b\.?s|b\.?tech|b\.?e|bachelor\s+of\s+science|bachelor(?:'s)?|bba|bca)\b", "Bachelor's Degree"),
    (r"\b(?:associate(?:'s)?\s+degree|diploma)\b", "Associate / Diploma")
]


def extract_text_from_pdf(file_bytes: bytes) -> str:
    """Extract readable text from PDF bytes."""
    reader = PdfReader(io.BytesIO(file_bytes))
    text_parts = []
    for page in reader.pages:
        txt = page.extract_text()
        if txt:
            text_parts.append(txt)
    return "\n".join(text_parts).strip()


def extract_text_from_docx(file_bytes: bytes) -> str:
    """Extract readable text from DOCX bytes."""
    doc = Document(io.BytesIO(file_bytes))
    text_parts = [p.text for p in doc.paragraphs if p.text.strip()]
    for table in doc.tables:
        for row in table.rows:
            row_txt = " | ".join([cell.text.strip() for cell in row.cells if cell.text.strip()])
            if row_txt:
                text_parts.append(row_txt)
    return "\n".join(text_parts).strip()


def extract_contact_info(text: str) -> Dict[str, Optional[str]]:
    """Extract email, phone, and profile URLs."""
    email_match = EMAIL_REGEX.search(text)
    phone_match = PHONE_REGEX.search(text)
    linkedin_match = LINKEDIN_REGEX.search(text)
    github_match = GITHUB_REGEX.search(text)

    return {
        "email": email_match.group(0) if email_match else None,
        "phone": phone_match.group(0) if phone_match else None,
        "linkedin": linkedin_match.group(0) if linkedin_match else None,
        "github": github_match.group(0) if github_match else None,
    }


def guess_candidate_name(text: str, filename: str) -> str:
    """
    Infers candidate name from resume heading or filename fallback.
    """
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    for line in lines[:6]:
        # Filter out common headers, email, phone, resume words
        if (
            len(line) < 40
            and not EMAIL_REGEX.search(line)
            and not PHONE_REGEX.search(line)
            and not any(k in line.lower() for k in ["resume", "curriculum", "vitae", "summary", "profile", "contact", "page"])
            and re.match(r"^[A-Z][a-zA-Z\s\.\-']+$", line)
        ):
            return line

    # Fallback to cleaning filename
    clean_fn = re.sub(r"[-_]", " ", filename)
    clean_fn = re.sub(r"\.(pdf|docx|txt)$", "", clean_fn, flags=re.I)
    clean_fn = re.sub(r"\b(resume|cv|profile|senior|junior|lead|developer|engineer)\b", "", clean_fn, flags=re.I).strip()
    return clean_fn.title() if clean_fn else "Candidate"


def calculate_experience_years(text: str) -> float:
    """
    Calculates candidate years of experience using explicit statements and work history date ranges.
    """
    # 1. Search for explicit overall experience statements
    explicit_matches = EXP_EXPLICIT_REGEX.findall(text)
    explicit_years = [float(m) for m in explicit_matches if 0 < float(m) <= 40]
    
    # 2. Date ranges
    current_year = datetime.now().year
    ranges = DATE_RANGE_REGEX.findall(text)
    total_months = 0

    month_lookup = {
        "jan": 1, "feb": 2, "mar": 3, "apr": 4, "may": 5, "jun": 6,
        "jul": 7, "aug": 8, "sep": 9, "oct": 10, "nov": 11, "dec": 12
    }

    for start_month_raw, start_yr, end_month_raw, end_yr_raw in ranges:
        try:
            s_year = int(start_yr)
            if s_year < 1980 or s_year > current_year:
                continue
            
            s_month = 1
            if start_month_raw:
                sm = start_month_raw[:3].lower()
                s_month = month_lookup.get(sm, 1)

            if end_yr_raw.lower() in ["present", "current", "now"]:
                e_year = current_year
                e_month = datetime.now().month
            else:
                e_year = int(end_yr_raw)
                e_month = 12
                if end_month_raw:
                    em = end_month_raw[:3].lower()
                    e_month = month_lookup.get(em, 12)

            if e_year < s_year:
                continue

            months = (e_year - s_year) * 12 + (e_month - s_month)
            if 0 < months <= 480:  # within 40 years
                total_months += months
        except Exception:
            continue

    calculated_years_from_dates = round(total_months / 12.0, 1) if total_months > 0 else 0.0

    # If explicit experience is stated in the summary/header (e.g. "6+ years"), prioritize it
    if explicit_years:
        return explicit_years[0]
    elif calculated_years_from_dates > 0:
        return calculated_years_from_dates
    
    return 1.0  # default baseline if unspecified


def extract_education(text: str) -> str:
    """Identify highest education credential found."""
    for pattern, label in EDUCATION_KEYWORDS:
        if re.search(pattern, text, re.IGNORECASE):
            return label
    return "Not explicitly specified"


def parse_resume(file_bytes: bytes, filename: str) -> Dict[str, Any]:
    """
    Parses a single resume file (PDF, DOCX, or TXT) and returns structured candidate details.
    """
    fn_lower = filename.lower()
    if fn_lower.endswith(".pdf"):
        raw_text = extract_text_from_pdf(file_bytes)
    elif fn_lower.endswith(".docx"):
        raw_text = extract_text_from_docx(file_bytes)
    else:
        raw_text = file_bytes.decode("utf-8", errors="ignore")

    contact = extract_contact_info(raw_text)
    name = guess_candidate_name(raw_text, filename)
    skills_data = extract_skills_from_text(raw_text)
    skill_names = get_skill_names(skills_data)
    years_exp = calculate_experience_years(raw_text)
    education = extract_education(raw_text)

    # First ~300 chars or summary section for display
    summary_snippet = " ".join(raw_text.split()[:50]) + "..." if raw_text else "No content extracted."

    return {
        "filename": filename,
        "name": name,
        "email": contact["email"] or "N/A",
        "phone": contact["phone"] or "N/A",
        "linkedin": contact["linkedin"],
        "github": contact["github"],
        "experience_years": years_exp,
        "education": education,
        "skills": skill_names,
        "skills_detailed": skills_data,
        "summary": summary_snippet,
        "raw_text": raw_text
    }
