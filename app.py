import streamlit as st
from resume_analyzer import analyze_resume

st.title("AI Resume Analyzer")

uploaded_file = st.file_uploader("Upload Resume", type=["pdf"])
job_description = st.text_area("Enter Job Description")

if st.button("Analyze"):
    if uploaded_file and job_description:
        result = analyze_resume(uploaded_file, job_description)

        st.write("Score:", result["score"])
        st.write("Skills:", result["skills_found"])
        st.write("Missing Skills:", result["missing_skills"])

        st.write("Suggestions:")
        for s in result["suggestions"]:
            st.write("-", s)
    else:
        st.warning("Please provide both inputs")