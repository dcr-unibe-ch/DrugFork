import os
import csv
import requests
import pandas as pd
import time

# 🚩 Dateipfad zur FDA-Produktedatei (UTF-8)
PRODUCTS_CSV = "./data/FDA/Products_all_columns.csv"
# 📁 Speicherort für PDFs
DOWNLOAD_DIR = "./data/FDA/FDA_PharmTox_byPattern/"
# 📄 Log-Dateien
MISSING_CSV = "./data/FDA/FDA_PharmTox_downloads/missing_nonclinical_urls.csv"
SUCCESS_CSV = "./data/FDA/FDA_PharmTox_downloads/successful_nonclinical_urls.csv"

# 🔍 Alle möglichen Endungen für non-klinische Dokumente
CANDIDATE_SUFFIXES = [
    "PharmR.pdf",
    "ToxR.pdf",
    "nonclinical.pdf",
    "nonclinical-review.pdf",
    "tox-review.pdf",
    "pharmtox.pdf",
    "pharmtox-review.pdf",
    "toxreview.pdf",
    "nonclinrev.pdf",
    "pharmtoxrev.pdf",
    "nonclin_review.pdf",
    "toxrev.pdf",
    "PharmtoxR.pdf",
]

def read_products_file(csv_path):
    try:
        df = pd.read_csv(csv_path, encoding="utf-8", sep=None, engine="python")
        return df
    except Exception as e:
        print(f"❌ Fehler beim Einlesen von {csv_path}: {e}")
        return pd.DataFrame()

def try_download_nonclinical_docs(df):
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    os.makedirs(os.path.dirname(MISSING_CSV), exist_ok=True)

    if "ApplNo" not in df.columns:
        print(f"❌ Spalte 'ApplNo' nicht gefunden. Verfügbare Spalten: {df.columns.tolist()}")
        return [], []

    appl_numbers = df["ApplNo"].dropna().unique()
    print(f"\n🔍 Einträge geladen: {len(appl_numbers)}")

    failed = []
    successful = []
    base_url = "https://www.accessdata.fda.gov/drugsatfda_docs/nda"

    for raw_appl in appl_numbers:
        appl = str(raw_appl).strip()
        found = False
        for suffix in CANDIDATE_SUFFIXES:
            url = f"{base_url}/0000/{appl}Orig1s000{suffix}"
            file_name = f"{appl}_{suffix}"
            file_path = os.path.join(DOWNLOAD_DIR, file_name)

            try:
                response = requests.get(url, timeout=15)
                if response.status_code == 200 and response.content.startswith(b"%PDF"):
                    with open(file_path, "wb") as f:
                        f.write(response.content)
                    print(f"📥 Erfolgreich: {file_name}")
                    successful.append({"ApplNo": appl, "URL": url, "Status": "OK"})
                    found = True
                    time.sleep(1)
                    break
            except Exception as e:
                print(f"⚠️ Fehler für {url}: {e}")
                continue

        if not found:
            failed.append({"ApplNo": appl, "TriedSuffixes": "|".join(CANDIDATE_SUFFIXES)})

    return failed, successful

def write_results(failed, successful):
    if failed:
        pd.DataFrame(failed).to_csv(MISSING_CSV, index=False, encoding="utf-8")
        print(f"⚠️ Fehlgeschlagene Downloads gespeichert in: {MISSING_CSV}")
    else:
        print("✅ Keine fehlgeschlagenen URLs.")

    if successful:
        pd.DataFrame(successful).to_csv(SUCCESS_CSV, index=False, encoding="utf-8")
        print(f"📄 Erfolgreiche Downloads gespeichert in: {SUCCESS_CSV}")
    else:
        print("📁 Erfolgreiche Downloads: 0")

def main():
    df = read_products_file(PRODUCTS_CSV)
    if df.empty:
        return
    failed, successful = try_download_nonclinical_docs(df)
    write_results(failed, successful)

if __name__ == "__main__":
    main()