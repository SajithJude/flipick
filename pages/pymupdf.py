import fitz
import streamlit as st

def extract_text(filename):
    doc = fitz.open(filename)
    

uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    doc = fitz.open(stream=uploaded_file.getvalue(), filetype="pdf")
    for page in doc:
        page_dims = page.bound()
        content_area = page.rect
        # st.write( page.get_text("text"))
        # content_area.bottom = page_dims[1] + 10  # adjust bottom margin
        header_area = fitz.Rect(0, 0, page_dims[2], 7)
        content_area = content_area - header_area
        content = page.get_text("text", clip=content_area)
        st.write(content)
    doc.close()