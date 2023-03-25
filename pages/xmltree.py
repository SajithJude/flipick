import streamlit as st
import xml.etree.ElementTree as ET

# Define the XML string
xml_string = """
<Page>
    <Topics>
        <Topic>
            <Topic_name>Topic 1</Topic_name>
            <Contents>Contents 1</Contents>
            <sub_Topics>
                <sub_Topic>
                    <sub_Topic_name>Sub-Topic 1.1</sub_Topic_name>
                    <sub_Topic_Contents>Sub-Contents 1.1</sub_Topic_Contents>
                </sub_Topic>
            </sub_Topics>
        </Topic>
        <Topic>
            <Topic_name>Topic 2</Topic_name>
            <Contents>Contents 2</Contents>
            <sub_Topics>
                <sub_Topic>
                    <sub_Topic_name>Sub-Topic 2.1</sub_Topic_name>
                    <sub_Topic_Contents>Sub-Contents 2.1</sub_Topic_Contents>
                </sub_Topic>
                <sub_Topic>
                    <sub_Topic_name>Sub-Topic 2.2</sub_Topic_name>
                    <sub_Topic_Contents>Sub-Contents 2.2</sub_Topic_Contents>
                </sub_Topic>
            </sub_Topics>
        </Topic>
    </Topics>
</Page>
"""

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
            sub_topic_contents = sub_topic.find("sub_Topic_Contents").text

            with st.container(sub_topic_name):
                st.write("Contents:", sub_topic_contents)
