"""
Job Description (JD) parsing and requirements extraction module.
Extracts title, required skills, min years of experience, education, and key responsibilities.
"""

import re
from typing import Dict, Any, List
from app.nlp.taxonomy import extract_skills_from_text, get_skill_names
from app.parsers.resume_parser import (
    extract_text_from_pdf,
    extract_text_from_docx,
    extract_education,
    EXP_EXPLICIT_REGEX
)


TITLE_KEYWORDS = [
    r"(?:senior|lead|principal|staff|junior|associate)?\s*(?:full\s*stack|backend|frontend|software|machine\s*learning|ai|data|devops|cloud|qa|systems)\s*(?:engineer|developer|architect|scientist|lead|specialist)",
    r"(?:python|java|react|node|golang|c\+\+|aws)\s*(?:engineer|developer|architect)"
]


def extract_job_title(text: str) -> str:
    """Detects likely job title from JD text header or prominent pattern."""
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    
    # Check first 5 lines for explicit 'Job Title:' or 'Role:'
    for line in lines[:8]:
        m = re.search(r"(?:job\s*title|position|role|opening)\s*:\s*([^\n\r]+)", line, re.I)
        if m:
            return m.group(1).strip()

    # Regex search for role patterns
    for pat in TITLE_KEYWORDS:
        found = re.search(pat, text, re.I)
        if found:
            return found.group(0).strip().title()

    # Fallback to first non-empty line
    return lines[0][:50] if lines else "Software Engineer"


def extract_required_experience(text: str) -> float:
    """Extracts minimum required years of experience stated in JD."""
    # Look for patterns like "5+ years", "minimum 4 years", "3-5 years"
    min_exp_matches = re.findall(
        r"(?:at\s+least|minimum|min|required|require)?\s*(\d+(?:\.\d+)?)\s*(?:-|to)?\s*(?:\d+)?\s*\+?\s*(?:years?|yrs?)(?:\s+(?:of\s+)?(?:experience|exp|hands-on))?",
        text,
        re.I
    )
    if min_exp_matches:
        valid_nums = [float(x) for x in min_exp_matches if 0 < float(x) <= 25]
        if valid_nums:
            return min(valid_nums) # The minimum required

    # Fallback search with generic regex
    general_matches = EXP_EXPLICIT_REGEX.findall(text)
    if general_matches:
        valid_nums = [float(x) for x in general_matches if 0 < float(x) <= 25]
        if valid_nums:
            return min(valid_nums)

    return 3.0  # standard industry baseline if not mentioned


def extract_key_responsibilities(text: str) -> List[str]:
    """Extracts bullet points or key responsibility lines."""
    responsibilities = []
    lines = text.splitlines()
    in_resp_section = False

    for line in lines:
        s = line.strip()
        if not s:
            continue
        if re.search(r"\b(responsibilities|what\s+you(?:'ll|\s+will)\s+do|duties|the\s+role)\b", s, re.I):
            in_resp_section = True
            continue
        if in_resp_section and re.search(r"\b(requirements|qualifications|skills|what\s+we\s+look\s+for|benefits)\b", s, re.I):
            in_resp_section = False
            continue

        if in_resp_section and (s.startswith("-") or s.startswith("•") or s.startswith("*") or re.match(r"^\d+\.", s)):
            clean_item = re.sub(r"^[-•*\d\.\s]+", "", s).strip()
            if len(clean_item) > 10:
                responsibilities.append(clean_item)

    # Fallback if no explicit section formatting
    if not responsibilities:
        for line in lines:
            s = line.strip()
            if (s.startswith("-") or s.startswith("•")) and len(s) > 20:
                responsibilities.append(s.lstrip("-•* "))

    return responsibilities[:8]


def parse_job_description(text: str, filename: str = "JobDescription.txt") -> Dict[str, Any]:
    """Parses JD text and extracts structured requirements."""
    title = extract_job_title(text)
    skills_data = extract_skills_from_text(text)
    required_skills = get_skill_names(skills_data)
    min_exp = extract_required_experience(text)
    education = extract_education(text)
    responsibilities = extract_key_responsibilities(text)

    return {
        "title": title,
        "required_skills": required_skills,
        "skills_detailed": skills_data,
        "min_experience_years": min_exp,
        "required_education": education,
        "responsibilities": responsibilities,
        "raw_text": text
    }
