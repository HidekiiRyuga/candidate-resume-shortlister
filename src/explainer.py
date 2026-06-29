def explain_candidate(features):

    reasons = []

    skills = features.get(
        "matched_skills",
        []
    )

    if skills:

        shown = skills[:3]

        reasons.append(

            "matched skills: "
            + ", ".join(shown)

        )

    experience = features.get(
        "experience_score",
        0
    )

    if experience:

        approx_years = round(
            experience / 3
        )

        reasons.append(

            f"estimated {approx_years}+ years experience"

        )

    title = features.get(
        "title_score",
        0
    )

    if title >= 4:

        reasons.append(

            "relevant engineering background"

        )

    achievement = features.get(
        "achievement_score",
        0
    )

    if achievement >= 3:

        reasons.append(

            "multiple measurable achievements"

        )

    if not reasons:

        reasons.append(

            "limited strong signals"

        )

    return reasons