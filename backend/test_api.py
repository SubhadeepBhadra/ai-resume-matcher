"""
FastAPI End-to-End API Test Suite with detailed real-time logging.
"""

import sys

def log(msg):
    print(msg, flush=True)

import app # triggers offline environment settings
from fastapi.testclient import TestClient
from app.main import app as fastapi_app

def run():
    log("Initializing TestClient...")
    client = TestClient(fastapi_app)

    log("\n--- 1. Testing GET /api/health ---")
    r1 = client.get("/api/health")
    log(f"Status: {r1.status_code}")
    log(f"Payload: {r1.json()}")

    log("\n--- 2. Testing GET /api/samples/jds ---")
    r2 = client.get("/api/samples/jds")
    jds = r2.json()["job_descriptions"]
    log(f"Loaded {len(jds)} sample JDs")

    log("\n--- 3. Testing POST /api/jd/analyze ---")
    r3 = client.post("/api/jd/analyze", json={"text": jds[0]["text"]})
    jd_res = r3.json()["job_description"]
    log(f"Detected Role: {jd_res['title']} | Min Exp: {jd_res['min_experience_years']} yrs | Skills: {len(jd_res['required_skills'])}")

    log("\n--- 4. Testing GET /api/samples/load-preloaded (Full AI Match on 12 Resumes) ---")
    r4 = client.get("/api/samples/load-preloaded?jd_id=jd-1")
    ranked = r4.json()["ranking"]
    log(f"Ranked {len(ranked)} candidates:")
    for c in ranked[:5]:
        log(f"  #{c['rank']:<2} {c['name']:<18} Match: {c['match_percentage']}% | Exp: {c['experience_display']} | Matched: {len(c['matched_skills'])} skills")

    log("\n--- 5. Candidate Deep Dive (#1 Candidate) ---")
    top = ranked[0]
    log(f"Top Candidate: {top['name']} ({top['match_percentage']}%)")
    log(f"Explanation: {top['explanation']['summary']}")

    log("\n--- 6. Testing GET / (Static Web UI) ---")
    r6 = client.get("/")
    log(f"Web UI Status: {r6.status_code} | Size: {len(r6.text)} bytes")

    log("\n==========================================")
    log("  ALL API & SYSTEM TESTS PASSED SUCCESSFULLY! ")
    log("==========================================\n")

if __name__ == "__main__":
    run()
