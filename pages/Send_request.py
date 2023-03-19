import streamlit as st
import openai
import os


openai.api_key = os.getenv("API_KEY")

Input_content = st.session_state.content 

xml_str = """
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












inputPrompt = " Remove the artifacts from the following pdf content, and write the content as per original without the artifacts :" + Input_content 
st.write(inputPrompt)

response = openai.Completion.create(
        model="text-davinci-003",
        prompt=inputPrompt,
        temperature=0.56,
        max_tokens=2066,
        top_p=1,
        frequency_penalty=0.35,
        presence_penalty=0
    )
step1Out = response.choices[0].text

st.code(step1Out)