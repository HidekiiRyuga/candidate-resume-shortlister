from src.feature_extractor import extract_candidate_features
from src.ranking_config import WEIGHTS
from src.semantic_match import semantic_score

JOB_DESCRIPTION = """
Senior AI Engineer

Python
LLMs
Retrieval
Ranking
Embeddings
Vector databases
Evaluation
Production ML
"""

def calculate_score(features, candidate):
    score = 0

    score += (features["skill_score"] / 40) * WEIGHTS["skills"]
    score += (features["experience_score"] / 25) * WEIGHTS["experience"]
    score += (features["achievement_score"] / 10) * WEIGHTS["achievements"]
    score += (features["title_score"] / 15) * 10

    skills = features["matched_skills"]

    # Bonus for important skill combinations
    if "python" in skills and ("retrieval" in skills or "ranking" in skills):
        score += 5

    if "python" in skills and ("lora" in skills or "rag" in skills):
        score += 3

    score += semantic_score(
    JOB_DESCRIPTION,
    str(candidate)
)

    return round(score, 2)


def rank_candidates(candidates):

    ranked = []

    for candidate in candidates:

        features = extract_candidate_features(candidate)

        semantic = semantic_score(JOB_DESCRIPTION, str(candidate))

        score = calculate_score(features, candidate)

        ranked.append(
            {
                "candidate": candidate,
                "score": calculate_score(features, candidate),
                "semantic_score": semantic,
                "features": features,
            }
        )

    ranked.sort(
        key=lambda item: item["score"],
        reverse=True,
    )

    return ranked