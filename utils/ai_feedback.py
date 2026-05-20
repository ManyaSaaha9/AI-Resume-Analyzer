import os
import streamlit as st

from groq import Groq


client = Groq(
    api_key=st.secrets["GROQ_API_KEY"]
)

@st.cache_data(show_spinner=False)
def generate_ai_feedback(resume, jd):

    prompt = f"""
    Analyze this resume against the job description.

    Resume:
    {resume}

    Job Description:
    {jd}

    Give ATS-focused feedback.
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

@st.cache_data(show_spinner=False)
def tailor_resume(resume, jd):

    prompt = f"""
You are an expert ATS resume writer.

Rewrite and tailor the resume
for the given job description.

IMPORTANT RULES:
- Return ONLY the tailored resume
- Do NOT add introductions
- Do NOT add explanations
- Do NOT add conclusions
- Do NOT say "Here is the resume"
- Output must look like a professional resume

Resume:
{resume}

Job Description:
{jd}
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