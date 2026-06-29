from pprint import pprint

from src.loader import load_candidates
from src.feature_extractor import (extract_candidate_features)

def run():
    candidates = (load_candidates(limit=3))

    for i, candidate in enumerate(
        candidates,
        start=1,
    ):

        print()
        print("=" * 50)
        print(f"Candidate {i}")
        pprint(extract_candidate_features(candidate))


if __name__ == "__main__":
    run()