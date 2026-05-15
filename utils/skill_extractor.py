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
    "docker",
    "git",
    "github",
    "llm",
    "rag"
]

def extract_skills(text):

    text = text.lower()

    found_skills = []

    for skill in skills_list:

        if skill in text:
            found_skills.append(skill)

    return found_skills