import time
import pandas as pd
from src.loader import load_candidates
from src.ranker import rank_candidates
from src.explainer import explain_candidate


def build_reason(row):

    

    return explain_candidate(
        candidate = row["candidate"],
        features = row["features"],
        rank = row["rank"]
    )


def export():

    print("loading candidates")

    start = time.time()

    candidates = load_candidates()
    print(f"Loaded {len(candidates)} candidates in {time.time()-start:.2f}s")

    start = time.time()

    ranked = rank_candidates(candidates)

    ranked.sort(
        key=lambda x: (
            -x["score"],
            x["candidate"]["candidate_id"]
        )
    )

    ranked = ranked[:100]

    print(f"Ranking completed in {time.time()-start:.2f}s")

    # -----------------------------
    # Keep monotonic score smoothing (optional safety step)
    # -----------------------------
    scores = [row["score"] for row in ranked]

    max_score = max(scores)
    min_score = min(scores)

    for row in ranked:

        row["score"] = round(
            0.40 +
            (
                (row["score"] - min_score)
                / (max_score - min_score + 1e-9)
            ) * 0.60,
            3
        )

    # -----------------------------
    # STEP 2: Normalize scores properly
    # -----------------------------
    top_score = max(row["score"] for row in ranked)
    bottom_score = min(row["score"] for row in ranked)

    score_range = max(
        top_score - bottom_score,
        1e-9
    )

    rows = []

    for i, row in enumerate(ranked, 1):

        row["rank"] = i

        normalized_score = (
            row["score"] - bottom_score
        ) / score_range

        score = round(normalized_score, 3)

        if rows:
            score = min(score, rows[-1]["score"])

        rows.append({
            "candidate_id":
                row["candidate"]["candidate_id"],

            "rank":
                i,

            "score":
                score,

            "reasoning":
                build_reason(row)
        })
    print("ranked:", len(rows))

    if rows:
        print(
            "Top score:",
            rows[0]["score"],
            "Bottom score:",
            rows[-1]["score"]
        )

    assert len(rows) == 100

    assert len(set(r["candidate_id"] for r in rows)) == 100

    assert sorted(r["rank"] for r in rows) == list(range(1, 101))

    for i in range(1, len(rows)):
        assert rows[i-1]["score"] >= rows[i]["score"]
        
    df = pd.DataFrame(rows)

    df.to_csv(
        "team_TitansGo.csv",
        index=False,
        encoding="utf-8"
    )

    print("team_TitansGo.csv created")


if __name__ == "__main__":
    export()