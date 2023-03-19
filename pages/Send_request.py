import streamlit as st
import openai
import os


openai.api_key = os.getenv("API_KEY")

Input_content = st.session_state.content 
st.write(Input_content)