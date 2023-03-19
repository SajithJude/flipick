import streamlit as st
import openai
import os


openai.api_key = os.getenv("API_KEY")

Input_content = st.session_state.content 
xml_struct = st.session_state.xml_structure 
xml_instructions = st.session_state.xml_conversion_instructions 

inputPrompt = " Convert the following pdf contents :" + Input_content + " As it is with the Level Numbers into the following XML Structure : " + xml_struct + " while following these instructions : " + xml_instructions
st.write(len(inputPrompt))
st.write(inputPrompt)

if st.submit("Generate XML content"):
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