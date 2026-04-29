import streamlit as st
from resume_analyzer import analyze_resume, extract_text_from_pdf, ai_resume_analysis

if st.button("Analyze"):
    if uploaded_file and job_description:

        text = extract_text_from_pdf(uploaded_file)

        result = ai_resume_analysis(text, job_description)

        st.subheader("AI Analysis")
        st.write(result)
