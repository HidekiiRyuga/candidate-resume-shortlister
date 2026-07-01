import re
from src.ranking_config import REQUIRED_SKILLS,PREFERRED_SKILLS,GOOD_TITLES,ACHIEVEMENT_WORDS

def candidate_to_text(candidate):
    return str(candidate).lower()

def get_skill_score(text):

    score=0
    matched=set()

    aliases={
        "python":["python"],
        "embeddings":[
            "embedding",
            "embeddings"
        ],
        "retrieval":[
            "retrieval",
            "rag",
            "retrieval augmented"
        ],
        "ranking":[
            "ranking",
            "relevance"
        ],
        "vector database":[
            "vector database",
            "vector db",
            "vector search",
            "milvus",
            "qdrant",
            "faiss",
            "weaviate",
            "pinecone",
            "opensearch",
            "elasticsearch"
        ],
        "evaluation":[
            "evaluation",
            "eval",
            "benchmark"
        ]
    }

    for skill in REQUIRED_SKILLS:

        variants=aliases.get(
            skill,
            [skill]
        )

        if any(
            v in text
            for v in variants
        ):
            score+=8
            matched.add(skill)

    for skill in PREFERRED_SKILLS:

        if skill in text:
            score+=4
            matched.add(skill)

    prod=[
        "retrieval",
        "ranking",
        "recommendation",
        "search",
        "production",
        "evaluation",
        "ab test",
        "embedding"
    ]

    score+=sum(
        2
        for p in prod
        if p in text
    )

    return min(score,40),sorted(
        list(matched)
    )


def get_experience_score(candidate):

    yrs=(
        candidate
        .get("profile",{})
        .get(
            "years_of_experience",
            0
        )
    )

    if yrs<4:
        return 4

    if 5<=yrs<=9:
        return 25

    if yrs<=12:
        return 18

    return 12


def get_title_score(text):

    score=0

    titles=[
        "ai engineer",
        "ml engineer",
        "machine learning",
        "search",
        "ranking",
        "recommendation",
        "relevance"
    ]

    for t in titles:
        if t in text:
            score+=3

    return min(score,15)


def get_achievement_score(text):

    score=0

    score+=len(
        re.findall(
            r"\d+%",
            text
        )
    )

    for w in ACHIEVEMENT_WORDS:
        score+=text.count(w)

    return min(score,10)


def get_signal_score(candidate):

    s=candidate.get(
        "redrob_signals",
        {}
    )

    score=0

    score+=(
        s.get(
            "recruiter_response_rate",
            0
        )*10
    )

    score+=(
        s.get(
            "interview_completion_rate",
            0
        )*8
    )

    score+=(
        s.get(
            "profile_completeness_score",
            0
        )/20
    )

    score+=(
        s.get(
            "search_appearance_30d",
            0
        )/30
    )

    score+=(
        s.get(
            "saved_by_recruiters_30d",
            0
        )/5
    )

    if s.get(
        "open_to_work_flag"
    ):
        score+=4

    return round(
        min(score,25),
        2
    )


def extract_candidate_features(candidate):

    text=candidate_to_text(
        candidate
    )

    skill,matched=(
        get_skill_score(
            text
        )
    )

    return{
        "skill_score":skill,
        "experience_score":
            get_experience_score(
                candidate
            ),
        "title_score":
            get_title_score(
                text
            ),
        "achievement_score":
            get_achievement_score(
                text
            ),
        "signal_score":
            get_signal_score(
                candidate
            ),
        "matched_skills":
            matched
    }