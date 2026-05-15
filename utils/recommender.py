import pandas as pd

internship_data = pd.read_csv(
    "internships.csv"
)

def recommend_internships(
    resume_skills
):

    recommendations = []

    for _, row in internship_data.iterrows():

        role_skills = (
            row["Skills"]
            .lower()
            .split(",")
        )

        matched = len(
            set(resume_skills)
            .intersection(role_skills)
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