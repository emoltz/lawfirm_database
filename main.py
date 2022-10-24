import psycopg2
import requests
import streamlit as st
from streamlit_lottie import st_lottie

st.set_page_config(page_title="Test", page_icon=":smile:", layout='wide')


def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


lottie_coding = load_lottieurl("https://assets3.lottiefiles.com/packages/lf20_w51pcehl.json")

with st.container():
    st.subheader("Hi, I am Ethan :wave:")
    st.title("This is a title")
    st.write("I am passionate about stuff")

    st.markdown("## This is a markdown header")

with st.container():
    st.write("---")
    left_column, right_column = st.columns(2)
    with left_column:
        st.write("Left column")
    with right_column:
        st.write("Right column")
        st_lottie(lottie_coding)
