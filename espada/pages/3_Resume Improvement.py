import streamlit as st
import docx
import pdfplumber
from module.text_generation import call_groq_llama

st.title("ATS Compatibility Feedback")

api_key = "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"

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
    return text

if st.button("Analyze Resume"):
    if resume_file and job_description.strip():
        resume_text = extract_resume_text(resume_file)
        prompt = f"""
        Analyze the following resume for ATS compatibility based on the given job description.
        Provide detailed feedback on missing keywords, formatting, and improvements.
        
        Job Description:
        {job_description}

        Resume:
        {resume_text}. And dont add Revised Version.
        """
        feedback = call_groq_llama(prompt, api_key=api_key, max_tokens=500, top_p=0.95, temperature=0.5)
        st.subheader("ATS Feedback")
        st.write(feedback)
    else:
        st.error("Please upload a resume and paste a job description.")
