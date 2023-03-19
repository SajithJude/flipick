import streamlit as st
import openai
import os
import fitz

openai.api_key = os.getenv("API_KEY")
st.title("Flipick XML generator GPT-4")


# Define default values
default_xml_structure = """<Course>
            <Topics>
                <Topic>
                    <Topic_name></Topic_name>			
                    <Contents>
                    </Contents>
                    <sub_Topics>
                        <sub_Topic>
                            <sub_Topic_name></sub_Topic_name>
                            <sub_Topic_Contents>
                            </sub_Topic_Contents>
                        </sub_Topic>
                    </sub_Topics>
                </Topic>
            </Topics>
</Course>"""
default_xml_conversion_instructions =  """Only content with the following numbers should be tagged as follows
1.1 and same levels to Topic
1.1.1 and same levels to Sub-Topic
1.1-1 and same levels to Sub-Topic
For example, 1.5-2 would be a sub-topic 
Include the Level Numbers in the XML exactly as in the original content
Sub_topic_Contents should  not be empty or concise
"""
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

col1, col2 = st.columns(2)


# Create expandable container
with col1.expander("Structure Configurations"):
    # Add input fields with default values
    xml_structure = st.text_area("XML Structure", default_xml_structure)
    xml_conversion_instructions = st.text_area("XML Conversion Instructions", default_xml_conversion_instructions)

    # Save button to save input values to session state
    if st.button("Save"):
        st.session_state.xml_structure = xml_structure
        st.session_state.xml_conversion_instructions = xml_conversion_instructions


# Upload PDF file


if uploaded_file is not None:
    pdf_doc = fitz.open(stream=uploaded_file.getvalue(), filetype="pdf")
    

    # Add a multi-select field to get the page numbers from the user
    page_numbers = col2.multiselect("Select page numbers", options=range(1, len(pdf_doc) + 1), default=[1])
    
    # Extract text from the selected page numbers
    content = ""
    for page_number in page_numbers:
        page = pdf_doc[page_number - 1] # page numbers are 0-indexed in PyMuPDF
        content += page.get_text("text")
    
    col2.text(content)
    st.session_state.content = content