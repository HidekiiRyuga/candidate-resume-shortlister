from src.feature_extractor import extract_candidate_features
from src.ranking_config import WEIGHTS


def calculate_score(features):
    """
    Calculate a weighted score for one candidate.
    """

    score = 0

    semantic = 0

    score += (
        features["skill_score"] / 40
    ) * WEIGHTS["skills"]

    score += (
        features["experience_score"] / 25
    ) * WEIGHTS["experience"]

    score += (
        features["achievement_score"] / 10
    ) * WEIGHTS["achievements"]

    score += (
        features["title_score"] / 15
    ) * 10

    score += semantic

    return round(score, 2)


def rank_candidates(candidates):

    ranked = []

    for candidate in candidates:

        features = extract_candidate_features(candidate)

        ranked.append(
            {
                "candidate": candidate,
                "score": calculate_score(features),
                "features": features,
            }
        )

    ranked.sort(
        key=lambda item: item["score"],
        reverse=True,
    )

    return ranked