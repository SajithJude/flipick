import streamlit as st
import openai
import os
import fitz

openai.api_key = os.getenv("API_KEY")
st.title("Flipick XML generator GPT-4")


# Define default values
default_xml_structure = "<Course>\n\t<Topics>\n\t\t<Topic>\n\t\t\t<Topic_name></Topic_name>\n\t\t\t<Contents></Contents>\n\t\t\t<sub_Topics>\n\t\t\t\t<sub_Topic>\n\t\t\t\t\t<sub_Topic_name></sub_Topic_name>\n\t\t\t\t\t<sub_Topic_Contents></sub_Topic_Contents>\n\t\t\t\t</sub_Topic>\n\t\t\t</sub_Topics>\n\t\t</Topic>\n\t</Topics>\n</Course>"
default_xml_conversion_instructions = "Only content with the following numbers should be tagged as follows\n1.1 and same levels to Topic\n1.1.1 and same levels to Sub-Topic\n1.1-1 and same levels to Sub-Topic\nFor example, 1.5-2 would be a sub-topic\nInclude the Level Numbers in the XML exactly as in the original content\nSub_topic_Contents should not be empty or concise"
default_scene_structure = "Chapter Name\nTopic Name\nScene number\nScene Template\nScene Title\nScene bodycopy in concise format suitable for eLearning\nScene Keywords, top 5\nScene Voice Over Copy\nSuggest if Avatar should be used"
default_scene_instructions = "Provide exactly 3 bullet points when Scene Template 'Bullet Points' is suggested for Scene bodycopy\nProvide exactly 5 points when Scene Template 'Agenda' is suggested\nProvide a maximum of 40 to 50 words when the 'Paragraph Layout' template is suggested\nProvide the output in XML format\nIf number of scenes are more than 10, please split them into modules. Each module should have a maximum of 10 scenes"

# Create expandable container
with st.expander("Profile Configurations"):
    # Add input fields with default values
    xml_structure = st.code("XML Structure", default_xml_structure)
    xml_conversion_instructions = st.text_area("XML Conversion Instructions", default_xml_conversion_instructions)
    scene_structure = st.text_area("Scene Structure", default_scene_structure)
    scene_instructions = st.text_area("Scene Instructions", default_scene_instructions)
    
    # Save button to save input values to session state
    if st.button("Save"):
        st.session_state.xml_structure = xml_structure
        st.session_state.xml_conversion_instructions = xml_conversion_instructions
        st.session_state.scene_structure = scene_structure
        st.session_state.scene_instructions = scene_instructions

# Display saved values from session state
if "xml_structure" in st.session_state:
    st.write("XML Structure:", st.session_state.xml_structure)
if "xml_conversion_instructions" in st.session_state:
    st.write("XML Conversion Instructions:", st.session_state.xml_conversion_instructions)
if "scene_structure" in st.session_state:
    st.write("Scene Structure:", st.session_state.scene_structure)
if "scene_instructions" in st.session_state:
    st.write("Scene Instructions:", st.session_state.scene_instructions)

# Upload PDF file
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

# If file was uploaded
if uploaded_file is not None:
    # Load PDF document
    pdf_doc = fitz.open(stream=uploaded_file.getvalue(), filetype="pdf")
    # Extract text from PDF pages
    content = ""
    for page in pdf_doc:
        content += page.get_text()
    # Display extracted text
    st.code(content)

    response = openai.Edit.create(
        model="text-davinci-003",
        input=content,
        instruction = "Remove the artifacts from the input and write the content as per original without the artifacts"
    )
    step_1_out = response.choices[0].text
    st.code(step_1_out)



