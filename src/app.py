import streamlit as st
st.set_page_config(page_title='Resume Relevance MVP', layout='wide')

try:
    st.write("✅ App started")

    # Your entire app logic goes here...
    # All imports, sidebar, buttons, evaluation, etc.

except Exception as e:
    st.error(f"❌ App crashed: {e}")
import os
try:
    from core.parser import (
        extract_text_from_file,
        normalize_text,
        extract_skills_from_jd,
        segment_jd_sections,
        classify_resume
    )
    from core.matcher import simple_hard_match, compute_embedding_similarity
    from core.scoring import compute_final_score, verdict_from_score
    from core.feedback import generate_feedback_scaffold
except Exception as e:
    st.error(f"❌ Import error: {e}")

hf_token = os.environ.get("HUGGINGFACE_TOKEN")

# Optional fallback for local development with .env
if hf_token is None:
    try:
        from dotenv import load_dotenv
        load_dotenv()
        hf_token = os.environ.get("HUGGINGFACE_TOKEN")
    except ModuleNotFoundError:
        hf_token = None

st.write(f"Hugging Face token loaded: {'✅' if hf_token else '❌'}")

st.set_page_config(page_title='Resume Relevance MVP', layout='wide')
st.title('🚀 Automated Resume Relevance Check')

with st.sidebar:
    st.markdown('## 📂 Upload Inputs')
    jd_file = st.file_uploader('Upload Job Description (PDF/DOCX/TXT)', type=['pdf', 'docx', 'txt'])
    jd_text_input = st.text_area('Or paste JD text here', height=150)
    resume_files = st.file_uploader('Upload Resume(s) (PDF/DOCX)', type=['pdf', 'docx'], accept_multiple_files=True)

    debug_mode = st.checkbox("🔍 Enable debug mode")
    if debug_mode:
        st.write("Debug mode is ON")

    # 🔥 Auto Skill Extraction
    if st.button('Auto-extract skills from JD'):
        jd_text = extract_text_from_file(jd_file) if jd_file else jd_text_input.strip()
        jd_text = normalize_text(jd_text)
        if jd_text:
            must, good = extract_skills_from_jd(jd_text)
            st.session_state['auto_must'] = must
            st.session_state['auto_good'] = good
            st.success("Skills extracted successfully!")
        else:
            st.warning("Please upload or paste a JD first.")

    # Show extracted skills
    if 'auto_must' in st.session_state:
        st.markdown(f"**Auto MUST-HAVE skills:** {', '.join(st.session_state['auto_must'])}")
    if 'auto_good' in st.session_state:
        st.markdown(f"**Auto GOOD-TO-HAVE skills:** {', '.join(st.session_state['auto_good'])}")

must_have = st.text_input('Comma-separated MUST-HAVE skills', 
                          ', '.join(st.session_state.get('auto_must', ['python', 'sql', 'ml'])))
good_have = st.text_input('Comma-separated GOOD-TO-HAVE skills', 
                          ', '.join(st.session_state.get('auto_good', ['nlp', 'cloud'])))

if 'evaluations' not in st.session_state:
    st.session_state['evaluations'] = []

def get_jd_text():
    if jd_file is not None:
        txt = extract_text_from_file(jd_file)
        return normalize_text(txt)
    return jd_text_input.strip()

st.header('📊 Run Evaluation')
if st.button('Evaluate Resume(s)'):
    jd_text = get_jd_text()
    if not jd_text:
        st.error('Please provide a JD (file or paste)')
    elif not resume_files:
        st.error('Please upload at least one resume file')
    else:
        must = [s.strip() for s in must_have.split(',') if s.strip()]
        good = [s.strip() for s in good_have.split(',') if s.strip()]

        for resume_file in resume_files:
            resume_text = normalize_text(extract_text_from_file(resume_file))
            resume_type = classify_resume(resume_text)
            edu_boost = 10 if resume_type == "Fresher" else 0

            hard_score, missing_skills = simple_hard_match(must, good, resume_text)
            semantic_score = compute_embedding_similarity(jd_text, resume_text)
            final = compute_final_score(hard_score, semantic_score, edu_boost=edu_boost)
            verdict = verdict_from_score(final)
            feedback = generate_feedback_scaffold(jd_text, resume_text, missing_skills, final, verdict)

            eval_record = {
                'resume_name': getattr(resume_file, 'name', 'uploaded_resume'),
                'score': round(final, 2),
                'verdict': verdict,
                'missing': missing_skills,
                'feedback': feedback,
                'resume_type': resume_type,
                'semantic_score': round(semantic_score, 2),
                'hard_score': round(hard_score, 2)
            }

            st.session_state['evaluations'].append(eval_record)

        st.success('✅ Evaluation complete. Scroll down to view the results.')

st.header('📁 Evaluations')
if not st.session_state['evaluations']:
    st.info("No evaluations yet. Upload resumes and click 'Evaluate Resume(s)' to begin.")

for i, e in enumerate(st.session_state['evaluations']):
    st.subheader(f"{i+1}. {e['resume_name']} — {e['score']} ({e['verdict']})")
    st.markdown(f"**Resume Type:** {e['resume_type']}")
    st.markdown(f"**Hard Skill Match Score:** {e['hard_score']}")
    st.markdown(f"**Semantic Similarity Score:** {e['semantic_score']}")
    st.markdown(f"**Missing Skills:** {', '.join(e['missing']) if e['missing'] else 'None'}")

    with st.expander('🧠 Feedback'):
        st.markdown(e['feedback']['summary'])
        st.markdown(f"**Explanation:** {e['feedback']['explanation']}")
        st.markdown("**Suggestions:**")
        for s in e['feedback']['suggestions']:
            st.markdown(f"- {s}")
