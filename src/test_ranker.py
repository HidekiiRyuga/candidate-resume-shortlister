from src.loader import load_candidates
from src.ranker import rank_candidates


def main():
    ranked = rank_candidates(load_candidates(limit=20))

    print("\nTop 10\n")

    for i, row in enumerate(ranked[:10], 1):
        f = row["features"]
        s = row["candidate"]["redrob_signals"]

        print(f"{i}. Score: {row['score']}")
        print("Skills:", f["matched_skills"])
        print("Response:", s["recruiter_response_rate"])
        print("Interview:", s["interview_completion_rate"])
        print("-" * 40)


if __name__ == "__main__":
    main()