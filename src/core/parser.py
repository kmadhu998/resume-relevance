import pdfplumber
import docx2txt
import fitz  # PyMuPDF

def extract_text_from_file(uploaded_file):
    filename = uploaded_file.name.lower()

    if filename.endswith('.pdf'):
        text = ""
        with pdfplumber.open(uploaded_file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text

    elif filename.endswith('.docx'):
        tmp_path = 'temp_upload.docx'
        with open(tmp_path, 'wb') as f:
            f.write(uploaded_file.read())
        return docx2txt.process(tmp_path)

    elif filename.endswith('.txt'):
        return uploaded_file.read().decode("utf-8")

    else:
        return ""

def normalize_text(text):
    import re
    text = re.sub(r'\n{2,}', '\n', text)
    text = ' '.join(text.split())
    return text.strip()

def extract_skills_from_jd(jd_text):
    import re

    skill_keywords = [
        'python', 'sql', 'r', 'excel', 'nlp', 'llm', 'generative ai', 'data analysis',
        'data cleaning', 'automation', 'pandas', 'machine learning', 'collaboration',
        'stakeholders', 'product managers', 'data scientists', 'data engineers',
        'power bi', 'tableau', 'git', 'jupyter', 'deep learning', 'cloud', 'aws', 'azure'
    ]

    jd_lower = jd_text.lower()
    must_have = []
    good_to_have = []

    for skill in skill_keywords:
        if skill in jd_lower:
            if re.search(rf"(must[- ]have|required|qualification).*{skill}", jd_lower):
                must_have.append(skill)
            else:
                good_to_have.append(skill)

    must_have = list(set(must_have))
    good_to_have = [s for s in set(good_to_have) if s not in must_have]

    return must_have, good_to_have

def segment_jd_sections(jd_text):
    import re
    sections = {
        "Responsibilities": "",
        "Requirements": "",
        "Qualifications": "",
        "Company Info": ""
    }
    patterns = {
        "Responsibilities": r"(?i)(Responsibilities|What you will do)[:\s]*(.*?)(?=\n[A-Z]|$)",
        "Requirements": r"(?i)(Requirements|Who you are)[:\s]*(.*?)(?=\n[A-Z]|$)",
        "Qualifications": r"(?i)(Qualifications|Skills)[:\s]*(.*?)(?=\n[A-Z]|$)",
        "Company Info": r"(?i)(About|Mission|Company)[:\s]*(.*?)(?=\n[A-Z]|$)"
    }
    for key, pattern in patterns.items():
        match = re.search(pattern, jd_text, re.DOTALL)
        if match:
            sections[key] = match.group(2).strip()
    return sections

def classify_resume(resume_text):
    resume_lower = resume_text.lower()
    if "internship" in resume_lower or "bachelor" in resume_lower or "fresher" in resume_lower:
        return "Fresher"
    elif "years of experience" in resume_lower or "lead" in resume_lower or "manager" in resume_lower:
        return "Experienced"
    else:
        return "General"
