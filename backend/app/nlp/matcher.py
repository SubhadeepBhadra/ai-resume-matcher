"""
AI-Powered Resume Matching, Scoring, and Explainability Engine.
Combines skill taxonomy overlap, sentence embedding semantic similarity,
experience seniority alignment, and education credentials into a composite score.
"""

from typing import Dict, Any, List
from app.nlp.embeddings import compute_semantic_similarity


# Default weights for composite matching formula
DEFAULT_WEIGHTS = {
    "skills": 0.45,       # 45% weight on hard & core skills
    "semantic": 0.35,     # 35% weight on deep semantic & contextual similarity
    "experience": 0.15,   # 15% weight on years of relevant experience
    "education": 0.05     # 5% weight on education qualification
}


def calculate_experience_score(candidate_exp: float, required_exp: float) -> float:
    """
    Evaluates candidate experience against JD required minimum.
    Returns score from 0 to 100.
    """
    if required_exp <= 0:
        return 100.0

    ratio = candidate_exp / required_exp
    if ratio >= 1.0:
        # Meets or exceeds requirements
        return 100.0
    elif ratio >= 0.8:
        return 85.0 + (ratio - 0.8) * 75.0  # 85 to 100
    elif ratio >= 0.5:
        return 60.0 + (ratio - 0.5) * 83.3  # 60 to 85
    else:
        return max(20.0, ratio * 120.0)     # Scaled down for significant shortfall


def calculate_education_score(candidate_edu: str, required_edu: str) -> float:
    """Evaluates candidate education level against requirement."""
    edu_rank = {
        "PhD": 4,
        "Master's Degree": 3,
        "Bachelor's Degree": 2,
        "Associate / Diploma": 1,
        "Not explicitly specified": 1
    }
    cand_rank = edu_rank.get(candidate_edu, 1)
    req_rank = edu_rank.get(required_edu, 2)

    if cand_rank >= req_rank:
        return 100.0
    elif cand_rank == req_rank - 1:
        return 80.0
    else:
        return 65.0


def generate_candidate_explanation(
    candidate: Dict[str, Any],
    jd: Dict[str, Any],
    matched_skills: List[str],
    missing_skills: List[str],
    bonus_skills: List[str],
    overall_score: float,
    skill_score: float,
    semantic_score: float,
    exp_score: float,
    edu_score: float
) -> Dict[str, Any]:
    """
    Generates structured, human-readable reasoning explaining why the candidate received their score,
    highlighting key strengths, critical gaps, experience alignment, and interview suggestions.
    """
    cand_name = candidate.get("name", "Candidate")
    cand_exp = candidate.get("experience_years", 0.0)
    req_exp = jd.get("min_experience_years", 3.0)
    total_req_skills = len(jd.get("required_skills", []))
    matched_count = len(matched_skills)

    # 1. Strengths
    strengths = []
    if matched_count > 0:
        pct_skill = round((matched_count / max(1, total_req_skills)) * 100)
        strengths.append(
            f"Demonstrates strong technical alignment with {matched_count} of {total_req_skills} ({pct_skill}%) core required skills: {', '.join(matched_skills[:5])}{'...' if len(matched_skills) > 5 else ''}."
        )

    if cand_exp >= req_exp:
        diff = round(cand_exp - req_exp, 1)
        if diff > 0:
            strengths.append(f"Exceeds minimum experience requirement with {cand_exp} years vs {req_exp} years required (+{diff} years advantage).")
        else:
            strengths.append(f"Directly satisfies the required {req_exp} years of industry experience.")

    if semantic_score >= 70:
        strengths.append(f"High contextual relevance ({round(semantic_score)}%) between candidate project responsibilities and the job role description.")

    if bonus_skills:
        strengths.append(f"Offers complementary domain skills: {', '.join(bonus_skills[:4])}.")

    # 2. Gaps & Areas for Evaluation
    gaps = []
    if missing_skills:
        gaps.append(f"Lacks explicit mentions of {len(missing_skills)} required skill(s): {', '.join(missing_skills)}.")
    
    if cand_exp < req_exp:
        shortfall = round(req_exp - cand_exp, 1)
        gaps.append(f"Experience shortfall: candidate has {cand_exp} years vs {req_exp} years required ({shortfall} years below requirement).")

    if semantic_score < 50:
        gaps.append("Resume terminology and project descriptions show moderate divergence from the JD scope.")

    if not gaps:
        gaps.append("No critical qualification gaps identified.")

    # 3. Overall Recommendation Summary
    if overall_score >= 85:
        tier = "Strong Match / Priority Interview"
        summary = f"{cand_name} is an exceptional match ({round(overall_score)}%) with high technical skill overlap and proven experience."
    elif overall_score >= 70:
        tier = "Good Match / Recommended for Screening"
        summary = f"{cand_name} is a solid candidate ({round(overall_score)}%) possessing the primary competencies, with minor skill or experience nuances to verify."
    elif overall_score >= 50:
        tier = "Moderate Match / Review Required"
        summary = f"{cand_name} has a moderate score ({round(overall_score)}%). While certain core foundations exist, there are notable missing skills or seniority gaps."
    else:
        tier = "Low Match"
        summary = f"{cand_name} has low alignment ({round(overall_score)}%) with current role requirements."

    # 4. Tailored Interview Focus
    interview_focus = []
    if missing_skills:
        interview_focus.append(f"Evaluate working familiarity with missing tools: {', '.join(missing_skills[:3])}.")
    if matched_skills:
        interview_focus.append(f"Deep-dive into hands-on architecture experience using {matched_skills[0]}.")
    if cand_exp < req_exp:
        interview_focus.append(f"Assess ability to take on senior responsibilities despite {cand_exp} years of tenure.")

    return {
        "tier": tier,
        "summary": summary,
        "strengths": strengths,
        "gaps": gaps,
        "interview_focus": interview_focus,
        "metrics_breakdown": {
            "skill_match_percentage": round(skill_score, 1),
            "semantic_similarity_percentage": round(semantic_score, 1),
            "experience_alignment_percentage": round(exp_score, 1),
            "education_score": round(edu_score, 1)
        }
    }


def match_resumes_to_jd(
    jd_data: Dict[str, Any],
    resumes_data: List[Dict[str, Any]],
    weights: Dict[str, float] = None
) -> List[Dict[str, Any]]:
    """
    Compares batch of resumes against a Job Description and ranks candidates.
    Returns list of candidate evaluations sorted in descending order of matching score.
    """
    if not resumes_data:
        return []

    if weights is None:
        weights = DEFAULT_WEIGHTS

    jd_text = jd_data.get("raw_text", "")
    req_skills = set(jd_data.get("required_skills", []))
    req_exp = float(jd_data.get("min_experience_years", 3.0))
    req_edu = jd_data.get("required_education", "Bachelor's Degree")

    # 1. Compute Semantic Similarities via embeddings
    resume_texts = [r.get("raw_text", "") for r in resumes_data]
    semantic_scores_raw, engine_info = compute_semantic_similarity(jd_text, resume_texts)

    results = []

    for idx, candidate in enumerate(resumes_data):
        cand_skills = set(candidate.get("skills", []))
        cand_exp = float(candidate.get("experience_years", 1.0))
        cand_edu = candidate.get("education", "Not explicitly specified")

        # Skills calculations
        matched_skills = sorted(list(req_skills.intersection(cand_skills)))
        missing_skills = sorted(list(req_skills.difference(cand_skills)))
        bonus_skills = sorted(list(cand_skills.difference(req_skills)))

        # Skill Score (0 - 100)
        if len(req_skills) > 0:
            raw_skill_ratio = len(matched_skills) / len(req_skills)
            # Add up to 5% bonus for relevant extra skills
            bonus_factor = min(0.05, len(bonus_skills) * 0.01)
            skill_score = min(100.0, (raw_skill_ratio + bonus_factor) * 100.0)
        else:
            skill_score = 75.0

        # Semantic Score (0 - 100)
        semantic_sim = semantic_scores_raw[idx] if idx < len(semantic_scores_raw) else 0.5
        semantic_score = semantic_sim * 100.0

        # Experience Score (0 - 100)
        exp_score = calculate_experience_score(cand_exp, req_exp)

        # Education Score (0 - 100)
        edu_score = calculate_education_score(cand_edu, req_edu)

        # Composite Match %
        overall_score = (
            weights["skills"] * skill_score +
            weights["semantic"] * semantic_score +
            weights["experience"] * exp_score +
            weights["education"] * edu_score
        )
        overall_score = round(max(0.0, min(100.0, overall_score)), 1)

        # Generate Explainable Reasons
        explanation = generate_candidate_explanation(
            candidate=candidate,
            jd=jd_data,
            matched_skills=matched_skills,
            missing_skills=missing_skills,
            bonus_skills=bonus_skills,
            overall_score=overall_score,
            skill_score=skill_score,
            semantic_score=semantic_score,
            exp_score=exp_score,
            edu_score=edu_score
        )

        results.append({
            "id": f"cand-{idx + 1}",
            "filename": candidate.get("filename", f"Resume_{idx + 1}"),
            "name": candidate.get("name", f"Candidate {chr(65 + idx)}"),
            "email": candidate.get("email", "N/A"),
            "phone": candidate.get("phone", "N/A"),
            "linkedin": candidate.get("linkedin"),
            "github": candidate.get("github"),
            "education": cand_edu,
            "experience_years": cand_exp,
            "experience_display": f"{cand_exp:g} years" if cand_exp != 1 else "1 year",
            "match_percentage": overall_score,
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
            "bonus_skills": bonus_skills,
            "all_skills": candidate.get("skills", []),
            "summary": candidate.get("summary", ""),
            "explanation": explanation,
            "raw_text": candidate.get("raw_text", "")
        })

    # Sort descending by match percentage
    results.sort(key=lambda x: x["match_percentage"], reverse=True)

    # Assign ranks
    for rank, item in enumerate(results, start=1):
        item["rank"] = rank

    return results
