from src.semantic_match import semantic_score

job = """
Python
Retrieval
Ranking
Vector database
"""

candidate = """
Python developer
Built retrieval systems
Worked with FAISS
"""

print(semantic_score(job, candidate))

