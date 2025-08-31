import sqlite3
import streamlit as st

# 🔹 Shared DB init function
def init_db():
    conn = sqlite3.connect("jobs.db", check_same_thread=False)
    c = conn.cursor()

    # Ensure all tables exist
    c.execute("""CREATE TABLE IF NOT EXISTS company (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    description TEXT)""")

    c.execute("""CREATE TABLE IF NOT EXISTS labels (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL)""")

    c.execute("""CREATE TABLE IF NOT EXISTS job (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    description TEXT,
                    label_id INTEGER,
                    company_id INTEGER,
                    FOREIGN KEY(company_id) REFERENCES company(id),
                    FOREIGN KEY(label_id) REFERENCES labels(id))""")

    conn.commit()
    return conn, c


# 🔹 Your Job Finder Section
def job_finder_section():
    conn, c = init_db()   # ✅ always initializes DB

    st.title("Job Finder Portal")
    st.subheader("Available Companies and Job Roles")

    # Fetch labels from DB
    c.execute("SELECT id, name FROM labels")
    labels = c.fetchall()
    label_dict = {name: lid for lid, name in labels}

    selected_label = st.selectbox("Select a skill label", ["All"] + list(label_dict.keys()))

    # Fetch companies
    c.execute("SELECT id, name, description FROM company")
    all_companies = c.fetchall()

    if not all_companies:
        st.info("No companies or jobs available yet. Please check back later.")
    else:
        for cid, cname, cdesc in all_companies:
            with st.expander(f"🏢 {cname}"):
                st.write(cdesc if cdesc else "No description.")

                # Filter jobs by label
                if selected_label == "All":
                    c.execute("""
                        SELECT job.id, job.title, job.description, labels.name
                        FROM job 
                        LEFT JOIN labels ON job.label_id = labels.id
                        WHERE job.company_id=?
                    """, (cid,))
                else:
                    c.execute("""
                        SELECT job.id, job.title, job.description, labels.name
                        FROM job 
                        LEFT JOIN labels ON job.label_id = labels.id
                        WHERE job.company_id=? AND job.label_id=?
                    """, (cid, label_dict[selected_label]))

                jobs = c.fetchall()

                if jobs:
                    for jid, title, desc, label in jobs:
                        st.markdown(f"**{title}**  _(Label: {label})_")
                        st.write(desc if desc else "No description.")
                        if st.button(f"Apply for {title}", key=f"apply_{jid}"):
                            st.success(f"✅ Application for '{title}' submitted!")
                else:
                    st.write("No jobs available for this label.")
