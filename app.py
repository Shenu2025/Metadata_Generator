# app.py

import streamlit as st
import tempfile
import os
from metadata_utils import extract_text, generate_metadata

st.set_page_config(page_title="Metadata Generator", layout="centered")
st.title(" Automated Metadata Generator")

uploaded_file = st.file_uploader("Upload a document (PDF, DOCX, TXT)", type=["pdf", "docx", "txt"])

if uploaded_file is not None:
    if uploaded_file.size > 5_000_000:
        st.error("File too large. Please upload a document under 5MB.")
        st.stop()

    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name

    try:
        ext = os.path.splitext(uploaded_file.name)[1].lower()
        with st.spinner(" Extracting and analyzing..."):
            text = extract_text(tmp_path, ext)
            metadata = generate_metadata(text)
        st.success(" Metadata generated!")

        st.subheader(" Metadata:")
        st.json(metadata)

    except Exception as e:
        st.error(f" Error: {str(e)}")
