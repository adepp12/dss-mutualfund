import streamlit as st
import math
from scraping import scrape_reksadana_saham
from preprocessing import cleaning_data
from mcdm_method import pembobotan_roc, moora_ranking

# judul web
st.title("Sistem Pendukung Keputusan Rekomendasi Reksa Dana Saham di Bibit")

tab1, tab2, tab3 = st.tabs(["Daftar Reksa Dana", "Kriteria Seleksi", "Rekomendasi Reksa Dana"])

# menu daftar produk reksa dana
with tab1:
    st.header("Daftar Produk Reksa Dana")

    data_reksadana = scrape_reksadana_saham()

    col1_rd, col2_rd, col3_rd = st.columns(3)

    with col1_rd:
        col1_rd_data = []

    with col2_rd:
        col2_rd_data = []

    with col3_rd:
        col3_rd_data = [] 
    
    jumlah_col = 3
    for data in data_reksadana:
        for i in range (1, math.ceil(len(data_reksadana)/3)):
            for j in range(1,3):
                col{j}_rd_data.append(data)
   
# menu informasi kriteria seleksi reksa dana
with tab2:
    st.header("Informasi Kriteria Seleksi Reksa Dana")

# menu rekomendasi produk reksa dana 
with tab3:
    st.header("Rekomendasi Produk Reksa Dana")
    


