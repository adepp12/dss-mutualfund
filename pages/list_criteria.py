import streamlit as st
import pandas as pd
from streamlit_extras.great_tables import great_tables
from great_tables import GT

st.title("Daftar Kriteria Seleksi")
st.write("Berikut merupakan daftar kriteria beserta penjelasannya yang digunakan untuk pertimbangan dalam memilih produk reksa dana")

data_criteria = [
    {
        "Nama Kriteria": "Return",
        "Deskripsi": "Total keuntungan yang diperoleh reksa dana",
        "Satuan": "Persen (%)",
        "Jenis": "🟢 Benefit"
    },
    {
        "Nama Kriteria": "Drawdown",
        "Deskripsi": "Penurunan terbesar yang pernah terjadi pada reksa dana dalam periode waktu tertentu",
        "Satuan": "Persen (%)",
        "Jenis": "🟢 Benefit"
    },
    {
        "Nama Kriteria": "Expense Ratio",
        "Deskripsi": "Biaya pengelolaan reksa dana oleh Manajer Investasi, mencakup biaya transaksi, biaya manajemen, biaya kustodian, dan lainnya",
        "Satuan": "Persen (%)",
        "Jenis": "🔴 Cost"
    },
    {
        "Nama Kriteria": "Asset Under Management (AUM)",
        "Deskripsi": "Total dana yang dikelola oleh Manajer Investasi pada suatu reksa dana",
        "Satuan": "Miliar (M) / Triliun (T) Rupiah",
        "Jenis": "🟢 Benefit"
    },
    {
        "Nama Kriteria": "Net Asset Value (NAV)",
        "Deskripsi": "Nilai pasar atau harga bersih reksa dana saat ini yang dihitung dan diperbarui setiap hari kerja. Kenaikan NAV mencerminkan potensi keuntungan dari reksa dana tersebut",
        "Satuan": "Ribu Rupiah",
        "Jenis": "🟢 Benefit"
    },
    {
        "Nama Kriteria": "Minimal Pembelian",
        "Deskripsi": "Jumlah minimal nilai pembelian reksa dana pada satu kali transaksi",
        "Satuan": "Ribu Rupiah",
        "Jenis": "🔴 Cost"
    }
]

df_criteria = pd.DataFrame(data_criteria)

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

great_tables(table_criteria)