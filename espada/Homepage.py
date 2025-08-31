import streamlit as st
from main import job_finder_section


def main():
    st.title("Recruitment Assistant")

    # Create two side-by-side columns (divisions)
    st.markdown("<br>", unsafe_allow_html=True)
    st.write("Welcome to the Recruitment Assistant! This tool helps you find job opportunities and optimize your resume for better chances of getting hired.")
    
    st.header("Your Job Finder Section")
    job_finder_section()

if __name__ == "__main__":
    main()
