import streamlit as st

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
home_page = st.Page("pages/home_page.py")
list_mutual_fund_page = st.Page("pages/list_mutual_fund.py")
list_criteria_page = st.Page("pages/list_criteria.py")
recommendation_page = st.Page("pages/recommendation.py")

with st.sidebar:
    st.title("Sistem Pendukung Keputusan Rekomendasi Reksa Dana")
    st.image("images/logo-bibit.png")

    st.page_link(home_page, label="Beranda", icon=":material/home:")
    st.page_link(list_mutual_fund_page, label="Daftar Reksa Dana", icon=":material/finance_mode:")
    st.page_link(list_criteria_page, label="Daftar Kriteria Seleksi", icon=":material/format_list_bulleted:")
    st.page_link(recommendation_page, label="Rekomendasi Reksa Dana", icon=":material/recommend:")

    st.caption("Copyright © 2025 by Putra U")

pg = st.navigation([home_page, list_mutual_fund_page, list_criteria_page, recommendation_page])
pg.run()
