import requests
import streamlit as st
from streamlit_lottie import st_lottie

st.set_page_config(page_title="Databse Webpage", page_icon=":tada:", layout="wide")
# Access the json information of the lottie animation
def load_lottieurl(url):
	r = requests.get(url)
	if r.status_code != 200:
		return None
	return r.json()
#---- Load Assests
lottie_coding = "https://assets5.lottiefiles.com/packages/lf20_fcfjwiyb.json"
#----- Header section -----
with st.container():
	st.subheader("Hi, we are Ethan and Julianna. Welcome to our database")
	st.title("This is a database for a lawfirm")

	st.write("To being, start by searching for anything related to this db")
	st.write("[To learn more about us >](linkedin profile here)")

# ----What this database does----
with st.container():
	st.write("---")
	left_column, right_column = st.columns(2)
	with left_column:
		st.header("What it does")
		st.write("##")
		st.write(
			"""
			Database made by Ethan and Julianna
			"""
		)
		st.write("[For more info hit >]")
	with right_column:
		st_lottie(lottie_coding, height=300, key="coding")