import streamlit as st
import pandas as pd
from classes import *
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


def page_intro(page_name):
    st.title(f"Welcome to the {page_name} Page")
    st.write('*Please use the left menu to navigate these pages*')
    st.markdown("---")


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

if selected == "Home":
    with header:
        st.title("Welcome to Ethan & Julie Attorneys at Law")
        st.text('Please use the left menu to navigate these pages')

        # TODO make this work?
        input_feature = st.text_input('What would you like to search for?'"")

if selected == "Lawyers":
    page_intro(selected)

    # lawyer1 = Laywer("Ethan", "Hunt")
    first_names = []
    last_names = []

    # this gets the names from the lawyers table
    query = run_query("SELECT firstName, lastName from lawyers;")
    lawyer_list = []
    # this puts them into three lists: one with the lawyers first and last names, and the other two with their first and last names isolated
    for i in range(0, len(query)):
        first_names.append(query[i][0])
        last_names.append(query[i][1])
        lawyer_list.append(query[i][0] + query[i][1])

    st.write("Lookup how many cases a lawyer has worked on:")
    # feed the list of lawyers into the dropdown menu
    choice = st.selectbox("Select a Lawyer", lawyer_list, index=0)
    choice_index = None

    # this is so we can isolate the first/last names of the lawyer. There's a better way to do this with string slicing but we can handle that later.
    for i in range(0, len(lawyer_list)):
        if choice == lawyer_list[i]:
            choice_index = i

    st.write("You selected:", choice)
    cases_worked_on = run_query(
        # TODO we should also have this grab last name
        f"SELECT COUNT(*) from lawyers l, cases c, works_on w where l.lid = w.lid and c.case_id = w.case_id and l.firstName = '{first_names[choice_index]}';")

    # this query finds the total number of hours worked on by a lawyer using their first and last names
    total_hours_query = f"""
        SELECT Sum(w.hours) as hours
        from lawyers l,
               cases c,
               works_on w
        where l.lid = w.lid
        and c.case_id = w.case_id
        and l.firstName = '{first_names[choice_index]}'
        and l.lastname = '{last_names[choice_index]}';
    """

    # run the query and return data
    try:
        total_hours_worked = run_query(total_hours_query)
        # put data into columns
        columns = st.columns(2)
        with columns[0]:
            st.metric("Cases Worked On", cases_worked_on[0][0])
        with columns[1]:
            st.metric("Total hours worked on all cases", total_hours_worked[0][0])
    except IndexError:
        st.write("Query did not work. ")

if selected == "Cases":
    page_intro(selected)

    st.markdown("### Lookup information about a case from the `CaseID`")
    case_num = st.number_input("Case ID", min_value=1, max_value=5)
    date_of_case_query = f"""
            SELECT	date_closed
            FROM cases
            WHERE 	case_id = {case_num}	
    """

    verdict_query = f"""
         SELECT	verdict
         FROM		cases
         WHERE 	case_id = {case_num}
    """

    tabs = st.tabs(["Date", "Verdict", "Topic", "Managed By", "Lawyers Involved"])
    columns = st.columns(2)
    try:
        verdict_of_case = run_query(verdict_query)
        date_of_case = run_query(date_of_case_query)
        with tabs[0]:
            st.write(date_of_case[0][0])
        with tabs[1]:
            st.write(verdict_of_case[0][0].title())
        with tabs[2]:
            st.write("TODO")
        with tabs[3]:
            st.write("TODO")
        with tabs[4]:
            st.write("TODO")
    except IndexError or ValueError:
        st.markdown("## A case with that ID doesn't exist!")

    st.markdown("---")
    st.markdown("### What cases were closed between two dates?")
    columns = st.columns(2)
    with columns[0]:
        start_date = st.date_input("Start Date")
        start_date_string = str(start_date.strftime("%Y-%m-%d"))
    with columns[1]:
        end_date = st.date_input("End Date")
        end_date_string = str(end_date.strftime("%Y-%m-%d"))

    cases_closed_between_dates_query = f"""
         SELECT distinct c.case_id, c.topic, c.date_closed
         FROM cases c
         WHERE date_closed BETWEEN '{start_date_string}' AND '{end_date_string}'
         order by c.date_closed;
    """

    try:
        cases_closed_between_dates = run_query(cases_closed_between_dates_query)
        cases_closed_between_dates_df = pd.DataFrame(cases_closed_between_dates,
                                                     columns=["Case ID", "Topic", "Date Closed"])
        st.write(cases_closed_between_dates_df)
    except IndexError or ValueError:
        st.markdown("No cases were closed between those dates!")

    st.markdown("---")
    st.markdown("### How many cases were there that made over the selected amount of money?")
    number_input = st.number_input("Amount of money", value=1.00, step=0.50)

    cases_over_amount_query = f"""
    SELECT COUNT(*)
    FROM cases c,
        lawyers l,
         works_on w
    WHERE w.lid = l.lid
    AND w.case_id = c.case_id
    AND ((w.hours * l.rate_per_hour) > {number_input});
  """

    try:
        cases_over_amount = run_query(cases_over_amount_query)
        st.metric("Cases: ", cases_over_amount[0][0])
    except IndexError or ValueError:
        st.markdown("No cases were closed between those dates!")

    st.markdown("---")
    st.markdown("### How many hours were spent on a particular topic?")
    # topic_list = ["Divorce", "Criminal", "Bankruptcy", "Real Estate", "Tax"]
    topic_list_query = """
    SELECT distinct c.topic from cases c;
    """

    topic_list = run_query(topic_list_query)
    # go through and clean the list
    for topic in topic_list:
        topic_list[topic_list.index(topic)] = topic[0]

    selection = st.selectbox("Select a topic", topic_list)

    hours_spent_on_topic_query = f"""
    SELECT	c.topic, sum(w.hours) as hours_spent
    FROM		cases c, works_on w
    WHERE 	c.case_id = w.case_id
    AND 		c.topic = '{selection}'
    GROUP BY	c.topic;"""

    try:
        hours_spent_on_topic = run_query(hours_spent_on_topic_query)
        st.metric("Hours Spent", hours_spent_on_topic[0][1])
    except IndexError or ValueError:
        st.markdown("**ERROR:** This topic hasn't been worked on yet!")

if selected == "Clients":
    page_intro(selected)

    st.markdown("### What was the topic of the case that a client was involved in?")
    client_list_query = """
     SELECT distinct c.firstname, c.lastname from clients c;
    """

    client_list = run_query(client_list_query)
    client_list_names = []
    # combine first and last names
    for name in client_list:
        client_list_names.append(name[0] + " " + name[1])

    selected_client = st.selectbox("Select a client", client_list_names)

    # split the name into first and last
    first_name = selected_client.split()[0]
    last_name = selected_client.split()[1]

    # query to get the case id
    query = f"""
    SELECT	c.topic
    FROM		cases c, part_of p, clients cl
    WHERE 	c.case_id = p.case_id
    AND 		p.client_id = cl.cid
    AND 		(cl.firstname = '{first_name}' AND cl.lastname = '{last_name}')
"""
    topics = run_query(query)
    for topic in topics:
        st.write(topic[0])

if selected == "Research":
    page_intro(selected)

if selected == "etc":
    page_intro(selected)
