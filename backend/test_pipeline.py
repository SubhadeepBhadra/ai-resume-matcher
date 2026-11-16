"""
Quick verification test script for resume parsing, JD analysis, and AI matching.
"""

import os
import glob
import json
from app.parsers.resume_parser import parse_resume
from app.parsers.jd_parser import parse_job_description
from app.nlp.matcher import match_resumes_to_jd
from app.sample_data.generate_samples import SAMPLE_JDS


def run_pipeline_test():
    print("=== 1. TESTING RESUME PARSER (PDF & DOCX) ===")
    resumes = []
    files = sorted(glob.glob("sample_resumes/*.*"))
    for filepath in files:
        filename = os.path.basename(filepath)
        with open(filepath, "rb") as f:
            data = parse_resume(f.read(), filename)
            resumes.append(data)
            print(f"Parsed: {data['name']:18} | {data['experience_years']} yrs | {len(data['skills'])} skills | {filename}")

    assert len(resumes) >= 10, f"Expected at least 10 resumes, found {len(resumes)}"

    print("\n=== 2. TESTING JD PARSING & AI MATCHING ===")
    test_jd_info = SAMPLE_JDS[0] # Java Lead JD
    print(f"Target JD: {test_jd_info['title']} (Min Exp: {test_jd_info['min_experience_years']} yrs)")
    
    parsed_jd = parse_job_description(test_jd_info["text"])
    print(f"Extracted JD Required Skills ({len(parsed_jd['required_skills'])}): {', '.join(parsed_jd['required_skills'])}")

    ranked_candidates = match_resumes_to_jd(parsed_jd, resumes)

    print("\n=== 3. CANDIDATE RANKING DASHBOARD RESULTS ===")
    print(f"{'Rank':<5} {'Candidate':<18} {'Exp':<10} {'Match %':<10} {'Matched Skills'}")
    print("-" * 75)
    for c in ranked_candidates:
        skills_summary = ", ".join(c["matched_skills"][:4])
        if len(c["matched_skills"]) > 4:
            skills_summary += f" (+{len(c['matched_skills']) - 4} more)"
        print(f"#{c['rank']:<4} {c['name']:<18} {c['experience_display']:<10} {c['match_percentage']}%      {skills_summary}")

    print("\n=== 4. CANDIDATE LEVEL DEEP-DIVE SAMPLE (#1 Candidate) ===")
    top = ranked_candidates[0]
    print(f"Candidate: {top['name']}")
    print(f"Match Score: {top['match_percentage']}% (Tier: {top['explanation']['tier']})")
    print(f"Matched Skills: {top['matched_skills']}")
    print(f"Missing Skills: {top['missing_skills']}")
    print(f"Summary: {top['explanation']['summary']}")
    print("Strengths:")
    for s in top["explanation"]["strengths"]:
        print(f"  + {s}")
    print("Gaps:")
    for g in top["explanation"]["gaps"]:
        print(f"  - {g}")

    print("\nALL PIPELINE TESTS PASSED!")


if __name__ == "__main__":
    run_pipeline_test()
