import re

REQUIRED_SKILLS = [
    "python",
    "llm",
    "rag",
    "retrieval",
    "ranking",
    "recommendation",
    "embedding",
    "search",
]

PREFERRED_SKILLS = [
    "vector",
    "evaluation",
    "pinecone",
    "faiss",
    "qdrant",
]


ACHIEVEMENT_WORDS = [
    "improved",
    "built",
    "deployed",
    "reduced",
    "scaled",
    "increased",
]


TITLES = [
    "engineer",
    "senior",
    "ml engineer",
    "ai engineer",
    "data scientist",
]


def extract_text(candidate):
    return str(candidate).lower()


def score_skills(text):
    score = 0
    matched = []

    for skill in REQUIRED_SKILLS:

        if skill in text:
            score += 5
            matched.append(skill)

    for skill in PREFERRED_SKILLS:

        if skill in text:
            score += 2
            matched.append(skill)

    return score, matched


def score_experience(text):

    years = re.findall(
        r"(\\d+)\\+?\\s*year",
        text
    )

    if not years:
        return 0
    return min(
        max(map(int, years)) * 5,
        25
    )


def score_achievement(text):

    return sum(
        text.count(word)
        for word in ACHIEVEMENT_WORDS
    )


def score_titles(text):
    return sum(
        1
        for title in TITLES
        if title in text
)


def extract_features(candidate):
    text = extract_text(candidate)
    skill_score, skills = score_skills(text)
    exp = score_experience(text)
    achievement = score_achievement(text)
    title_score = score_titles(text)
    total = (skill_score+exp+achievement+title_score)
    return {
        "skill_score": skill_score,
        "experience_score": exp,
        "achievement_score":achievement,
        "title_score":title_score,
        "matched_skills":skills,
        "final_feature_score":total,
    }