import streamlit as st
import openai
import os
import fitz

openai.api_key = os.getenv("API_KEY")
st.title("Flipick XML generator GPT-4")


# Define default values
default_xml_structure = """
                        <Course>
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
                        </Course>
                        """
default_xml_conversion_instructions =   """
                                            Only content with the following numbers should be tagged as follows
                                            1.1 and same levels to Topic
                                            1.1.1 and same levels to Sub-Topic
                                            1.1-1 and same levels to Sub-Topic
                                            For example, 1.5-2 would be a sub-topic 
                                            Include the Level Numbers in the XML exactly as in the original content
                                            Sub_topic_Contents should  not be empty or concise
                                        """
# Create expandable container
with st.expander("Profile Configurations"):
    # Add input fields with default values
    xml_structure = st.text_area("XML Structure", default_xml_structure)
    xml_conversion_instructions = st.text_area("XML Conversion Instructions", default_xml_conversion_instructions)

    # Save button to save input values to session state
    if st.button("Save"):
        st.session_state.xml_structure = xml_structure
        st.session_state.xml_conversion_instructions = xml_conversion_instructions

# Display saved values from session state
if "xml_structure" in st.session_state:
    st.write("XML Structure:", st.session_state.xml_structure)
if "xml_conversion_instructions" in st.session_state:
    st.write("XML Conversion Instructions:", st.session_state.xml_conversion_instructions)

# Upload PDF file

uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    pdf_doc = fitz.open(stream=uploaded_file.getvalue(), filetype="pdf")
    
    # Add a number input field to get the page number from the user
    page_number = st.number_input("Enter page number", min_value=1, max_value=len(pdf_doc), value=1, step=1)
    
    # Extract text from the selected page number
    page = pdf_doc[page_number - 1] # page numbers are 0-indexed in PyMuPDF
    content = page.get_text("text")
    
    st.text(content)
    st.session_state.content = content
