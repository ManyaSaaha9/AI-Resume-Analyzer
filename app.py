import streamlit as st
import ast
import pdfplumber
import spacy
import pandas as pd
import plotly.express as px
import os

from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from groq import Groq

# -------------------------------
# LOAD ENV VARIABLES
# -------------------------------

load_dotenv()

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
# LOAD MODELS
# -------------------------------

nlp = spacy.load("en_core_web_sm")

model = SentenceTransformer('all-MiniLM-L6-v2')

# -------------------------------
# GROQ CLIENT
# -------------------------------

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

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
# EXTRACT TEXT
# -------------------------------

def extract_text(pdf_file):

    text = ""

    with pdfplumber.open(pdf_file) as pdf:

        for page in pdf.pages:

            extracted = page.extract_text()

            if extracted:
                text += extracted

    return text

# -------------------------------
# SKILLS DATABASE
# -------------------------------

skills_list = [
    "python",
    "machine learning",
    "deep learning",
    "nlp",
    "tensorflow",
    "pytorch",
    "sql",
    "java",
    "streamlit",
    "langchain",
    "data analysis",
    "communication",
    "flask",
    "fastapi",
    "react",
    "docker",
    "git",
    "github",
    "pandas",
    "numpy",
    "scikit-learn",
    "data visualization",
    "power bi",
    "tableau",
    "api",
    "generative ai",
    "llm",
    "rag"
]
internship_data = pd.read_csv("internships.csv")

# -------------------------------
# EXTRACT SKILLS
# -------------------------------

def extract_skills(text):

    text = text.lower()

    found_skills = []

    for skill in skills_list:

        if skill in text:
            found_skills.append(skill)

    return found_skills

# -------------------------------
# ATS SCORE
# -------------------------------

def calculate_similarity(resume, jd):

    embeddings = model.encode([resume, jd])

    similarity = cosine_similarity(
        [embeddings[0]],
        [embeddings[1]]
    )[0][0]

    return round(similarity * 100, 2)

# -------------------------------
# MISSING SKILLS
# -------------------------------

def missing_skills(resume_skills, jd_text):

    jd_text = jd_text.lower()

    missing = []

    for skill in skills_list:

        if skill in jd_text and skill not in resume_skills:
            missing.append(skill)

    return missing

# -------------------------------
# AI FEEDBACK
# -------------------------------

def generate_ai_feedback(resume, jd):

    prompt = f"""
    You are an expert ATS resume reviewer.

    Analyze this resume against the job description.

    Resume:
    {resume}

    Job Description:
    {jd}

    Give:
    1. Strengths
    2. Weaknesses
    3. Missing skills
    4. Resume improvement suggestions
    5. ATS optimization advice

    Use markdown formatting with headings and bullet points.
    Keep feedback concise, professional, and ATS-focused.
    """

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content

# -------------------------------
# TAILOR RESUME
# -------------------------------

def tailor_resume(resume, jd):

    prompt = f"""
    You are an expert resume writer.

    Improve and tailor this resume for the job description.

    Resume:
    {resume}

    Job Description:
    {jd}

    Tasks:
    1. Rewrite resume bullet points professionally
    2. Improve ATS optimization
    3. Add stronger action verbs
    4. Align skills with the job description
    5. Make projects more impactful

    Keep formatting clean and professional.
    """

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content
def recommend_internships(resume_skills):

    recommendations = []

    for _, row in internship_data.iterrows():

        role_skills = row["Skills"].lower().split(",")

        matched = len(
            set(resume_skills).intersection(role_skills)
        )

        score = round(
            (matched / len(role_skills)) * 100,
            2
        )

        recommendations.append({
            "Role": row["Role"],
            "Company": row["Company"],
            "Location": row["Location"],
            "Match": score
        })

    recommendations = sorted(
        recommendations,
        key=lambda x: x["Match"],
        reverse=True
    )

    return recommendations

# -------------------------------
# MAIN LOGIC
# -------------------------------

if uploaded_file:

    # Extract resume text
    resume_text = extract_text(uploaded_file)

    # Resume preview
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

    # Job Description Analysis
    if job_description:

        # Create Tabs
        tab1, tab2, tab3, tab4 = st.tabs([
    "Analysis",
    "AI Feedback",
    "Tailored Resume",
    "Internship Matches"
])

        # ATS Score
        score = calculate_similarity(
            resume_text,
            job_description
        )

        # Missing skills
        missing = missing_skills(
            skills,
            job_description
        )

        # Skill Match %
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

            # Metrics Layout
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
                st.success("Excellent Resume Match")

            elif score >= 60:
                st.info("Good Resume Match")

            else:
                st.error("Resume Needs Improvement")

            # Progress Bar
            st.progress(int(score))

            # Missing Skills
            st.subheader("Missing Skills")

            if missing:
                st.warning(", ".join(missing))

            else:
                st.success("No major skills missing!")

            # Resume Suggestions
            st.subheader("Resume Suggestions")

            suggestions = []

            if score < 60:
                suggestions.append(
                    "Improve resume alignment with the job description."
                )

            if missing:
                suggestions.append(
                    "Add projects or experience related to missing skills."
                )

            if "projects" not in resume_text.lower():
                suggestions.append(
                    "Add a projects section to strengthen your resume."
                )

            if "experience" not in resume_text.lower():
                suggestions.append(
                    "Add internship or practical experience if available."
                )

            if suggestions:

                for suggestion in suggestions:
                    st.write(f"- {suggestion}")

            else:
                st.success("Your resume looks strong!")

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

            st.plotly_chart(fig)

        # -------------------------------
        # TAB 2 - AI FEEDBACK
        # -------------------------------

        with tab2:

            st.subheader("AI Resume Feedback")

            with st.spinner("Generating AI feedback..."):

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

            st.subheader("AI Tailored Resume")

            with st.spinner("Tailoring resume for the job..."):

                tailored_resume = tailor_resume(
                    resume_text,
                    job_description
                )

                st.markdown(tailored_resume)

            st.download_button(
                label="Download Tailored Resume",
                data=tailored_resume,
                file_name="tailored_resume.txt",
                mime="text/plain"
            )
        with tab4:
            st.subheader("Recommended Internships")
            recommendations = recommend_internships(
                skills
            )
            for rec in recommendations[:5]:
                st.markdown(f"""
        ### {rec['Role']}
        **Company:** {rec['Company']}

        **Location:** {rec['Location']}

        **Match Score:** {rec['Match']}%
        """)

        st.progress(int(rec["Match"]))