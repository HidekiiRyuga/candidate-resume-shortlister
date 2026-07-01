import pandas as pd

from src.loader import load_candidates
from src.ranker import rank_candidates
from src.explainer import explain_candidate


def build_reason(row):

    candidate = row["candidate"]

    return explain_candidate(
        candidate,
        row["features"]
    )


def export():

    print("loading candidates")

    ranked = rank_candidates(
        load_candidates()
    )[:100]

    for i in range(1, len(ranked)):
        ranked[i]["score"] = min(
            ranked[i]["score"],
            ranked[i - 1]["score"]
        )

    rows = []

    for i, row in enumerate(ranked, 1):

        rows.append({
            "candidate_id":
                row["candidate"]["candidate_id"],

            "rank":
                i,

            "score":
                round(
                    row["score"] / 100,
                    3
                ),

            "reasoning":
                build_reason(row)
        })

    print("ranked:", len(rows))

    df = pd.DataFrame(rows)

    df.to_csv(
        "submission.csv",
        index=False,
        encoding="utf-8"
    )

    print("submission.csv created")


if __name__ == "__main__":
    export()