import os
import json
import requests
from bs4 import BeautifulSoup

# --------------- Einstellungen ---------------
JSON_PATH = "data/FDA/drugs@fda_openFDA.json"
SAVE_DIR = "data/FDA/FDA_nonclinical/"

FILTER_KEYWORDS = [
    "pharm", "tox", "pharmtox", "nonclin", "nonclinical",
    "pharmacology", "toxicology", "nonclinical-evaluation",
    "pharm-tox", "pharm_tox", "review-of-pharmacology", "carcinogenicity"
]

BASE_URL = "https://www.accessdata.fda.gov/drugsatfda_docs/nda"

os.makedirs(SAVE_DIR, exist_ok=True)

# --------------- Funktionen ---------------

def extract_ndas_blas_from_json(json_path):
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    app_nos = set()
    for entry in data.get("results", []):
        app_no = entry.get("application_number", "")
        if app_no.startswith("NDA") or app_no.startswith("BLA"):
            app_nos.add(app_no.replace("NDA", "").replace("BLA", "").zfill(6))
    
    return sorted(app_nos)

def find_toc_url(app_no):
    suffixes = ["Orig1s000TOC.cfm", "Orig1s001TOC.cfm", "Orig2s000TOC.cfm"]
    for suffix in suffixes:
        toc_url = f"{BASE_URL}/{app_no}{suffix}"
        resp = requests.head(toc_url)
        if resp.status_code == 200:
            return toc_url
    return None

def extract_pdf_links(toc_url):
    try:
        resp = requests.get(toc_url)
        soup = BeautifulSoup(resp.content, "html.parser")
        links = soup.find_all("a", href=True)

        pdf_links = []
        for link in links:
            href = link["href"]
            if href.lower().endswith(".pdf"):
                if any(kw in href.lower() for kw in FILTER_KEYWORDS):
                    full_url = f"https://www.accessdata.fda.gov{href}" if href.startswith("/") else href
                    pdf_links.append(full_url)
        return pdf_links
    except Exception as e:
        print(f"⚠️ Fehler beim Parsen von {toc_url}: {e}")
        return []

def download_pdf(url, save_dir):
    filename = os.path.basename(url)
    save_path = os.path.join(save_dir, filename)

    if os.path.exists(save_path):
        return False  # bereits vorhanden

    try:
        resp = requests.get(url)
        if resp.status_code == 200 and resp.content.startswith(b"%PDF"):
            with open(save_path, "wb") as f:
                f.write(resp.content)
            return True
    except Exception as e:
        print(f"❌ Fehler beim Download von {url}: {e}")
    
    return False

# --------------- Hauptprogramm ---------------

def main():
    app_nos = extract_ndas_blas_from_json(JSON_PATH)
    print(f"🔍 {len(app_nos)} NDA-Applikationen gefunden.")

    for app_no in app_nos:
        toc_url = find_toc_url(app_no)
        if not toc_url:
            print(f"⚠️ NDA{app_no}: TOC nicht gefunden")
            continue

        pdf_links = extract_pdf_links(toc_url)
        if not pdf_links:
            print(f"⚠️ NDA{app_no}: keine passenden PDF-Links gefunden")
            continue

        for url in pdf_links:
            success = download_pdf(url, SAVE_DIR)
            if success:
                print(f"⬇️ {os.path.basename(url)} heruntergeladen")
            else:
                print(f"⚠️ {os.path.basename(url)} übersprungen oder fehlgeschlagen")

if __name__ == "__main__":
    main()
