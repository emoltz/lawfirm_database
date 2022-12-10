import requests
import streamlit as st
import pandas as pd
from streamlit_lottie import st_lottie
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


def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


def get_first_last_names_from_query(query):
    list = run_query(query)
    list_names = []
    # combine first and last names
    for name in list:
        list_names.append(name[0] + " " + name[1])

    return list_names


conn = init_connection()


def page_intro(page_name):
    st.title(f"Welcome to the {page_name} Page")
    st.write('*Please use the left menu to navigate these pages*')
    st.markdown("---")


def horizontal_line():
    st.markdown("---")


@st.experimental_memo(ttl=600)
def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()


with st.sidebar:
    sidebar_selection = option_menu(
        menu_title="Menu",  # required
        options=["Home", "Lawyers & Cases", "Clients", "Courts"],  # required
        default_index=0
    )
# --------------------------------- Home page --------------------------------------
if sidebar_selection == "Home":
    with header:
        st.title("Moltz & Goldbas Attorneys at Law")
        st.markdown("*Please use the left menu to navigate these pages*")
    st.balloons()

    lottie_url = "https://assets4.lottiefiles.com/packages/lf20_bmqwuqs8.json"
    lottie_json = load_lottieurl(lottie_url)
    st_lottie(lottie_json, speed=1, height=300, key="initial")

# --------------------------------- Lawyers page --------------------------------------
if sidebar_selection == "Lawyers & Cases":
    page_intro(sidebar_selection)

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
    horizontal_line()

    st.markdown("### Look up information about a case from the `CaseID`")
    total_cases_query = "SELECT COUNT(*) from cases;"
    total_cases = run_query(total_cases_query)

    case_num = st.number_input("Case ID", min_value=1, max_value=total_cases[0][0])
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

    columns = st.columns(4)
    try:
        verdict_of_case = run_query(verdict_query)
        date_of_case = run_query(date_of_case_query)
        with columns[0]:
            st.write("**Date of Case**")
            st.write(date_of_case[0][0])
        with columns[1]:
            st.write("**Verdict**")
            st.write(verdict_of_case[0][0].title())
        with columns[2]:
            st.write("**Judge**")
            st.write("TODO")
        with columns[3]:
            st.write("**Managed By**")
            st.write("TODO")
    except IndexError or ValueError:
        st.markdown("## A case with that ID doesn't exist!")

    horizontal_line()
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

    horizontal_line()
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

    horizontal_line()
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
        GROUP BY	c.topic;
    """

    try:
        hours_spent_on_topic = run_query(hours_spent_on_topic_query)
        st.metric("Hours Spent", hours_spent_on_topic[0][1])
    except IndexError or ValueError:
        st.markdown("**ERROR:** This topic hasn't been worked on yet!")

# --------------------------------- Clients page --------------------------------------
if sidebar_selection == "Clients":
    page_intro(sidebar_selection)

    st.markdown("### What was the topic of the case that a client was involved in?")
    client_list_query = """
     SELECT distinct c.firstname, c.lastname from clients c;
    """

    client_list = run_query(client_list_query)
    client_list_names = []
    # combine first and last names
    for name in client_list:
        client_list_names.append(name[0] + " " + name[1])

    selected_client = st.selectbox("Select a client", client_list_names, key="client01")

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

    for i, topic in enumerate(topics):
        st.write(topic[i])

    horizontal_line()
    st.markdown("### What is the phone number of a client's contact?")
    selected_client = st.selectbox("Select a client", client_list_names, key="client02")

    # get id from selected client
    selected_client_firstName = selected_client.split()[0]
    selected_client_lastName = selected_client.split()[1]

    # get the id of the client
    client_id_query = f"""
    SELECT cid from clients where firstname = '{selected_client_firstName}' and lastname = '{selected_client_lastName}';
    """

    client_id = run_query(client_id_query)
    client_id = client_id[0][0]

    contacts_query = f"""
    select firstname, lastname, phone, email from contacts_related_to where cid = {client_id};"""
    #
    contacts_list = run_query(contacts_query)
    if not contacts_list:
        st.markdown("No contacts for this client!")
    else:
        st.markdown("**Contacts:**")
    # st.write(contacts_list)

    try:
        num_of_columns = len(contacts_list)
        columns = st.columns(num_of_columns)
    except:
        pass
    for i, contact in enumerate(contacts_list):
        with columns[i]:
            st.write("**Name:**", contact[0], contact[1])
            st.write("**Phone:**", contact[2])
            st.write(contact[3])
            horizontal_line()

    horizontal_line()
    st.markdown("### How many clients have outstanding balances?")

    client_outstanding_balance_query = f"""
        select count(*)
        from cases c, clients cl, part_of p
        where c.case_id = p.case_id
        and cl.cid = p.client_id
        and c.paid = false
    """

    number_of_clients_query = f"""
        select count(*)
        from clients;
    """

    total_clients = run_query(number_of_clients_query)
    client_outstanding_balance = run_query(client_outstanding_balance_query)
    columns = st.columns(2)
    client_delta = -1
    with columns[0]:
        st.metric("Outstanding Balances", client_outstanding_balance[0][0], delta=client_delta)
    with columns[1]:
        st.metric("Fully Paid Clients", total_clients[0][0] - client_outstanding_balance[0][0], delta=-1 * client_delta)
    st.bar_chart(data=[client_outstanding_balance[0][0], total_clients[0][0] - client_outstanding_balance[0][0]])

# --------------------------------- Research page ------------------------------------

# if selected == "Research":
#     page_intro(selected)

# --------------------------------- Courts page --------------------------------------
if sidebar_selection == "Courts":
    page_intro(sidebar_selection)

    st.markdown("### Look up courts based on `CaseID`")
    case_num = st.number_input("Case ID", min_value=1, max_value=5)
    court_query = f"""
                SELECT	j.court
                FROM judges j, cases c
                WHERE j.judgeid = c.presided_by
                AND c.case_id = {case_num}	
        """

    try:
        court_output = run_query(court_query)
        court_output = court_output[0][0]
        st.write("This case was tried in: ", court_output, "court")

        judge_query = f"""
                        SELECT	j.firstname, j.lastname, c.topic, j.court
                        FROM judges j, cases c
                        WHERE j.judgeid = c.presided_by
                        AND c.case_id = {case_num}	
                """
        judges_list = run_query(judge_query)
        judges_list_names = []
        # combine first and last names of judge
        for name in judges_list:
            judges_list_names.append(name[0] + " " + name[1])

        judge_name = judges_list_names
        st.write("The presiding judge for case number ", case_num, " was the honorable", judge_name[0], ".")

    except IndexError or ValueError:
        st.write("### Case number: ", case_num, " was not tried in any court.")

    horizontal_line()

    # how many cases has [judge] presided over that dealth with [topic]?
    st.markdown("### How many cases has a judge presided over that dealt with a specific topic?")
    judge_list_query = """
        SELECT distinct j.firstname, j.lastname from judges j;
    """
    judge_list_names = []
    judge_list = run_query(judge_list_query)
    # combine first and last names
    for name in judge_list:
        judge_list_names.append(name[0] + " " + name[1])

    case_topics_query = f"""
        SELECT distinct c.topic from cases c;
    """
    case_topics = run_query(case_topics_query)
    case_topics_list = []
    for topic in case_topics:
        case_topics_list.append(topic[0])
    columns = st.columns(2)
    with columns[0]:
        selected_judge = st.selectbox("Select a judge", judge_list_names, key="judge01")
    with columns[1]:
        selected_topic = st.selectbox("Select a topic", case_topics_list, key="topic01")

    selected_judge_firstName = selected_judge.split()[0]
    selected_judge_lastName = selected_judge.split()[1]

    try:
        number_of_times_query = f"""
        SELECT count(c.topic)
        FROM judges j,
             cases c
        WHERE j.judgeid = c.presided_by
          and j.firstname = '{selected_judge_firstName}'
          and j.lastname = '{selected_judge_lastName}'
          and c.topic = '{selected_topic}'
        group by j.firstname, j.lastname
        """

        number_of_times = run_query(number_of_times_query)

        st.metric(f"Number of times {selected_judge} has presided over topic {selected_topic.lower()}:",
                  number_of_times[0][0])
    except IndexError or ValueError:
        st.metric(f"Number of times {selected_judge} has presided over topic {selected_topic.lower()}:", 0)
