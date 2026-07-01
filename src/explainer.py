def explain_candidate(candidate, features):

    reasons = []

    profile = candidate.get(
        "profile",
        {}
    )

    signals = candidate.get(
        "redrob_signals",
        {}
    )

    title = profile.get(
        "current_title",
        "Candidate"
    )

    yrs = profile.get(
        "years_of_experience",
        0
    )

    skills = features.get(
        "matched_skills",
        []
    )

    response = signals.get(
        "recruiter_response_rate",
        0
    )

    reasons.append(
        f"{title}"
    )

    reasons.append(
        f"{yrs} yrs"
    )

    if skills:

        reasons.append(
            f"{len(skills)} AI skills"
        )

        reasons.append(
            ", ".join(
                skills[:3]
            )
        )

    reasons.append(
        f"response rate {round(response, 2)}"
    )

    if signals.get(
        "open_to_work_flag"
    ):
        reasons.append(
            "open to work"
        )

    return "; ".join(reasons)