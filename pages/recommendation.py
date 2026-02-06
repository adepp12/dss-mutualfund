import streamlit as st
import pandas as pd
from streamlit_sortables import sort_items
from function.mcdm_method import roc_weighting2, moora_ranking2
from constant import DATA_CRITERIA

# styling-page
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
        div.st-key-priority-direction-info-container,
        div.st-key-pc-barchart-container {
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

if "selected_criteria" not in st.session_state:
    st.session_state.selected_criteria = [item["Nama Kolom"] for item in DATA_CRITERIA]
if "sorted_criteria" not in st.session_state:
    st.session_state.sorted_criteria = st.session_state.selected_criteria.copy()

# gunakan key "bayangan" untuk widget, simpan ke key permanen via callback
def store_selected():
    st.session_state.selected_criteria = st.session_state._selected_criteria
    st.session_state.sorted_criteria = st.session_state.selected_criteria.copy()
# callback untuk menyimpan hasil sort
def store_sorted():
    st.session_state.sorted_criteria = st.session_state._sorted_criteria

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
    st.caption("Urutkan dari paling penting (atas) ke paling tidak penting (bawah).") # muncul saat width layar paling kecil (mobile), karna kontainer info gk cukup
    st.caption("Urutkan dengan tahan kriteria beberapa saat, lalu pindahkan ke urutan yang diinginkan.")

# --- dengan st.columns
col1, col2 = st.columns([3, 1], vertical_alignment="center")
with col1:
    with st.container(border=True, width="stretch"):
        # key untuk mempertahankan posisi urutan
        sort_key = f"sortable-{'-'.join(sorted(selected_criteria))}"

        # items = [{'items': options}]
        st.session_state._sorted_criteria = st.session_state.sorted_criteria
        sorted_items = sort_items(items=st.session_state._sorted_criteria, 
                                  direction='vertical', 
                                  multi_containers=False, 
                                  key=sort_key)
        st.session_state._sorted_criteria = sorted_items
        store_sorted()
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
data = st.session_state.get("clean_df", None)

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
        if data is None:
            st.error("Tidak ada data untuk ditampilkan.", icon=":material/warning:")
        else:
            st.session_state.moora_ranking_df = moora_ranking2(data=data, kriteria=kriteria_dipertimbangkan, jenis_kriteria=jenis_kriteria, bobot=bobot_kriteria_fungsi)

            st.toast("Rekomendasi rekda dana berhasil dibuat!", icon=":material/celebration:", duration=2)
else:
    st.error("Pilih minimal 1 (satu) kriteria untuk dipertimbangkan", icon=":material/error:")

if st.session_state.get("moora_ranking_df") is not None:
    moora_ranking_df = st.session_state.moora_ranking_df
    
    st.markdown("#### :material/leaderboard: Rekomendasi Produk Reksa Dana:")

    # container preview button, download button
        # dataframe for preview, download
    columns_to_exclude = ["Tanggal Peluncuran", "Min. Penjualan", "URL Detail", "Waktu Scraping", "Bank Kustodian", "Bank Penampung"]
    moora_preview_download_df = moora_ranking_df.drop(columns=columns_to_exclude, errors="ignore")

    with st.container(horizontal=True, horizontal_alignment="right"):
        # preview-calculation-detail-button
        @st.dialog("Pratinjau Hasil Perhitungan SPK", width="large")
        def preview_calculation_table():
            # parent-container-roc-moora
            with st.container(width="content", horizontal=True, border=True):
                # container-tabel-roc
                with st.container(width="content", horizontal_alignment="center"):
                    with st.container(width="content"):
                        st.markdown("#### Tabel Bobot ROC")
                    weight_preview_df = (pd.DataFrame(list(bobot_kriteria.items()), columns=["Nama Kriteria", "Bobot ROC"]))
                    st.dataframe(
                        weight_preview_df,
                        width="content",
                        hide_index=True
                    )

                # container-tabel-moora
                with st.container(width="stretch", horizontal_alignment="center"):
                    with st.container(width="content"):
                        st.markdown("#### Tabel Perhitungan MOORA")
                    st.dataframe(moora_preview_download_df.drop(columns=["Jenis", "Tingkat Resiko"], errors="ignore"), hide_index=True, width="content")

            # barchart-moora-score
                # barchart-parent-container
            with st.container(width="stretch", border=True, horizontal_alignment="center"):
                # title-chart-container
                with st.container(width="content"):
                        st.markdown("#### Grafik Skor Akhir Perhitungan SPK")
                # set-color-barchart
                moora_preview_download_df["barchart-color"] = moora_preview_download_df["Skor Akhir"].apply(
                        lambda v: "#ff4b4b" if v < 0 else "#00c853"
                    )
                # if-device width > 769px-parent-container (pc)
                with st.container(width="stretch", key="pc-barchart-container"):  
                    st.bar_chart(
                        moora_preview_download_df,
                        x="Nama Produk",
                        y="Skor Akhir",
                        color="barchart-color",
                        sort=False,
                        x_label=None
                    )
                # if-device < 769px-parent-container (mobile)
                with st.container(width="stretch", key="mobile-barchart-container"):
                    cols_barchart = st.columns(2, border=True)
                    # top-10-barchart
                    with cols_barchart[0]:
                        st.write("Produk 10 Teratas :material/arrow_upward:")
                        st.bar_chart(
                            moora_preview_download_df.head(10),
                            x="Nama Produk",
                            y="Skor Akhir",
                            color="barchart-color",
                            sort=False
                        )
                    # bottom-10-barchart
                    with cols_barchart[1]:
                        st.write("Produk 10 Terbawah :material/arrow_downward:")
                        st.bar_chart(
                            moora_preview_download_df.tail(10),
                            x="Nama Produk",
                            y="Skor Akhir",
                            color="barchart-color",
                            sort=False
                        )

        if st.button("Pratinjau Hasil Perhitungan", icon=":material/description:"):
            preview_calculation_table()
        
        # download-csv button
        moora_result_csv = (
            moora_preview_download_df.drop(columns=["barchart-color"], errors="ignore").to_csv(index=False, sep=';', decimal=',').encode("utf-8")
        )
        last_update = st.session_state.get("last_update", "unknown")
        st.download_button(
            label="Unduh Detail Perhitungan (.csv)",
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

    # recommendation-result-container
    with st.container(width="stretch", horizontal_alignment="center"):
        with st.container(width="content", horizontal_alignment="center"):
            width_container_product = 1200
            for index, row in moora_ranking_df.iterrows():
                if row['Ranking'] <=5:
                    width_container_product = width_container_product - 20*int(row['Ranking'])
                with st.container(border=True, horizontal=True, horizontal_alignment="center", width=width_container_product):

                    cols = st.columns([1, 2, 1.5, 2, 2, 1.2], vertical_alignment="center")
                        
                    # ranking
                    with cols[0]:
                        with st.container(horizontal=True, width="content"):
                            if row['Ranking'] <= 3:
                                st.write("#### :material/thumb_up:")
                                st.markdown(f"### {row['Ranking']}")
                            else:
                                st.markdown(f"#### {row['Ranking']}")
                        
                    # nama produk, perusahaan penyedia
                    with cols[1]:
                        st.markdown(f"**{row['Nama Produk']}**")
                        st.caption(f":material/factory: {row['Perusahaan Penyedia']}")
                        
                     # skor akhir
                    with cols[2]:
                        st.metric(label="Skor Akhir", value=f"{round(row['Skor Akhir'], 4)}")

                    # return, drawdown
                    with cols[3]:
                        ret = row['Return 1Y']
                        drw = row['Drawdown 1Y']

                        st.caption("Return | Drawdown")
                        st.write(f":material/trending_up: :{'green' if ret >=0 else 'red'}[{ret}%]")
                        st.write(f":material/trending_down: :{'red' if drw < 0 else 'green'}[{drw}%]")
                        
                    # NAV, total AUM
                    with cols[4]:
                        st.caption("Last NAV | Total AUM")
                        st.write(f"**Rp {row['Last NAV']}**")
                        st.write(f"**Rp {row['Total AUM']} M**")
                        
                    # detail produk button
                    with cols[5]:
                        # btn_type = "primary" if row['Ranking'] <= 3 else "secondary"
                        st.link_button("Detail Produk", url=row['URL Detail'], width="content")