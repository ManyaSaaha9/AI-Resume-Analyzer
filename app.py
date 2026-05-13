import streamlit as st
import pdfplumber
import spacy

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load NLP model
nlp = spacy.load("en_core_web_sm")

# Streamlit title
st.title("AI Resume Analyzer")

# Upload PDF
uploaded_file = st.file_uploader(
    "Upload Resume PDF",
    type=["pdf"]
)

# Job description input
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
    "communication"
]

# Extract skills
def extract_skills(text):

    text = text.lower()

    found_skills = []

    for skill in skills_list:

        if skill in text:
            found_skills.append(skill)

    return found_skills

# Calculate ATS score
def calculate_similarity(resume, jd):

    documents = [resume, jd]

    cv = CountVectorizer()

    matrix = cv.fit_transform(documents)

    similarity = cosine_similarity(matrix)[0][1]

    return round(similarity * 100, 2)

# Main logic
if uploaded_file:

    resume_text = extract_text(uploaded_file)

    st.subheader("Resume Text")
    st.write(resume_text[:2000])

    skills = extract_skills(resume_text)

    st.subheader("Detected Skills")
    st.write(skills)

    if job_description:

        score = calculate_similarity(
            resume_text,
            job_description
        )

        st.subheader("ATS Match Score")
        st.success(f"{score}%")