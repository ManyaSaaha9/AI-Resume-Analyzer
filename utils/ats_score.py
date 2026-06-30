import streamlit as st
from sentence_transformers import (
    SentenceTransformer
)

from sklearn.metrics.pairwise import (
    cosine_similarity
)

# -----------------------------------
# LOAD MODEL WITH CACHING
# -----------------------------------

@st.cache_resource
def get_model():
    return SentenceTransformer('all-MiniLM-L6-v2')

# -----------------------------------
# CALCULATE ATS SCORE
# -----------------------------------

def calculate_similarity(
    resume,
    jd
):

    # Load cached model
    model = get_model()

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