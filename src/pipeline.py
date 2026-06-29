import json
from src.loader import (load_candidates)
from src.ranker import (rank_candidates)
from src.explainer import (explain_candidate)


TOP_K = 20


def build_output():

    candidates = (load_candidates())
    ranked = (rank_candidates(candidates))
    results = []

    for i, row in enumerate(
        ranked[:TOP_K],
        start=1,
    ):

        results.append(
            {
                "rank": i,
                "score":row["score"],
                "reason":
                    explain_candidate(row["features"]),
                "skills":
                    row["features"]["matched_skills"],
            }
        )

    return results


def save():
    output = (build_output())

    with open(
        "submission_preview.json",
        "w",
        encoding="utf-8",
    ) as f:

        json.dump(
            output,
            f,
            indent=2,
        )

    print("submission_preview.json created")


if __name__ == "__main__":    save()