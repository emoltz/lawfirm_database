import psycopg2
import streamlit as st

st.set_page_config(page_title="Test", page_icon=":smile:", layout='wide')

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