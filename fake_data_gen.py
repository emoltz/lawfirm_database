from faker import Faker
import streamlit as st
import psycopg2
from faker.providers import DynamicProvider
import numpy as np


def connect_to_database_return_query(query):
    conn = psycopg2.connect(**st.secrets["postgres"])
    cur = conn.cursor()
    cur.execute(query)
    return cur.fetchall()


def connect_to_database_and_insert(query):
    conn = psycopg2.connect(**st.secrets["postgres"])
    cur = conn.cursor()
    cur.execute(query)
    conn.commit()


# CLASSES:
class FakeLawyer:
    lid = 0
    firstname = ""
    lastname = ""
    title = ""
    email = ""
    specialty = ""
    rate_per_hour = 0

    def __init__(self):
        fake = Faker()
        self.lid = fake.unique.random_int(min=0, max=10000)
        self.firstname = fake.first_name()
        self.lastname = fake.last_name()
        self.title = fake.job()
        self.email = fake.email()
        self.specialty = fake.word()
        self.rate_per_hour = fake.random_int(min=1, max=500)


class FakeCase:
    fake = Faker()
    case_id = 0
    topic = ""
    date_closed = ""
    paid = True
    verdict = ""
    managed_by = 0  # foreign key - lawyers
    lawyer_id = []
    presided_by = 0  # foreign key - judges
    judge_id = []
    topic_provider = DynamicProvider(
        provider_name="topic_provider",
        elements=[
            "Divorce",
            "Child Custody",
            "Child Support",
            "Estate Planning",
            "Real Estate",
            "Criminal",
            "Traffic",
            "Bankruptcy",
        ]
    )
    verdict_provider = DynamicProvider(
        provider_name="verdict_provider",
        elements=[
            "Guilty",
            "Not Guilty",
            "Dismissed",
            "Settled",
            "Continued",
        ]
    )

    def __init__(self):
        self.get_lawyer_ids()
        self.get_judge_ids()
        self.fake.add_provider(self.topic_provider)
        self.fake.add_provider(self.verdict_provider)
        self.case_id = self.fake.unique.random_int(min=0, max=10000)
        self.paid = self.fake.boolean(chance_of_getting_true=50)
        self.topic = self.fake.topic_provider()
        self.date_closed = self.fake.date_between(start_date="-10y", end_date="today")
        self.verdict = self.fake.verdict_provider()
        self.managed_by = int(self.fake.random_element(self.lawyer_id))
        self.presided_by = int(self.fake.random_element(self.judge_id))

    def get_lawyer_ids(self):
        query = "SELECT lid FROM lawyers"
        self.lawyer_id = connect_to_database_return_query(query)
        self.lawyer_id = np.array(self.lawyer_id)

    def get_judge_ids(self):
        query = "SELECT judgeid FROM judges"
        self.judge_id = connect_to_database_return_query(query)
        self.judge_id = np.array(self.judge_id)


class FakeLawfirm:
    list_of_lawyers = []

    def __init__(self):
        for _ in range(25):
            self.list_of_lawyers.append(FakeLawyer())

    def print_lawyers(self):
        for lawyer in self.list_of_lawyers:
            print(
                lawyer.firstname,
                lawyer.lastname,
                lawyer.title,
                lawyer.email,
                lawyer.specialty,
                lawyer.rate_per_hour,
            )


class FakeClient:
    cid = 0
    firstname = ""
    lastname = ""
    email = ""
    phone = ""

    def __init__(self):
        fake = Faker()
        self.cid = fake.unique.random_int(min=10000, max=20000)
        self.firstname = fake.first_name()
        self.lastname = fake.last_name()
        self.email = fake.email()
        self.phone = fake.random_int(min=1111111, max=9999999)


class FakeContacts:
    cid = 0  # client ID -- foreign key
    id = 0
    firstname = ""
    lastname = ""
    phone = ""
    email = ""
    type_of_relation = ""
    relationship_provider = DynamicProvider(
        provider_name="relationship_provider",
        elements=[
            "mother",
            "father",
            "son",
            "daughter",
            "cousin",
            "friend",
            "neighbor",
        ],
    )
    client_ids = []

    def get_client_ids(self):
        conn = psycopg2.connect(**st.secrets["postgres"])
        cur = conn.cursor()

        cur.execute(f"SELECT cid from clients;")
        self.client_ids = cur.fetchall()

    def __init__(self):
        fake = Faker()
        fake.add_provider(self.relationship_provider)
        self.get_client_ids()

        self.cid = fake.random_element(self.client_ids)[0]
        self.id = fake.unique.random_int(min=0, max=10000)
        self.firstname = fake.first_name()
        self.lastname = fake.last_name()
        self.phone = fake.unique.random_int(min=1111111, max=9999999)
        self.email = fake.email()
        self.type_of_relation = fake.relationship_provider()

    def __str__(self):
        return f"{self.cid}, {self.firstname} {self.lastname} {self.phone} {self.email} {self.type_of_relation}"


class FakeParalegal:
    pid = 0
    rate_per_hour = 0
    speciality = ""
    firstname = ""
    lastname = ""
    assigned_to_case = 0

    def __init__(self):
        fake = Faker()
        self.pid = fake.unique.random_int(min=20000, max=30000)
        self.rate_per_hour = fake.random_int(min=1, max=500)
        self.speciality = fake.word()
        self.firstname = fake.first_name()
        self.lastname = fake.last_name()


class FakeJudge:
    court = ""
    judge_id = 0
    firstname = ""
    lastname = ""

    def __init__(self):
        fake = Faker()
        self.court = fake.word()
        self.judge_id = fake.unique.random_int(min=30000, max=40000)
        self.firstname = fake.first_name()
        self.lastname = fake.last_name()


# DB CONNECTION
conn = psycopg2.connect(**st.secrets["postgres"])
cur = conn.cursor()


# FUNCTIONS:


def populate_judge_table():
    judge_list = []
    for _ in range(5):
        judge_list.append(FakeJudge())
    for judge in judge_list:
        cur.execute(
            f"INSERT INTO judges (court, judgeid, firstname, lastname) VALUES ('{judge.court}', '{judge.judge_id}', '{judge.firstname}','{judge.lastname}')"
        )
        conn.commit()


def populate_paralegal_table(number_of_paralegals=5):
    paralegal_list = []
    for _ in range(number_of_paralegals):
        paralegal_list.append(FakeParalegal())
    for paralegal in paralegal_list:
        cur.execute(
            f"INSERT INTO paralegals (pid, rate_per_hour, specialty, firstname, lastname) VALUES ('{paralegal.pid}', '{paralegal.rate_per_hour}', '{paralegal.speciality}', '{paralegal.firstname}','{paralegal.lastname}')"
        )
        conn.commit()


def gen_client_list(number_of_clients=100):
    client_list = []
    for _ in range(number_of_clients):
        client_list.append(FakeClient())
    return client_list


def populate_client_table():
    client_list = gen_client_list()
    for client in client_list:
        cur.execute(
            f"INSERT INTO clients (cid, firstname, lastname, email, phone) VALUES ('{client.cid}', '{client.firstname}', '{client.lastname}', '{client.email}','{client.phone}')"
        )
        conn.commit()


def populate_lawyer_table():
    lawfirm = FakeLawfirm()
    for lawyer in lawfirm.list_of_lawyers:
        cur.execute(
            f"INSERT INTO lawyers (lid, firstname, lastname, title, email, specialty, rate_per_hour) VALUES ('{lawyer.lid}', '{lawyer.firstname}', '{lawyer.lastname}', '{lawyer.title}','{lawyer.email}','{lawyer.specialty}','{lawyer.rate_per_hour}')"
        )
        conn.commit()


def populate_contacts_table(amount=25):
    contacts_list = []
    for _ in range(amount):
        contacts_list.append(FakeContacts())
    for contact in contacts_list:
        cur.execute(
            f"INSERT INTO contacts_related_to (cid, id, firstname, lastname, phone, email, type_of_relation) VALUES ('{contact.cid}', '{contact.id}', '{contact.firstname}', '{contact.lastname}', '{contact.phone}','{contact.email}','{contact.type_of_relation}')"
        )
        conn.commit()


def populate_part_of_table(amount=15):
    # so I need to get the client IDs and the case IDs and then randomly assign
    fake = Faker()

    id_query = "SELECT cid from clients;"
    case_id_query = "select case_id from cases;"
    client_ids = connect_to_database_return_query(id_query)
    case_ids = connect_to_database_return_query(case_id_query)
    client_ids = np.asarray(client_ids)
    case_ids = np.asarray(case_ids)

    already_used_client_ids = []
    already_used_case_ids = []

    for _ in range(amount):
        # insert into part_of table random cids
        client_id_temp = fake.random_element(client_ids)
        case_id_temp = fake.random_element(case_ids)
        client_id_temp = int(client_id_temp)
        case_id_temp = int(case_id_temp)
        if client_id_temp not in already_used_client_ids and case_id_temp not in already_used_case_ids:
            query = f"INSERT INTO part_of (client_id, case_id) VALUES ({client_id_temp}, {case_id_temp})"
            connect_to_database_and_insert(query)
        already_used_case_ids.append(case_id_temp)
        already_used_client_ids.append(client_id_temp)


# generate cases table
def populate_cases_table(amount=15):
    for _ in range(amount):
        case = FakeCase()
        query = f"INSERT INTO cases (case_id, topic, date_closed, paid, verdict, managed_by, presided_by) VALUES ('{case.case_id}','{case.topic}', '{case.date_closed}','{case.paid}', '{case.verdict}', '{case.managed_by}', '{case.presided_by}')"
        connect_to_database_and_insert(query)


# ----------- SCRIPTS: Uncomment to run  -----

# populate_lawyer_table()
# populate_client_table()
# populate_paralegal_table()
# populate_judge_table()
# populate_contacts_table(100)
# populate_part_of_table()
# populate_cases_table()
