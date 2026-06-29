from src.feature_extractor import (
    extract_candidate_features
)

from src.ranking_config import (
    WEIGHTS
)


def calculate_score(features):

    score = 0

    score += (
        features["skill_score"]
        * WEIGHTS["skills"]
        / 20
    )

    score += (
        features["experience_score"]
        * WEIGHTS["experience"]
        / 25
    )

    score += (
        features["achievement_score"]
        * WEIGHTS["achievements"]
        / 10
    )

    score += (
        features["title_score"]
        * 2
    )

    return round(score, 2)


def rank_candidates(candidates):

    ranked = []

    for candidate in candidates:

        features = (
            extract_candidate_features(
                candidate
            )
        )

        final_score = (
            calculate_score(
                features
            )
        )

        ranked.append(
            {
                "score": final_score,
                "features": features,
            }
        )

    ranked.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return ranked