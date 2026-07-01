from src.loader import load_candidates
from src.ranker import rank_candidates


ranked=rank_candidates(
    load_candidates(limit=10)
)

for i,row in enumerate(
    ranked[:5],
    1
):

    print("\n",i)
    print(
        row["candidate"]
    )