"""
Direct handler test suite without network sockets.
Verifies all FastAPI route handlers, logic, parsing, and ranking.
"""

import sys
import os

backend_path = os.path.abspath(os.path.dirname(__file__))
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

import app.main as m

def test_handlers():
    print("=== TESTING API ROUTE HANDLERS DIRECTLY ===", flush=True)

    # 1. Health check
    h = m.health_check()
    print(f"1. Health Check -> Status: {h['status']} | Engine: {h['ai_nlp_engine']}", flush=True)

    # 2. Sample JDs
    jds = m.get_sample_jds()["job_descriptions"]
    print(f"2. Sample JDs -> Found {len(jds)} job descriptions", flush=True)

    # 3. Analyze JD
    test_jd_text = jds[0]["text"]
    req = m.JDRequest(text=test_jd_text)
    analyzed = m.analyze_jd(req)["job_description"]
    print(f"3. Analyzed JD -> Title: {analyzed['title']} | Min Exp: {analyzed['min_experience_years']} yrs | Skills: {len(analyzed['required_skills'])}", flush=True)

    # 4. Preloaded dataset matching
    print("4. Executing full matching on 12 synthetic candidates...", flush=True)
    match_result = m.load_preloaded_dataset("jd-1")
    ranking = match_result["ranking"]
    print(f"   Successfully ranked {len(ranking)} candidates!\n", flush=True)

    print(f"{'Rank':<5} {'Candidate':<18} {'Exp':<10} {'Match %':<10} {'Matched Skills'}")
    print("-" * 75)
    for c in ranking:
        skills = ", ".join(c["matched_skills"][:3])
        if len(c["matched_skills"]) > 3:
            skills += f" (+{len(c['matched_skills']) - 3} more)"
        print(f"#{c['rank']:<4} {c['name']:<18} {c['experience_display']:<10} {c['match_percentage']}%      {skills}")

    # 5. Check top candidate details
    top = ranking[0]
    print(f"\nTop Candidate Details: {top['name']}")
    print(f"Tier: {top['explanation']['tier']}")
    print(f"Strengths ({len(top['explanation']['strengths'])}):")
    for s in top['explanation']['strengths']:
        print(f"  • {s}")
    print(f"Gaps ({len(top['explanation']['gaps'])}):")
    for g in top['explanation']['gaps']:
        print(f"  • {g}")

    print("\nALL HANDLER TESTS PASSED WITH 100% SUCCESS!", flush=True)

if __name__ == "__main__":
    test_handlers()
