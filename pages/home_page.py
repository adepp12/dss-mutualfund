import streamlit as st

st.title("Sistem Pendukung Keputusan Rekomendasi Reksa Dana")

st.markdown('''
Sistem Pendukung Keputusan (SPK) ini merupakan sebuah sistem yang dapat membantu pengguna, khususnya investor reksa dana, untuk memilih produk reksa dana berdasarkan perhitungan matematis yang sesuai dengan preferensi bobot kriteria investor.  

Alternatif yang tersedia merupakan produk reksa dana saham yang terdapat pada aplikasi investasi **Bibit**, yang dapat diakses pada laman [Daftar Reksa Dana Bibit](https://bibit.id/reksadana?limit=60&page=1&sort=asc&sort_by=7&tradable=1&type=1).  

Metode SPK yang digunakan pada sistem ini yaitu *Rank Order Centroid (ROC)*[[1]](https://ejournal.sidyanusa.org/index.php/jkdn/article/view/193), [[2]](https://jtiik.ub.ac.id/index.php/jtiik/article/view/9218) untuk menentukan bobot kriteria dan *Multi-Objective Optimization on the basis of Ratio Analysis (MOORA)*[[3]](https://ejournal.undiksha.ac.id/index.php/insert/article/view/59054), [[4]](https://journal.ilmudata.co.id/index.php/RIGGS/article/view/780) untuk metode pemeringkatan akhir alternatif.
''')
