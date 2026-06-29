from src.loader import load_candidates

def inspect():

    candidates = load_candidates(limit=1)

    if not candidates:
        print("No candidates loaded")
        return

    sample = candidates[0]

    print("\nTop-level fields:\n")

    for key in sample.keys():
        print("-", key)

if __name__ == "__main__":
    inspect()