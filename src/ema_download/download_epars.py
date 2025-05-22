import os
import time
import requests
import csv

save_dir = "./data/EMA/EMA_downloads/"
os.makedirs(save_dir, exist_ok=True)

headers = {
    "User-Agent": "Mozilla/5.0"
}

def download_pdfs_from_csv(csv_path, start_line=1):
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

    csvfile.seek(0)  # Reset file pointer to the beginning
    next(reader)  # Skip the header row

    # Skip rows until the specified starting line
    for _ in range(start_line - 1):
        next(reader, None)

    try:
        idx_category = header.index("Category")
        idx_name = header.index("Name of medicine")
        idx_pdf = 38  # <-- column 39
    except ValueError:
        print("❌ Benötigte Spalten nicht gefunden.")
        csvfile.close()
        return

    row_count = start_line - 1
    download_count = 0
    for row in reader:
        row_count += 1
        if len(row) <= idx_pdf:
            print(f"❌ Zeile {row_count}: Zu wenig Spalten.")
            continue
        if row[idx_category].strip() != "Human":
            continue
        med_name_raw = row[idx_name].strip()
        # Extract name in parentheses after "previously" if present
        if "previously" in med_name_raw:
            start_idx = med_name_raw.find("previously") + len("previously")
            med_name_raw = med_name_raw[start_idx:].strip(" ()")
        med_name_url = med_name_raw.replace(" ", "-").replace("/", "-").replace("\\", "-")
        pdf_url = f"https://www.ema.europa.eu/en/documents/assessment-report/{med_name_url}-epar-public-assessment-report_en.pdf"
        file_name = f"{med_name_url}-epar-public-assessment-report_en.pdf"
        file_path = os.path.join(save_dir, file_name)
        if os.path.exists(file_path):
            continue
        try:
            resp = requests.get(pdf_url, headers=headers)
            if resp.status_code == 429:  # Too Many Requests
                print(f"⬇️ Fehler 429 (Too Many Requests) bei Zeile {row_count}. Warte 5 Minuten und versuche erneut.")
                time.sleep(300)  # Wait for 5 minutes
                row_count -= 1  # Retry the same line
                continue  # Retry the current line
            if resp.status_code == 200 and resp.content.startswith(b'%PDF'):
                with open(file_path, "wb") as f:
                    f.write(resp.content)
                time.sleep(5)
                download_count += 1
                if download_count % 50 == 0:
                    sleep_time = 60
            else:
                # Test the alternative URL if the primary URL fails
                alt_pdf_url = f"https://www.ema.europa.eu/en/documents/scientific-discussion/{med_name_url}-epar-scientific-discussion_en.pdf"
                alt_file_name = f"{med_name_url}-epar-scientific-discussion_en.pdf"
                alt_file_path = os.path.join(save_dir, alt_file_name)
                alt_resp = requests.get(alt_pdf_url, headers=headers)
                if alt_resp.status_code == 200 and alt_resp.content.startswith(b'%PDF'):
                    with open(alt_file_path, "wb") as f:
                        f.write(alt_resp.content)
                    time.sleep(5)
                    download_count += 1
                else:
                    # Test the withdrawal report URL if the alternative URL also fails
                    withdrawal_pdf_url = f"https://www.ema.europa.eu/en/documents/withdrawal-report/withdrawal-assessment-report-{med_name_url}_en.pdf"
                    withdrawal_file_name = f"{med_name_url}-withdrawal-assessment-report_en.pdf"
                    withdrawal_file_path = os.path.join(save_dir, withdrawal_file_name)
                    withdrawal_resp = requests.get(withdrawal_pdf_url, headers=headers)
                    if withdrawal_resp.status_code == 200 and withdrawal_resp.content.startswith(b'%PDF'):
                        with open(withdrawal_file_path, "wb") as f:
                            f.write(withdrawal_resp.content)
                        time.sleep(5)
                        download_count += 1
                    else:
                        print(f"❌ Fehler beim Download von {med_name_url}")
        except Exception as e:
            print(f"❌ Fehler bei {pdf_url} oder alternativer URL: {e}")
    csvfile.close()
    print(f"🔎 Verarbeitete Zeilen: {row_count}")
    print(f"⬇️ Neue Downloads: {download_count}")

def main():
    csv_path = r"./DrugFork/data/EMA/EMA_CSV_UTF8_3.csv"
    start_line = 1541  # Ensure the program skips the fist start_line - 1 lines
    download_pdfs_from_csv(csv_path, start_line)

if __name__ == "__main__":
    main()