import re
from src.ranking_config import REQUIRED_SKILLS,PREFERRED_SKILLS,GOOD_TITLES,ACHIEVEMENT_WORDS

def candidate_to_text(candidate):

    profile = candidate.get("profile", {})
    history = candidate.get("career_history", [])
    skills = candidate.get("skills", [])
    education = candidate.get("education", [])

    parts = [
        profile.get("headline", ""),
        profile.get("summary", ""),
        profile.get("current_title", "")
    ]

    for skill in skills:
        parts.append(
            skill.get("name", "")
        )

    for job in history[:2]:
        parts.append(
            job.get("title", "")
        )
        parts.append(
            job.get("description", "")
        )

    if education:
        edu = education[0]
        parts.append(
            edu.get("degree", "")
        )
        parts.append(
            edu.get("field_of_study", "")
        )

    return " ".join(parts).lower()

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

    score = 0

    for title in GOOD_TITLES:
        if title.lower() in text:
            score += 2

    return min(score, 15)


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

def consistency_penalty(candidate):

    penalty = 0

    profile = candidate.get("profile", {})
    history = candidate.get("career_history", [])
    skills = candidate.get("skills", [])

    years = profile.get("years_of_experience", 0)

    expert = sum(
        1
        for s in skills
        if s.get("proficiency") == "expert"
    )

    if years < 2 and expert >= 8:
        penalty += 8

    if len(history) == 0:
        penalty += 4

    total_months = sum(
        job.get("duration_months", 0)
        for job in history
    )

    if total_months < years * 8:
        penalty += 5

    return penalty

def extract_candidate_features(candidate):

    text = candidate_to_text(candidate)

    skill, matched = get_skill_score(text)

    profile = candidate.get("profile", {})

    title_text = (
        profile.get("current_title", "")
        + " "
        + profile.get("headline", "")
    ).lower()

    achievement_text = profile.get("summary", "")

    for job in candidate.get("career_history", [])[:2]:
        achievement_text += " "
        achievement_text += job.get("description", "")

    return {
        "skill_score": skill,
        "experience_score": get_experience_score(candidate),
        "title_score": get_title_score(title_text),
        "achievement_score": get_achievement_score(achievement_text),
        "signal_score": get_signal_score(candidate),
        "matched_skills": matched,
        "consistency_penalty": consistency_penalty(candidate),
    }