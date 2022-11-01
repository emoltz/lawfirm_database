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


data = pd.DataFrame(run_query("SELECT * "
                              "from lawyers;")).rename(columns={0: "lid", 1: "firstname",
                                                                2: "lastname", 3: "title",
                                                                4: "email", 5: "specialty",
                                                                6: "rate_per_hour"})

with header:
    st.title("Welcome!")
    st.text('In this project, I will look into a lawfirm database')

    # trying to create a dialogue box up top for writing queries
    #sel_col = st.columns(1)
    #input_feature = sel_col.text_input('Which feature should be used as input feature?', 'lid')
    input_feature = st.text_input('What would you like to search for?'"")
    st.markdown(f"Your input is : {input_feature}")

    # collecting number inputs, perhaps for looking for lid, pid, cid
    number_input = st.number_input("Enter a client id", min_value=0, max_value=500, value=50, step=1)

    st.markdown(
        f"""
        * Query: {input_feature}
        * ID value: {number_input}
        """
    )

    # Checkbox for a yes or no question
    check_box_input = st.checkbox("Was this case closed?")
    st.write(check_box_input)

    selected_element = st.selectbox("Pick an item", ("item1", "item2", "item3"))
    st.write(selected_element)

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
    st.header("Year selection, if known")
    st.text("Use the slider to select the year")
    sel_col, disp_col = st.columns(2)
    sel_col.slider("What year are you searching?", min_value=2010,
                   max_value=2020)

    # Drop-down menu, maybe for sorting the results?
    n_estimators = sel_col.selectbox('Sort by:', options=[100,200,300,400,'no limit'], index=0)
    #dialogue box with a default value of 'lid', remove to set default to be empty
    input_feature = sel_col.text_input('Which feature should be used as input feature?', 'lid')

    # Another way to incorporate a slider
    threshold = st.slider("Pick a threshold:", min_value=1, max_value=100, value=50, step=1)
    st.write(threshold)





