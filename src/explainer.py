def explain_candidate(candidate,features):

    reasons=[]

    skills=features["matched_skills"]

    if skills:
        reasons.append(
            f"{len(skills)} AI core skills"
        )

    yrs=(
        candidate
        .get("profile",{})
        .get("years_of_experience",0)
    )

    reasons.append(
        f"{yrs} yrs"
    )

    response=(
        candidate
        .get("redrob_signals",{})
        .get("recruiter_response_rate",0)
    )

    reasons.append(
        f"response rate {round(response,2)}"
    )

    return "; ".join(reasons)