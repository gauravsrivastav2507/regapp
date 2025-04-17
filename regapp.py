import streamlit as st
import os
import re
import PyPDF2
import docx
import spacy

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# ----------- File Readers -----------
def read_txt(file):
    return file.read().decode('utf-8')

def read_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def read_docx(file):
    doc = docx.Document(file)
    return '\n'.join([para.text for para in doc.paragraphs])

def extract_text(uploaded_file):
    ext = os.path.splitext(uploaded_file.name)[1].lower()
    if ext == '.pdf':
        return read_pdf(uploaded_file)
    elif ext == '.docx':
        return read_docx(uploaded_file)
    elif ext == '.txt':
        return read_txt(uploaded_file)
    else:
        return None

# ----------- Regex & NLP Extractors -----------
def extract_with_regex(text):
    phone = re.findall(r"\+91[-\s]?\d{10}", text)
    email = re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)
    date = re.findall(r"\d{1,2}[a-z]{2} [A-Za-z]+ \d{4}", text)
    return phone, email, date

def extract_entities(text):
    doc = nlp(text)
    return [(ent.text, ent.label_) for ent in doc.ents]

# ----------- Streamlit UI -----------
st.set_page_config(page_title="Regex & NLP Extractor", layout="wide")

st.title("📄 File Analyzer: Extract Email, Phone, Dates & Entities")
uploaded_file = st.file_uploader("Upload a .txt, .pdf, or .docx file", type=["txt", "pdf", "docx"])

if uploaded_file:
    st.success("File uploaded successfully!")
    text = extract_text(uploaded_file)

    if text:
        st.subheader("📑 Extracted Text")
        st.text_area("Raw Text", text, height=200)

        phones, emails, dates = extract_with_regex(text)
        entities = extract_entities(text)

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("📞 Phone Numbers")
            st.write(phones)

            st.subheader("📧 Emails")
            st.write(emails)

            st.subheader("📅 Dates")
            st.write(dates)

        with col2:
            st.subheader("🔍 Named Entities (NLP)")
            for entity, label in entities:
                st.markdown(f"**{label}**: {entity}")
    else:
        st.error("Unsupported file format.")
