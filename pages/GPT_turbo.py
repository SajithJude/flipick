import streamlit as st
import re

iput = st.text_area("Paste here")

if st.button("submit"):

    topic_names = re.findall("<Topic_name>(.*?)</Topic_name>", iput)
    st.write(topic_names)
