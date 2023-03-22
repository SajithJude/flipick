import streamlit as st
import openai
import os
import base64
import json
import fitz


st.set_page_config(
    page_title="Generate XML Content with GPT Turbo",
    layout="wide",
    initial_sidebar_state="expanded",
)

openai.api_key = os.getenv("API_KEY")






uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
if uploaded_file is not None:

    pdf_doc = fitz.open(stream=uploaded_file.getvalue(), filetype="pdf")
    
    Input_content = pdf_doc.get_text()

    st.session_state.Input_content = Input_content



if st.button("Generate XML content"):

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

    prompt_request = "Insert the contents of this pdf into the specified XML structure : " + Input_content

    messages = [{"role": "system", "content":default_xml_structure }]    
    messages.append({"role": "user", "content": prompt_request})

    response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=.5,
            max_tokens=500,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
    )

    outs = response["choices"][0]["message"]['content'].strip()
    st.write(outs)
    
    # Create dictionary with prompt and completion
    data = {
        "prompt": Input_content,
        "completion": step1Out
    }
    
    # Generate download button that saves data as a JSON file
    json_data = json.dumps(data, indent=4)
    b64 = base64.b64encode(json_data.encode()).decode()
    href = f'<a href="data:file/json;base64,{b64}" download="output.json">Download JSON File</a>'
    st.markdown(href, unsafe_allow_html=True)
