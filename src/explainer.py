def explain_candidate(features):
    reasons = []
    if features["skill_score"] >= 10:
        reasons.append("strong skill alignment")

    if features["experience_score"] >= 15:
        reasons.append("relevant experience")

    if features["achievement_score"] >= 3:
        reasons.append("impact indicators")

    if features["title_score"] >= 2:
        reasons.append("relevant job titles")

    if not reasons:
        reasons.append("limited matching signals")

    return reasons