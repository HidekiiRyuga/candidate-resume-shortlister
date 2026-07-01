import pandas as pd
from src.loader import load_candidates
from src.ranker import rank_candidates
from src.explainer import explain_candidate


def build_reason(row):

    candidate=row["candidate"]

    title=(
        candidate
        .get("profile",{})
        .get(
            "current_title",
            "Candidate"
        )
    )

    details=explain_candidate(
        candidate,
        row["features"]
    )

    return f"{title} with {details}."

def export():

    ranked=rank_candidates(
        load_candidates()
    )

    print("loading candidates")

    rows=[]

    for i,row in enumerate(ranked,1):

        rows.append({
            "candidate_id":
                row["candidate"]["candidate_id"],
            "rank":i,
            "score":
                round(
                    row["score"]/100,
                    3
                ),
            "reasoning":
                build_reason(row)
        })

    print("ranked:", len(ranked))

    df=pd.DataFrame(rows)

    df.to_csv(
        "submission.csv",
        index=False
    )

    print("submission.csv created")


if __name__=="__main__":
    export()