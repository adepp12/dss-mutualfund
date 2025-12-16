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

# moora
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