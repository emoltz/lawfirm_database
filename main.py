import psycopg2
import streamlit as st
import pandas as pd
import psycopg2
from streamlit_option_menu import option_menu

st.set_page_config(page_title="Lawfirm Database", page_icon=":card_index:")


# local CSS
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


local_css("static/styles.css")

# CONTAINERS
header = st.container()
dataset = st.container()


# FUNCTIONS
@st.experimental_singleton
def init_connection():
    return psycopg2.connect(**st.secrets["postgres"])


conn = init_connection()


@st.experimental_memo(ttl=600)
def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()


with st.sidebar:
    selected = option_menu(
        menu_title="Menu",  # required
        options=["Home", "Lawyers", "Cases", "Clients", "Research", "etc"],  # required
        default_index=0
    )


def page_intro(selected):
    st.title(f"Welcome to the {selected} Page")
    st.text('Please use the left menu to navigate these pages')
    st.write(":heavy_minus_sign:" * 35)


if selected == "Home":
    with header:
        st.title("Welcome to Ethan & Julie Attorneys at Law")
        st.text('Please use the left menu to navigate these pages')

        # TODO make this work?
        # input_feature = st.text_input('What would you like to search for?'"")

if selected == "Clients":
    page_intro(selected)

if selected == "Lawyers":
    page_intro(selected)

if selected == "Cases":
    page_intro(selected)

if selected == "Research":
    page_intro(selected)

if selected == "etc":
    page_intro(selected)