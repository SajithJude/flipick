import streamlit as st
import xmltodict

def display_tree(node):
    # Display the node name
    st.write(f"## {node['@name']}")
    
    # Display the topic contents
    st.write(node['Topic_Contents'])
    
    # Display the subtopics if any
    if 'Sub_Topics' in node:
        for subtopic in node['Sub_Topics']['Sub_Topic']:
            # Display the subtopic name and contents
            st.write(f"### {subtopic['@name']}")
            st.write(subtopic['Sub_Topic_Contents'])
            
            # Display the sub-subtopics if any
            if 'Sub_Topics' in subtopic:
                for subsubtopic in subtopic['Sub_Topics']['Sub_Topic']:
                    # Display the sub-subtopic name and contents
                    st.write(f"#### {subsubtopic['@name']}")
                    st.write(subsubtopic['Sub_Topic_Contents'])
                    # Recursive call to display any further sub-subtopics
                    display_tree(subsubtopic)

# Define the Streamlit app
def app():
    # Create a text area input for the XML string
    xml_string = st.text_area("Enter XML String")
    
    # Display the tree if the user clicks the button
    if st.button("Display Tree"):
        # Convert the XML string to a Python dictionary
        xml_dict = xmltodict.parse(xml_string)
        
        # Display the root node and its contents
        display_tree(xml_dict['Page'])
