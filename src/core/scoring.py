def compute_final_score(hard_score, semantic_score, edu_boost=0):
    """
    Final score is a weighted combination:
    - Hard skill match: 40%
    - Semantic similarity: 50%
    - Education boost: 10% (optional)
    """
    final = final = 0.25 * hard_score + 0.65 * semantic_score + 0.1 * edu_boost
    return round(final, 2)

def verdict_from_score(score):
    """
    Converts final score into a verdict label.
    """
    if score >= 65:
        return 'High'
    elif score >= 45:
        return 'Medium'
    else:
        return 'Low'
