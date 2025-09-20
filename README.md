
# Automated Resume Relevance Check System (Streamlit MVP)

## Overview
This is a Streamlit-only MVP for the "Automated Resume Relevance Check System" (Theme 2 hackathon).
It provides:
- JD upload (paste or upload file)
- Resume upload (PDF/DOCX)
- Text extraction, keyword hard-match, semantic matching (embeddings), scoring, and LLM-powered feedback scaffolding.
- Streamlit dashboard to view evaluations.

## Quickstart (local)
1. Unzip and enter folder:
   ```bash
   unzip resume-relevance.zip
   cd resume-relevance
   ```
2. (Optional) Create virtualenv and activate:
   ```bash
   python -m venv genai_env
   source genai_env/bin/activate  # mac/linux
   genai_env\Scripts\activate   # windows
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Copy `.env.example` to `.env` and add API keys:
   ```bash
   cp .env.example .env
   # Then edit .env and fill OPENAI_API_KEY=your_key_here (or HF token)
   ```
5. Run the Streamlit app:
   ```bash
   streamlit run src/app.py
   ```

## Notes
- This scaffold is an MVP. Replace or extend the LLM calls with your preferred provider/keys.
- Do **not** commit your `.env` with secrets.

## File structure
See `docs/architecture.md` for the architecture and scoring formula.
