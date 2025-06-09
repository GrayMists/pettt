import streamlit as st
import pandas as pd


from upload_csv import show_data
from data_db import show_data_db

url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]

TABLE_NAME = "sales_data"



headers = {
    "apikey": key,
    "Authorization": f"Bearer {key}",
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