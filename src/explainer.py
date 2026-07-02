def explain_candidate(candidate, features, rank=None):

    profile = candidate.get("profile", {})
    signals = candidate.get("redrob_signals", {})

    title = profile.get(
        "current_title",
        "AI Professional"
    )

    years = profile.get(
        "years_of_experience",
        0
    )

    matched = features.get(
        "matched_skills",
        []
    )

    response = signals.get(
        "recruiter_response_rate",
        0
    )

    notice = signals.get(
        "notice_period_days",
        None
    )

    github = signals.get(
        "github_activity_score",
        -1
    )

    open_to_work = signals.get(
        "open_to_work_flag",
        False
    )

    reasons = []

    reasons.append(
        f"{title} with {years:.1f} years of experience."
    )

    if len(matched) >= 5:

        reasons.append(
            "Strong alignment with the core AI requirements."
        )

    elif len(matched) >= 3:

        reasons.append(
            "Good alignment with the job description."
        )

    else:

        reasons.append(
            "Partial alignment with the required AI skills."
        )

    if matched:

        reasons.append(
            "Key skills: "
            + ", ".join(matched[:3])
            + "."
        )

    if response >= 0.80:

        reasons.append(
            "Excellent recruiter engagement."
        )

    elif response >= 0.60:

        reasons.append(
            "Good recruiter engagement."
        )

    elif response >= 0.40:

        reasons.append(
            "Moderate recruiter engagement."
        )

    if github >= 75:

        reasons.append(
            "High recent GitHub activity."
        )

    if open_to_work:

        reasons.append(
            "Currently open to work."
        )

    if notice is not None and notice >= 90:

        reasons.append(
            f"Long notice period ({notice} days)."
        )

    if rank is not None and rank > 70:

        if len(matched) < 3:

            reasons.append(
                "Matches only part of the required AI skill set."
            )

        elif response < 0.40:

            reasons.append(
                "Recruiter engagement is lower than higher-ranked candidates."
            )

    return " ".join(reasons)