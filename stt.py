import streamlit as st
import pandas as pd


from upload_csv import show_data
from data_db import show_data_db


SUPABASE_URL = "https://vimswywxzejgyvxjzuvf.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZpbXN3eXd4emVqZ3l2eGp6dXZmIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc0NTg1OTk0NiwiZXhwIjoyMDYxNDM1OTQ2fQ.31GnQn8Bf_tcM-JXIdP4fk8Hnf3wMEKrhofd4Vy3EiY"
TABLE_NAME = "sales_data"



headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=representation"
}


st.sidebar.title("Навігація")
page = st.sidebar.selectbox("Обери сторінку", ["Головна", "Завантаження CSV", "Перегляд з Supabase"])

if page == "Головна":
    st.title("Головна")
    st.write("Вітання у застосунку!")

elif page == "Завантаження CSV":
    show_data()

elif page == "Перегляд з Supabase":
    st.title("Перегляд даних з Supabase")
    show_data_db()
    # встав код для GET-запиту і відображення