from src.loader import load_candidates
from src.ranker import rank_candidates


def main():
    ranked = rank_candidates(load_candidates(limit=20))

    print("\nTop 10\n")

    for i, row in enumerate(ranked[:10], 1):
        f = row["features"]

        print(f"{i}. Score: {row['score']}")
        print(f"Semantic: {row['semantic_score']}")
        print(f"Skills: {f['matched_skills']}")
        print(
            f"Exp={f['experience_score']} "
            f"Title={f['title_score']} "
            f"Achievement={f['achievement_score']}"
        )
        print("-" * 40)


if __name__ == "__main__":
    main()