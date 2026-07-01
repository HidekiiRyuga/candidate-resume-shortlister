from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer("all-MiniLM-L6-v2")


def semantic_score(job_text, candidate_text):
    job_embedding = model.encode([job_text])
    candidate_embedding = model.encode([candidate_text])

    score = cosine_similarity(
        job_embedding,
        candidate_embedding
    )[0][0]

    return round(score * 20, 2)