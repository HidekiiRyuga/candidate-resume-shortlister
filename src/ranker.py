from src.feature_extractor import extract_candidate_features
from src.ranking_config import WEIGHTS
from src.semantic_match import semantic_scores_batch
import heapq
import time
from src.feature_extractor import candidate_to_text

JOB_DESCRIPTION="""
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

REQUIRED={
    "python",
    "retrieval",
    "ranking",
    "embeddings",
    "evaluation"
}

VECTOR={
    "milvus",
    "qdrant",
    "weaviate",
    "faiss",
    "opensearch",
    "elasticsearch"
}

def calculate_score(features, candidate, semantic):

    score=0

    score+=(features["skill_score"]/40)*WEIGHTS["skills"]
    score+=(features["experience_score"]/25)*WEIGHTS["experience"]
    score+=(features["achievement_score"]/10)*WEIGHTS["achievements"]
    score+=(features["title_score"]/15)*10

    skills=set(features["matched_skills"])
    matched=len(REQUIRED & skills)

    signal=features["signal_score"]

    if matched==0:
        signal*=0.3
    elif matched<=2:
        signal*=0.7

    score+=signal

    signals = candidate.get("redrob_signals", {})

    if signals.get("recruiter_response_rate", 0) >= 0.80:
        score += 2

    if signals.get("interview_completion_rate", 0) >= 0.90:
        score += 2

    if signals.get("github_activity_score", -1) >= 80:
        score += 2

    notice = signals.get("notice_period_days", 0)

    if notice >= 120:
        score -= 4
    elif notice >= 90:
        score -= 2
        
    if matched>=4:
        semantic*=0.55
    elif matched>=2:
        semantic*=0.40
    else:
        semantic*=0.18

    score+=semantic

    score+=matched*5

    if matched >= 4:
        score += 8
    elif matched == 3:
        score += 5

    if (
        "python" in skills
        and (
            "retrieval" in skills
            or "ranking" in skills
        )
    ):
        score+=6

    vector_matches = len(VECTOR & skills)

    score += min(vector_matches * 2, 6)

    if (
        "evaluation" in skills
        and (
            "retrieval" in skills
            or "ranking" in skills
        )
    ):
        score+=4

    elif "evaluation" in skills:
        score-=2

    if len(skills)==0:
        score-=12

    score -= features[
    "consistency_penalty"
]

    if semantic < 4:
        score -= 6

    elif semantic < 6:
        score -= 3

    return round(score,2)


def rank_candidates(candidates):

    total_start = time.time()

    # -------- Stage 1 : Fast ranking --------
    t1 = time.time()

    stage1 = []

    for candidate in candidates:

        features = extract_candidate_features(candidate)

        fast_score = (
            (features["skill_score"] / 40) * WEIGHTS["skills"]
            + (features["experience_score"] / 25) * WEIGHTS["experience"]
            + (features["achievement_score"] / 10) * WEIGHTS["achievements"]
            + (features["title_score"] / 15) * 10
            + features["signal_score"]
        )

        stage1.append({
            "candidate": candidate,
            "features": features,
            "fast_score": fast_score
        })

    print("Stage 1 time:", time.time() - t1)

    # -------- Stage 1.5 : Top-K selection --------
    t2 = time.time()

    stage2 = heapq.nlargest(
        2000,
        stage1,
        key=lambda x: x["fast_score"]
    )

    print("Top-K time:", time.time() - t2)

    # -------- Stage 2 : Semantic reranking --------
    t3 = time.time()

    candidate_texts = [
        candidate_to_text(row["candidate"])
        for row in stage2
    ]

    semantic_scores = semantic_scores_batch(
        JOB_DESCRIPTION,
        candidate_texts
    )

    print("Semantic batch time:", time.time() - t3)

    # -------- Final scoring --------
    t4 = time.time()

    ranked = []

    for row, semantic in zip(stage2, semantic_scores):

        score = calculate_score(
            row["features"],
            row["candidate"],
            semantic
        )

        ranked.append({
            "candidate": row["candidate"],
            "score": score,
            "semantic_score": semantic,
            "features": row["features"]
        })

    ranked.sort(
        key=lambda x: (
            x["score"],
            len(x["features"]["matched_skills"]),
            x["semantic_score"],
            x["features"]["signal_score"],
            -x["candidate"]["profile"]["years_of_experience"],
            x["candidate"]["candidate_id"]
        ),
        reverse=True
    )

    for rank, row in enumerate(ranked, 1):
        row["rank"] = rank

    print("Final ranking time:", time.time() - t4)
    print("TOTAL time:", time.time() - total_start)

    return ranked