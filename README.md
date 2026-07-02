# Redrob Intelligent Candidate Discovery

An AI-powered candidate ranking system built for the **Redrob Intelligent Candidate Discovery Hackathon**. The system ranks candidates for a given job description using a hybrid approach combining structured feature extraction, recruiter engagement signals, and semantic similarity while remaining fully reproducible under the competition's CPU-only constraints.

---

# Team

**Team:** TitansGo

| Name | Role |
|------|------|
| Nitin | Team Lead / ML Engineer |
| Stuti Jeisa Toppo | ML Engineer |

---

# Project Overview

The ranking pipeline is designed to identify the top 100 candidates that best match the provided job description while satisfying the competition requirements:

- CPU-only execution
- No external API calls during ranking
- Deterministic ranking
- Explainable candidate reasoning
- Runtime under 5 minutes
- Fully reproducible

---

# Features

- Structured candidate feature extraction
- Hybrid feature + semantic ranking
- Recruiter signal integration
- Explainable candidate reasoning
- Deterministic tie-breaking
- Automatic score normalization
- CSV generation matching the submission specification

---

# Repository Structure

```
.
├── src/
│   ├── export_results.py
│   ├── ranker.py
│   ├── feature_extractor.py
│   ├── semantic_match.py
│   ├── explainer.py
│   ├── loader.py
│   ├── ranking_config.py
│   └── ...
├── candidates.jsonl
├── requirements.txt
├── submission_metadata.yaml
├── README.md
└── submission.csv
```

---

# Installation

Clone the repository:

```bash
git clone https://github.com/HidekiiRyuga/candidate-resume-shortlister.git
cd candidate-resume-shortlister
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# Generating the Submission

Place the released `candidates.jsonl` file in the project root.

Run:

```bash
python -m src.export_results
```

The script will:

1. Load all candidates
2. Extract candidate features
3. Perform fast heuristic ranking
4. Select the top candidate pool
5. Compute semantic similarity
6. Produce the final weighted ranking
7. Generate candidate explanations
8. Normalize scores
9. Export the submission CSV

Output:

```
team_TitansGo.csv
```

---

# Ranking Pipeline

The system uses a two-stage ranking architecture.

## Stage 1 — Feature Extraction

Each candidate profile is processed to extract structured information, including:

- Technical skills
- Experience
- Current title
- Recruiter engagement
- Achievement indicators
- Open-to-work status
- Notice period
- GitHub activity
- Profile consistency signals

A lightweight heuristic score is computed to efficiently rank the entire candidate pool.

---

## Stage 2 — Semantic Re-ranking

The highest-scoring candidates from Stage 1 are semantically compared with the job description.

Semantic similarity is combined with engineered features using weighted scoring to produce the final ranking.

Additional bonuses are applied for candidates demonstrating expertise in areas such as:

- Retrieval systems
- Ranking
- Embeddings
- Evaluation
- Vector databases
- Production ML

---

## Final Ranking

The final ranking process includes:

- weighted score aggregation
- deterministic tie-breaking
- monotonic score normalization
- unique ranks (1–100)
- automatic explanation generation

---

# Explainability

Each ranked candidate includes a concise explanation generated directly from profile data.

Reasoning references factual information such as:

- current title
- years of experience
- matched technical skills
- recruiter engagement
- GitHub activity
- open-to-work status
- notice period

No information is inferred beyond what is present in the candidate profile.

---

# Reproducibility

The ranking pipeline is fully deterministic.

Given the same:

- candidates.jsonl
- configuration
- model artifacts

the generated submission will be identical across runs.

No manual edits are required after execution.

---

# Competition Constraints

The implementation is designed to satisfy the Redrob evaluation constraints:

- CPU-only execution
- No hosted LLM or external API calls during ranking
- Deterministic ranking
- Reproducible results
- Explainable output
- Submission generated in CSV format

---

# Dependencies

All Python dependencies are listed in:

```
requirements.txt
```

Install using:

```bash
pip install -r requirements.txt
```
---

# Methodology

The system combines engineered candidate features with semantic similarity to produce an efficient and explainable ranking pipeline. Candidate profiles are first scored using structured signals such as technical skills, experience, recruiter engagement, achievements, and role relevance. A fast heuristic stage filters the candidate pool before semantic matching is performed against the target job description. Final scores are computed using weighted feature aggregation, semantic relevance, and domain-specific bonuses for retrieval, embeddings, ranking, evaluation, vector databases, and production ML experience. Rankings are deterministic through candidate ID tie-breaking, scores are normalized to satisfy submission requirements, and concise explanations are generated directly from candidate profile attributes without hallucinating information. The complete ranking pipeline executes locally without external API calls during inference and is fully reproducible.