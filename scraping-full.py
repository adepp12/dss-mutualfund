import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import pytz
from datetime import datetime
import os # Untuk membuat direktori jika diperlukan

# konfigurasi WebDriver
def scraping_reksadana_saham():
    '''
    documentation
    .
    '''
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')       # jalankan Chrome tanpa GUI
    #  options.add_argument('--no-sandbox')     # Bypass OS security model - tidak perlu
    options.add_argument('--disable-dev-shm-usage') # Perbaikan untuk lingkungan Linux - opsional untuk keamanan
    options.add_argument('--disable-gpu')    # matikan GPU hardware acceleration
    options.add_argument('--window-size=1920,1080') # menentukan ukuran jendela browser

    driver = webdriver.Chrome(options=options)

    base_url = "https://bibit.id"
    list_url = f"{base_url}/reksadana?limit=60&page=1&sort=asc&sort_by=7&tradable=1&type=1"

    all_products_data = [] # list menyimpan data lengkap dari semua produk rd

    try:
        print(f"\nMemulai proses scraping..")
        driver.get(list_url)

        # --- Tunggu hingga tabel daftar produk dimuat ---
        try:
            WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.CLASS_NAME, "ContentReksaDana_table-reksadana__db5Lt"))
            )
            time.sleep(3) # Beri waktu ekstra untuk memastikan semua elemen child di render
            # print("✅ Tabel daftar produk ditemukan dan dimuat.")
        except:
            print("Tabel daftar produk tidak ditemukan atau tidak dimuat dalam 20 detik. Menghentikan script.")
            driver.quit()
            exit()

        html_list_page = driver.page_source
        soup_list = BeautifulSoup(html_list_page, "html.parser")

        table = soup_list.find("table", class_="ContentReksaDana_table-reksadana__db5Lt")

        if not table:
            print("Error: Objek tabel tidak ditemukan. Menghentikan script.")
            driver.quit()
            exit()

        rows = table.find("tbody").find_all("tr")
        print(f"Ditemukan {len(rows)} produk Reksa Dana Saham..")

        # --- 2. Ekstraksi Data Ringkasan dan URL Detail ---
        temp_product_summaries = []
        for i, row in enumerate(rows):
            cols = row.find_all("td")

            try:
                nama_reksadana = cols[0].find("a").text.strip()
                relative_link = cols[0].find("a")['href']
                full_detail_url = f"{base_url}{relative_link}"

                summary_data = {
                    "Nama Produk": nama_reksadana,
                    "Jenis": cols[1].text.strip(),
                    # "1D": cols[2].get_text(strip=True),
                    # "1M": cols[3].get_text(strip=True),
                    # "3M": cols[4].get_text(strip=True),
                    # "YTD": cols[5].get_text(strip=True),
                    "1Y": cols[6].get_text(strip=True),
                    # "3Y": cols[7].get_text(strip=True),
                    # "5Y": cols[8].get_text(strip=True),
                    # "10Y": cols[9].get_text(strip=True),
                    "Last NAV": cols[10].get_text(strip=True),
                    "Drawdown 1Y": cols[11].get_text(strip=True),
                    # "Total AUM": cols[12].get_text(strip=True),
                    "URL Detail": full_detail_url
                }

                temp_product_summaries.append(summary_data)

            except Exception as e:
                print(f"Error mengambil ringkasan produk di baris {i+1}: {e}")
                continue

        # print(f"Total {len(temp_product_summaries)} link detail produk berhasil dikumpulkan.")

        # --- 3. Mengunjungi Setiap Halaman Detail Produk dan Scraping Data Tambahan ---
        # print(f"\n--- Tahap 2: Mengumpulkan Data Detail Produk Tambahan ---")
        total_products = len(temp_product_summaries) # opsional - untuk bar progress scraping

        for i, product_summary in enumerate(temp_product_summaries):
        # for i, product_summary in enumerate(tqdm(temp_product_summaries, desc="Scraping Detail Produk")): # loading bar, yg bener di atas
            detail_url = product_summary["URL Detail"]
            product_name_from_summary = product_summary["Nama Produk"]

            # Mengganti print biasa dengan progress bar
            # print(f"\r[{i+1}/{total_products}] Mengunjungi detail '{product_name_from_summary}'...", end="")
            print(f"\rMemproses detail {i+1} dari {total_products} produk...", end="")
            # sys.stdout.flush() # Penting untuk memastikan output langsung terlihat
            # print(f"[{i+1}/{len(temp_product_summaries)}] Mengunjungi detail '{product_name_from_summary}' di: {detail_url}")

            current_product_full_data = product_summary.copy() # Salin data ringkasan

            try:
                driver.get(detail_url)

                # Tunggu elemen nama produk di header muncul dan terlihat di halaman detail
                WebDriverWait(driver, 15).until(
                    EC.visibility_of_element_located((By.CLASS_NAME, "HeaderStlye_header-title-text__nWH6S"))
                )
                time.sleep(2) # Jeda ekstra setelah halaman dimuat

                html_detail_page = driver.page_source
                soup_detail = BeautifulSoup(html_detail_page, "html.parser")

                # class header
                header_box = soup_detail.find("div", class_="reksadana-card-box HeaderStlye_header-container__SS5eL")
                if header_box:
                    # ambil data Perusahaan Penyedia
                    company_tag = header_box.find("div", class_="HeaderStlye_header-title-text-desc__LE0Ff")
                    if company_tag:
                        current_product_full_data["Perusahaan Penyedia"] = company_tag.get_text(strip=True)
                    else:
                        current_product_full_data["Perusahaan Penyedia"] = "N/A"
                    # ambil data Total AUM
                    aum_text_label = header_box.find("div", class_="HeaderStlye_header-title-right-text__Fonfc", string=lambda text: "Total AUM" in text if text else False)
                    if aum_text_label:
                        total_aum_tag = aum_text_label.find_next_sibling("div", class_="HeaderStlye_header-title-right-text-value__p3wlc")
                        if total_aum_tag:
                            current_product_full_data["Total AUM"] = total_aum_tag.get_text(strip=True)
                        else:
                            current_product_full_data["Total AUM"] = "N/A" 
                    else:
                        current_product_full_data["Total AUM"] = "N/A"
                else:
                    current_product_full_data["Perusahaan Penyedia"] = "N/A"
                    current_product_full_data["Total AUM"] = "N/A"

                # ekstraksi data dari Detail Produk (Tingkat Resiko, Expense Ratio, Tgl Peluncuran, Min Pembelian, Min Penjualan, Bank Kustodian, Bank Penampung)
                detail_box = soup_detail.find("div", class_="reksadana-card-box DetailProductStyle_detail-produk-container__nSje6")
                if detail_box:
                    detail_items = detail_box.find_all("div", class_="DetailProductStyle_detail-produk-body-item__2cxm1")

                    for item in detail_items:
                        key_tag = item.find("div", class_="DetailProductStyle_detail-produk-header-tag__wLjST")
                        value_tag = item.find("div", class_="DetailProductStyle_detail-produk-header-tag-label__ZtDrq")

                        if key_tag and value_tag:
                            key = key_tag.get_text(strip=True).replace(" ", "").replace("\n", "")
                            value = value_tag.get_text(strip=True)

                            if "TingkatResiko" in key:
                                current_product_full_data["Tingkat Resiko"] = value
                            elif "ExpenseRatio" in key:
                                current_product_full_data["Expense Ratio"] = value
                            elif "TanggalPeluncuran" in key:
                                current_product_full_data["Tanggal Peluncuran"] = value
                            elif "Min.Pembelian" in key:
                                current_product_full_data["Min. Pembelian"] = value
                            elif "Min.Penjualan" in key:
                                current_product_full_data["Min. Penjualan"] = value
                            elif "BankKustodian" in key:
                                current_product_full_data["Bank Kustodian"] = value
                            elif "BankPenampung" in key:
                                current_product_full_data["Bank Penampung"] = value

                # nilai default jika data tidak ditemukan
                current_product_full_data.setdefault("Tingkat Resiko", "N/A")
                current_product_full_data.setdefault("Expense Ratio", "N/A")
                current_product_full_data.setdefault("Tanggal Peluncuran", "N/A")
                current_product_full_data.setdefault("Min. Pembelian", "N/A")
                current_product_full_data.setdefault("Min. Penjualan", "N/A")
                current_product_full_data.setdefault("Bank Kustodian", "N/A")
                current_product_full_data.setdefault("Bank Penampung", "N/A")

                all_products_data.append(current_product_full_data)
                time.sleep(1.5) # jeda antar permintaan

            except Exception as e:
                print(f"Error saat scraping halaman detail untuk '{product_name_from_summary}' ({detail_url}): {e}")
                
                # jika ada error, set kolom detail yang baru dengan 'Error'
                error_keys = [
                    "Perusahaan Penyedia", "Total AUM","Tingkat Resiko", "Expense Ratio", "Tanggal Peluncuran",
                    "Min. Pembelian", "Min. Penjualan", "Bank Kustodian", "Bank Penampung"
                ]
                for key in error_keys:
                    current_product_full_data.setdefault(key, "Error")
                all_products_data.append(current_product_full_data)


    except Exception as e:
        print(f"Terjadi kesalahan umum pada proses scraping: {e}")
    finally:
        driver.quit() # Pastikan browser ditutup di akhir
        print("\nProses scraping selesai.")

    # menyimpan data dalam DataFrame
    df = pd.DataFrame(all_products_data)

    # simpan informasi waktu scraping
    time_zone = pytz.timezone("Asia/Makassar")
    record_time = datetime.now(time_zone).strftime("%d %B %Y %H:%M:%S")
    df['Waktu Scraping'] = record_time

    # reorder kolom
    desired_order = [
            "Nama Produk", "Perusahaan Penyedia", "Jenis", "Tingkat Resiko",
            "Total AUM", "Last NAV", "1Y",
            "Drawdown 1Y", "Expense Ratio", "Tanggal Peluncuran",
            "Min. Pembelian", "Min. Penjualan", "Bank Kustodian",
            "Bank Penampung", "URL Detail", "Waktu Scraping"
    ]

    final_columns = [col for col in desired_order if col in df.columns]
    df = df[final_columns]

    return df

        # print("\n✅ Data Reksa Dana Saham berhasil di-scrape:")
        # print(df) # Tampilkan beberapa baris pertama
        # print(f"\nTotal {len(df)} produk dengan detail lengkap ditemukan.")

        # Menggunakan waktu saat ini untuk nama file (WITA timezone)
        # current_time_wita = datetime.now(pytz.timezone("Asia/Makassar"))
        # timestamp = current_time_wita.strftime("%Y%m%d_%H%M%S")
        # output_filename = f"reksadana_saham_bibit_lengkap_{timestamp}.csv"

        # Pastikan direktori 'data_reksadana' ada (opsional, jika ingin menyimpan di subfolder)
        # output_dir = "data_reksadana"
        # os.makedirs(output_dir, exist_ok=True)
        # output_filepath = os.path.join(output_dir, output_filename)
        # df.to_csv(output_filepath, index=False)

        # df.to_csv(output_filename, index=False) # Simpan langsung di direktori saat ini
        # print(f"\nData lengkap telah disimpan ke '{output_filename}'")