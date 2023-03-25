import streamlit as st
import xml.etree.ElementTree as ET

# Define the XML string
xml_string = st.text_area("paste text here")

# Parse the XML string using ElementTree
root = ET.fromstring(xml_string)

# Display the topics, topic names, contents, sub-topics, sub-topic names, and sub-topic contents using Streamlit
st.title("XML Viewer")

for topic in root.findall("./Topics/Topic"):
    topic_name = topic.find("Topic_name").text
    contents = topic.find("Contents").text

    with st.beta_expander(topic_name):
        st.write("Contents:", contents)

        for sub_topic in topic.findall("./sub_Topics/sub_Topic"):
            sub_topic_name = sub_topic.find("sub_Topic_name").text
            for sub_topic_content in sub_topic_name:
                sub_topic_contents = sub_topic.find("sub_Topic_Contents").text

                with st.container():
                    st.write(sub_topic_name)
                    st.write("Contents:", sub_topic_contents)
