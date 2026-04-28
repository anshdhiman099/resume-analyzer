import PyPDF2
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Expanded skills database
SKILLS_DB = {  "technical" : [
    "python", "java", "c++", "javascript", "sql",
    "machine learning", "data analysis", "html", "css",
    "react", "angular", "node", "django", "flask",
    "git", "mongodb", "excel", "power bi"
],
"business" : ["sales marketing", "sales", "management", "leadership", "teamwork"
],
"finance": [
        "accounting", "financial analysis", "excel", "budgeting", "tax", "auditing"
    ],
"general": [
        "problem solving", "time management" "adaptability", "critical thinking"
        ]
}

def extract_text_from_pdf(pdf_file):
    text = ""
    reader = PyPDF2.PdfReader(pdf_file)
    for page in reader.pages:
        text += page.extract_text() or ""
    return text.lower()


def extract_skills(text):
    found_skills = []
    for skill in SKILLS_DB:
        if skill in text:
            found_skills.append(skill)
    return list(set(found_skills))


def calculate_similarity(resume_text, job_description):
    # TF-IDF based similarity (better than CountVectorizer)
    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf = vectorizer.fit_transform([resume_text, job_description])

    score = cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0]
    return round(score * 100, 2)


def analyze_resume(pdf_file, job_description):
    text = extract_text_from_pdf(pdf_file)

    skills = extract_skills(text)

    # Extract JD skills properly
    jd_skills = [skill for skill in SKILLS_DB if skill in job_description.lower()]
    missing_skills = [skill for skill in jd_skills if skill not in skills]

    score = calculate_similarity(text, job_description)

    suggestions = []

    # Smart suggestions
    if missing_skills:
        suggestions.append("Add these missing skills: " + ", ".join(missing_skills))

    if score < 40:
        suggestions.append("Resume is poorly aligned with job description")
    elif score < 70:
        suggestions.append("Resume is moderately aligned, needs improvement")
    else:
        suggestions.append("Resume is well aligned with the job")

    if len(skills) < 5:
        suggestions.append("Add more technical skills to strengthen your resume")

    return {
        "score": score,
        "skills_found": skills,
        "missing_skills": missing_skills,
        "suggestions": suggestions
    }
