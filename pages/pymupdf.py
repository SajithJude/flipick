import fitz
import streamlit as st

def extract_text(filename):
    doc = fitz.open(filename)
    

uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    pdf_doc = fitz.open(stream=uploaded_file.getvalue(), filetype="pdf")
    for page in pdf_doc:
        page_dims = page.MediaBox
        content_area = page.cropBox
        content_area.bottom = page_dims.bottom + 10  # adjust bottom margin
        content = page.get_text("text", clip=content_area)
        st.write(content)
    pdf_doc.close()
    