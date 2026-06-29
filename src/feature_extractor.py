import re

from src.ranking_config import (
    REQUIRED_SKILLS,
    PREFERRED_SKILLS,
    GOOD_TITLES,
    ACHIEVEMENT_WORDS,
)


def candidate_to_text(candidate):
    """
    Convert candidate object to one text blob.
    """
    return str(candidate).lower()


def get_skill_score(text):

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


def get_experience_score(text):

    years = re.findall(
        r"(\\d+)\\+?\\s*year",
        text
    )

    if not years:
        return 0

    highest = max(map(int, years))

    return min(highest * 4,25)


def get_title_score(text):
    score = 0

    for title in GOOD_TITLES:
        if title in text:
            score += 3

    return score


def get_achievement_score(text):
    score = 0

    for word in ACHIEVEMENT_WORDS:
        score += text.count(word)

    return min(score, 10)


def extract_candidate_features(candidate):

    text = candidate_to_text(candidate)
    skill_score, skills = (get_skill_score(text))
    experience = (get_experience_score(text))
    title = (get_title_score(text))

    achievement = (get_achievement_score(text))
    return {
        "skill_score":skill_score,
        "experience_score":experience,
        "title_score":title,
        "achievement_score":achievement,
        "matched_skills":skills,

    }