"""
FastAPI Application Entry Point for AI Resume Matching & Candidate Ranking System.
Provides RESTful APIs for JD analysis, batch resume parsing, semantic matching, and reporting.
"""

import os
import glob
from typing import List, Optional, Dict, Any
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel

from app.parsers.resume_parser import parse_resume
from app.parsers.jd_parser import parse_job_description
from app.nlp.matcher import match_resumes_to_jd
from app.nlp.embeddings import get_engine_status
from app.sample_data.generate_samples import SAMPLE_JDS, generate_all_samples


app = FastAPI(
    title="AI Resume Matching & Candidate Ranking API",
    description="Enterprise-grade AI engine comparing candidate resumes against Job Descriptions using hybrid semantic embeddings and skill ontology extraction.",
    version="1.0.0"
)

# Enable CORS for frontend development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SAMPLE_RESUMES_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../sample_resumes"))


class JDRequest(BaseModel):
    text: str
    filename: Optional[str] = "JobDescription.txt"


class MatchRequest(BaseModel):
    jd: Dict[str, Any]
    resumes: List[Dict[str, Any]]
    weights: Optional[Dict[str, float]] = None


@app.get("/api/health")
def health_check():
    """System status and AI embedding engine diagnostic."""
    return {
        "status": "healthy",
        "service": "AI Resume Matching & Ranking Engine",
        "ai_nlp_engine": get_engine_status(),
        "sample_resumes_available": len(glob.glob(os.path.join(SAMPLE_RESUMES_DIR, "*.*")))
    }


@app.get("/api/samples/jds")
def get_sample_jds():
    """Returns pre-configured realistic Job Descriptions for instant testing."""
    return {"job_descriptions": SAMPLE_JDS}


@app.post("/api/jd/analyze")
def analyze_jd(payload: JDRequest):
    """
    Module 1: Extract key requirements, skills, experience, and qualifications from JD.
    """
    if not payload.text or not payload.text.strip():
        raise HTTPException(status_code=400, detail="Job description text cannot be empty.")
    
    parsed = parse_job_description(payload.text, payload.filename)
    return {"job_description": parsed}


@app.post("/api/jd/upload")
async def upload_jd_file(file: UploadFile = File(...)):
    """Upload JD as PDF, DOCX, or TXT file."""
    content = await file.read()
    filename = file.filename
    fn_lower = filename.lower()

    if fn_lower.endswith(".pdf"):
        from app.parsers.resume_parser import extract_text_from_pdf
        raw_text = extract_text_from_pdf(content)
    elif fn_lower.endswith(".docx"):
        from app.parsers.resume_parser import extract_text_from_docx
        raw_text = extract_text_from_docx(content)
    else:
        raw_text = content.decode("utf-8", errors="ignore")

    parsed = parse_job_description(raw_text, filename)
    return {"job_description": parsed}


@app.post("/api/resumes/upload-batch")
async def upload_resumes_batch(files: List[UploadFile] = File(...)):
    """
    Module 2: Batch upload resumes (PDF, DOCX). Supports 10+ resumes in a single call.
    Extracts candidate details, contact info, experience, and skills.
    """
    if not files:
        raise HTTPException(status_code=400, detail="No files uploaded.")

    parsed_resumes = []
    errors = []

    for file in files:
        try:
            content = await file.read()
            parsed = parse_resume(content, file.filename)
            parsed_resumes.append(parsed)
        except Exception as e:
            errors.append({"filename": file.filename, "error": str(e)})

    return {
        "count": len(parsed_resumes),
        "resumes": parsed_resumes,
        "errors": errors
    }


@app.post("/api/match")
def match_candidates(request: MatchRequest):
    """
    Module 3 & 4: Hybrid AI matching engine.
    Computes overall score (0-100), matched/missing skills, experience evaluation,
    semantic similarity, and ranked dashboard table.
    """
    if not request.resumes:
        raise HTTPException(status_code=400, detail="No resumes provided to match.")

    ranked = match_resumes_to_jd(request.jd, request.resumes, request.weights)

    return {
        "total_candidates": len(ranked),
        "job_title": request.jd.get("title", "Target Role"),
        "min_experience_required": request.jd.get("min_experience_years", 0),
        "required_skills_count": len(request.jd.get("required_skills", [])),
        "ranking": ranked
    }


@app.get("/api/samples/load-preloaded")
def load_preloaded_dataset(jd_id: Optional[str] = "jd-1"):
    """
    One-click instant demonstration endpoint.
    Parses the 12 synthetic resumes and selected sample JD, running full AI match.
    """
    # 1. Get JD
    selected_jd = next((jd for jd in SAMPLE_JDS if jd["id"] == jd_id), SAMPLE_JDS[0])
    parsed_jd = parse_job_description(selected_jd["text"])

    # 2. Parse all sample resumes
    files = sorted(glob.glob(os.path.join(SAMPLE_RESUMES_DIR, "*.*")))
    if not files:
        # Generate them if missing
        generate_all_samples(SAMPLE_RESUMES_DIR)
        files = sorted(glob.glob(os.path.join(SAMPLE_RESUMES_DIR, "*.*")))

    resumes = []
    for filepath in files:
        filename = os.path.basename(filepath)
        with open(filepath, "rb") as f:
            data = parse_resume(f.read(), filename)
            resumes.append(data)

    # 3. Match
    ranked = match_resumes_to_jd(parsed_jd, resumes)

    return {
        "job_description": parsed_jd,
        "sample_jd_id": selected_jd["id"],
        "total_resumes_loaded": len(resumes),
        "ranking": ranked
    }


@app.get("/api/sample-resumes/download/{filename}")
def download_sample_resume(filename: str):
    """Download individual synthetic resume file for verification."""
    filepath = os.path.join(SAMPLE_RESUMES_DIR, filename)
    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="File not found.")
    
    media_type = "application/pdf" if filename.lower().endswith(".pdf") else "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    return FileResponse(filepath, media_type=media_type, filename=filename)


# Mount static build of the frontend UI if available
STATIC_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../static"))
if os.path.exists(STATIC_DIR):
    app.mount("/", StaticFiles(directory=STATIC_DIR, html=True), name="static")
