import streamlit as st

st.set_page_config(page_title="Test Nav", layout="wide")

# Simple navigation test
pages = ["Dashboard", "Liability", "Simulation", "AI", "Analytics", "Reports"] 
page = st.sidebar.selectbox("Test Navigation", pages)

st.title(f"Current Page: {page}")
st.write("Navigation working properly!")