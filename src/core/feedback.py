# feedback.py — Enhanced feedback generator for resume–JD relevance

def generate_feedback_scaffold(jd_text, resume_text, missing_skills, score, verdict):
    import textwrap

    # Summary block
    summary = textwrap.dedent(f"""
    ✅ **Verdict:** {verdict}
    📊 **Final Score:** {round(score, 1)} / 100
    🔍 **Missing Skills:** {', '.join(missing_skills) if missing_skills else 'None'}
    """)

    # Explanation block
    explanation = ""
    if score < 50:
        explanation = "The resume lacks several core skills and shows limited alignment with the job description. Consider adding relevant projects, certifications, and technical keywords."
    elif score < 75:
        explanation = "The resume shows partial alignment. Strengthen it by quantifying achievements, highlighting relevant tools, and emphasizing collaboration or domain-specific experience."
    else:
        explanation = "The resume is a strong match. Ensure clarity in project outcomes and tailor the language to reflect the job's priorities."

    # Suggestions block
    suggestions = []
    if missing_skills:
        suggestions.append("🔧 Add or emphasize these skills: " + ', '.join(missing_skills))
    if "project" not in resume_text.lower():
        suggestions.append("📁 Include relevant projects to demonstrate applied experience.")
    if "certification" not in resume_text.lower():
        suggestions.append("🎓 Mention certifications or training programs to boost credibility.")
    if "collaborate" not in resume_text.lower():
        suggestions.append("🤝 Highlight teamwork or cross-functional collaboration.")

    # Return structured feedback
    return {
        'summary': summary.strip(),
        'explanation': explanation.strip(),
        'suggestions': suggestions
    }

# Optional: LLM-powered feedback generator (plug into OpenAI or Hugging Face)
def generate_llm_feedback(jd_text, resume_text, score, verdict):
    import openai

    prompt = f"""
    JD: {jd_text}
    Resume: {resume_text}
    Score: {score}, Verdict: {verdict}

    Write a 3-paragraph feedback:
    1. Strengths of the resume
    2. Gaps or missing elements
    3. Suggestions to improve alignment with the JD
    """

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )

    return response['choices'][0]['message']['content']
