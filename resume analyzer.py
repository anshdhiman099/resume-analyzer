import PyPDF2
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Basic skill database
SKILLS_DB = [
    "python", "java", "c++", "javascript", "sql",
    "machine learning", "data analysis", "html", "css",
    "react", "angular", "node", "django", "flask",
    "git", "mongodb", "excel", "power bi"
]


def extract_text_from_pdf(pdf_file):
    """Extract text from uploaded PDF"""
    try:
        text = ""
        reader = PyPDF2.PdfReader(pdf_file)
        for page in reader.pages:
            text += page.extract_text() or ""
        return text.lower()
    except Exception:
        return ""


def extract_skills(text):
    """Simple keyword-based skill extraction"""
    found = []
    for skill in SKILLS_DB:
        if skill in text:
            found.append(skill)
    return list(set(found))


def calculate_similarity(resume_text, job_description):
    """Calculate similarity score"""
    try:
        vectorizer = CountVectorizer().fit_transform([resume_text, job_description])
        vectors = vectorizer.toarray()
        score = cosine_similarity([vectors[0]], [vectors[1]])[0][0]
        return round(score * 100, 2)
    except Exception:
        return 0


def highlight_keywords(text, keywords):
    """Highlight matched keywords"""
    for word in keywords:
        text = text.replace(word, f"**{word}**")
    return text


def analyze_resume(pdf_file, job_description):
    text = extract_text_from_pdf(pdf_file)

    if not text:
        return {"error": "Unable to read PDF"}

    skills = extract_skills(text)
    score = calculate_similarity(text, job_description)

    # Missing skills
    missing_skills = [
        skill for skill in SKILLS_DB
        if skill in job_description.lower() and skill not in skills
    ]

    # Suggestions
    suggestions = []

    if missing_skills:
        suggestions.append("Add missing skills: " + ", ".join(missing_skills))

    if score < 50:
        suggestions.append("Resume content is weak compared to job description")

    if len(skills) < 5:
        suggestions.append("Add more technical skills")

    # ATS-style feedback
    ats_feedback = []
    if score > 75:
        ats_feedback.append("Strong match for job role")
    elif score > 50:
        ats_feedback.append("Moderate match, needs improvement")
    else:
        ats_feedback.append("Low match, optimize resume")

    return {
        "score": score,
        "skills_found": skills,
        "missing_skills": missing_skills,
        "suggestions": suggestions,
        "ats_feedback": ats_feedback,
        "highlighted_text": highlight_keywords(text[:1000], skills)
    }