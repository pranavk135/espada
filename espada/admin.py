import streamlit as st
import sqlite3

# Connect to DB
conn = sqlite3.connect("jobs.db", check_same_thread=False)
c = conn.cursor()

# Create tables if not exist
c.execute("""CREATE TABLE IF NOT EXISTS company (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT)""")
c.execute("""CREATE TABLE IF NOT EXISTS job (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                labels TEXT,
                company_id INTEGER,
                FOREIGN KEY(company_id) REFERENCES company(id))""")
conn.commit()

st.title("Admin Portal - Add Companies and Job Roles")

# Admin login state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.subheader("Admin Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username == "admin" and password == "password123":
            st.session_state.logged_in = True
            st.experimental_rerun()
        else:
            st.error("Invalid username or password")
else:
    st.subheader("Add Company")
    with st.form("add_company_form"):
        company_name = st.text_input("Company Name")
        company_desc = st.text_area("Description")
        submit_company = st.form_submit_button("Add Company")
        if submit_company:
            if company_name.strip():
                c.execute("INSERT INTO company (name, description) VALUES (?, ?)", (company_name, company_desc))
                conn.commit()
                st.success(f"Company '{company_name}' added!")
            else:
                st.error("Company name cannot be empty")

    st.subheader("Add Job Role")
    c.execute("SELECT id, name FROM company")
    companies = c.fetchall()
    if companies:
        with st.form("add_job_form"):
            company_dict = {f"{name} (id:{_id})": _id for _id, name in companies}
            chosen = st.selectbox("Select Company", list(company_dict.keys()))
            job_title = st.text_input("Job Title")
            job_desc = st.text_area("Job Description")
            job_labl = st.text_input("Job Labels (comma separated)")
            submit_job = st.form_submit_button("Add Job")
            if submit_job:
                if job_title.strip():
                    cid = company_dict[chosen]
                    c.execute("INSERT INTO job (title, description, label, company_id) VALUES (?, ?, ?, ?)", (job_title, job_desc, job_labl, cid))
                    conn.commit()
                    st.success(f"Job '{job_title}' added for {chosen}")
                else:
                    st.error("Job title cannot be empty")
    else:
        st.warning("Add a company first to add jobs.")

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.experimental_rerun()