import streamlit as st
import pandas as pd

# styling responsif pada perangkat mobile
st.html(
    """
    <style>
        @media (max-width: 639px) {
            [data-testid="stLayoutWrapper"][height="420px"] {
                height: auto !important;
            }
            
            .stVerticalBlock[height="420px"] {
                height: auto !important;
            }
        }
        @media (min-width: 640px) and (max-width: 1200px) {
            .st-key-list-mutual-fund-container [data-testid="stLayoutWrapper"] {
                display: flex !important;
                flex-wrap: wrap !important;
                gap: 1rem !important;
            }
            .st-key-list-mutual-fund-container [data-testid="stColumn"] {
                flex: 0 0 calc(50% - 0.5rem) !important;
                max-width: calc(50% - 0.5rem) !important;
            }
        }
    </style>
    """
)

if "sort_label" not in st.session_state:
    st.session_state.sort_label = "Nama Reksa Dana"
if "sort_asc" not in st.session_state:
    st.session_state.sort_asc = True

def store_sort_label():
    st.session_state.sort_label = st.session_state["_sort_label"]
def store_sort_asc():
    st.session_state.sort_asc = st.session_state["_sort_asc"] == "A-Z"

st.title("Daftar Reksa Dana Saham")

clean_df = st.session_state.clean_df

col_text, col_sort, col_asc = st.columns([3, 2, 1])
with col_text:
    st.write("Data yang ditampilkan dalam periode 1 Tahun (1Y)")
    last_update = st.session_state.get("last_update", "unknown")
    st.write(f":material/update: Terakhir diperbarui pada: {last_update}")

with col_sort:
    st.session_state["_sort_label"] = st.session_state.sort_label
    sort_options = {
        "Nama Reksa Dana": "Nama Produk",
        "Return": "Return 1Y",
        "Drawdown": "Drawdown 1Y",
        "Total AUM": "Total AUM",
        "Expense Ratio": "Expense Ratio",
        "Last NAV": "Last NAV"
    }
    sort_by_label = st.selectbox("Urutkan berdasarkan:", 
                                 list(sort_options.keys()), 
                                 key="_sort_label", on_change=store_sort_label)

with col_asc:
    st.session_state["_sort_asc"] = "A-Z" if st.session_state.sort_asc else "Z-A"
    asc_label = st.radio("", ["A-Z", "Z-A"], horizontal=True, key="_sort_asc", on_change=store_sort_asc)
    ascending = asc_label == "A-Z"

sort_col = sort_options[sort_by_label]

clean_df_sorted = clean_df.sort_values(by=sort_col, ascending=ascending, ignore_index=True)

# --- logika loop baru, data terurut saat responsif
with st.container(width="stretch", key="list-mutual-fund-container"):
    cols_count = 3
    
    # Loop per baris, bukan per item
    for i in range(0, len(clean_df_sorted), cols_count):
        cols = st.columns(cols_count)
        
        # Ambil data untuk 1 baris (3 item)
        for j in range(cols_count):
            index = i + j
            if index < len(clean_df_sorted):  # Cek jika masih ada data
                row = clean_df_sorted.iloc[index]
                
                with cols[j]:
                    with st.container(border=True, height=420, vertical_alignment="distribute", horizontal_alignment="right"):
                        st.markdown(f"#### {row['Nama Produk']}")
                        st.write(row['Perusahaan Penyedia'])
                        
                        cols_in = st.columns(2)
                        with cols_in[0]:
                            color_return = "red" if row["Return 1Y"] < 0 else "green"
                            st.write(f"**Return:** :{color_return}[{row['Return 1Y']}%]")
                            color_drawdown = "red" if row["Drawdown 1Y"] < 0 else "green"
                            st.write(f"**Drawdown:** :{color_drawdown}[{row['Drawdown 1Y']}%]")
                            st.write(f"**Expense Ratio:** {row['Expense Ratio']}%")   
                            st.write(f"**Bank Penampung:** {row['Bank Penampung']}")
                        
                        with cols_in[1]:
                            st.write(f"**Total AUM:** Rp {row['Total AUM']} M")
                            st.write(f"**NAV:** Rp {row['Last NAV']}")
                            st.write(f"**Min. Pembelian:** Rp {row['Min. Pembelian']:,.0f}")
                        
                        st.link_button("Detail Produk", url=row['URL Detail'])

# --- data tidak terurut saat tampilan responsif
# with st.container(width="stretch", key="list-mutual-fund-container"):
#     cols_count = 3
#     cols = st.columns(cols_count)

#     for index, row in clean_df_sorted.iterrows():
#         with cols[index % cols_count]:
#             with st.container(border=True, height=420, vertical_alignment="distribute", horizontal_alignment="right"):
#                 # st.subheader(row['Nama Produk']) -> terlalu besar
#                 st.markdown(f"#### {row['Nama Produk']}")
#                 st.write(row['Perusahaan Penyedia'])

#                 cols_in = st.columns(2)
#                 with cols_in[0]:
#                     color_return = "red" if row["Return 1Y"] < 0 else "green"
#                     st.write(f"**Return:** :{color_return}[{row['Return 1Y']}%]")
#                     # st.write("**Return:**")
#                     # st.badge(f"{row['Return 1Y']}", color=color) -> isi kyk bg color hijau
#                     color_drawdown = "red" if row["Drawdown 1Y"] < 0 else "green"
#                     st.write(f"**Drawdown:** :{color_drawdown}[{row['Drawdown 1Y']}%]")
#                     st.write(f"**Expense Ratio:** {row['Expense Ratio']}%")   
#                     st.write(f"**Bank Penampung:** {row['Bank Penampung']}")             

#                 with cols_in[1]:
#                     st.write(f"**Total AUM:** Rp {row['Total AUM']} M")
#                     st.write(f"**NAV:** Rp {row['Last NAV']}")
#                     st.write(f"**Min. Pembelian:** Rp {row['Min. Pembelian']:,.0f}")
                
#                 st.link_button("Detail Produk", url=row['URL Detail'])