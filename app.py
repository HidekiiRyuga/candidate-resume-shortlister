import tempfile
import pandas as pd
import streamlit as st

from src.loader import load_candidates
from src.ranker import rank_candidates
from src.explainer import explain_candidate


st.set_page_config(
    page_title="Redrob Candidate Ranker",
    page_icon="🤖",
    layout="wide"
)

st.title("Redrob Intelligent Candidate Discovery")
st.write(
    "Upload a candidate JSONL file (up to 100 candidates). "
    "The system will rank candidates and generate a submission CSV."
)

uploaded_file = st.file_uploader(
    "Upload candidates.jsonl",
    type=["jsonl"]
)

if uploaded_file is not None:

    with tempfile.NamedTemporaryFile(delete=False, suffix=".jsonl") as temp:
        temp.write(uploaded_file.read())
        temp_path = temp.name

    with st.spinner("Loading candidates..."):
        candidates = load_candidates(temp_path)

    if len(candidates) > 100:
        st.error("Please upload a file containing at most 100 candidates.")
        st.stop()

    st.success(f"Loaded {len(candidates)} candidates.")

    if st.button("Run Ranking"):

        with st.spinner("Ranking candidates..."):

            ranked = rank_candidates(candidates)

            scores = [r["score"] for r in ranked]

            max_score = max(scores)
            min_score = min(scores)

            for row in ranked:
                row["score"] = round(
                    0.40
                    + (
                        (row["score"] - min_score)
                        / (max_score - min_score + 1e-9)
                    )
                    * 0.60,
                    3,
                )

            top_score = max(r["score"] for r in ranked)
            bottom_score = min(r["score"] for r in ranked)

            score_range = max(top_score - bottom_score, 1e-9)

            rows = []

            for i, row in enumerate(ranked, 1):

                row["rank"] = i

                normalized_score = (
                    row["score"] - bottom_score
                ) / score_range

                rows.append(
                    {
                        "candidate_id": row["candidate"]["candidate_id"],
                        "rank": i,
                        "score": round(normalized_score, 3),
                        "reasoning": explain_candidate(
                            candidate=row["candidate"],
                            features=row["features"],
                            rank=i,
                        ),
                    }
                )

        df = pd.DataFrame(rows)

        st.success("Ranking completed.")

        st.dataframe(
            df,
            hide_index=True,
            use_container_width=True
        )

        csv = df.to_csv(index=False).encode("utf-8")

        st.download_button(
            "Download submission.csv",
            data=csv,
            file_name="submission.csv",
            mime="text/csv",
        )