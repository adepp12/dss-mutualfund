import streamlit as st
import pandas as pd
from function.preprocessing import cleaning_data

st.title("Daftar Reksa Dana Saham")

url_dataset = "https://raw.githubusercontent.com/adepp12/test-csv-mutualfund/refs/heads/main/latest.csv"
dataset_df = pd.read_csv(url_dataset)
clean_df = cleaning_data(dataset_df)
st.session_state["clean_df"] = clean_df

col_text, col_sort, col_asc = st.columns([3, 2, 1])
with col_text:
    st.write("Data yang ditampilkan dalam periode 1 Tahun (1Y)")
    last_update = pd.to_datetime(clean_df['Waktu Scraping'][0]).strftime('%d %B %Y')
    st.write(f":material/update: Terakhir diperbarui pada: {last_update}")

with col_sort:
    sort_options = {
        "Nama Reksa Dana": "Nama Produk",
        "Return": "Return 1Y",
        "Drawdown": "Drawdown 1Y",
        "Total AUM": "Total AUM",
        "Expense Ratio": "Expense Ratio",
        "Last NAV": "Last NAV"
    }
    sort_by_label = st.selectbox("Urutkan berdasarkan:", list(sort_options.keys()))

with col_asc:
    ascending = st.radio("", ["A-Z", "Z-A"], horizontal=True) == "A-Z"


# with st.container(horizontal=True):
#     st.write("Data yang ditampilkan dalam periode 1 Tahun (1Y)")
#     cols1, cols2 = st.columns(2, border=True)
#     with cols1:
#         sort_options = {
#             "Nama Reksa Dana": "Nama Produk",
#             "Return": "Return 1Y",
#             "Drawdown": "Drawdown 1Y",    
#             "Total AUM": "Total AUM",
#             "Expense Ratio": "Expense Ratio",
#             "Last NAV": "Last NAV"
#         }
#         sort_by_label = st.selectbox("Urutkan berdasarkan:", list(sort_options.keys()))
#     with cols2:
#             ascending = st.radio("", ["A-Z", "Z-A"], horizontal=True) == "A-Z"

sort_col = sort_options[sort_by_label]

clean_df_sorted = clean_df.sort_values(
    by=sort_col,
    ascending=ascending,
    ignore_index=True,
)

cols_count = 3
cols = st.columns(cols_count)

for index, row in clean_df_sorted.iterrows():
    with cols[index % cols_count]:
        with st.container(border=True, height=420, vertical_alignment="distribute", horizontal_alignment="right"):
            # st.subheader(row['Nama Produk']) -> terlalu besar
            st.markdown(f"#### {row['Nama Produk']}")
            st.write(row['Perusahaan Penyedia'])

            cols_in = st.columns(2)
            with cols_in[0]:
                color_return = "red" if row["Return 1Y"] < 0 else "green"
                st.write(f"**Return:** :{color_return}[{row['Return 1Y']}%]")
                # st.write("**Return:**")
                # st.badge(f"{row['Return 1Y']}", color=color) -> isi kyk bg color hijau
                color_drawdown = "red" if row["Drawdown 1Y"] < 0 else "green"
                st.write(f"**Drawdown:** :{color_drawdown}[{row['Drawdown 1Y']}%]")
                st.write(f"**Expense Ratio:** {row['Expense Ratio']}%")   
                st.write(f"**Bank Penampung:** {row['Bank Penampung']}")             

            with cols_in[1]:
                st.write(f"**Total AUM:** Rp {row['Total AUM']} M")
                st.write(f"**NAV:** Rp {row['Last NAV']}")
                st.write(f"**Min. Pembelian:** Rp {row['Min. Pembelian']}")
            
            st.link_button("Detail Produk", url=row['URL Detail'])