import streamlit as st
import pandas as pd
import psycopg2

header = st.container()
dataset = st.container()
features = st.container()
model_training = st.container()


@st.experimental_singleton
def init_connection():
    return psycopg2.connect(**st.secrets["postgres"])


conn = init_connection()


@st.experimental_memo(ttl=600)
def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()


data = pd.DataFrame(run_query("SELECT * from lawyers;")).rename(columns={0: "lid", 1: "firstname", 2: "lastname", 3: "title", 4: "email", 5: "specialty", 6: "rate_per_hour"})

with header:
    st.title("Welcome!")
    st.text('In this project, I will look into transactions of taxis in NYC')

with dataset:
    # dataset section
    st.header("Fake Lawyer Dataset")
    st.text("I found this dataset on blahblahblah")
    # data = pd.read_csv('sample_data/sample_data.csv')
    st.write(data)


with features:
    # section
    st.header("Features I created")
    st.text("Some features")
    st.markdown('* **feature1**: description')

with model_training:
    st.header("Model Training")
    st.text("Description")
    sel_col, disp_col = st.columns(2)
    sel_col.slider("What should be the max_depth?", min_value=1, max_value=10)
