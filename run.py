"""
Main entry point to launch the AI Resume Matching & Ranking Application.
Usage:
    python run.py
or
    uv run run.py
"""

import os
import sys
import uvicorn

# Add backend directory to sys.path
backend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "backend"))
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

from app.sample_data.generate_samples import generate_all_samples


def main():
    sample_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "sample_resumes"))
    if not os.path.exists(sample_dir) or len(os.listdir(sample_dir)) == 0:
        print("[*] Generating 12 synthetic sample resumes (PDF & DOCX)...")
        generate_all_samples(sample_dir)

    print("\n" + "="*70)
    print("  AI-BASED RESUME MATCHING & CANDIDATE RANKING SYSTEM")
    print("="*70)
    print("  • Web Application Dashboard: http://localhost:8000")
    print("  • Interactive API Documentation: http://localhost:8000/docs")
    print("  • AI Engine: SentenceTransformers all-MiniLM-L6-v2 + Skills Ontology")
    print("="*70 + "\n")

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=False)


if __name__ == "__main__":
    main()
