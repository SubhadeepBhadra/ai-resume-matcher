"""
Streamlit Web Application for AI-Based Resume Matching & Candidate Ranking.
Deployable directly on Streamlit Community Cloud or locally via:
    streamlit run streamlit_app.py
"""

import os
import sys
import glob
import pandas as pd
import streamlit as st

# Configure paths so backend modules can be imported
root_dir = os.path.abspath(os.path.dirname(__file__))
backend_dir = os.path.join(root_dir, "backend")
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

# Ensure HF offline mode if cached
os.environ.setdefault("HF_HUB_OFFLINE", "1")

from backend.app.parsers.jd_parser import parse_job_description
from backend.app.parsers.resume_parser import parse_resume
from backend.app.nlp.matcher import match_resumes_to_jd
from backend.app.sample_data.generate_samples import SAMPLE_JDS, generate_all_samples

# ==============================================================================
# Page Configuration & Modern Light Theme Styling
# ==============================================================================
st.set_page_config(
    page_title="MatchWise AI — Resume Matching & Candidate Ranking",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for clean enterprise look
st.markdown("""
<style>
    /* Global Styles */
    .main { background-color: #f8fafc; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
    
    /* Header branding */
    .brand-header {
        background: #ffffff;
        padding: 1.25rem 1.5rem;
        border-radius: 0.75rem;
        border: 1px solid #e2e8f0;
        margin-bottom: 1.5rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 1px 3px rgba(0,0,0,0.03);
    }
    
    /* KPI Card styling */
    .metric-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 0.5rem;
        padding: 1rem;
        text-align: center;
        box-shadow: 0 1px 2px rgba(0,0,0,0.03);
    }
    .metric-val { font-size: 1.75rem; font-weight: 800; color: #0f172a; }
    .metric-label { font-size: 0.75rem; font-weight: 700; color: #64748b; text-transform: uppercase; margin-top: 0.25rem; }

    /* Badges */
    .badge-matched { background: #ecfdf5; color: #065f46; border: 1px solid #a7f3d0; padding: 2px 8px; border-radius: 4px; font-size: 0.75rem; font-weight: 600; margin: 2px; display: inline-block; }
    .badge-missing { background: #fff1f2; color: #9f1239; border: 1px solid #fecdd3; padding: 2px 8px; border-radius: 4px; font-size: 0.75rem; font-weight: 600; margin: 2px; display: inline-block; }
    .badge-extra { background: #f1f5f9; color: #334155; border: 1px solid #e2e8f0; padding: 2px 8px; border-radius: 4px; font-size: 0.75rem; font-weight: 600; margin: 2px; display: inline-block; }

    /* Detail blocks */
    .strength-box { background: #ecfdf5; border: 1px solid #a7f3d0; border-radius: 0.5rem; padding: 1rem; }
    .gap-box { background: #fff1f2; border: 1px solid #fecdd3; border-radius: 0.5rem; padding: 1rem; }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# Helper Functions & Session State Initialization
# ==============================================================================
def ensure_sample_resumes():
    sample_dir = os.path.join(root_dir, "sample_resumes")
    if not os.path.exists(sample_dir) or len(os.listdir(sample_dir)) == 0:
        generate_all_samples(sample_dir)
    return sample_dir

def load_cached_samples():
    sample_dir = ensure_sample_resumes()
    resumes = []
    for filepath in sorted(glob.glob(os.path.join(sample_dir, "*.*"))):
        filename = os.path.basename(filepath)
        try:
            with open(filepath, "rb") as f:
                content = f.read()
                data = parse_resume(content, filename)
                resumes.append(data)
        except Exception as e:
            pass
    return resumes

# Initialize Session State
if "resumes" not in st.session_state:
    st.session_state.resumes = load_cached_samples()

if "parsed_jd" not in st.session_state:
    default_text = SAMPLE_JDS[0]["text"]
    st.session_state.parsed_jd = parse_job_description(default_text)

if "ranking" not in st.session_state:
    st.session_state.ranking = []

if "weights" not in st.session_state:
    st.session_state.weights = {
        "skills": 0.45,
        "semantic": 0.35,
        "experience": 0.15,
        "education": 0.05
    }

# ==============================================================================
# Sidebar: Engine Configuration & Weights (Module 3)
# ==============================================================================
with st.sidebar:
    st.title("🎯 MatchWise AI")
    st.markdown("**AI-Based Resume Matching & Candidate Ranking System**")
    st.divider()

    st.subheader("⚙️ Scoring Weights (Module 3)")
    st.markdown("Calibrate the composite scoring formula:")
    
    w_skills = st.slider("Skills Match Weight", 0, 100, 45, step=5, help="Weight for technical skill overlap")
    w_semantic = st.slider("Semantic Similarity Weight", 0, 100, 35, step=5, help="Weight for all-MiniLM-L6-v2 vector embeddings")
    w_exp = st.slider("Experience Tenure Weight", 0, 100, 15, step=5, help="Weight for candidate experience vs required years")
    w_edu = st.slider("Education Credential Weight", 0, 100, 5, step=5, help="Weight for degree level")

    total_w = w_skills + w_semantic + w_exp + w_edu
    if total_w > 0:
        st.session_state.weights = {
            "skills": w_skills / total_w,
            "semantic": w_semantic / total_w,
            "experience": w_exp / total_w,
            "education": w_edu / total_w
        }
        st.caption(f"Normalized Total: **{total_w}%**")
    
    st.divider()
    st.caption("🚀 **Architecture Overview**")
    st.caption("• **Vector Embeddings**: SentenceTransformers `all-MiniLM-L6-v2`")
    st.caption("• **Skill Taxonomy**: 150+ canonical skills with alias resolution")
    st.caption("• **Document Parsers**: `pypdf` & `python-docx`")
    st.caption("• **Explainability**: Multi-factor scoring with automated reasoning")

# ==============================================================================
# Main Workspace: Navigation Tabs
# ==============================================================================
st.markdown("""
<div class="brand-header">
    <div>
        <h2 style="margin:0; color:#0f172a; font-weight:800;">MatchWise AI Dashboard</h2>
        <p style="margin:2px 0 0 0; color:#64748b; font-size:0.875rem;">Enterprise Candidate Evaluation & Explainable Ranking Engine</p>
    </div>
</div>
""", unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs([
    "📄 1. Job Description",
    "📂 2. Batch Resumes",
    "🏆 3. Candidate Ranking",
    "🔍 4. Candidate Deep-Dive"
])

# ------------------------------------------------------------------------------
# TAB 1: Job Description Input & Analysis (Module 1)
# ------------------------------------------------------------------------------
with tab1:
    st.subheader("Module 1: Job Description Input & Requirements Extraction")
    st.markdown("Select a sample preset or paste a custom Job Description to extract requirements in real time.")

    col_presets, col_actions = st.columns([3, 1])
    with col_presets:
        preset_names = [jd["title"] for jd in SAMPLE_JDS]
        selected_preset = st.selectbox("Quick Job Profiles:", ["Custom Job Description"] + preset_names)

    if selected_preset != "Custom Job Description":
        jd_match = next((j for j in SAMPLE_JDS if j["title"] == selected_preset), SAMPLE_JDS[0])
        initial_text = jd_match["text"]
    else:
        initial_text = st.session_state.parsed_jd.get("raw_text", "")

    jd_text = st.text_area("Job Description Content", value=initial_text, height=220)

    col_btn, _ = st.columns([1, 4])
    with col_btn:
        if st.button("Extract Requirements", type="primary", use_container_width=True):
            if jd_text.strip():
                with st.spinner("Extracting entities, required skills, and tenure..."):
                    st.session_state.parsed_jd = parse_job_description(jd_text)
                    st.success("Extracted requirements successfully!")

    # Display Parsed JD Results
    pjd = st.session_state.parsed_jd
    st.markdown("---")
    c1, c2, c3 = st.columns([2, 1, 1])
    with c1:
        st.markdown(f"**Extracted Title:** `{pjd.get('title', 'Target Role')}`")
        st.markdown(f"**Required Experience:** `{pjd.get('min_experience_years', 0)}+ years`")
    with c2:
        st.metric("Required Skills Count", len(pjd.get("required_skills", [])))
    with c3:
        st.metric("Responsibilities Count", len(pjd.get("responsibilities", [])))

    st.markdown("**Core Required Technical Skills:**")
    skills_html = "".join([f'<span class="badge-matched">{s}</span>' for s in pjd.get("required_skills", [])])
    st.markdown(skills_html or "_No required skills extracted_", unsafe_allow_html=True)

    if pjd.get("responsibilities"):
        st.markdown("**Extracted Responsibilities:**")
        for r in pjd.get("responsibilities", [])[:4]:
            st.markdown(f"- {r}")

# ------------------------------------------------------------------------------
# TAB 2: Batch Resume Upload & Processing (Module 2)
# ------------------------------------------------------------------------------
with tab2:
    st.subheader("Module 2: High-Volume Batch Resume Parsing")
    st.markdown("Upload candidate resumes (PDF & DOCX) in a single batch, or test with the 12 pre-loaded synthetic resumes.")

    col_up, col_reset = st.columns([3, 1])
    with col_reset:
        if st.button("🔄 Reset to 12 Synthetic Resumes", use_container_width=True):
            st.session_state.resumes = load_cached_samples()
            st.success("Loaded 12 pre-generated synthetic candidate resumes!")

    uploaded_files = st.file_uploader(
        "Upload candidate resumes (PDF / DOCX)",
        accept_multiple_files=True,
        type=["pdf", "docx", "doc"]
    )

    if uploaded_files:
        with st.spinner(f"Parsing {len(uploaded_files)} candidate resume(s)..."):
            new_resumes = []
            for uploaded_file in uploaded_files:
                bytes_data = uploaded_file.read()
                parsed = parse_resume(bytes_data, uploaded_file.name)
                new_resumes.append(parsed)
            st.session_state.resumes = new_resumes
            st.success(f"Successfully parsed {len(new_resumes)} resume(s)!")

    # Display Current Resumes
    current_resumes = st.session_state.resumes
    st.markdown(f"**Current Candidate Pool ({len(current_resumes)} resumes loaded):**")
    
    if current_resumes:
        summary_rows = []
        for r in current_resumes:
            summary_rows.append({
                "Candidate": r.get("name", "Unknown"),
                "Format": r.get("file_type", "PDF").upper(),
                "Experience": f"{r.get('experience_years', 0)} yrs",
                "Education": r.get("education", ["Degree in STEM"])[0] if r.get("education") else "B.S. in CS",
                "Skills Count": len(r.get("skills", [])),
                "Email": r.get("email", "N/A"),
                "Phone": r.get("phone", "N/A")
            })
        st.dataframe(pd.DataFrame(summary_rows), use_container_width=True)
    else:
        st.info("No resumes currently loaded. Click 'Reset to 12 Synthetic Resumes' or upload files.")

# ------------------------------------------------------------------------------
# TAB 3: Candidate Ranking Dashboard (Module 4)
# ------------------------------------------------------------------------------
with tab3:
    st.subheader("Module 4: Candidate Ranking Dashboard")
    st.markdown("Rank all candidates against the active Job Description using the multi-factor scoring model.")

    col_run, col_kpi1, col_kpi2, col_kpi3 = st.columns([1.5, 1, 1, 1])
    with col_run:
        if st.button("🚀 Analyze & Match Candidates", type="primary", use_container_width=True):
            if not st.session_state.resumes:
                st.error("No resumes loaded. Please upload or load sample resumes first.")
            else:
                with st.spinner("Computing dense vector embeddings and composite match scores..."):
                    ranking = match_resumes_to_jd(
                        st.session_state.parsed_jd,
                        st.session_state.resumes,
                        st.session_state.weights
                    )
                    st.session_state.ranking = ranking
                    st.success(f"Successfully ranked {len(ranking)} candidates!")

    ranking = st.session_state.ranking

    if ranking:
        # KPI Metrics
        with col_kpi1:
            st.metric("Total Evaluated", len(ranking))
        with col_kpi2:
            top_score = ranking[0]["match_percentage"] if ranking else 0
            st.metric("Top Match", f"{top_score:.1f}%")
        with col_kpi3:
            avg_score = sum(c["match_percentage"] for c in ranking) / len(ranking) if ranking else 0
            st.metric("Average Score", f"{avg_score:.1f}%")

        st.markdown("---")
        
        # Search & Filtering
        search_query = st.text_input("🔍 Filter by Candidate Name or Skill:", placeholder="e.g. Sarah, Java, Docker...")
        
        filtered_ranking = ranking
        if search_query.strip():
            sq = search_query.lower()
            filtered_ranking = [
                c for c in ranking 
                if sq in c["name"].lower() or any(sq in s.lower() for s in c.get("matched_skills", []))
            ]

        # Table formatting
        table_data = []
        for c in filtered_ranking:
            matched_str = ", ".join(c.get("matched_skills", [])[:4])
            if len(c.get("matched_skills", [])) > 4:
                matched_str += f" (+{len(c['matched_skills']) - 4} more)"
            
            table_data.append({
                "Rank": f"#{c['rank']}",
                "Candidate": c["name"],
                "Experience": c.get("experience_display", f"{c.get('total_experience_years', 0)} yrs"),
                "Match %": f"{c['match_percentage']:.1f}%",
                "Matched Skills": matched_str,
                "Tier": c.get("explanation", {}).get("tier", "Screening")
            })

        st.dataframe(pd.DataFrame(table_data), use_container_width=True)

        # CSV Export
        csv_df = pd.DataFrame([{
            "Rank": c["rank"],
            "Candidate": c["name"],
            "Email": c.get("email", ""),
            "Experience": c.get("experience_display", ""),
            "Match %": f"{c['match_percentage']:.1f}%",
            "Matched Skills": "; ".join(c.get("matched_skills", [])),
            "Missing Skills": "; ".join(c.get("missing_skills", [])),
            "Tier": c.get("explanation", {}).get("tier", "")
        } for c in ranking])

        st.download_button(
            label="📥 Download Candidate Rankings (CSV)",
            data=csv_df.to_csv(index=False),
            file_name="candidate_rankings.csv",
            mime="text/csv",
            use_container_width=True
        )
    else:
        st.info("Click 'Analyze & Match Candidates' to run the evaluation engine and view ranking results.")

# ------------------------------------------------------------------------------
# TAB 4: Candidate-Level Deep-Dive Analysis (Module 5)
# ------------------------------------------------------------------------------
with tab4:
    st.subheader("Module 5: Candidate-Level Deep-Dive & Explainable AI")
    st.markdown("Detailed breakdown of matching scores, skill alignment, and automated AI justifications.")

    if not st.session_state.ranking:
        st.info("Please run the matching engine in the 'Candidate Ranking' tab first.")
    else:
        candidate_names = [f"#{c['rank']} - {c['name']} ({c['match_percentage']:.1f}%)" for c in st.session_state.ranking]
        selected_str = st.selectbox("Select Candidate to Inspect:", candidate_names)
        
        # Get selected candidate
        selected_rank = int(selected_str.split(" - ")[0].replace("#", ""))
        candidate = next((c for c in st.session_state.ranking if c["rank"] == selected_rank), st.session_state.ranking[0])

        # Header Card
        st.markdown(f"""
        <div style="background:#ffffff; border:1px solid #e2e8f0; border-radius:0.5rem; padding:1.25rem; margin-bottom:1rem;">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <div>
                    <h3 style="margin:0; color:#0f172a;">{candidate['name']}</h3>
                    <p style="margin:2px 0 0 0; color:#64748b; font-size:0.875rem;">
                        {candidate.get('email', 'N/A')} • {candidate.get('phone', 'N/A')} • {candidate.get('experience_display', '')}
                    </p>
                </div>
                <div style="text-align:right;">
                    <span style="font-size:2rem; font-weight:800; color:#4f46e5;">{candidate['match_percentage']:.1f}%</span>
                    <br><span style="font-size:0.8125rem; font-weight:700; color:#059669;">{candidate.get('explanation', {}).get('tier', 'Recommended')}</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # 4-Factor Breakdown
        st.markdown("**Composite Score Breakdown:**")
        sb = candidate.get("score_breakdown", {})
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.metric("Skills Overlap (45%)", f"{sb.get('skills_score', 0)*100:.0f}%")
        with c2:
            st.metric("Semantic Relevance (35%)", f"{sb.get('semantic_score', 0)*100:.0f}%")
        with c3:
            st.metric("Experience Alignment (15%)", f"{sb.get('experience_score', 0)*100:.0f}%")
        with c4:
            st.metric("Education Fit (5%)", f"{sb.get('education_score', 0)*100:.0f}%")

        st.markdown("---")

        # Explainable AI (XAI) Reasons
        col_str, col_gap = st.columns(2)
        with col_str:
            st.markdown("#### ✅ Key Matching Strengths")
            strengths = candidate.get("explanation", {}).get("strengths", [])
            for s in strengths:
                st.markdown(f"- {s}")
        with col_gap:
            st.markdown("#### ⚠️ Skill Gaps & Shortfalls")
            gaps = candidate.get("explanation", {}).get("gaps", [])
            for g in gaps:
                st.markdown(f"- {g}")

        st.markdown("---")

        # Skills Matrix
        st.markdown("#### 🧩 Skills Matrix")
        
        st.markdown(f"**Matched Skills ({len(candidate.get('matched_skills', []))}):**")
        matched_html = "".join([f'<span class="badge-matched">✓ {s}</span>' for s in candidate.get("matched_skills", [])])
        st.markdown(matched_html or "_None_", unsafe_allow_html=True)

        st.markdown(f"**Missing Required Skills ({len(candidate.get('missing_skills', []))}):**")
        missing_html = "".join([f'<span class="badge-missing">✕ {s}</span>' for s in candidate.get("missing_skills", [])])
        st.markdown(missing_html or "_None! All required skills matched._", unsafe_allow_html=True)

        st.markdown(f"**Additional / Complementary Skills ({len(candidate.get('additional_skills', []))}):**")
        extra_html = "".join([f'<span class="badge-extra">{s}</span>' for s in candidate.get("additional_skills", [])[:12]])
        st.markdown(extra_html or "_None_", unsafe_allow_html=True)

        # Raw Text Preview
        with st.expander("📄 View Parsed Resume Text Preview"):
            st.text(candidate.get("raw_text", "No preview available."))
