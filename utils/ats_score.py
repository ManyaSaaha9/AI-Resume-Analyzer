from sentence_transformers import (
    SentenceTransformer
)

from sklearn.metrics.pairwise import (
    cosine_similarity
)

# -----------------------------------
# CALCULATE ATS SCORE
# -----------------------------------

def calculate_similarity(
    resume,
    jd
):

    # Load model ONLY when needed
    model = SentenceTransformer(
        'all-MiniLM-L6-v2'
    )

    embeddings = model.encode(
        [resume, jd]
    )

    similarity = cosine_similarity(
        [embeddings[0]],
        [embeddings[1]]
    )[0][0]

    return round(
        similarity * 100,
        2
    )