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
    signal_bonus = get_signal_bonus(candidate)
    score += signal_bonus
    

    score = max(0, min(score, 100))
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
        key=lambda x: x["score"],
        reverse=True
    )

    for rank, row in enumerate(ranked, 1):
        row["rank"] = rank

    return ranked

def get_signal_bonus(candidate):
    signals = candidate.get("redrob_signals", {})

    bonus = 0

    if signals.get("open_to_work_flag"):
        bonus += 2

    bonus += signals.get("profile_completeness_score", 0) / 50
    bonus += signals.get("recruiter_response_rate", 0) * 3
    bonus += signals.get("interview_completion_rate", 0) * 2

    return round(bonus, 2)