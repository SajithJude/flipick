import streamlit as st
import re


def app():
    # Create a text area input for the XML string
    xml_string = st.text_area("Enter XML String")
    
    if st.button("Fetch content"):

        # Extract all topics and their contents
        topics = re.findall("<Topic>(.*?)</Topic>", xml_string)
        topic_contents = re.findall("<Topic_Contents>(.*?)</Topic_Contents>", xml_string)

        # Iterate over each topic and create an expander for it
        for i, topic in enumerate(topics):
            with st.expander(f"Topic {i+1}: {topic}"):
                st.write("Topic Contents:", topic_contents[i])

                # Extract all subtopics and their contents for this topic
                sub_topics = re.findall(f"<sub_Topic>.*?<Name>{topic}</Name>.*?</sub_Topic>", xml_string, re.DOTALL)
                sub_topic_contents = re.findall(f"<sub_Topic_Contents>.*?<Name>{topic}</Name>.*?</sub_Topic_Contents>", xml_string, re.DOTALL)

                # Iterate over each subtopic and create an expander for it
                for j, sub_topic in enumerate(sub_topics):
                    sub_topic_name = re.findall("<sub_Topic_name>(.*?)</sub_Topic_name>", sub_topic)[0]
                    sub_topic_name_contents = re.findall("<sub_Topic_name_Contents>(.*?)</sub_Topic_name_Contents>", sub_topic)[0]
                    with st.expander(f"Sub Topic {j+1}: {sub_topic_name}"):
                        st.write("Sub Topic Contents:", sub_topic_contents[j])
                        st.write("Sub Topic Name Contents:", sub_topic_name_contents)


app()