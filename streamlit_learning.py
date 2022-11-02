from datetime import time

import streamlit as st
import pandas as pd
import psycopg2
import streamlit.components.v1 as components
from streamlit_option_menu import option_menu

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
# Sidebar for a menu <--- breaks everything
# with st.sidebar:
#     with st.echo():
#         st.write("This code will be printed to the sidebar.")
#
#     with st.spinner("Loading..."):
#         time.sleep(5)
#     st.success("Done!")

# Sidebar menu!!
with st.sidebar:
    selected = option_menu(
        menu_title="Menu", #required
        options=["Home", "Lawyers", "Cases", "Clients", "Research", "etc"], #required
        default_index=0
    )

# ------------------------------------------- Home or beginning of app -------------------------------------------
if selected == "Home":
    with header:
        st.title("Welcome to Ethan & Julie's Lawfirm!")
        st.text('Please use the left menu to navigate these pages')

        # trying to create a dialogue box up top for writing queries
        # sel_col = st.columns(1)
        # input_feature = sel_col.text_input('Which feature should be used as input feature?', 'lid')
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

# ------------------------------------------- Lawyers -------------------------------------------
if selected == "Lawyers":
    #st.title(f"You have selected {selected}")
    with header:
        st.header("Lawyers")
        st.write(":heavy_minus_sign:" * 35)
        lefthand_col, somethingelse_col = st.columns(2)
        # Drop-down menu example
        lawyer_dropdown_col = lefthand_col.selectbox('Select a lawyer you want to search for:', options=[
                                                                                 'Ethan',
                                                                                 'Julie',
                                                                                 "Sharon",
                                                                                 "Julia",
                                                                                 'no limit'], index=0)
# ------------------------------------------- Cases -------------------------------------------
if selected == "Cases":
    with header:
        st.header("Cases")
        # divider line
        st.write(":heavy_minus_sign:" * 35)
        # another divider line
        st.markdown("""<hr style="height:5px;border:none;color:#222;background-color:#333;" /> """,
                    unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        # Radio buttons for what case is related to, should have more options: (in left-hand column)
        with col1:
            genre = st.radio(
                "What topic was your case related to?",
                ('real estate', 'contract', 'divorce'), key=0)

            if genre == 'real estate':
                st.write('You selected real estate.')
            else:
                st.write("You didn't select real estate.")

        # Another way to incorporate a slider (in right-hand column)
        with col2:
            threshold = st.slider("What year was the case closed?", min_value=2010, max_value=2022, value=2010, step=1)
            st.write(threshold)

# ------------------------------------------- Clients -------------------------------------------
if selected == "Clients":
    st.title(f"You have selected {selected}")
    st.header("Clients")
    with header:
        st.header("Clients")
        st.write(":heavy_minus_sign:" * 35)
        # collecting number inputs, looking for cid
        client_id_input = st.number_input("Search for a client by their ID", min_value=0, max_value=500, value=50, step=1)


# ------------------------------------------- Research -------------------------------------------
if selected == "Research":
    # st.title(f"You have selected {selected}")
    # st.header("Research")
    with header:
        st.header("Research")
        st.write(":heavy_minus_sign:" * 35)
        # dialogue box with a default value of 'lid', remove to set default to be empty
        input_feature = st.text_input('Type in what research document you want:', 'Contract 152', key =0)



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

    sel_col, disp_col = st.columns(2)
    # sel_col.slider("What year are you searching?", min_value=2010,
    #                max_value=2020, step= 1)

    # dialogue box with a default value of 'lid', remove to set default to be empty
    input_feature = sel_col.text_input('Which feature should be used as input feature?', 'lid')



# with header:
#     st.header("Cases")
#     # divider line
#     st.write(":heavy_minus_sign:" * 35)
#     # another divider line
#     st.markdown("""<hr style="height:5px;border:none;color:#222;background-color:#333;" /> """, unsafe_allow_html=True)
#     # Radio buttons for what case is related to, should have more options:
#     genre = st.radio(
#         "What topic was your case related to?",
#          ('real estate', 'contract', 'divorce'))
#
#     if genre == 'real estate':
#         st.write('You selected real estate.')
#     else:
#         st.write("You didn't select real estate.")
#
#     # Another way to incorporate a slider
#     threshold = st.slider("What year was the case closed?", min_value=2010, max_value=2022, value=2010, step=1)
#     st.write(threshold)


