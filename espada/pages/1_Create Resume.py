import streamlit as st
from module.reusme_word_creator import generate_resume
from module.text_generation import call_groq_llama

st.set_page_config(page_title="Resume Maker", layout="wide")

api_key = "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"

if "page" not in st.session_state:
    st.session_state.page = "form"
if "resume_data" not in st.session_state:
    st.session_state.resume_data = {}
if "num_exp" not in st.session_state:
    st.session_state.num_exp = 1
if "num_proj" not in st.session_state:
    st.session_state.num_proj = 1
if "num_cert" not in st.session_state:
    st.session_state.num_cert = 1

if st.session_state.page == "form":
    st.title("Create Your ATS Friendly Resume Here !")

    col1, col2 = st.columns([1.5, 1])

    with col1:
        st.header("Personal Information")
        name = st.text_input("Full Name")
        col11, col12 = st.columns(2)
        with col11:
            email = st.text_input("Email")
        with col12:
            phone = st.text_input("Phone Number")
        location = st.text_input("Location")
        job_role = st.text_input("Job Role")

        st.header("Skills")
        skills_input = st.text_area("Enter skills separated by commas")
        skills = [s.strip() for s in skills_input.split(",") if s.strip()]

        work_experience = {}
        for i in range(st.session_state.num_exp):
            st.subheader(f"{i+1}) Experience")
            company = st.text_input(f"Company {i+1}", key=f"company_{i}")
            role = st.text_input(f"Role {i+1}", key=f"role_{i}")
            col_start, col_end = st.columns(2)
            with col_start:
                start = st.text_input(f"Start Date {i+1}", key=f"start_{i}")
            with col_end:
                end = st.text_input(f"End Date {i+1}", key=f"end_{i}")
            work_experience[f"experience_{i+1}"] = {
                "company": company, "role": role, "start": start, "end": end
            }
        if st.button("+ Add Work Experience"):
            st.session_state.num_exp += 1

        st.header("Projects")
        projects = {}
        for i in range(st.session_state.num_proj):
            st.subheader(f"{i+1}) Project")
            title = st.text_input(f"Project Title {i+1}", key=f"title_{i}")
            desc = st.text_area(f"Project Description {i+1}", key=f"proj_desc_{i}")
            projects[f"project_{i+1}"] = {"title": title, "description": desc}
        if st.button("+ Add Project"):
            st.session_state.num_proj += 1

        st.header("Certifications")
        certifications = {}
        for i in range(st.session_state.num_cert):
            st.subheader(f"{i+1}) Certification")
            col_name, col_org = st.columns([2, 2])
            with col_name:
                cert_name = st.text_input(f"Certification Name {i+1}", key=f"cert_name_{i}")
            with col_org:
                cert_org = st.text_input(f"Issuing Organization {i+1}", key=f"cert_org_{i}")
            certifications[f"certification_{i+1}"] = {"name": cert_name, "organization": cert_org}
        if st.button("+ Add Certification"):
            st.session_state.num_cert += 1

        if st.button("Generate Resume"):
            st.session_state.resume_data = {
                "name": name,
                "email": email,
                "phone": phone,
                "job_role": job_role,
                "location": location,
                "skills": skills,
                "work_experience": work_experience,
                "projects": projects,
                "certifications": certifications
            }
            st.session_state.generated_file = generate_resume(st.session_state.resume_data, api_key=api_key)
            st.session_state.page = "download"
            st.experimental_rerun()  

    with col2:
        st.header("Upload Files")
        st.markdown("""
        <style>
        .drag-drop-box {
            border: 2px dashed #aaa;
            border-radius: 8px;
            padding: 40px;
            text-align: center;
            color: #666;
            background-color: rgba(255, 255, 255, 0.0);
            font-size: 16px;
        }
        </style>
        <div class="drag-drop-box">
            Drag & Drop your files here<br>or click to upload
        </div>
        """, unsafe_allow_html=True)

        uploaded_files = st.file_uploader(
            "Upload your documents",
            type=["pdf", "docx"],
            accept_multiple_files=True
        )
        if uploaded_files:
            st.success(f"{len(uploaded_files)} file(s) uploaded successfully!")

if st.session_state.page == "download":
    st.title("Your Resume is Ready!")
    st.success("Click the button below to download your ATS-friendly resume:")

    st.download_button(
        "Download Resume",
        data=open(st.session_state.generated_file, "rb").read(),
        file_name="resume.docx"
    )

    if st.button("Back to Form"):
        st.session_state.page = "form"
        st.experimental_rerun()

    st.markdown("<hr style='border: 1px solid #aaa'>", unsafe_allow_html=True)

    st.header("ATS Score Tester")
    import docx
    import pdfplumber
    import re

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
            st.info(f"Matched Keywords ({len(matched)}): {', '.join(list(matched)[:20])}...")
            if missing:
                st.warning(f"Missing Keywords ({len(missing)}): {', '.join(list(missing)[:20])}...")
        else:
            st.error("Please upload a resume and paste a job description.")

