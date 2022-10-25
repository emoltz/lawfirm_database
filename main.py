import psycopg2
import streamlit as st

st.set_page_config(page_title="Lawfirm Database", page_icon=":card_index:")

# local CSS
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


local_css("static/styles.css")
st.write("This app is all set up!")