import streamlit as st
import pandas as pd
import plotly.express as px

from utils.pdf_parser import extract_text

from utils.skill_extractor import (
    extract_skills,
    skills_list
)

from utils.ats_score import (
    calculate_similarity
)

from utils.ai_feedback import (
    generate_ai_feedback,
    tailor_resume
)

from utils.recommender import (
    recommend_internships
)

# -------------------------------
# PAGE CONFIG
# -------------------------------

st.set_page_config(
    page_title="AI Resume Analyzer",
    layout="wide"
)

# -------------------------------
# SIDEBAR
# -------------------------------

st.sidebar.title("Dashboard")

st.sidebar.markdown("""
## AI Resume Analyzer

Built using:
- NLP
- Sentence Transformers
- Groq LLM
- Streamlit
""")

# -------------------------------
# MAIN TITLE
# -------------------------------

st.title("AI Resume Analyzer")

st.markdown(
    "### AI-Powered ATS Resume Analyzer using NLP & Generative AI"
)

# -------------------------------
# FILE UPLOAD
# -------------------------------

uploaded_file = st.file_uploader(
    "Upload Resume PDF",
    type=["pdf"]
)

# -------------------------------
# JOB DESCRIPTION
# -------------------------------

job_description = st.text_area(
    "Paste Job Description"
)

# -------------------------------
# MAIN APP LOGIC
# -------------------------------

if uploaded_file:

    # Extract resume text
    resume_text = extract_text(uploaded_file)

    # Resume Preview
    with st.expander("View Resume Text"):
        st.write(resume_text[:3000])

    # Extract skills
    skills = extract_skills(resume_text)

    st.subheader("Detected Skills")

    if skills:

        for skill in skills:
            st.markdown(f"`{skill}`")

    else:
        st.warning("No skills detected.")

    # Job Description Logic
    if job_description:

        # Create Tabs
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "Analysis",
            "AI Feedback",
            "Tailored Resume",
            "Internship Matches",
            "Career Copilot"
        ])

        # -------------------------------
        # CALCULATIONS
        # -------------------------------

        # ATS Score
        score = calculate_similarity(
            resume_text,
            job_description
        )

        # Missing Skills
        missing = []

        jd_lower = job_description.lower()

        for skill in skills_list:

            if (
                skill in jd_lower and
                skill not in skills
            ):
                missing.append(skill)

        # Skill Match
        matched_skills = len(skills) - len(missing)

        total_skills = len(skills) if len(skills) > 0 else 1

        skill_match = round(
            (matched_skills / total_skills) * 100,
            2
        )

        # -------------------------------
        # TAB 1 - ANALYSIS
        # -------------------------------

        with tab1:

            col1, col2 = st.columns(2)

            with col1:

                st.metric(
                    label="ATS Match Score",
                    value=f"{score}%"
                )

            with col2:

                st.metric(
                    label="Skill Match",
                    value=f"{skill_match}%"
                )

            # Resume Strength
            if score >= 80:

                st.success(
                    "Excellent Resume Match"
                )

            elif score >= 60:

                st.info(
                    "Good Resume Match"
                )

            else:

                st.error(
                    "Resume Needs Improvement"
                )

            # Progress Bar
            st.progress(int(score))

            # Missing Skills
            st.subheader("Missing Skills")

            if missing:

                st.warning(
                    ", ".join(missing)
                )

            else:

                st.success(
                    "No major skills missing!"
                )

            # Suggestions
            st.subheader(
                "Resume Suggestions"
            )

            suggestions = []

            if score < 60:

                suggestions.append(
                    "Improve resume alignment with the job description."
                )

            if missing:

                suggestions.append(
                    "Add projects or experience related to missing skills."
                )

            if (
                "projects"
                not in resume_text.lower()
            ):

                suggestions.append(
                    "Add a projects section to strengthen your resume."
                )

            if (
                "experience"
                not in resume_text.lower()
            ):

                suggestions.append(
                    "Add internship or practical experience if available."
                )

            if suggestions:

                for suggestion in suggestions:

                    st.write(
                        f"- {suggestion}"
                    )

            else:

                st.success(
                    "Your resume looks strong!"
                )

            # Score Chart
            chart_data = pd.DataFrame({

                "Category": [
                    "ATS Score",
                    "Skill Match"
                ],

                "Score": [
                    score,
                    skill_match
                ]
            })

            fig = px.bar(
                chart_data,
                x="Category",
                y="Score",
                title="Resume Analysis Scores"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        # -------------------------------
        # TAB 2 - AI FEEDBACK
        # -------------------------------

        with tab2:

            st.subheader(
                "AI Resume Feedback"
            )

            with st.spinner(
                "Generating AI feedback..."
            ):

                feedback = generate_ai_feedback(
                    resume_text,
                    job_description
                )

                st.markdown(feedback)

            # Download Report
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
                label="Download Report",
                data=report,
                file_name="resume_analysis_report.txt",
                mime="text/plain"
            )

        # -------------------------------
        # TAB 3 - TAILORED RESUME
        # -------------------------------

        with tab3:

            st.subheader(
                "AI Tailored Resume"
            )

            with st.spinner(
                "Tailoring resume..."
            ):

                tailored_resume = tailor_resume(
                    resume_text,
                    job_description
                )

                st.markdown(
                    tailored_resume
                )

            st.download_button(
                label="Download Tailored Resume",
                data=tailored_resume,
                file_name="tailored_resume.txt",
                mime="text/plain"
            )

        # -------------------------------
        # TAB 4 - INTERNSHIPS
        # -------------------------------

        with tab4:

            st.subheader(
                "Recommended Internships"
            )

            recommendations = (
                recommend_internships(
                    skills
                )
            )

            for rec in recommendations[:5]:

                st.markdown(f"""
### {rec['Role']}

**Company:** {rec['Company']}

**Location:** {rec['Location']}

**Match Score:** {rec['Match']}%
""")

                st.progress(
                    int(rec["Match"])
                )

        # -------------------------------
        # TAB 5 - CAREER COPILOT
        # -------------------------------

        with tab5:

            st.subheader(
                "AI Career Copilot"
            )

            st.markdown("""
### Recommended Next Steps

- Build more AI/ML projects
- Practice DSA regularly
- Learn LangChain and RAG
- Deploy projects publicly
- Contribute to open source
- Prepare for internship interviews
""")

            st.info(
                "Your AI journey is progressing well 🚀"
            )