import streamlit as st
import openai
import os
import fitz


st.title("Flipick XML generator GPT-4")

# Upload PDF file
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

# If file was uploaded
if uploaded_file is not None:
    # Load PDF document
    pdf_doc = fitz.open(stream=uploaded_file.getvalue(), filetype="pdf")
    # Extract text from PDF pages
    text = ""
    for page in pdf_doc:
        text += page.get_text()
    # Display extracted text
    st.code(text)
