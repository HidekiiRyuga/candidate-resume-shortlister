"""
Central configuration for candidate ranking.

All weights and keywords used by the ranking engine
should be defined here.
"""
# Feature Weights

WEIGHTS = {
    "semantic_match": 40,
    "experience": 25,
    "skills": 20,
    "achievements": 10,
    "behavior": 5,
}
# Required Skills
REQUIRED_SKILLS = [

    "python",

    "embeddings",

    "retrieval",

    "ranking",

    "vector database",

    "evaluation",

]
# Preferred Skills
PREFERRED_SKILLS = [

    "pinecone",

    "qdrant",

    "weaviate",

    "faiss",

    "opensearch",

    "elasticsearch",

    "milvus",

    "lora",

    "qlora",

    "peft",

    "xgboost",

]


# Positive Job Titles

GOOD_TITLES = [

    "engineer",
    "software engineer",

    "data scientist",

    "machine learning engineer",

    "ml engineer",

    "ai engineer",

    "senior engineer",

    "developer",

    "research engineer",

    "backend engineer",

]

# Achievement Words

ACHIEVEMENT_WORDS = [

    "built",

    "designed",

    "deployed",

    "scaled",

    "improved",

    "optimized",

    "reduced",

    "increased",

]