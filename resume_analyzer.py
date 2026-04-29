import os
import PyPDF2
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import google.generativeai as genai


# ✅ Configure Gemini API (USE ONLY ONE METHOD)
genai.configure(api_key="YOUR_GEMINI_API_KEY")

model = genai.GenerativeModel("gemini-pro")


# ✅ Skills Database (proper structure)
SKILLS_DB = {
    "technical": [
        "python", "java", "c++", "javascript", "sql",
        "machine learning", "data analysis", "html", "css",
        "react", "angular", "node", "django", "flask",
        "git", "mongodb", "excel", "power bi"
    ],
    "business": [
        "sales", "marketing", "management", "leadership", "teamwork"
    ],
    "finance": [
        "accounting", "financial analysis", "budgeting", "tax", "auditing"
    ],
    "general": [
        "problem solving", "time management", "adaptability", "critical thinking"
    ]
}


# ✅ Extract text from PDF
def extract_text_from_pdf(pdf_file):
    text = ""
    reader = PyPDF2.PdfReader(pdf_file)

    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted

    return text.lower()


# ✅ Extract skills properly from DB
def extract_skills(text):
    found_skills = []

    for category in SKILLS_DB.values():
        for skill in category:
            if skill in text:
                found_skills.append(skill)

    return list(set(found_skills))


# ✅ Extract skills from job description
def extract_jd_skills(job_description):
    jd_skills = []

    job_description = job_description.lower()

    for category in SKILLS_DB.values():
        for skill in category:
            if skill in job_description:
                jd_skills.append(skill)

    return list(set(jd_skills))


# ✅ Calculate similarity score
def calculate_similarity(resume_text, job_description):
    vectorizer = TfidfVectorizer(stop_words="english")

    tfidf = vectorizer.fit_transform([resume_text, job_description])

    score = cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0]

    return round(score * 100, 2)


# ✅ Rule-based analyzer (fast + reliable)
def analyze_resume_basic(resume_text, job_description):
    skills = extract_skills(resume_text)
    jd_skills = extract_jd_skills(job_description)

    missing_skills = [skill for skill in jd_skills if skill not in skills]

    score = calculate_similarity(resume_text, job_description)

    return {
        "score": score,
        "matched_skills": skills,
        "missing_skills": missing_skills
    }


# ✅ AI-based analysis (Gemini)
def ai_resume_analysis(resume_text, job_description):
    prompt = f"""
You are an ATS (Applicant Tracking System).

Analyze the resume based on the job description.

Resume:
{resume_text}

Job Description:
{job_description}

Give output in this format:

Score (0-100):
Strengths:
- ...
Missing Skills:
- ...
Suggestions:
- ...
"""

    try:
        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        return f"Error in AI analysis: {str(e)}"
