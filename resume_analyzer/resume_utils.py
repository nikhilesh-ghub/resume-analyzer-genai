import io
import os
import re
from pdfminer.high_level import extract_text_to_fp
from gemini_llm import (
    extract_info_with_langchain,
    generate_improvement_suggestions,
    generate_cover_letter
)

def extract_text_from_pdf(pdf_path):
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF file not found at: {pdf_path}")
    output_string = io.StringIO()
    with open(pdf_path, 'rb') as in_file:
        extract_text_to_fp(in_file, output_string)
    return output_string.getvalue()

def extract_text_from_text(text_path):
    if not os.path.exists(text_path):
        raise FileNotFoundError(f"Text file not found at: {text_path}")
    with open(text_path, 'r', encoding='utf-8') as f:
        return f.read()

def load_and_process_input(file_path, file_type):
    if file_type.lower() == 'pdf':
        return extract_text_from_pdf(file_path)
    elif file_type.lower() == 'txt':
        return extract_text_from_text(file_path)
    else:
        raise ValueError("Unsupported file type")

def find_skill_gaps(resume_skills_str, job_skills_str):
    resume_skills = [s.strip().lower() for s in resume_skills_str.replace(',', '\n').splitlines() if s.strip()]
    job_skills = [s.strip().lower() for s in job_skills_str.replace(',', '\n').splitlines() if s.strip()]
    return [s for s in job_skills if s not in resume_skills]

def calculate_job_fit_score(resume_info, job_description_info):
    resume_skills = [s.strip().lower() for s in resume_info.get('Skills', '').replace(',', '\n').splitlines()]
    job_skills = [s.strip().lower() for s in job_description_info.get('Skills', '').replace(',', '\n').splitlines()]
    resume_experience = resume_info.get('Experience', '').lower()
    job_keywords_str = job_description_info.get('Keywords', '').lower()

    skill_score = (len(set(resume_skills) & set(job_skills)) / len(job_skills)) * 50 if job_skills else 0
    exp_keywords = [k.strip() for k in job_description_info.get('Experience', '').lower().replace(',', '\n').splitlines()]
    exp_score = (sum(k in resume_experience for k in exp_keywords) / len(exp_keywords)) * 30 if exp_keywords else 10
    jd_keywords = [k.strip() for k in job_keywords_str.replace(',', '\n').splitlines()]
    keyword_score = (sum(len(re.findall(r'\b' + re.escape(k) + r'\b', resume_experience)) > 0 for k in jd_keywords) / len(jd_keywords)) * 20 if jd_keywords else 0

    return min(skill_score + exp_score + keyword_score, 100)

def analyze_resume(resume_file, job_file):
    if resume_file is None or job_file is None:
        return "Please upload both a resume and a job description.", "", "", "", ""

    try:
        resume_type = os.path.splitext(resume_file)[1].lstrip('.').lower()
        job_type = os.path.splitext(job_file)[1].lstrip('.').lower()

        if resume_type not in ['pdf', 'txt'] or job_type not in ['pdf', 'txt']:
            return "Unsupported file type. Please upload PDF or TXT.", "", "", "", ""

        resume_text = load_and_process_input(resume_file, resume_type)
        job_text = load_and_process_input(job_file, job_type)

        resume_info = extract_info_with_langchain(resume_text)
        job_info = extract_info_with_langchain(job_text)

        skill_gaps = find_skill_gaps(resume_info.get("Skills", ""), job_info.get("Skills", ""))
        skill_gaps_text = "\n".join(skill_gaps) if skill_gaps else "No significant skill gaps found."

        score = calculate_job_fit_score(resume_info, job_info)
        score_text = f"{score:.2f}/100"

        suggestions = generate_improvement_suggestions(resume_info, job_info, skill_gaps)
        cover_letter = generate_cover_letter(resume_info, job_info)

        return "Analysis complete.", skill_gaps_text, score_text, suggestions, cover_letter

    except Exception as e:
        return f"An error occurred: {e}", "", "", "", ""
