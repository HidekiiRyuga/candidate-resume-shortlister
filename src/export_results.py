import json
from src.loader import load_candidates
from src.ranker import rank_candidates
from src.explainer import explain_candidate


def run():
    candidates = load_candidates(limit=20)
    ranked = rank_candidates(candidates)

    output = []

    for rank, row in enumerate(
        ranked,
        start=1
    ):
        output.append(
    {

        "rank":
            rank,

        "score":
            row["score"],

        "matched_skills":
            row[
                "features"
            ][
                "matched_skills"
            ],

        "experience_score":
            row[
                "features"
            ][
                "experience_score"
            ],

        "reasons":
            explain_candidate(
                row[
                    "features"
                ]
            ),

    }
)

    with open(
        "results.json",
        "w",
        encoding="utf-8",
    ) as f:
        json.dump(
            output,
            f,
            indent=2,
        )

    print("results.json created")

if __name__ == "__main__":
    run()