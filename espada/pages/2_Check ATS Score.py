import streamlit as st
import os
import docx
import pdfplumber
import re

st.title("Download Your Resume & Test ATS Score")

st.markdown("<hr style='border: 1px solid #aaa'>", unsafe_allow_html=True)

st.header("Download Resume")
if "generated_file" in st.session_state:
    file_path = st.session_state["generated_file"]
    
    if os.path.exists(file_path):
        st.success("Your resume is ready to download!")
        st.download_button(
            label="Download Resume",
            data=open(file_path, "rb").read(),
            file_name="resume.docx"
        )
    else:
        st.error("Resume file not found. Please generate it first on the main page.")
else:
    st.info("Please generate the resume first on the main page.")

st.markdown("<hr style='border: 1px solid #aaa'>", unsafe_allow_html=True)

st.header("ATS Score Tester")
resume_file = st.file_uploader("Upload your resume (PDF or DOCX)", type=["docx", "pdf"])
job_description = st.text_area("Paste Job Description here")

def extract_resume_text(file):
    text = ""
    if file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        doc = docx.Document(file)
        for para in doc.paragraphs:
            text += para.text + " "
    elif file.type == "application/pdf":
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + " "
    return text.lower()

def compute_ats_score(resume_text, job_text):
    job_keywords = set(re.findall(r'\b\w+\b', job_text.lower()))
    resume_words = set(re.findall(r'\b\w+\b', resume_text.lower()))
    matched = job_keywords & resume_words
    score = int(len(matched) / len(job_keywords) * 100) if job_keywords else 0
    missing_keywords = job_keywords - resume_words
    return score, matched, missing_keywords

if st.button("Calculate ATS Score"):
    if resume_file and job_description.strip():
        resume_text = extract_resume_text(resume_file)
        score, matched, missing = compute_ats_score(resume_text, job_description)
        
        st.success(f"ATS Score: {score}%")
    else:
        st.error("Please upload a resume and paste a job description.")
