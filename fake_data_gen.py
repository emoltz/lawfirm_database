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
            print(lawyer.firstname, lawyer.lastname, lawyer.title, lawyer.email, lawyer.specialty, lawyer.rate_per_hour)

class FakeClient:
    cid = 0
    firstname = ""
    lastname = ""
    email = ""
    phone = ""

    def __init__(self):
        pass


conn = psycopg2.connect(**st.secrets["postgres"])
cur = conn.cursor()



# FUNCTIONS:
def populate_laywer_table():
    lawfirm = FakeLawfirm();
    for lawyer in lawfirm.list_of_lawyers:
        cur.execute(
            f"INSERT INTO lawyers (lid, firstname, lastname, title, email, specialty, rate_per_hour) VALUES ('{lawyer.lid}', '{lawyer.firstname}', '{lawyer.lastname}', '{lawyer.title}','{lawyer.email}','{lawyer.specialty}','{lawyer.rate_per_hour}')")
        conn.commit()









# SCRIPTS:
populate_laywer_table();



