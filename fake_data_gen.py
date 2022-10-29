from faker import Faker
import streamlit as st
import psycopg2

fake = Faker()

conn = psycopg2.connect(**st.secrets["postgres"])

cur = conn.cursor()

# cur.execute("insert into lawyers(lid, firstname, lastname, rate_per_hour) values (2, 'John', 'Smith', 2);")
# conn.commit()

for _ in range(15):
    cur.execute(
        f"INSERT INTO lawyers (lid, firstname, lastname, title, email, rate_per_hour) VALUES ('{fake.random_int(min=18, max=1000)}', '{fake.first_name()}', '{fake.last_name()}', 'random_title','{fake.first_name()}@gmail.com','{fake.random_int(min=1, max=500)}')")
    conn.commit()
