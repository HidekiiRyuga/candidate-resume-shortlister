from src.loader import load_candidates
from src.ranker import rank_candidates


def main():

    candidates = load_candidates(limit=10)

    ranked = rank_candidates(candidates)

    print("\nTop 5 Candidates\n")

    for rank, candidate in enumerate(ranked[:5], start=1):

        print("-" * 50)

        print(f"Rank {rank}")
        print(f"Score : {candidate['score']}")

        print(candidate["features"])


if __name__ == "__main__":
    main()