def semantic_score(job_text, candidate_text):
    """
    Placeholder for semantic matching.
    Returns 0–10.
    """

    if not job_text or not candidate_text:
        return 0

    job=set(job_text.lower().split())
    candidate=set(candidate_text.lower().split())

    overlap=len(job & candidate)

    return min(overlap,10)