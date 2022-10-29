import streamlit as st

header = st.container()
dataset = st.container()
features = st.container()
model_training = st.container()

with header:
    st.title("Welcome!")
    st.text('In this project, I will look into transactions of taxis in NYC')


with dataset:
    # dataset section
    st.header("NYC Taxi Dataset")
    st.text("I found this dataset on blahblahblah")

with features:
    # section
    st.header("Features I created")
    st.text("Some features")

with model_training:
    st.header("Model Training")
    st.text("Description")