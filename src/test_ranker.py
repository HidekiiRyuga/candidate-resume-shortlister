from src.loader import load_candidates
from src.ranker import rank_candidates


data = load_candidates(
    limit=10
)

results = rank_candidates(
    data
)

for i, row in enumerate(
    results[:5],
    start=1
):

    print()

    print(
        f"Rank {i}"
    )

    print(
        row["score"]
    )