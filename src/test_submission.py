from src.submission_builder import build_submission


def main():

    submission = build_submission()

    print("\nSubmission Preview\n")

    for row in submission:

        print(row)


if __name__ == "__main__":
    main()