from sentence_transformers import SentenceTransformer
from fuzzywuzzy import fuzz
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Lightweight model for fast embeddings
MODEL = SentenceTransformer('all-MiniLM-L6-v2')

def simple_hard_match(must_have, good_have, resume_text):
    resume_l = resume_text.lower()
    matched = []
    missing = []
    total_skills = len(must_have) + len(good_have)
    score_count = 0

    for s in must_have:
        r = fuzz.partial_ratio(s.lower(), resume_l)
        if r >= 70:
            score_count += 1.0  # must-have weight
            matched.append(s)
        else:
            missing.append(s)

    for s in good_have:
        r = fuzz.partial_ratio(s.lower(), resume_l)
        if r >= 65:
            score_count += 0.5  # good-to-have weight
            matched.append(s)
        else:
            missing.append(s)

    denominator = len(must_have) + 0.5 * len(good_have)
    hard_score = 0 if denominator == 0 else (score_count / denominator) * 100
    return hard_score, missing

def compute_embedding_similarity(text1, text2):
    try:
        v1 = MODEL.encode([text1])[0]
        v2 = MODEL.encode([text2])[0]
        sim = float(cosine_similarity([v1], [v2])[0][0])
        # Normalize from [-1, 1] to [0, 100]
        return max(0.0, min(100.0, (sim + 1) / 2 * 100))
    except Exception:
        return 50.0  # fallback score
