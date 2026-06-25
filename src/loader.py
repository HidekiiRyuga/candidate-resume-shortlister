import json
from src.config import FULL_DATASET_FILE

def load_candidates(limit=None):
    candidates = []
    try:
        with open(FULL_DATASET_FILE,"r",encoding="utf-8") as file:

            for line in file:
                if not line.strip():
                    continue

                candidates.append(json.loads(line))

                if (limit is not None and len(candidates)>=limit):
                    break
    except FileNotFoundError:
        print("Dataset not found yet.")
    return candidates