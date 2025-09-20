
# Architecture & Scoring (MVP)

## Workflow
1. Upload JD (paste text or upload .txt/.pdf/.docx)
2. Upload Resume(s) (.pdf / .docx)
3. Parser extracts text and normalizes it (basic cleaning)
4. Hard-match: keyword/fuzzy matching for must-have and good-to-have skills
5. Semantic-match: sentence-transformers embeddings + cosine similarity
6. Score aggregation into final 0-100 score and verdict (High/Medium/Low)
7. LLM (optional) generates improvement suggestions (scaffolded prompts included)

## Scoring formula (example)
final = 0.4 * hard_score + 0.5 * semantic_score + 0.1 * edu_boost
- Hard score: match percentage of must-have & good-to-have skills (0-100)
- Semantic score: normalized cosine similarity (0-100)
- edu_boost: 0 or 100 depending on education match (simple boost)

## Files of interest
- src/core/parser.py
- src/core/matcher.py
- src/core/scoring.py
- src/core/feedback.py
- src/app.py (Streamlit frontend)
