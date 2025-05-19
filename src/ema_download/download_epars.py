import os
import time
import requests
import csv

save_dir = "./data/EMA/EMA_downloads/"
os.makedirs(save_dir, exist_ok=True)

headers = {
    "User-Agent": "Mozilla/5.0"
}

def download_pdfs_from_csv(csv_path):
    if not os.path.exists(csv_path):
        print(f"❌ CSV-Datei nicht gefunden: {csv_path}")
        return
    try:
        csvfile = open(csv_path, newline='', encoding='utf-8')
        reader = csv.reader(csvfile, delimiter=';')
    except UnicodeDecodeError:
        csvfile = open(csv_path, newline='', encoding='latin1')
        reader = csv.reader(csvfile, delimiter=';')
    for header in reader:
        if header and "Category" in header and "Name of medicine" in header:
            break
    else:
        print("❌ Headerzeile mit 'Category' und 'Name of medicine' nicht gefunden.")
        csvfile.close()
        return
    try:
        idx_category = header.index("Category")
        idx_name = header.index("Name of medicine")
        idx_pdf = 38  # <-- Spalte 39
    except ValueError:
        print("❌ Benötigte Spalten nicht gefunden.")
        csvfile.close()
        return

    row_count = 0
    download_count = 0
    for row in reader:
        row_count += 1
        if len(row) <= idx_pdf:
            print(f"❌ Zeile {row_count}: Zu wenig Spalten.")
            continue
        if row[idx_category].strip() != "Human":
            continue
        med_name_raw = row[idx_name].strip()
        med_name_url = med_name_raw.replace(" ", "-").replace("/", "-").replace("\\", "-")
        pdf_url = f"https://www.ema.europa.eu/en/documents/assessment-report/{med_name_url}-epar-public-assessment-report_en.pdf"
        file_name = f"{med_name_url}-epar-public-assessment-report_en.pdf"
        file_path = os.path.join(save_dir, file_name)
        if os.path.exists(file_path):
            continue
        try:
            resp = requests.get(pdf_url, headers=headers)
            if resp.status_code == 200 and resp.content.startswith(b'%PDF'):
                with open(file_path, "wb") as f:
                    f.write(resp.content)
                time.sleep(1)
                download_count += 1
            else:
                print(f"❌ Fehler beim Download von {pdf_url} (Status: {resp.status_code})")
        except Exception as e:
            print(f"❌ Fehler bei {pdf_url}: {e}")
    csvfile.close()
    print(f"🔎 Verarbeitete Zeilen: {row_count}")
    print(f"⬇️ Neue Downloads: {download_count}")

def main():
    csv_path = r"./data/EMA/EMA_UTF8.csv"
    download_pdfs_from_csv(csv_path)

if __name__ == "__main__":
    main()