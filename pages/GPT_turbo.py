import streamlit as st

iput = st.text_area("Paste here")

if st.button("submit"):

    topic_names = re.findall("<Topic_name>(.*?)</Topic_name>", iput)
