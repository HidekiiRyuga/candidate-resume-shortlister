TOP_TEMPLATES = [
    "Strong alignment with the core AI requirements.",
    "Excellent match for the target role.",
    "Profile closely matches the primary technical requirements."
]

MID_TEMPLATES = [
    "Good alignment with the technical requirements.",
    "Relevant experience for the target role.",
    "Solid AI background with several matching skills."
]

LOW_TEMPLATES = [
    "Partial alignment with the required skills.",
    "Relevant background but fewer core matches than higher-ranked candidates.",
    "Some relevant experience, although overall fit is weaker."
]
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

    if rank is None:
        rank = 100

    if rank <= 10:
        intro = TOP_TEMPLATES[
            hash(candidate["candidate_id"]) % len(TOP_TEMPLATES)
        ]

    elif rank <= 50:
        intro = MID_TEMPLATES[
            hash(candidate["candidate_id"]) % len(MID_TEMPLATES)
        ]

    else:
        intro = LOW_TEMPLATES[
            hash(candidate["candidate_id"]) % len(LOW_TEMPLATES)
        ]

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

    reasons.append(intro)


    if matched:

        reasons.append(
            "Key skills: "
            + ", ".join(matched[:3])
            + "."
        )

    if response >= 0.80:

        reasons.append(
            "Excellent recruiter response rate."
        )

    elif response >= 0.60:

        reasons.append(
            "Strong recruiter engagement."
        )

    elif response >= 0.40:

        reasons.append(
            "Moderate recruiter engagement."
        )

    else:

        reasons.append(
            "Lower recruiter engagement than higher-ranked candidates."
        )

    if github >= 75:

        reasons.append(
            "Strong recent GitHub activity."
        )

    if open_to_work:

        reasons.append(
            "Currently open to work."
        )

    if notice is not None and notice >= 90:

        reasons.append(
            f"Long notice period ({notice} days) may delay availability."
        )
    
    return " ".join(reasons)