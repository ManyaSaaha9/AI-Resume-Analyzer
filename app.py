import streamlit as st
import pdfplumber

st.title("AI Resume Analyzer")

uploaded_file = st.file_uploader(
    "Upload Resume PDF",
    type=["pdf"]
)

def extract_text(pdf_file):
    text = ""

    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            extracted = page.extract_text()

            if extracted:
                text += extracted

    return text

if uploaded_file:

    resume_text = extract_text(uploaded_file)

    st.subheader("Extracted Resume Text")

    st.write(resume_text)