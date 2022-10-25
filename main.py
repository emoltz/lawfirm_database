import psycopg2
import streamlit as st

st.set_page_config(page_title="Lawfirm Database", page_icon=":card_index:")


# local CSS
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


local_css("static/styles.css")
st.write("This app is all set up!")


# DATABASE CONNECTION
@st.experimental_singleton
def init_connection():
    return psycopg2.connect(**st.secrets["postgres"])


conn = init_connection()


# perform query
@st.experimental_memo(ttl=600)
def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()


rows = run_query("SELECT * from lawyers;")

for row in rows:
    st.write(
        f"{row[0]}'s name is: {row[1]}"
    )
