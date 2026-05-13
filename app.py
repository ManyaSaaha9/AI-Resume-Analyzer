import streamlit as st
import pdfplumber
import spacy

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Load NLP model
nlp = spacy.load("en_core_web_sm")

# Load embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Streamlit UI
st.title("AI Resume Analyzer")
st.markdown("### AI-Powered ATS Resume Analyzer")

# Upload Resume
uploaded_file = st.file_uploader(
    "Upload Resume PDF",
    type=["pdf"]
)

# Job Description Input
job_description = st.text_area(
    "Paste Job Description"
)

# Extract text from PDF
def extract_text(pdf_file):

    text = ""

    with pdfplumber.open(pdf_file) as pdf:

        for page in pdf.pages:

            extracted = page.extract_text()

            if extracted:
                text += extracted

    return text


# Skills list
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
    "github"
]


# Extract skills
def extract_skills(text):

    text = text.lower()

    found_skills = []

    for skill in skills_list:

        if skill in text:
            found_skills.append(skill)

    return found_skills


# Semantic ATS similarity
def calculate_similarity(resume, jd):

    embeddings = model.encode([resume, jd])

    similarity = cosine_similarity(
        [embeddings[0]],
        [embeddings[1]]
    )[0][0]

    return round(similarity * 100, 2)


# Detect missing skills
def missing_skills(resume_skills, jd_text):

    jd_text = jd_text.lower()

    missing = []

    for skill in skills_list:

        if skill in jd_text and skill not in resume_skills:
            missing.append(skill)

    return missing


# Main App Logic
if uploaded_file:

    # Extract Resume Text
    resume_text = extract_text(uploaded_file)

    # Display Resume Text
    st.subheader("Resume Text")
    st.write(resume_text[:2000])

    # Extract Skills
    skills = extract_skills(resume_text)

    # Show Skills
    st.subheader("Detected Skills")

    if skills:
        st.success(", ".join(skills))
    else:
        st.warning("No skills detected.")

    # If JD entered
    if job_description:

        # Calculate ATS Score
        score = calculate_similarity(
            resume_text,
            job_description
        )

        # Display ATS Score
        st.metric(
            label="ATS Match Score",
            value=f"{score}%"
        )

        # Missing Skills
        missing = missing_skills(
            skills,
            job_description
        )

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