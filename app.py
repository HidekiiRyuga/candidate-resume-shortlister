import tempfile
import pandas as pd
import streamlit as st

from src.loader import load_candidates
from src.ranker import rank_candidates
from src.explainer import explain_candidate

st.set_page_config(
    page_title="Redrob Candidate Ranker",
    layout="wide"
)

st.title("Redrob Candidate Ranking Demo")

st.write(
    "Upload a candidates.jsonl file (up to 100 candidates), "
    "run the ranking pipeline, and download the ranked CSV."
)

uploaded_file = st.file_uploader(
    "Upload candidates.jsonl",
    type=["jsonl"]
)

if uploaded_file is not None:

    contents = uploaded_file.getvalue().decode("utf-8")

    lines = contents.strip().splitlines()

    if len(lines) > 100:

        st.error(
            "Please upload at most 100 candidates."
        )

        st.stop()
    temp = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".jsonl"
    )

    temp.write(uploaded_file.getvalue())

    temp.close()

    if st.button("Run Ranking"):

        candidates = load_candidates(
            temp.name
        )