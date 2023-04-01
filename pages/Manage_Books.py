import streamlit as st
import openai
import os
import fitz
import base64
import json

CONTENT_DIR = "content"

def display_pdf(pdf_file):
    with open(os.path.join(CONTENT_DIR, pdf_file), "rb") as f:
        pdf_reader = PyPDF2.PdfFileReader(f)
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            with st.expander(f"Page {page_num+1}"):
                st.write(page.extractText())

# Define a function to delete a PDF file
def delete_file(file_name):
    pdf_path = os.path.join(CONTENT_DIR, file_name)
    if os.path.exists(pdf_path):
        os.remove(pdf_path)
        st.success(f"File {file_name} deleted successfully!")
    else:
        st.error(f"File {file_name} not found!")




def main():
    
    
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

    if uploaded_file is not None:
        with open(os.path.join("content", uploaded_file.name), "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success("File saved successfully")

    files =  os.listdir(CONTENT_DIR)
    
    # Display the list of PDF files
    if len(files) > 0:
        st.write("Available PDF files:")
        for file_name in files:
            col1, col2, col3 = st.columns((4, 1, 1))
            col1.caption(file_name)
            col2.button("View", key=file_name, on_click=display_pdf, args=(file_name,))
            col3.button("Delete", key=file_name, on_click=delete_file, args=(file_name,))
    else:
        st.write("No PDF files found in the content directory.")

if __name__ == "__main__":
    main()