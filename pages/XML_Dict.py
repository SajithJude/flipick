import streamlit as st
import re

def display_tree(node):
    # Display the node name
    node_name = re.search(r'<Topic\s+name="([^"]+)">', node).group(1)
    st.write(f"## {node_name}")
    
    # Display the topic contents
    topic_contents = re.search(r'<Topic_Contents>(.+?)</Topic_Contents>', node, re.DOTALL).group(1)
    st.write(topic_contents.strip())
    
    # Display the subtopics if any
    subtopics = re.findall(r'<Sub_Topic\s+name="([^"]+)">(.+?)</Sub_Topic>', node, re.DOTALL)
    if subtopics:
        for subtopic in subtopics:
            # Display the subtopic name and contents
            st.write(f"### {subtopic[0]}")
            st.write(subtopic[1].strip())
            
            # Display the sub-subtopics if any
            subsubtopics = re.findall(r'<Sub_Topic\s+name="([^"]+)">(.+?)</Sub_Topic>', subtopic[1], re.DOTALL)
            if subsubtopics:
                for subsubtopic in subsubtopics:
                    # Display the sub-subtopic name and contents
                    st.write(f"#### {subsubtopic[0]}")
                    st.write(subsubtopic[1].strip())
                    # Recursive call to display any further sub-subtopics
                    display_tree(subsubtopic[1])

# Define the Streamlit app
def app():
    # Create a text area input for the XML string
    xml_string = st.text_area("Enter XML String")
    
    # Display the tree if the user clicks the button
    if st.button("Display Tree"):
        # Display the root node and its contents
        root_node = re.search(r'<Page>(.+)</Page>', xml_string, re.DOTALL).group(1)
        display_tree(root_node)



app()