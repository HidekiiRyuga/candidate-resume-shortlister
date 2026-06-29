from pprint import pprint
from src.loader import load_candidates
from src.features import extract_features

data = load_candidates(limit=3)

for i, candidate in enumerate(data):
    print()
    print("=" * 40)
    print(f"Candidate {i+1}")
    pprint(extract_features(candidate))