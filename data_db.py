import requests
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]

TABLE_NAME = "sales_data"

headers = {
    "apikey": key,
    "Authorization": f"Bearer {key}",
}

@st.cache_data
def fetch_sales_data():
    all_data = []
    limit = 1000
    offset = 0

    while True:
        response = requests.get(
            f"{url}/rest/v1/{TABLE_NAME}",
            headers=headers,
            params={
                "select": "*",
                "limit": limit,
                "offset": offset
            }
        )
        if response.status_code != 200:
            raise Exception(f"Помилка при отриманні даних: {response.text}")

        data = response.json()
        if not data:
            break
        all_data.extend(data)
        offset += limit

    df = pd.DataFrame(all_data)
    return df




def show_data_db():
    try:
        df = fetch_sales_data()
        unique_regions = df['region'].unique()
        region_tabs = st.tabs(list(unique_regions))

        for region_tab, region in zip(region_tabs, unique_regions):
            with region_tab:
                st.header(f"Регіон: {region}")
                region_df = df[df["region"] == region]
                unique_managers = region_df["manager_name"].unique()
                manager_tabs = st.tabs(list(unique_managers))
                for manager_tab, manager in zip(manager_tabs, unique_managers):
                    with manager_tab:
                        st.subheader(f"МП: {manager}")
                        manager_df = region_df[region_df["manager_name"] == manager]
                        with st.expander("Таблиця"):
                            st.dataframe(manager_df.drop(columns=["id","name","region_code"]).reset_index(drop=True), hide_index=True)
                        fig, ax = plt.subplots(layout='constrained')

                        # Prepare data for grouped bar chart
                        grouped = manager_df.groupby(['month', 'year'])['quantity'].sum().unstack(fill_value=0)

                        month_order = ["Січень", "Лютий", "Березень", "Квітень", "Травень", "Червень",
                                       "Липень", "Серпень", "Вересень", "Жовтень", "Листопад", "Грудень"]
                        grouped.index = pd.CategoricalIndex(grouped.index, categories=month_order, ordered=True)
                        grouped = grouped.sort_index()

                        months = grouped.index.tolist()
                        years = grouped.columns.tolist()
                        bar_width = 0.8 / len(years) if len(years) > 0 else 0.8
                        x = np.arange(len(months))

                        for i, year in enumerate(years):
                            ax.bar(x + i * bar_width, grouped[year], width=bar_width, label=str(year))

                        ax.set_xticks(x + bar_width * (len(years) - 1) / 2 if len(years) > 0 else x)
                        ax.set_xticklabels(months, rotation=45)
                        ax.set_ylabel('quantity')
                        ax.set_title('sales')
                        ax.legend(title='Year')

                        st.pyplot(fig)

    except Exception as e:
        st.error(str(e))