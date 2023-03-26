import streamlit as st
import re


def app():
    # Create a text area input for the XML string
    xml_string = st.text_area("Enter XML String")
    
    if st.button("Fetch content"):

        Topic = re.findall("<Topic>(.*?)</Topic>", xml_string)
        Topic_Contents = re.findall("<Topic_Contents>(.*?)</Topic_Contents>", xml_string)
        sub_Topic = re.findall("<sub_Topic>(.*?)</sub_Topic>", xml_string)
        sub_Topic_Contents = re.findall("<sub_Topic_Contents>(.*?)</sub_Topic_Contents>", xml_string)
        sub_Topic_name = re.findall("<sub_Topic_name>(.*?)</sub_Topic_name>", xml_string)
        sub_Topic_name_Contents = re.findall("<sub_Topic_name_Contents>(.*?)</sub_Topic_name_Contents>", xml_string)

        

app()