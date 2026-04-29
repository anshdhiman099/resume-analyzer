import streamlit as st
from resume_analyzer import (
    extract_text_from_pdf,
    analyze_resume_basic,
    ai_resume_analysis
)

# ✅ Page config
st.set_page_config(page_title="AI Resume Analyzer", layout="centered")

st.title("📄 AI Resume Analyzer")
st.write("Upload your resume and compare it with a job description.")

# ✅ File uploader
uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

# ✅ Job description input
job_description = st.text_area("Paste Job Description")

# ✅ Button
if st.button("Analyze Resume"):

    if uploaded_file is None:
        st.error("Please upload a resume.")
    
    elif not job_description.strip():
        st.error("Please enter a job description.")
    
    else:
        # ✅ Extract resume text
        with st.spinner("Reading resume..."):
            resume_text = extract_text_from_pdf(uploaded_file)

        # ✅ Basic Analysis
        with st.spinner("Analyzing (ATS Score)..."):
            result = analyze_resume_basic(resume_text, job_description)

        st.subheader("📊 ATS Score")
        st.success(f"{result['score']} % match")

        # ✅ Matched Skills
        st.subheader("✅ Matched Skills")
        if result["matched_skills"]:
            st.write(", ".join(result["matched_skills"]))
        else:
            st.write("No matching skills found.")

        # ✅ Missing Skills
        st.subheader("❌ Missing Skills")
        if result["missing_skills"]:
            st.write(", ".join(result["missing_skills"]))
        else:
            st.write("No missing skills. Good match!")

        # ✅ AI Analysis
        st.subheader("🤖 AI Feedback")
        with st.spinner("Generating AI insights..."):
            ai_result = ai_resume_analysis(resume_text, job_description)

        st.write(ai_result)
