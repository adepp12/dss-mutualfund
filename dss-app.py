import streamlit as st
import pandas as pd
from function.preprocessing import cleaning_data

st.set_page_config(layout="wide")

# mengambil dataset dan simpan di session_state
if "clean_df" not in st.session_state:
    url_dataset = st.secrets["URL_DATASET"]
    dataset_df = pd.read_csv(url_dataset)
    clean_df = cleaning_data(dataset_df)
    st.session_state["clean_df"] = clean_df
    
    last_update = pd.to_datetime(clean_df['Waktu Scraping'][0]).strftime('%d %B %Y')
    st.session_state.last_update = last_update

# st.sidebar.write("Copyright 2025")

# # home_page = st.Page("./pages/home_page.py", title="Home Page"),
# # list_mutual_fund_page =  st.Page("./pages/list_mutual_fund.py", title="Daftar Reksa Dana"),
# # list_criteria_page = st.Page("./pages/list_criteria.py", title="Daftar Kriteria Seleksi"),
# # recommendation_page = st.Page("./pages/recommendation.py", title="Rekomendasi Reksa Dana"),

# 22/12 -> navbar pada sidebar dg st.Page + st.navigation, namun tidak bisa menambahkan logo dan judul di sidebar (bisa, namun malah di bawah navigation)
# pages = [
#     st.Page("pages/home_page.py", title="Beranda"),
#     st.Page("pages/list_mutual_fund.py", title="Daftar Reksa Dana"),
#     st.Page("pages/list_criteria.py", title="Daftar Kriteria Seleksi"),
#     st.Page("pages/recommendation.py", title="Rekomendasi Reksa Dana"),
# ]

# navigation = st.navigation(pages)
# navigation.run()


# pendekatan dgn st.Page ditaruh pada page_link (membuat custom navigation di sidebar), biar bisa nambah logo + judul di sidebar
home_page = st.Page("pages/home_page.py", title="Beranda")
list_mutual_fund_page = st.Page("pages/list_mutual_fund.py", title="Daftar Reksa Dana")
list_criteria_page = st.Page("pages/list_criteria.py", title="Daftar Kriteria Seleksi")
recommendation_page = st.Page("pages/recommendation.py", title="Rekomendasi Reksa Dana")

with st.sidebar:
    st.title("Sistem Pendukung Keputusan Rekomendasi Reksa Dana")
    st.image("images/logo-bibit.png")

    st.page_link(home_page, label="Beranda", icon=":material/home:")
    st.page_link(list_mutual_fund_page, label="Daftar Reksa Dana", icon=":material/finance_mode:")
    st.page_link(list_criteria_page, label="Daftar Kriteria Seleksi", icon=":material/format_list_bulleted:")
    st.page_link(recommendation_page, label="Rekomendasi Reksa Dana", icon=":material/recommend:")
    
    st.caption("Copyright © 2025")

pg = st.navigation([home_page, list_mutual_fund_page, list_criteria_page, recommendation_page])
pg.run()
