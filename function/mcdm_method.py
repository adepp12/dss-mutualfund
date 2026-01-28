import numpy as np

# roc
def pembobotan_roc(daftar_prioritas):
    '''
    documentation
    '''
    jumlah_kriteria = len(daftar_prioritas)
    bobot = []
    for i in range(jumlah_kriteria):
      prioritas_kriteria = daftar_prioritas[i]
      sum = 0
      while prioritas_kriteria <= jumlah_kriteria:
        x = 1/prioritas_kriteria
        sum += x
        prioritas_kriteria += 1
      
      bobot_kriteria = sum / jumlah_kriteria
      bobot.append(bobot_kriteria)
    return bobot

def roc_weighting2(sorted_criteria):
    '''
    Menghitung bobot menggunakan metode ROC (Rank Order Centroid)
    
    Parameters:
    -----------
    sorted_criteria : list
        Daftar nama kriteria yang sudah diurutkan berdasarkan prioritas
        (index 0 = prioritas tertinggi)
    
    Returns:
    --------
    dict : Dictionary dengan key=nama kriteria, value=bobot
    
    Example:
    --------
    >>> sorted_criteria = ["Return", "Drawdown", "Total AUM"]
    >>> pembobotan_roc(sorted_criteria)
    {'Return': 0.611, 'Drawdown': 0.277, 'Total AUM': 0.111}
    '''
    # hitung bobot untuk setiap kriteria yang dipilih
    jumlah_kriteria = len(sorted_criteria)
    bobot_dict = {}
    
    for i in range(jumlah_kriteria):
        prioritas = i + 1
        sum_bobot = 0
        
        # menghitung nilai (1/1 + ... + 1/n)
        for k in range(prioritas, jumlah_kriteria + 1):
            sum_bobot += 1/k
        
        bobot_kriteria = sum_bobot / jumlah_kriteria

        bobot_dict[sorted_criteria[i]] = bobot_kriteria
    
    return bobot_dict

# moora
def moora_ranking2(data, kriteria, jenis_kriteria, bobot=None):
    '''
    Melakukan perankingan menggunakan metode MOORA
    
    Parameters:
    -----------
    data : DataFrame
        Data alternatif yang akan diranking
    kriteria : list
        Nama kolom yang dijadikan kriteria penilaian
    jenis_kriteria : list
        Jenis setiap kriteria: 'benefit' (lebih besar lebih baik) atau 'cost' (lebih kecil lebih baik)
    bobot : list, optional
        Bobot untuk setiap kriteria. Jika None, semua kriteria berbobot sama
    
    Returns:
    --------
    DataFrame
        Data asli ditambah kolom normalisasi, terbobot, dan ranking
    
    Example:
    --------
    >>> kriteria = ['Return 1Y', 'Drawdown 1Y', 'Total AUM']
    >>> jenis = ['benefit', 'cost', 'benefit']
    >>> bobot = [0.611, 0.277, 0.111]
    >>> hasil = moora_ranking2(data, kriteria, jenis, bobot)
    '''
    full_data_df = data.copy()
    kriteria_df = full_data_df[kriteria]

    # normalisasi
    normalisasi_df = kriteria_df.copy()
    normalisasi_df = normalisasi_df.add_suffix('_nor')
    
    for col in normalisasi_df.columns:
        pembagi = np.sqrt((normalisasi_df[col]**2).sum())
        normalisasi_df[col] = normalisasi_df[col] / pembagi

    # perhitungan dengan bobot
    if bobot is not None:
        terbobot_df = normalisasi_df.copy()
        # terbobot_df = terbobot_df.add_suffix('_wg')

        for i, col in enumerate(terbobot_df.columns):
            terbobot_df[col] = terbobot_df[col] * bobot[i]
        
        rename_map = {
            col: f"{col}_wg({bobot[i]})"
            for i, col in enumerate(terbobot_df.columns)
        }
        
        terbobot_df = terbobot_df.rename(columns=rename_map)

    # hitung skor preferensi
    skor = []
    list_nilai_benefit = []
    list_nilai_cost = []

    cols_benefit = [col for col, jenis in zip(terbobot_df.columns, jenis_kriteria) if "benefit" in jenis.lower()]
    cols_cost = [col for col, jenis in zip(terbobot_df.columns, jenis_kriteria) if "cost" in jenis.lower()]
    
    for i in range(len(terbobot_df)):
        nilai_benefit = terbobot_df.loc[i, cols_benefit].sum()
        list_nilai_benefit.append(nilai_benefit)

        nilai_cost = terbobot_df.loc[i, cols_cost].sum()
        list_nilai_cost.append(nilai_cost)

        nilai_yi = nilai_benefit - nilai_cost
        
        skor.append(nilai_yi)

    # hasil pemeringkatan
    full_data_df = full_data_df.join(normalisasi_df)
    full_data_df = full_data_df.join(terbobot_df)
    full_data_df["Nilai Benefit"] = list_nilai_benefit
    full_data_df["Nilai Cost"] = list_nilai_cost
    full_data_df["Skor Akhir"] = skor
    full_data_df["Ranking"] = full_data_df["Skor Akhir"].rank(ascending=False).astype(int)
    full_data_df = full_data_df.sort_values("Ranking")

    return full_data_df

def moora_ranking(data, jenis_kriteria, bobot=None):
    '''
    documentation
    '''
    dataset_df = data.copy()
    nama_produk_df = dataset_df[[dataset_df.columns[0]]]
    kriteria_df = dataset_df.drop(columns=dataset_df.columns[0])

    # normalisasi
    normalisasi_df = kriteria_df.copy()
    for col in kriteria_df.columns:
        pembagi = np.sqrt((kriteria_df[col]**2).sum())
        normalisasi_df[col] = kriteria_df[col] / pembagi

    # perhitungan dengan bobot
    if bobot is not None:
        for i, col in enumerate(kriteria_df.columns):
            normalisasi_df[col] = normalisasi_df[col] * bobot[i]

    # hitung skor preferensi
    skor = []
    for i in range(len(normalisasi_df)):
        nilai_benefit = normalisasi_df.iloc[i][[j for j in range(len(jenis_kriteria)) if jenis_kriteria[j] == "benefit"]].sum()
        nilai_cost = normalisasi_df.iloc[i][[j for j in range(len(jenis_kriteria)) if jenis_kriteria[j] == "cost"]].sum()
        skor.append(nilai_benefit - nilai_cost)

    # hasil pemeringkatan
    hasil_df = nama_produk_df.copy()
    hasil_df["Skor Akhir"] = skor
    hasil_df["Ranking"] = hasil_df["Skor Akhir"].rank(ascending=False).astype(int)
    hasil_df = hasil_df.sort_values("Ranking")

    return hasil_df