import json

from src.pipeline import build_output


TOP_K = 10


def build_submission():

    ranked = build_output()

    submission = []

    for candidate in ranked[:TOP_K]:

        submission.append(
            {
                "rank": candidate["rank"],
                "score": round(candidate["score"], 2),
                "reasons": candidate["reason"],
            }
        )

    return submission


def save_submission():

    output = build_submission()

    with open(
        "submission_preview.json",
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            output,
            file,
            indent=2,
        )

    print("submission_preview.json created")


if __name__ == "__main__":
    save_submission()