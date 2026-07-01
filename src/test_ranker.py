from src.loader import load_candidates
from src.ranker import rank_candidates


def main():
    ranked = rank_candidates(load_candidates(limit=20))

    print("\nTop 10\n")

    for row in ranked[:10]:
        print(f"Rank: {row['rank']}")
        print(f"Score: {row['score']}")
        print(f"Skills: {row['features']['matched_skills']}")
        print("-" * 40)


if __name__ == "__main__":
    main()