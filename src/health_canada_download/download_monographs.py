import os
import time
import requests

# Zielverzeichnis für gespeicherte PDFs
save_dir = "./data/HealthCanada/ProductMonographs/"
os.makedirs(save_dir, exist_ok=True)

# HTTP-Header (für respektvolles Crawlen)
headers = {
    "User-Agent": "Mozilla/5.0"
}

# Funktion zum Einlesen der DINs aus drug.txt (Spalte 4)
def read_dins_from_drugtxt(drugtxt_path):
    if not os.path.exists(drugtxt_path):
        print(f"❌ Datei nicht gefunden: {drugtxt_path}")
        return []

    dins = set()
    with open(drugtxt_path, encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split(',')  # Kommagetrennte Datei
            if len(parts) > 3:
                raw_din = parts[3].strip().strip('"')  # Spalte 4
                if raw_din.isdigit():
                    din = raw_din.zfill(8)  # immer 8-stellig
                    dins.add(din)
    return sorted(dins)

# Funktion zum Herunterladen der PDFs
def download_healthcanada_pdfs(dins):
    download_count = 0
    for i, din in enumerate(dins, start=1):
        pdf_url = f"https://pdf.hres.ca/dpd_pm/{din}.PDF"
        file_path = os.path.join(save_dir, f"{din}.PDF")

        if os.path.exists(file_path):
            continue  # Datei bereits vorhanden

        try:
            resp = requests.get(pdf_url, headers=headers)
            if resp.status_code == 200 and resp.content.startswith(b'%PDF'):
                with open(file_path, "wb") as f:
                    f.write(resp.content)
                download_count += 1
                print(f"⬇️ ({i}) Erfolgreich: {din}")


            elif resp.status_code == 429:
                print(f"❌ ({i}) Zu viele Anfragen, warte 60 Sekunden...")
                time.sleep(60)  # Wartezeit bei Rate-Limiting
                i = i - 1  # Wiederhole die aktuelle DIN nach der Wartezeit
                continue  # Nächste DIN nach der Wartezeit
            else:
                print(f"❌ ({i}) Kein PDF gefunden für DIN {din}")
        except Exception as e:
            print(f"❌ ({i}) Fehler beim Abruf von {din}: {e}")

        time.sleep(1)  # kurze Pause für Netzhygiene

    print(f"\n🔎 Verarbeitete DINs: {len(dins)}")
    print(f"⬇️ Neue Downloads: {download_count}")

# Hauptfunktion
def main():
    drugtxt_path = "./data/HealthCanada/allfiles/drug.txt"
    dins = read_dins_from_drugtxt(drugtxt_path)
    print(f"🔎 {len(dins)} DINs gefunden.")
    download_healthcanada_pdfs(dins)

# Ausführung
if __name__ == "__main__":
    main()