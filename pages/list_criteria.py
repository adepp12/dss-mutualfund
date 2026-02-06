import streamlit as st
import pandas as pd
from streamlit_extras.great_tables import great_tables
from great_tables import GT
from constant import DATA_CRITERIA

st.html(
"""
<style>
.gt_table {
    background-color: transparent !important;
    color: inherit !important;
}

.gt_col_heading {
    background-color: transparent !important;
    color: inherit !important;
    text-align: center !important;
}

</style>
""")

st.title("Daftar Kriteria Seleksi")
st.write("Berikut merupakan daftar kriteria beserta penjelasannya yang digunakan untuk pertimbangan dalam memilih produk reksa dana")

df_criteria = pd.DataFrame(DATA_CRITERIA).drop(columns=["Nama Kolom"])

table_criteria = (
    GT(df_criteria)
    .cols_align(
        align="left",
        columns=["Nama Kriteria", "Deskripsi"]
    )
    .cols_align(
        align="center",
        columns=["Satuan", "Jenis"]
    )
)

great_tables(table_criteria)  

# menggunakan markdown table, lebih cepat
# md_table = "| **Nama Kriteria** | **Deskripsi** | **Satuan** | **Jenis** |\n"
# md_table += "| --- | --- | --- | --- |\n"
# for row in DATA_CRITERIA:
#     md_table += f"| {row['Nama Kriteria']} | {row['Deskripsi']} | {row['Satuan']} | {row['Jenis']} |\n"
# st.markdown(md_table)