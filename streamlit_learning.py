import streamlit as st
import pandas as pd
import psycopg2

header = st.container()
dataset = st.container()
features = st.container()
model_training = st.container()

conn = psycopg2.connect(**st.secrets["postgres"])
cur = conn.cursor()
data = pd.read_sql_query('SELECT * FROM lawyers', conn)

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

with model_training:
    st.header("Model Training")
    st.text("Description")
