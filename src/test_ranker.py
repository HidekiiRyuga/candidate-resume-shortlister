from src.loader import load_candidates
from src.ranker import rank_candidates


def main():
    ranked = rank_candidates(load_candidates(limit=20))

    print("\nTop 10\n")

    for i, row in enumerate(ranked[:10], 1):
        print(f"{i}. Score: {row['score']}")
        print("Skills:", row["features"]["matched_skills"])
        print()

if __name__ == "__main__":
    main()