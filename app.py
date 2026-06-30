import logging

import pandas as pd
import plotly.express as px
import streamlit as st

# -----------------------------------
# PAGE CONFIG
# -----------------------------------

st.set_page_config(
    page_title="ClockIt 🤏",
    page_icon="🤏",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------
# LOAD CUSTOM CSS
# -----------------------------------
def load_css():
    try:
        with open("assets/style.css", "r") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        pass

load_css()

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
<div style="text-align: center; margin-bottom: 20px;">
    <h1 style="font-size: 2rem; margin-bottom: 5px;">🤏 ClockIt</h1>
    <p style="color: #a1a1aa; font-size: 0.9rem;">Your AI Career Copilot</p>
</div>

---

### ⚡ Superpowers

✅ **ATS X-Ray**  
✅ **Brutal AI Feedback**  
✅ **Resume Tailoring**  
✅ **Internship Matcher**  
✅ **Career Roadmap**  

---
""", unsafe_allow_html=True
)

st.sidebar.success("🟢 Systems Operational")
st.sidebar.info("🚀 AI Models Locked & Loaded")

# -----------------------------------
# HERO SECTION
# -----------------------------------

st.markdown(
    """
<div class="hero-section">
    <div class="hero-title">Stop Getting Ghosted by Recruiters.</div>
    <div class="hero-subtitle">Let AI roast, fix and optimize your resume.</div>
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
    "📄 Yeet your PDF here.",
    type=["pdf"],
    help="We only accept PDFs because Word docs are so 2010.",
)

# -----------------------------------
# JOB DESCRIPTION
# -----------------------------------

st.subheader("📝 Job Description")

with st.form("jd_form"):

    job_description = st.text_area(
        "Paste the internship/job description here...",
        height=150
    )

    col1, col2 = st.columns([8, 2])

    with col2:
        submit_button = st.form_submit_button(
            "✨ Cook My Resume"
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

    st.markdown("### 🧠 Detected Skills")

    if skills and len(skills) > 0:
        skills_html = "".join([f'<span class="skill-pill">{skill}</span>' for skill in skills])
        st.markdown(f'<div>{skills_html}</div>', unsafe_allow_html=True)
    else:
        st.warning("Bro, where are your skills? 💀")

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

        import time
        import random
        
        loading_messages = [
            "🧠 Reading your resume...",
            "☕ Making diet cokes...",
            "🔍 Finding hidden skills...",
            "🤖 Talking to AI...",
            "🚀 Optimizing...",
            "🔥 Cooking up some heat..."
        ]

        with st.spinner(random.choice(loading_messages)):
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

            col1, col2 = st.columns([1, 2])

            with col1:
                # Custom ATS Gauge
                gauge_message = "Needs seasoning."
                if score >= 95:
                    gauge_message = "🔥 Recruiters don't stand a chance."
                elif score >= 85:
                    gauge_message = "You're cooking. 🍳"
                elif score >= 70:
                    gauge_message = "Almost there."
                elif score >= 50:
                    gauge_message = "Needs seasoning. 🧂"
                else:
                    gauge_message = "Who let bro upload this 💀"
                
                # Map score to degrees (0-100 to 0-360deg for conic gradient)
                score_deg = int((score / 100) * 360)
                
                st.markdown(
                    f"""
                    <div class="gauge-container">
                        <div class="gauge-circle" style="--score: {score_deg}deg;">
                            <span class="gauge-score">{score}%</span>
                        </div>
                        <div class="gauge-text">{gauge_message}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            with col2:
                st.markdown(
                    f"""
                    <div class="glass-card">
                        <h3>Skill Match: {skill_match}%</h3>
                        <p style="color: #a1a1aa;">Based on the provided job description.</p>
                    </div>
                    """, unsafe_allow_html=True
                )

                st.markdown("### ⚠️ Missing Power-Ups")

                if missing:
                    missing_html = "".join([f'<span class="skill-pill missing">{skill}</span>' for skill in missing])
                    st.markdown(f'<div>{missing_html}</div>', unsafe_allow_html=True)
                    st.info("Looks like you're missing these power-ups.")
                else:
                    st.success("No major skills missing! You're stacked.")

            st.divider()

            st.markdown("### 📌 Resume Roast Suggestions")

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
                color_discrete_sequence=["#8B5CF6"]
            )

            fig.update_traces(
                textposition="outside"
            )
            
            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font_color="#FAFAFA"
            )

            col_chart1, col_chart2 = st.columns(2)
            
            with col_chart1:
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
                color_discrete_sequence=["#8B5CF6", "#ef4444"]
            )
            
            pie_fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font_color="#FAFAFA"
            )

            with col_chart2:
                st.plotly_chart(
                    pie_fig,
                    use_container_width=True,
                )

        # ===================================
        # TAB 2 — AI FEEDBACK
        # ===================================

        with tab2:

            st.markdown("### 🤖 AI Roast & Feedback")

            with st.spinner("☕ Making diet cokes and talking to AI..."):

                feedback = generate_ai_feedback(
                    resume_text,
                    job_description,
                )

                st.markdown(
                    f"""
                    <div class="chat-bubble-ai">
                        <div class="chat-avatar">🤖</div>
                        <div class="chat-content">
                            {feedback.replace(chr(10), "<br>")}
                        </div>
                    </div>
                    """, unsafe_allow_html=True
                )

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
                on_click=lambda: st.toast("🎉 Resume kidnapped successfully.")
            )

        # ===================================
        # TAB 3 — TAILORED RESUME
        # ===================================

        with tab3:

            st.markdown("### ✍️ AI Tailored Resume")

            with st.spinner("🔥 Cooking up the perfect resume..."):

                tailored_resume = tailor_resume(
                    resume_text,
                    job_description,
                )

                st.markdown(
                    f"""
                    <div class="code-window">
                        <div class="code-window-header">
                            <div class="mac-dots">
                                <div class="mac-dot red"></div>
                                <div class="mac-dot yellow"></div>
                                <div class="mac-dot green"></div>
                            </div>
                            <span style="margin-left: 15px; color: #a1a1aa; font-family: 'Space Grotesk', sans-serif; font-size: 0.8rem;">tailored_resume.txt</span>
                        </div>
                        <div class="code-window-body">{tailored_resume.replace(chr(10), "<br>")}</div>
                    </div>
                    """, unsafe_allow_html=True
                )

            st.download_button(
                label="📥 Download Tailored Resume",
                data=tailored_resume,
                file_name="tailored_resume.txt",
                mime="text/plain",
                on_click=lambda: st.toast("🔥 Resume cooked and downloaded.")
            )

        # ===================================
        # TAB 4 — INTERNSHIP MATCHES
        # ===================================

        with tab4:

            st.markdown("### 💼 Recommended Internships")

            recommendations = recommend_internships(skills)

            for rec in recommendations[:5]:
                
                st.markdown(
                    f"""
                    <div class="internship-card">
                        <div class="internship-info">
                            <h4>{rec['Role']} @ {rec['Company']}</h4>
                            <p>📍 {rec['Location']}</p>
                        </div>
                        <div class="internship-match">{rec['Match']}% Match</div>
                    </div>
                    """, unsafe_allow_html=True
                )

        # ===================================
        # TAB 5 — CAREER COPILOT
        # ===================================

        with tab5:

            st.markdown("### 🚀 Career Copilot")

            st.markdown(
                """
<div class="glass-card">
    <h4>Recommended Next Steps</h4>
    <ul style="color: #a1a1aa; line-height: 1.8;">
        <li>Build more AI/ML projects that solve real problems.</li>
        <li>Grind Leetcode but don't forget system design.</li>
        <li>Learn LangChain, RAG, and Agentic AI.</li>
        <li>Deploy projects publicly (Vercel, Streamlit Cloud).</li>
        <li>Stop scrolling, start building.</li>
    </ul>
</div>
""", unsafe_allow_html=True
            )

            st.info("You're on the right track! 🚀")

else:
    st.markdown(
        """
        <div style="text-align: center; margin-top: 50px;">
            <h3>No resume? Let's change that.</h3>
            <p style="color: #a1a1aa;">Drag your PDF above to get started.</p>
        </div>
        """, unsafe_allow_html=True
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

