import pandas as pd
from src.loader import load_candidates
from src.ranker import rank_candidates
from src.explainer import explain_candidate


def build_reason(row):

    f=row["features"]

    skills=len(f["matched_skills"])

    return (
        f"{row['candidate'].get('current_title','Candidate')} "
        f"with {round(f['experience_score']/3,1)} yrs; "
        f"{skills} AI core skills; "
        f"semantic score {round(row.get('semantic_score',0),2)}."
    )


def export():

    ranked=rank_candidates(
        load_candidates()
    )

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

    df=pd.DataFrame(rows)

    df.to_csv(
        "submission.csv",
        index=False
    )

    print("submission.csv created")


if __name__=="__main__":
    export()