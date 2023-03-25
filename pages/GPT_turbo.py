import streamlit as st
import re

iput = st.text_area("Paste here")

if st.button("submit"):

    topic_names = re.findall("<Topic_name>(.*?)</Topic_name>", iput)
    st.write(topic_names)



# Parse the XML string to extract the possible values for the dropdowns
topic_names = re.findall("<Topic_name>(.*?)</Topic_name>", iput)
sub_topic_names = re.findall("<sub_Topic_name>(.*?)</sub_Topic_name>", iput)

# Create a dropdown to select the tag name
tag_names = ["Topic_name", "sub_Topic_name"]
selected_tag_name = st.selectbox("Select a tag name", tag_names)

# Create a dropdown to select the value of the selected tag
if selected_tag_name == "Topic_name":
    selected_value = st.selectbox("Select a topic name", topic_names)
else:
    selected_value = st.selectbox("Select a sub-topic name", sub_topic_names)

# Use regex to extract the tag contents based on the selected tag name and value
regex_pattern = f"<{selected_tag_name}>{selected_value}</{selected_tag_name}>"
tag_contents = re.findall(f"{regex_pattern}.*?</{selected_tag_name}>", iput, re.DOTALL)

# Display the extracted tag contents
if tag_contents:
    st.write(tag_contents[0])
else:
    st.write("No matching tag found.")