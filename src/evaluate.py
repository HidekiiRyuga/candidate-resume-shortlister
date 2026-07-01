from statistics import mean
from src.loader import load_candidates
from src.ranker import rank_candidates


def evaluate():

    candidates=load_candidates(limit=100)

    ranked=rank_candidates(candidates)

    scores=[x["score"] for x in ranked]

    print("\nEvaluation\n")

    print("Candidates:",len(scores))
    print("Top score:",max(scores))
    print("Bottom score:",min(scores))
    print("Average:",round(mean(scores),2))

    print("\nTop 5\n")

    for i,row in enumerate(ranked[:5],1):
        print(
            i,
            row["score"],
            row["features"]["matched_skills"]
        )


if __name__=="__main__":
    evaluate()