import streamlit as st
import xml.etree.ElementTree as ET
import re

def display_node(node):
    # Display the node name
    try:
        node_name = node.attrib['name']
    except KeyError:
        node_name = ""
    st.write(f"## {node_name}")
    
    # Display the topic contents
    topic_contents = node.find('Topic_Contents').text.strip()
    st.write(topic_contents)
    
    # Display the subtopics if any
    subtopics = node.findall('Sub_Topics/Sub_Topic')
    if subtopics:
        for subtopic in subtopics:
            # Display the subtopic name and contents
            try:
                subtopic_name = subtopic.attrib['name']
            except KeyError:
                subtopic_name = ""
            st.write(f"### {subtopic_name}")
            subtopic_contents = subtopic.find('Sub_Topic_Contents').text.strip()
            st.write(subtopic_contents)
            
            # Display the sub-subtopics if any
            subsubtopics = subtopic.findall('Sub_Topics/Sub_Topic')
            if subsubtopics:
                for subsubtopic in subsubtopics:
                    # Display the sub-subtopic name and contents
                    try:
                        subsubtopic_name = subsubtopic.attrib['name']
                    except KeyError:
                        subsubtopic_name = ""
                    st.write(f"#### {subsubtopic_name}")
                    subsubtopic_contents = subsubtopic.find('Sub_Topic_Contents').text.strip()
                    st.write(subsubtopic_contents)
                    # Recursive call to display any further sub-subtopics
                    display_node(subsubtopic)

def app():
    # Create a text area input for the XML string
    xml_string = st.text_area("Enter XML String")
    
    # Display the tree if the user clicks the button
    if st.button("Display Tree"):
        # Parse the XML string using ElementTree
        root = ET.fromstring(xml_string)
        
        # Display the root node and its contents
        display_node(root)
app()