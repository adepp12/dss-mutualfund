# import requests
from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from datetime import datetime
import pytz
import pandas as pd

def scrape_reksadana_saham():
    '''
    documentation
    .
    .
    '''
    
    url = "https://bibit.id/reksadana?limit=60&page=1&sort=asc&sort_by=7&tradable=1&type=1"

    # inisialisasi webdriver (Chrome)
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # jalankan Chrome tanpa GUI
    options.add_argument('--no-sandbox') # bypass OS security model

    driver = webdriver.Chrome(options=options)

    # buka halaman
    driver.get(url)

    # tunggu tabel muncul maksimal 10 detik
    # try:
    #     tabel = WebDriverWait(driver, 10).until(
    #         EC.presence_of_element_located((By.CLASS_NAME, "ContentReksaDana_table-reksadana__db5Lt"))
    #     )
    #     print("Tabel ditemukan!")
    # except:
    #     print("Tabel tidak ditemukan dalam 10 detik.")
    #     driver.quit()
    #     exit()

    # ambil HTML setelah tabel dimuat
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    tabel = soup.find("table", class_="ContentReksaDana_table-reksadana__db5Lt")

    if tabel:  # proceed only if the table is found
        # ambil semua baris data dalam <tbody>
        rows = tabel.find("tbody").find_all("tr")

        # simpan data ke list
        data = []

        for row in rows:
            cols = row.find_all("td")  # ambil semua kolom dalam baris

            # ambil data dari setiap kolom
            nama_reksadana = cols[0].find("a").text.strip()
            # jenis = cols[1].text.strip()
            # return_1d = cols[2].text.strip()
            # return_1m = cols[3].text.strip()
            # return_3m = cols[4].text.strip()
            # return_ytd = cols[5].text.strip()
            return_1y = cols[6].text.strip()
            # return_3y = cols[7].text.strip()
            # return_5y = cols[8].text.strip()
            # return_10y = cols[9].text.strip()
            last_nav = cols[10].text.strip()
            drawdown_1y = cols[11].text.strip()
            aum = cols[12].text.strip()

            # Simpan ke list
            data.append([nama_reksadana, return_1y, drawdown_1y, aum, last_nav])

        # Simpan informasi waktu scraping
        time_zone = pytz.timezone("Asia/Makassar")
        record_time = datetime.now(time_zone).strftime("%d %B %Y")

        # simpan data ke dalam DataFrame
        columns = ["Nama Produk", "Return", "Drawdown", "Total AUM", "Last NAV"]
        df = pd.DataFrame(data, columns=columns)

    driver.quit()

    return df