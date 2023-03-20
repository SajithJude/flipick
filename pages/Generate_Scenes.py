import streamlit as st
import openai
import os
import base64
import json

st.set_page_config(
    page_title="Generate XML Content",
    layout="wide",
    initial_sidebar_state="expanded",
)

openai.api_key = os.getenv("API_KEY")

Input_content = st.session_state.content 
xml_struct = st.session_state.xml_structure 
xml_instructions = st.session_state.xml_conversion_instructions 

inputPrompt = " Convert the following pdf contents :" + Input_content + " As it is with the Level Numbers into the following XML Structure : " + xml_struct + " while following these instructions : " + xml_instructions
st.write(len(inputPrompt))
st.write(inputPrompt)

if st.button("Generate XML content"):
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
