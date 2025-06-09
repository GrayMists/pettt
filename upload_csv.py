import streamlit as st
import pandas as pd
import requests
import json

url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]

def show_data():
    st.title("Завантаження CSV")
    uploaded_file = st.file_uploader("Завантаж CSV файл", type="csv")

    if uploaded_file is not None:
        try:
            # Читання файлу у DataFrame
            df = pd.read_csv(uploaded_file, sep=";", on_bad_lines="skip")
            df = df.dropna(how='all')      # прибираємо повністю пусті рядки
            df = df.fillna("")
            st.write("Ось ваш датафрейм:")
            st.dataframe(df)

            # Кнопка для завантаження в Supabase
            if st.button("Завантажити в Supabase"):
                TABLE_NAME = "sales_data"

                headers = {
                    "apikey": key,
                    "Authorization": f"Bearer {key}",
                    "Content-Type": "application/json",
                    "Prefer": "return=representation"
                }

                data = df.to_dict(orient="records")

                chunk_size = 500
                for i in range(0, len(data), chunk_size):
                    chunk = data[i:i + chunk_size]
                    response = requests.post(
                        f"{url}/rest/v1/{TABLE_NAME}",
                        headers=headers,
                        data=json.dumps(chunk)
                    )
                    if response.status_code not in [200, 201]:
                        st.error(f"Помилка при вставці: {response.text}")
                        break
                else:
                    st.success("Дані успішно завантажено в Supabase!")

        except Exception as e:
            st.error(f"Помилка при обробці: {e}")
