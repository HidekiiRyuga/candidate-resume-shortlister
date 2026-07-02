from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")

_job_cache = {}


def semantic_scores_batch(job_text, candidate_texts):

    if job_text not in _job_cache:
        _job_cache[job_text] = model.encode(
            job_text,
            convert_to_numpy=True,
            show_progress_bar=False
        )

    job_embedding = _job_cache[job_text]

    candidate_embeddings = model.encode(
        candidate_texts,
        batch_size=256,
        convert_to_numpy=True,
        show_progress_bar=False
    )

    similarities = cosine_similarity(
        [job_embedding],
        candidate_embeddings
    )[0]

    return np.round(similarities * 20, 2).tolist()


def semantic_score(job_text, candidate_text):
    return semantic_scores_batch(
        job_text,
        [candidate_text]
    )[0]