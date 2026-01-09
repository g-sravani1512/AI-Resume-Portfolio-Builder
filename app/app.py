import os
import re
from io import BytesIO

import joblib
import streamlit as st
from docx import Document
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


# ---------------- PATH SETUP ----------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(
    BASE_DIR,
    "..",
    "model",
    "resume_classifier_model.pkl",
)

VECTORIZER_PATH = os.path.join(
    BASE_DIR,
    "..",
    "model",
    "tfidf_vectorizer.pkl",
)

model = joblib.load(MODEL_PATH)
tfidf = joblib.load(VECTORIZER_PATH)


# ---------------- UI STYLING ----------------

def load_css():
    """
    Apply custom CSS for professional UI.
    """
    st.markdown(
        """
        <style>
        body {
            background-color: #0f172a;
        }

        .main {
            background-color: #0f172a;
            color: #e5e7eb;
        }

        h1, h2, h3 {
            color: #f8fafc;
        }

        .stButton > button {
            background-color: #22c55e;
            color: white;
            border-radius: 8px;
            padding: 0.5em 1.2em;
            border: none;
            font-weight: bold;
        }

        .stButton > button:hover {
            background-color: #16a34a;
            color: white;
        }

        textarea {
            border-radius: 8px !important;
        }

        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }

        .result-box {
            background-color: #022c22;
            padding: 1rem;
            border-radius: 8px;
            color: #bbf7d0;
            font-weight: bold;
            margin-top: 1rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


# ---------------- TEXT CLEANING ----------------

def clean_text(text):
    """
    Clean input text by removing numbers and symbols,
    converting to lowercase, and removing extra spaces.
    """
    text = str(text).lower()
    text = re.sub(r"\d+", "", text)
    text = re.sub(r"[^a-zA-Z\s]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text


# ---------------- CONTENT GENERATORS ----------------

def generate_resume(role):
    """
    Generate a professional resume based on predicted role.
    """
    return (
        "PROFESSIONAL RESUME\n\n"
        f"Target Role: {role}\n\n"
        "PROFESSIONAL SUMMARY\n"
        "Motivated professional seeking a role in this domain.\n"
        "Strong foundation in technical skills and problem solving.\n\n"
        "CORE SKILLS\n"
        "- Python, Machine Learning, Streamlit, Data Analysis\n"
        "- Communication, Teamwork, Problem Solving\n"
        "- Tools: Git, Jupyter Notebook, VS Code\n\n"
        "PROJECT EXPERIENCE\n"
        "AI Resume & Portfolio Builder\n"
        "- Built a ML model to classify resumes.\n"
        "- Deployed an interactive app using Streamlit.\n\n"
        "EDUCATION\n"
        "Bachelor’s Degree in a relevant discipline\n\n"
        "CERTIFICATIONS\n"
        "- Python for Data Science\n"
        "- Machine Learning Fundamentals\n\n"
        "ADDITIONAL INFORMATION\n"
        "Strong interest in continuous learning and AI applications.\n"
    )


def generate_cover_letter(role):
    """
    Generate a professional cover letter based on predicted role.
    """
    return (
        "Dear Hiring Manager,\n\n"
        f"I am applying for the {role} position at your organization.\n"
        "I have strong technical skills and hands-on project experience.\n\n"
        "I recently built an AI Resume & Portfolio Builder using\n"
        "machine learning and Streamlit to automate document creation.\n\n"
        "I am motivated, adaptable, and eager to contribute effectively.\n\n"
        "Thank you for your time and consideration.\n\n"
        "Sincerely,\n"
        "Applicant\n"
    )


def generate_portfolio(role):
    """
    Generate a professional portfolio profile based on predicted role.
    """
    return (
        f"PORTFOLIO PROFILE – {role}\n\n"
        "ABOUT ME\n"
        "Aspiring professional with strong interest in AI and software.\n\n"
        "TECHNICAL SKILLS\n"
        "- Python, SQL\n"
        "- Machine Learning, NLP\n"
        "- Streamlit\n"
        "- Git, Jupyter, VS Code\n\n"
        "PROJECTS\n"
        "AI Resume & Portfolio Builder\n"
        "- Built a resume classification model.\n"
        "- Integrated into a Streamlit web app.\n\n"
        "CAREER OBJECTIVE\n"
        "To apply technical skills, grow professionally, and\n"
        "contribute to innovative projects.\n\n"
        "CONTACT\n"
        "Email: your_email@example.com\n"
        "GitHub: https://github.com/yourprofile\n"
        "LinkedIn: https://linkedin.com/in/yourprofile\n"
    )


# ---------------- STAGE 2: JOB CUSTOMIZATION ----------------

def customize_for_job(role, resume_input, job_desc):
    """
    Customize resume content based on the provided job description.
    """
    if job_desc.strip() == "":
        return generate_resume(role)

    return (
        "PROFESSIONAL RESUME (CUSTOMIZED)\n\n"
        f"Target Role: {role}\n\n"
        "CUSTOMIZED SUMMARY\n"
        "This resume has been tailored to align with the job description.\n\n"
        "JOB DESCRIPTION KEY REQUIREMENTS\n"
        f"{job_desc}\n\n"
        "CANDIDATE PROFILE\n"
        f"{resume_input}\n\n"
        "KEY ALIGNMENT\n"
        "- Skills aligned with job requirements.\n"
        "- Keywords optimized for ATS systems.\n"
        "- Content adjusted to match role expectations.\n"
    )


# ---------------- STAGE 1: FILE EXPORT ----------------

def generate_word_file(text):
    """
    Convert text content into a Word (.docx) file.
    """
    doc = Document()
    for line in text.split("\n"):
        doc.add_paragraph(line)

    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer


def generate_pdf_file(text):
    """
    Convert text content into a PDF file.
    """
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    _, height = A4
    y_position = height - 40

    for line in text.split("\n"):
        pdf.drawString(40, y_position, line)
        y_position -= 14

        if y_position < 40:
            pdf.showPage()
            y_position = height - 40

    pdf.save()
    buffer.seek(0)
    return buffer


# ---------------- STAGE 3: PORTFOLIO WEBSITE ----------------

def generate_portfolio_website(role, resume_input):
    """
    Generate a simple HTML portfolio website.
    """
    return (
        "<!DOCTYPE html>\n"
        "<html lang='en'>\n"
        "<head>\n"
        "  <meta charset='UTF-8'>\n"
        "  <meta name='viewport' content='width=device-width, "
        "initial-scale=1.0'>\n"
        f"  <title>Portfolio - {role}</title>\n"
        "</head>\n"
        "<body>\n\n"
        f"<h1>Portfolio – {role}</h1>\n\n"
        "<pre>\n"
        f"{resume_input}\n"
        "</pre>\n\n"
        "</body>\n"
        "</html>\n"
    )


# ---------------- STREAMLIT UI ----------------

st.set_page_config(
    page_title="AI Resume Builder",
    layout="wide",
)

load_css()

st.title("AI Resume & Portfolio Builder")
st.markdown("Build resumes, cover letters, and portfolio websites using AI.")

option = st.selectbox(
    "Choose what you want to do:",
    [
        "Predict Job Category",
        "Generate Resume",
        "Generate Cover Letter",
        "Generate Portfolio",
    ],
)

left_col, right_col = st.columns(2)

with left_col:
    st.subheader("Resume Input")
    resume_text = st.text_area(
        "Paste your resume text here",
        height=250,
    )

with right_col:
    st.subheader("Job Description (Optional)")
    job_description = st.text_area(
        "Paste job description for customization",
        height=250,
    )

st.markdown("---")

if st.button("Submit"):
    if resume_text.strip() == "":
        st.warning("Please enter resume text.")
    else:
        cleaned_input = clean_text(resume_text)
        vectorized_input = tfidf.transform([cleaned_input])
        prediction = model.predict(vectorized_input)

        predicted_role = prediction[0]

        st.markdown(
            f"<div class='result-box'>"
            f"Predicted Job Category: {predicted_role}"
            f"</div>",
            unsafe_allow_html=True,
        )

        if option == "Predict Job Category":
            st.info("Job category predicted successfully.")

        elif option == "Generate Resume":
            resume_output = customize_for_job(
                predicted_role,
                resume_text,
                job_description,
            )

            st.text_area(
                "Generated Resume",
                resume_output,
                height=350,
            )

            st.download_button(
                "Download Resume (Word)",
                generate_word_file(resume_output),
                "resume.docx",
            )

            st.download_button(
                "Download Resume (PDF)",
                generate_pdf_file(resume_output),
                "resume.pdf",
            )

        elif option == "Generate Cover Letter":
            cover_output = generate_cover_letter(predicted_role)

            st.text_area(
                "Generated Cover Letter",
                cover_output,
                height=350,
            )

            st.download_button(
                "Download Cover Letter (Word)",
                generate_word_file(cover_output),
                "cover_letter.docx",
            )

            st.download_button(
                "Download Cover Letter (PDF)",
                generate_pdf_file(cover_output),
                "cover_letter.pdf",
            )

        elif option == "Generate Portfolio":
            portfolio_output = generate_portfolio(predicted_role)

            st.text_area(
                "Generated Portfolio",
                portfolio_output,
                height=350,
            )

            st.download_button(
                "Download Portfolio (Word)",
                generate_word_file(portfolio_output),
                "portfolio.docx",
            )

            st.download_button(
                "Download Portfolio (PDF)",
                generate_pdf_file(portfolio_output),
                "portfolio.pdf",
            )

            website_html = generate_portfolio_website(
                predicted_role,
                resume_text,
            )

            st.download_button(
                "Download Portfolio Website (HTML)",
                website_html,
                "portfolio.html",
                mime="text/html",
            )
