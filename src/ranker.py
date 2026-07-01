from src.feature_extractor import extract_candidate_features
from src.ranking_config import WEIGHTS
from src.semantic_match import semantic_score

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


def calculate_score(features,candidate):

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

    semantic=semantic_score(
        JOB_DESCRIPTION,
        str(candidate)
    )

    if matched>=4:
        semantic*=0.55
    elif matched>=2:
        semantic*=0.40
    else:
        semantic*=0.18

    score+=semantic

    score+=matched*4

    if matched>=3:
        score+=6

    if (
        "python" in skills
        and (
            "retrieval" in skills
            or "ranking" in skills
        )
    ):
        score+=6

    if len(VECTOR & skills)>0:
        score+=5

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

    score=max(0,min(score,100))

    return round(score,2)


def rank_candidates(candidates):

    ranked=[]

    for candidate in candidates:

        features=extract_candidate_features(
            candidate
        )

        ranked.append({
            "candidate":candidate,
            "score":calculate_score(
                features,
                candidate
            ),
            "semantic_score":semantic_score(
                JOB_DESCRIPTION,
                str(candidate)
            ),
            "features":features
        })

    ranked.sort(
        key=lambda x:(
            x["score"],
            len(
                x["features"]["matched_skills"]
            )
        ),
        reverse=True
    )

    for i,row in enumerate(
        ranked,
        1
    ):
        row["rank"]=i

    return ranked