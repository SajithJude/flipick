import streamlit as st
import openai
import os
import fitz
import base64
import json


openai.api_key = os.getenv("API_KEY")
# st.title("Flipick XML generator GPT-4")
st.set_page_config(
    page_title="Generate XML Content",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Define default values
default_xml_structure = """<Course>
            <Topics>
                <Objectives>
                    <Objective_name></Objective_name>
                </Objectives>
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
If Objectives are present add Objective_names as bullet points, if not Dont include Objectives in the output
For example, 1.5-2 would be a sub-topic 
Include the Level Numbers in the XML exactly as in the original content
Sub_topic_Contents should  not be empty or concise
"""
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

col1, col2 = st.columns(2)


# Create expandable container
with col1.expander("Structure Configurations"):
    # Add input fields with default values
    xml_structure = st.text_area("XML Structure", default_xml_structure, height=430, )
    xml_conversion_instructions = st.text_area("XML Conversion Instructions", default_xml_conversion_instructions,height=280)

    # Save button to save input values to session state
    if st.button("Save"):
        st.session_state.xml_structure = xml_structure
        st.session_state.xml_conversion_instructions = xml_conversion_instructions


# Upload PDF file


if uploaded_file is not None:
    pdf_doc = fitz.open(stream=uploaded_file.getvalue(), filetype="pdf")
    
    with col2.expander("Pdf data"):
        # Add a multi-select field to get the page numbers from the user
        page_numbers = st.multiselect("Select page numbers", options=range(1, len(pdf_doc) + 1), default=[1])
        
        # Extract text from the selected page numbers
        content = ""
        for page_number in page_numbers:
            page = pdf_doc[page_number - 1] # page numbers are 0-indexed in PyMuPDF
            content += page.get_text()
        
        st.text(content)
        st.session_state.content = content

butn = col2.button("Generate XML")
if butn:
    with st.expander("XML data"):
        Input_content = st.session_state.content 
        xml_struct = st.session_state.xml_structure 
        xml_instructions = st.session_state.xml_conversion_instructions 
        inputPrompt = " Convert the following pdf contents :" + Input_content + " As it is with the Level Numbers into the following XML Structure : " + xml_struct + " while following these instructions : " + xml_instructions
        response = openai.Completion.create(
                                                model="text-davinci-003",
                                                prompt=inputPrompt,
                                                temperature=0.56,
                                                max_tokens=1000,
                                                top_p=1,
                                                frequency_penalty=0.35,
                                                presence_penalty=0
                                            )
        step1Out = response.choices[0].text
        st.code(step1Out)
        data = {
        "prompt": Input_content,
        "completion": step1Out
        }
        
        # Generate download button that saves data as a JSON file
        json_data = json.dumps(data, indent=4)
        b64 = base64.b64encode(json_data.encode()).decode()
        href = f'<a href="data:file/json;base64,{b64}" download="output.json">Download JSON File</a>'
        st.markdown(href, unsafe_allow_html=True)

