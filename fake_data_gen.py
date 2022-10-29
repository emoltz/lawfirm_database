from faker import Faker
import streamlit as st
import psycopg2


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


# DB CONNECTION
conn = psycopg2.connect(**st.secrets["postgres"])
cur = conn.cursor()


# FUNCTIONS:
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


def populate_laywer_table():
    lawfirm = FakeLawfirm()
    for lawyer in lawfirm.list_of_lawyers:
        cur.execute(
            f"INSERT INTO lawyers (lid, firstname, lastname, title, email, specialty, rate_per_hour) VALUES ('{lawyer.lid}', '{lawyer.firstname}', '{lawyer.lastname}', '{lawyer.title}','{lawyer.email}','{lawyer.specialty}','{lawyer.rate_per_hour}')"
        )
        conn.commit()


# SCRIPTS:
# populate_laywer_table()
# populate_client_table()
