import PyPDF2
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ✅ Multi-domain skills database
SKILLS_DB = {
    "technical": [
        "python", "java", "c++", "javascript", "sql",
        "machine learning", "data analysis", "html", "css",
        "react", "angular", "node", "django", "flask",
        "git", "mongodb", "excel", "power bi"
    ],
    "business": [
        "sales", "marketing", "management", "leadership", "teamwork",
        "communication", "negotiation"
    ],
    "finance": [
        "accounting", "financial analysis", "excel", "budgeting",
        "tax", "auditing"
    ],
    "general": [
        "problem solving", "time management", "adaptability",
        "critical thinking"
    ]
}


# ✅ Clean text for better processing
def clean_text(text):
    text = re.sub(r'[^a-zA-Z ]', ' ', text)
    return text.lower()


# ✅ Extract text from PDF (optimized)
def extract_text_from_pdf(pdf_file):
    text = ""
    reader = PyPDF2.PdfReader(pdf_file)

    for page in reader.pages:
        text += page.extract_text() or ""

    # Limit text for speed
    return clean_text(text[:2000])


# ✅ Extract skills correctly from dictionary
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
    jd_text = job_description.lower()

    for category in SKILLS_DB.values():
        for skill in category:
            if skill in jd_text:
                jd_skills.append(skill)

    return list(set(jd_skills))


# ✅ Improved similarity using TF-IDF
def calculate_similarity(resume_text, job_description):
    vectorizer = TfidfVectorizer(stop_words="english", max_features=1000)
    tfidf = vectorizer.fit_transform([resume_text, job_description])

    score = cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0]
    return score * 100


# ✅ Main analysis function
def analyze_resume(pdf_file, job_description):

    resume_text = extract_text_from_pdf(pdf_file)
    job_description = clean_text(job_description)

    skills = extract_skills(resume_text)
    jd_skills = extract_jd_skills(job_description)

    # ✅ Text similarity score
    text_score = calculate_similarity(resume_text, job_description)

    # ✅ Skill-based score
    skill_match_ratio = 0
    if jd_skills:
        matched = [s for s in jd_skills if s in skills]
        skill_match_ratio = len(matched) / len(jd_skills)

    skill_score = skill_match_ratio * 100

    # ✅ Final combined score (balanced)
    final_score = (0.6 * text_score) + (0.4 * skill_score)
    final_score = round(final_score, 2)

    # ✅ Missing skills
    missing_skills = [s for s in jd_skills if s not in skills]

    # ✅ Suggestions
    suggestions = []

    if missing_skills:
        suggestions.append("Add these missing skills: " + ", ".join(missing_skills))

    if final_score < 40:
        suggestions.append("Resume is poorly aligned with job description")
    elif final_score < 70:
        suggestions.append("Resume is moderately aligned, needs improvement")
    else:
        suggestions.append("Resume is well aligned with the job")

    if len(skills) < 5:
        suggestions.append("Add more role-specific skills to strengthen your resume")

    if not skills:
        suggestions.append("No relevant skills detected, try improving resume content")

    return {
        "score": final_score,
        "skills_found": skills,
        "missing_skills": missing_skills,
        "suggestions": suggestions
    }
