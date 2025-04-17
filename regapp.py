import streamlit as st
import re
from PyPDF2 import PdfReader
import docx

def extract_text(file):
    if file.name.endswith(".pdf"):
        reader = PdfReader(file)
        return "\n".join([page.extract_text() or "" for page in reader.pages])
    elif file.name.endswith(".docx"):
        doc = docx.Document(file)
        return "\n".join([para.text for para in doc.paragraphs])
    elif file.name.endswith(".txt"):
        return file.read().decode("utf-8")
    else:
        return ""

def extract_info(text):
    emails = re.findall(r"\S+@\S+", text)
    phones = re.findall(r"\b\d{10}\b", text)
    return emails, phones

st.title("Document Information Extractor (PDF, Word, TXT)")

uploaded_file = st.file_uploader("Upload file", type=["pdf", "docx", "txt"])
if uploaded_file:
    text = extract_text(uploaded_file)
    st.subheader("Extracted Text:")
    st.text_area("Text", text, height=200)

    st.subheader("Extracted Info:")
    emails, phones = extract_info(text)
    st.write("📧 Emails:", emails)
    st.write("📞 Phones:", phones)
