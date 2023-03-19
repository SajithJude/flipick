import streamlit as st
import openai
import os


openai.api_key = os.getenv("API_KEY")

Input_content = st.session_state.content 
st.write(len(Input_content))

def trim_string(input_string):
    tokens = input_string.split()[:1000]
    return ' '.join(tokens)

# example usage
output_string = trim_string(Input_content)
# print(output_string)

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












inputPrompt = " Convert the following pdf contents :" + output_string + "  Into the following XML structure : " + xml_str + "  Only content with the following numbers should be tagged as follows :1.1 and same levels to Topic, 1.1.1 and same levels to Sub-Topic, 1.1-1 and same levels to Sub-Topic, Include the Level Numbers in the XML exactly as in the original content , Sub_topic_Contents should  not be empty or concise" 
st.write(len(inputPrompt))

response = openai.Completion.create(
        model="text-davinci-003",
        prompt=inputPrompt,
        temperature=0.56,
        max_tokens=1500,
        top_p=1,
        frequency_penalty=0.35,
        presence_penalty=0
    )
step1Out = response.choices[0].text

st.write(step1Out)