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


def populate_laywer_table():
    lawfirm = FakeLawfirm()
    for lawyer in lawfirm.list_of_lawyers:
        cur.execute(
            f"INSERT INTO lawyers (lid, firstname, lastname, title, email, specialty, rate_per_hour) VALUES ('{lawyer.lid}', '{lawyer.firstname}', '{lawyer.lastname}', '{lawyer.title}','{lawyer.email}','{lawyer.specialty}','{lawyer.rate_per_hour}')"
        )
        conn.commit()


# SCRIPTS:
populate_laywer_table()
populate_client_table()
populate_paralegal_table()
populate_judge_table()