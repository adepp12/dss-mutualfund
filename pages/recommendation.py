import streamlit as st
import pandas as pd
from streamlit_sortables import sort_items
from function.mcdm_method import roc_weighting2, moora_ranking2
from constant import DATA_CRITERIA

st.html(
    """
    <style>
    .floating-link {
        position: fixed;
        bottom: 2.5rem;
        right: 2.5rem;
        z-index: 9999;
                
        background-color: #ff4b4b; /* Warna primary default */
        color: white !important;
        padding: 8px 16px;
        border-radius: 4px;
        text-decoration: none !important;
        font-size: 14px; /* Ukuran standar Streamlit */
    }

    @media (max-width: 768px) {
        div.st-key-priority-direction-info-container {
            display: none !important;
        }

    }

    @media (min-width: 769px) {
        div.st-key-caption-priority-info-container {
            display: none !important;
        }
    }
    </style>
    """
)

clean_df = st.session_state.clean_df
if "selected_criteria" not in st.session_state:
    st.session_state.selected_criteria = [item["Nama Kolom"] for item in DATA_CRITERIA]
if "sorted_criteria" not in st.session_state:
    st.session_state.sorted_criteria = st.session_state.selected_criteria.copy()

# gunakan key "bayangan" untuk widget, simpan ke key permanen via callback
def store_selected():
    st.session_state.selected_criteria = st.session_state._selected_criteria
    st.session_state.sorted_criteria = st.session_state.selected_criteria.copy()
# callback untuk menyimpan hasil sort
def store_sorted(new_order):
    st.session_state.sorted_criteria = new_order

st.title("Rekomendasi Reksa Dana")
st.markdown("#### :material/select_check_box: Pilih Kriteria yang Ingin Dipertimbangkan:")

# list_criteria = ['Return 1Y', 'Drawdown 1Y', 'Total AUM', 'Last NAV', 'Expense Ratio', 'Min. Pembelian']
# list_criteria = [item["Nama Kriteria"] for item in data_criteria]
list_criteria = [item["Nama Kolom"] for item in DATA_CRITERIA]

st.session_state._selected_criteria = st.session_state.selected_criteria
selected_criteria = st.multiselect("", list_criteria, key="_selected_criteria", on_change=store_selected)
# st.write("You selected:", options)

st.markdown("#### :material/sort: Urutkan Kriteria Sesuai Prioritasmu:")
with st.container(width="stretch", key="caption-priority-info-container"):
    st.caption("Urutkan dari paling penting (atas) ke paling tidak penting (bawah).") # muncul saat width layar paling kecil, karna kontainer info gk cukup

# --- dengan st.columns
col1, col2 = st.columns([3, 1], vertical_alignment="center")
with col1:
    with st.container(border=True, width="stretch"):
        # Inisialisasi daftar kriteria jika belum ada di session state
        # if "kriteria" not in st.session_state:
        #     st.session_state.kriteria = ['Return', 'Drawdown', 'Total AUM', 'Last NAV', 'Expense Ratio', 'Minimal Pembelian']

        # Menampilkan widget pengurutan
        # sort_key = f"sortable-{'-'.join(sorted(selected_criteria))}"

        # items = [{'items': options}]
        sorted_items = sort_items(items=st.session_state.sorted_criteria, direction='vertical', multi_containers=False)
        store_sorted(sorted_items)
        # sorted_items akan berisi daftar yang sudah diurutkan oleh user
        # st.write("Hasil urutan:", sorted_items)

with col2:
    with st.container(border=True, width=100, height="stretch", key="priority-direction-info-container"):
        st.write(":material/arrow_upward:")
        st.write("Prioritas Tinggi")
        st.space("stretch")
        st.write("Prioritas Rendah")
        st.write(":material/arrow_downward:")

# st.write("Hasil urutan:", sorted_items)
data = clean_df

if sorted_items:
    urutan_kriteria = sorted_items 
    # hitung bobot
    bobot_kriteria = roc_weighting2(urutan_kriteria)
    
    # menampilkan hasil pembobotan
    # st.write("**Bobot Kriteria:**")
    # for kriteria, nilai_bobot in bobot_kriteria.items():
    #     st.write(f"- {kriteria}: {nilai_bobot}")

    kriteria_dipertimbangkan = list(bobot_kriteria.keys())
    bobot_kriteria_fungsi = list(bobot_kriteria.values())

    map_jenis = {item["Nama Kolom"]: item["Jenis"] for item in DATA_CRITERIA}
    jenis_kriteria = [map_jenis[kolom] for kolom in kriteria_dipertimbangkan]

    if "moora_ranking_df" not in st.session_state:
        st.session_state.moora_ranking_df = None

    # trigger decision-making step
    if st.button("Lihat Hasil Rekomendasi :material/arrow_forward:"):
        st.session_state.moora_ranking_df = moora_ranking2(data=data, kriteria=kriteria_dipertimbangkan, jenis_kriteria=jenis_kriteria, bobot=bobot_kriteria_fungsi)

        st.toast("Rekomendasi rekda dana berhasil dibuat!", icon=":material/celebration:", duration=2)
else:
    st.error("Pilih minimal 1 (satu) kriteria untuk dipertimbangkan", icon=":material/error:")

if st.session_state.get("moora_ranking_df") is not None:
    moora_ranking_df = st.session_state.moora_ranking_df
    
    st.markdown("#### :material/leaderboard: Rekomendasi Produk Reksa Dana:")

    # container button download csv
    with st.container(horizontal=True, horizontal_alignment="right"):
        # moora_result_csv = pd.DataFrame.to_csv(moora_ranking_df, index=False).encode("utf-8")
        cols_to_exclude = ["Tanggal Peluncuran", "Min. Penjualan", "URL Detail", "Waktu Scraping"]

        moora_result_csv = (
            moora_ranking_df
            .drop(columns=cols_to_exclude, errors="ignore")  # hanya untuk output
            .to_csv(index=False)
            .encode("utf-8")
        )
        last_update = st.session_state.get("last_update", "unknown")
        st.download_button(
            label="Download Hasil Perhitungan (.csv)",
            data=moora_result_csv,
            file_name=f"hasil_perhitungan_dss_{last_update}.csv",
            mime="text/csv",
            icon=":material/download:",
            on_click="ignore"
        )
    # floating button "Atur Ulang Kriteria"
    st.markdown(
        """
        <a href="#rekomendasi-reksa-dana" class="floating-link">
            Atur Ulang Kriteria
        </a>
        """,
        unsafe_allow_html=True
    )

        # with st.container(key="tombol_floating"):
        #     st.markdown(
        #         # Tambahkan class CSS khusus ke link agar mudah distyling
        #         """
        #         <a href="#select-check-box-pilih-kriteria-yang-ingin-dipertimbangkan" class="floating-link">
        #             Atur Ulang Kriteria
        #         </a>
        #         """, 
        #         unsafe_allow_html=True
        #     )
        
        # st.html(
        #     """
        #     <style>
        #     /* 1. Target Container Utamanya */
        #     div.st-key-tombol_floating {
        #         position: fixed;            /* Agar melayang */
        #         bottom: 2.5rem;             /* Jarak dari bawah */
        #         right: 2.5rem;              /* Jarak dari kanan */
        #         z-index: 9999;              /* Selalu di paling depan */
        #         width: fit-content;         /* Lebar menyesuaikan teks */
                
        #         /* Styling Tampilan Container (seperti tombol) */
        #         background-color: var(--primary-color); /* Ikuti warna tema Streamlit */
        #         border-radius: 8px;         /* Sudut melengkung */
        #         box-shadow: 0 4px 10px rgba(0,0,0,0.2); /* Bayangan */
        #         padding: 0;                 /* Reset padding container */
        #         transition: transform 0.2s; /* Animasi halus saat hover */
        #     }

        #     /* 2. Efek Hover pada Container */
        #     div.st-key-tombol_floating:hover {
        #         transform: translateY(-5px); /* Naik sedikit saat di-hover */
        #         box-shadow: 0 6px 14px rgba(0,0,0,0.3);
        #     }

        #     /* 3. Target Link di dalam Container */
        #     a.floating-link {
        #         display: block;             /* Agar area klik memenuhi tombol */
        #         padding: 12px 20px;         /* Jarak teks ke pinggir tombol */
        #         color: white !important;    /* Warna teks putih (pakai !important biar gak ditimpa) */
        #         text-decoration: none;      /* Hilangkan garis bawah link */
        #         font-weight: 600;           /* Teks tebal */
        #         font-size: 16px;
        #     }

        #     /* 4. Hapus margin bawaan markdown paragraph (Opsional, untuk kerapihan) */
        #     div.st-key-tombol_floating p {
        #         margin-bottom: 0;
        #     }
        #     </style>
        #     """
        # )
        
    with st.container(width="stretch", horizontal_alignment="center"):
        with st.container(width="content", horizontal_alignment="center"):
            width_container_product = 1200
            for index, row in moora_ranking_df.iterrows():
                if row['Ranking'] <=5:
                    width_container_product = width_container_product - 20*int(row['Ranking'])
                with st.container(border=True, horizontal=True, horizontal_alignment="center", width=width_container_product):
                    # Mengubah rasio kolom agar Nama Produk & Skor punya ruang lebih luas
                    cols = st.columns([1, 2, 1.5, 2, 2, 1.2], vertical_alignment="center")
                        
                    # 1. Ranking dengan Circle Icon (Native)
                    with cols[0]:
                        with st.container(horizontal=False, width="content"):
                            if row['Ranking'] <= 3:
                                st.write("#### :material/thumb_up:")
                                st.markdown(f"### {row['Ranking']}")
                            else:
                                st.markdown(f"#### {row['Ranking']}")
                        
                    # 2. Nama Produk & Perusahaan (Lebih Dominan)
                    with cols[1]:
                        st.markdown(f"**{row['Nama Produk']}**")
                        st.caption(f":material/factory: {row['Perusahaan Penyedia']}")
                        
                     # 3. Skor Akhir (Gunakan st.metric agar terlihat profesional)
                    with cols[2]:
                        st.metric(label="Skor Akhir", value=f"{round(row['Skor Akhir'], 4)}")

                    # 4. Kinerja (Return & Drawdown)
                    with cols[3]:
                        ret = row['Return 1Y']
                        drw = row['Drawdown 1Y']
                            
                        # Menggunakan warna teks standar untuk tren
                        st.caption("Return | Drawdown")
                        st.write(f":material/trending_up: :{'green' if ret >=0 else 'red'}[{ret}%]")
                        st.write(f":material/trending_down: :{'red' if drw < 0 else 'green'}[{drw}%]")
                        
                    # 5. Asset & NAV
                    with cols[4]:
                        st.caption("Last NAV | Total AUM")
                        st.write(f"**Rp {row['Last NAV']}**")
                        st.write(f"**Rp {row['Total AUM']} M**")
                        
                    # 6. Tombol Aksi (Gunakan type 'primary' untuk peringkat 1-3)
                    with cols[5]:
                        # btn_type = "primary" if row['Ranking'] <= 3 else "secondary"
                        st.link_button("Detail Produk", url=row['URL Detail'], width="content")
        
        # for index, row in hasil_moora_df.iterrows():
        #     with st.container(border=True):
        #         # Mengubah rasio kolom agar Nama Produk & Skor punya ruang lebih luas
        #         cols = st.columns([0.5, 2.5, 1.5, 2, 2, 1.2], vertical_alignment="center", )
                
        #         # 1. Ranking dengan Circle Icon (Native)
        #         with cols[0]:
        #             if row['Ranking'] <= 3:
        #                 st.write("### :material/thumb_up:")
        #                 st.markdown(f"### {row['Ranking']}")
        #             else:
        #                 st.markdown(f"#### {row['Ranking']}")
                
        #         # 2. Nama Produk & Perusahaan (Lebih Dominan)
        #         with cols[1]:
        #             st.markdown(f"**{row['Nama Produk']}**")
        #             st.caption(f":material/factory: {row['Perusahaan Penyedia']}")
                
        #         # 3. Skor Akhir (Gunakan st.metric agar terlihat profesional)
        #         with cols[2]:
        #             st.metric(label="Skor Akhir", value=f"{round(row['Skor Akhir'], 4)}")

        #         # 4. Kinerja (Return & Drawdown)
        #         with cols[3]:
        #             ret = row['Return 1Y']
        #             drw = row['Drawdown 1Y']
                    
        #             # Menggunakan warna teks standar untuk tren
        #             st.caption("Return | Drawdown")
        #             st.write(f":material/trending_up: :{'green' if ret >=0 else 'red'}[{ret}%]")
        #             st.write(f":material/trending_down: :{'red' if drw < 0 else 'green'}[{drw}%]")
                    
                
        #         # 5. Asset & NAV
        #         with cols[4]:
        #             st.caption("Last NAV | Total AUM")
        #             st.write(f"**Rp {row['Last NAV']}**")
        #             st.write(f"**Rp {row['Total AUM']} M**")
                
        #         # 6. Tombol Aksi (Gunakan type 'primary' untuk peringkat 1-3)
        #         with cols[5]:
        #             btn_type = "primary" if row['Ranking'] <= 3 else "secondary"
        #             st.link_button("Detail", url=row['URL Detail'], type=btn_type, use_container_width=True)

        # for index, row in hasil_moora_df.iterrows():
        #     with st.container(border=True):
        #         cols = st.columns([1, 3, 1, 2, 2, 1], vertical_alignment="center")
        #         # rank
        #         with cols[0]:
        #             st.write(f"**{row['Ranking']}**")
                
        #         # name and company
        #         with cols[1]:
        #             st.write(f"**{row['Nama Produk']}**")
        #             st.caption(f"{row['Perusahaan Penyedia']}")
                
        #         # score
        #         with cols[2]:
        #             st.write(f"**Skor Akhir**: **{round(row['Skor Akhir'], 4)}**")

        #         # return, drawdown
        #         with cols[3]:
        #             color_return = "red" if row["Return 1Y"] < 0 else "green"
        #             st.write(f"*Return:* :{color_return}[{row['Return 1Y']}%]")
        #             color_drawdown = "red" if row["Drawdown 1Y"] < 0 else "green"
        #             st.write(f"*Drawdown:* :{color_drawdown}[{row['Drawdown 1Y']}%]")
                
        #         # NAV, total AUM
        #         with cols[4]:
        #             st.write(f"*NAV:* Rp {row['Last NAV']}")
        #             st.write(f"*Total AUM:* Rp {row['Total AUM']} M")
                
        #         # link to detail product
        #         with cols[5]:
        #             st.link_button("Detail Produk", url=row['URL Detail'])

        


    # opsi jika tidak melibatkan bobot
    # kriteria_dipertimbangkan = [item["Nama Kolom"] for item in DATA_CRITERIA]
    # jenis_kriteria = [item["Jenis"] for item in DATA_CRITERIA]


# st.page_link()


# st.page_link(home_page, label="Beranda", icon=":material/arrow_forward:")
# --- dengan st.container
# with st.container(height="content", border=True, horizontal=True, horizontal_alignment="center"):
#     with st.container(border=True, width=400):
        
#         # Inisialisasi daftar kriteria jika belum ada di session state
#         if "kriteria" not in st.session_state:
#             st.session_state.kriteria = ['Return', 'Drawdown', 'Total AUM', 'Last NAV', 'Expense Ratio', 'Minimal Pembelian']

#         # Menampilkan widget pengurutan
#         items = [
#             {'items': st.session_state.kriteria}
#         ]

#         sorted_items = sort_items(items, direction='vertical', multi_containers=True, key="sortable-item")

#     with st.container(border=True, width=100, height="stretch"):
#         st.write(":material/arrow_upward:")
#         st.write("Prioritas Tinggi")
#         st.space("stretch")
#         st.write("Prioritas Rendah")
#         st.write(":material/arrow_downward:")
#         # sorted_items akan berisi daftar yang sudah diurutkan oleh user
#         # st.write("Hasil urutan:", sorted_items)

# --- dengan column + container

# cols, = st.columns(1, vertical_alignment="center")
# with cols:
#     with st.container(border=True, width='stretch', horizontal=True, horizontal_alignment="center"):
#         # urutan kriteria
#         with st.container(border=True, width=400):
#             # Inisialisasi daftar kriteria jika belum ada di session state
#             if "kriteria" not in st.session_state:
#                 st.session_state.kriteria = ['Return', 'Drawdown', 'Total AUM', 'Last NAV', 'Expense Ratio', 'Minimal Pembelian']

#                 # Menampilkan widget pengurutan
#             items = [
#                 {'items': st.session_state.kriteria}
#             ]

#             sorted_items = sort_items(items, direction='vertical', multi_containers=True, key="sortable-item")

#             # sorted_items akan berisi daftar yang sudah diurutkan oleh user
#             # st.write("Hasil urutan:", sorted_items)
#         # keterangan urutan
#         with st.container(border=True, width=100):
#             st.write(":material/arrow_upward:")
#             st.write("Prioritas Tinggi")
#             st.space("stretch")
#             st.write("Prioritas Rendah")
#             st.write(":material/arrow_downward:")

# st.write("test-----------------")

# data_criteria = [
#     {"Nama Kriteria": "Return", "Jenis": "🟢 Benefit"},
#     {"Nama Kriteria": "Drawdown", "Jenis": "🟢 Benefit"},
#     {"Nama Kriteria": "Expense Ratio", "Jenis": "🔴 Cost"},
#     {"Nama Kriteria": "Asset Under Management (AUM)", "Jenis": "🟢 Benefit"},
#     {"Nama Kriteria": "Net Asset Value (NAV)", "Jenis": "🟢 Benefit"},
#     {"Nama Kriteria": "Minimal Pembelian", "Jenis": "🔴 Cost"}
# ]

# st.title("Filter Kriteria Reksa Dana")

# # 1. Siapkan daftar nama untuk pilihan
# list_nama = [item["Nama Kriteria"] for item in data_criteria]
# # 2. Siapkan map untuk pencarian jenis
# map_jenis = {item["Nama Kriteria"]: item["Jenis"] for item in data_criteria}

# # Widget Multiselect (User bisa memilih dan urutannya tergantung klik user)
# pilihan = st.multiselect("Pilih Kriteria (Urutan bisa acak):", options=list_nama)

# if pilihan:
#     st.write("### Hasil Pemetaan:")
#     for p in pilihan:
#         # Mencari jenis berdasarkan nama yang dipilih
#         jenis = map_jenis[p]
#         st.info(f"Kriteria: **{p}** | Jenis: **{jenis}**")


# list_criteria3 = ['Return 1Y', 'Drawdown 1Y', 'Total AUM', 'Last NAV', 'Expense Ratio', 'Min. Pembelian']
# st.dataframe(list_criteria3)

# list_criteria4 = [item["Nama Kriteria"] for item in data_criteria]
# st.dataframe(list_criteria4)