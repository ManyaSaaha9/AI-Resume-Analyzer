import os

from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

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

def tailor_resume(resume, jd):

    prompt = f"""
    Tailor this resume for the job description.

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