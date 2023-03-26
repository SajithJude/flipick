import streamlit as st
import xml.etree.ElementTree as ET
import re


def app():
    # Create a text area input for the XML string
    xml_string = st.text_area("Enter XML String")
    
    # Display the tree if the user clicks the button
    if st.button("Display Tree"):
        # Parse the XML string using ElementTree
        topic_names = re.findall("<Topic_Contents>(.*?)</Topic_Contents>", xml_string)
        sub_topic_names = re.findall("<sub_Topic_Contents>(.*?)</sub_Topic_Contents>", xml_string)

        
        # Display the root node and its contents
        st.write(topic_names)
        st.write(sub_topic_names)

app()