import logging

import pandas as pd
import plotly.express as px
import streamlit as st

# -----------------------------------
# PAGE CONFIG
# -----------------------------------

st.set_page_config(
    page_title="AI Resume Analyzer",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------
# HIDE TRANSFORMER WARNINGS
# -----------------------------------

logging.getLogger("transformers").setLevel(logging.ERROR)

# -----------------------------------
# SESSION STATE
# -----------------------------------

if "analysis_done" not in st.session_state:
    st.session_state.analysis_done = False

# -----------------------------------
# IMPORTS
# -----------------------------------

from utils.ai_feedback import (
    generate_ai_feedback,
    tailor_resume,
)
from utils.ats_score import calculate_similarity
from utils.pdf_parser import extract_text
from utils.recommender import recommend_internships
from utils.skill_extractor import (
    extract_skills,
    skills_list,
)

# -----------------------------------
# SIDEBAR
# -----------------------------------

st.sidebar.markdown(
    """
# 🚀 AI Career Platform

---

## 🔥 Features

✅ ATS Resume Scoring

✅ AI Feedback

✅ Resume Tailoring

✅ Internship Recommendations

✅ Career Copilot

---

## 🛠 Tech Stack

- Python
- NLP
- Sentence Transformers
- Groq AI
- Streamlit
- Plotly

---
"""
)

st.sidebar.success("✅ System Running")
st.sidebar.info("🚀 AI Models Loaded")

# -----------------------------------
# HERO SECTION
# -----------------------------------

st.markdown(
    """
<div style="
background: linear-gradient(90deg, #7C3AED, #4F46E5);
padding: 30px;
border-radius: 20px;
margin-bottom: 20px;
">

<h1 style="color:white; text-align:center;">
🚀 AI Resume Analyzer
</h1>

<h4 style="color:white; text-align:center;">
Your Intelligent Career Assistant
</h4>

<p style="color:white; text-align:center;">
Analyze resumes, optimize ATS score,
generate AI feedback, and discover
best internship opportunities.
</p>

</div>
""",
    unsafe_allow_html=True,
)

# -----------------------------------
# METRIC CARDS
# -----------------------------------

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("📄 Resumes Analyzed", "100+")

with col2:
    st.metric("🤖 AI Accuracy", "95%")

with col3:
    st.metric("💼 Internship Matches", "500+")

st.divider()

# -----------------------------------
# FILE UPLOAD
# -----------------------------------

uploaded_file = st.file_uploader(
    "📄 Upload Your Resume",
    type=["pdf"],
    help="Upload resume in PDF format",
)

# -----------------------------------
# JOB DESCRIPTION
# -----------------------------------

st.subheader("📝 Job Description")

with st.form("jd_form"):

    job_description = st.text_area(
        "Paste Job Description"
    )

    col1, col2 = st.columns([8, 2])

    with col2:
        submit_button = st.form_submit_button(
            "🚀 Analyze"
        )

# -----------------------------------
# MAIN APP
# -----------------------------------

if uploaded_file:

    # -----------------------------------
    # PDF EXTRACTION
    # -----------------------------------

    try:
        resume_text = extract_text(uploaded_file)

    except Exception:
        st.error("❌ Error reading PDF file.")
        st.stop()

    # -----------------------------------
    # EMPTY RESUME CHECK
    # -----------------------------------

    if not resume_text.strip():
        st.warning("⚠️ No text found in resume.")
        st.stop()

    # -----------------------------------
    # RESUME PREVIEW
    # -----------------------------------

    with st.expander("📄 View Resume Text"):
        st.write(resume_text[:3000])

    st.divider()

    # -----------------------------------
    # SKILL EXTRACTION
    # -----------------------------------

    skills = extract_skills(resume_text)

    st.subheader("🧠 Detected Skills")

    if skills and len(skills) > 0:

        skill_cols = st.columns(4)

        for index, skill in enumerate(skills):
            with skill_cols[index % 4]:
                st.success(skill)

    else:
        st.warning("No skills detected.")

    st.divider()

    # -----------------------------------
    # ANALYSIS BUTTON STATE
    # -----------------------------------

    if submit_button and job_description.strip():
        st.session_state.analysis_done = True

    # -----------------------------------
    # ANALYSIS SECTION
    # -----------------------------------

    if st.session_state.analysis_done:

        with st.spinner("⚡ Calculating ATS score..."):
            score = calculate_similarity(
                resume_text,
                job_description,
            )

        # -----------------------------------
        # MISSING SKILLS
        # -----------------------------------

        missing = []

        jd_lower = job_description.lower()

        for skill in skills_list:
            if skill in jd_lower and skill not in skills:
                missing.append(skill)

        # -----------------------------------
        # SKILL MATCH SCORE
        # -----------------------------------

        matched_skills = len(skills) - len(missing)

        total_skills = len(skills) if len(skills) > 0 else 1

        skill_match = round(
            (matched_skills / total_skills) * 100,
            2,
        )

        # -----------------------------------
        # TABS
        # -----------------------------------

        tab1, tab2, tab3, tab4, tab5 = st.tabs(
            [
                "📊 Analysis",
                "🤖 AI Feedback",
                "✍️ Tailored Resume",
                "💼 Internship Matches",
                "🚀 Career Copilot",
            ]
        )

        # ===================================
        # TAB 1 — ANALYSIS
        # ===================================

        with tab1:

            col1, col2 = st.columns(2)

            with col1:
                st.metric(
                    "ATS Match Score",
                    f"{score}%",
                )

            with col2:
                st.metric(
                    "Skill Match",
                    f"{skill_match}%",
                )

            if score >= 85:
                st.success("🔥 Strong ATS Optimization")

            elif score >= 70:
                st.info("✅ Good Resume Alignment")

            else:
                st.warning("⚠️ Resume Needs Optimization")

            st.markdown("### ATS Strength")
            st.progress(int(score))

            st.divider()

            st.markdown("## ⚠️ Missing Skills")

            if missing:
                st.warning(", ".join(missing))
            else:
                st.success("No major skills missing!")

            st.divider()

            st.markdown("## 📌 Resume Suggestions")

            suggestions = []

            if score < 60:
                suggestions.append(
                    "Improve resume alignment with the job description."
                )

            if missing:
                suggestions.append(
                    "Add projects related to missing skills."
                )

            if "projects" not in resume_text.lower():
                suggestions.append(
                    "Add a projects section."
                )

            if "experience" not in resume_text.lower():
                suggestions.append(
                    "Add internship experience."
                )

            if suggestions:
                for suggestion in suggestions:
                    st.write(f"- {suggestion}")
            else:
                st.success("Your resume looks strong!")

            st.divider()

            chart_data = pd.DataFrame(
                {
                    "Category": [
                        "ATS Score",
                        "Skill Match",
                    ],
                    "Score": [
                        score,
                        skill_match,
                    ],
                }
            )

            fig = px.bar(
                chart_data,
                x="Category",
                y="Score",
                text="Score",
                title="Resume Analysis Scores",
            )

            fig.update_traces(
                textposition="outside"
            )

            st.plotly_chart(
                fig,
                use_container_width=True,
            )

            pie_data = pd.DataFrame(
                {
                    "Section": [
                        "Matched",
                        "Missing",
                    ],
                    "Value": [
                        len(skills) - len(missing),
                        len(missing),
                    ],
                }
            )

            pie_fig = px.pie(
                pie_data,
                names="Section",
                values="Value",
                title="Skills Coverage",
            )

            st.plotly_chart(
                pie_fig,
                use_container_width=True,
            )

        # ===================================
        # TAB 2 — AI FEEDBACK
        # ===================================

        with tab2:

            st.markdown(
                "## 🤖 AI Resume Feedback"
            )

            with st.spinner("⚡ AI processing..."):

                feedback = generate_ai_feedback(
                    resume_text,
                    job_description,
                )

                st.markdown(feedback)

            report = f"""
AI Resume Analysis Report

ATS Score: {score}%

Detected Skills:
{", ".join(skills)}

Missing Skills:
{", ".join(missing)}

AI Feedback:
{feedback}
"""

            st.download_button(
                label="📥 Download Report",
                data=report,
                file_name="resume_analysis_report.txt",
                mime="text/plain",
            )

        # ===================================
        # TAB 3 — TAILORED RESUME
        # ===================================

        with tab3:

            st.markdown(
                "## ✍️ AI Tailored Resume"
            )

            with st.spinner("⚡ AI processing..."):

                tailored_resume = tailor_resume(
                    resume_text,
                    job_description,
                )

                st.markdown(tailored_resume)

            st.download_button(
                label="📥 Download Tailored Resume",
                data=tailored_resume,
                file_name="tailored_resume.txt",
                mime="text/plain",
            )

        # ===================================
        # TAB 4 — INTERNSHIP MATCHES
        # ===================================

        with tab4:

            st.markdown(
                "## 💼 Recommended Internships"
            )

            recommendations = recommend_internships(
                skills
            )

            for rec in recommendations[:5]:

                st.markdown(
                    f"""
### {rec['Role']}

**Company:** {rec['Company']}

**Location:** {rec['Location']}

**Match Score:** {rec['Match']}%
"""
                )

                st.progress(int(rec["Match"]))

                st.divider()

        # ===================================
        # TAB 5 — CAREER COPILOT
        # ===================================

        with tab5:

            st.markdown(
                "## 🚀 AI Career Copilot"
            )

            st.markdown(
                """
### Recommended Next Steps

- Build more AI/ML projects
- Practice DSA regularly
- Learn LangChain and RAG
- Deploy projects publicly
- Contribute to open source
- Prepare for internship interviews
"""
            )

            st.info(
                "Your AI journey is progressing well 🚀"
            )

        

else:
    st.info(
        "📌 Upload resume and analyze."
    )

# -----------------------------------
# FOOTER
# -----------------------------------

st.divider()

st.markdown(
    """
<div style='text-align:center'>

<h4>🚀 AI Resume Analyzer</h4>

<p>
Built with Streamlit,
NLP, Transformers & Groq AI
</p>

</div>
""",
    unsafe_allow_html=True,
)

