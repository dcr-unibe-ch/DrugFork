from __future__ import annotations
import pandas as pd
from pathlib import Path
from bs4 import BeautifulSoup
import requests
import time
import random
import re
import json
import sys
from urllib.parse import urljoin, urlparse


# ==================== GET LINKS ====================

def generate_links():
    """Generate DPD info links for Health Canada drugs"""
    # Input and output files
    input_csv = Path("./data/HealthCanada/with_extracted_data/HEALTHCANADA.csv") # TODO does not exist
    drug_txt = Path("./data/HealthCanada/allfiles/drug.txt") # TODO does not exist
    output_csv = input_csv.with_name(input_csv.stem + "_with_links.csv")

    BASE_URL = "https://health-products.canada.ca/dpd-bdpp/info?lang=eng&code="

    # Read CSV (DIN is Marketing_authorisation_number)
    df = pd.read_csv(input_csv, dtype=str)

    # Read drug.txt (Column 0 = Drug_number, Column 3 = DIN)
    drug_df = pd.read_csv(
        drug_txt,
        header=None,
        sep=",",
        usecols=[0, 3],
        names=["Drug_number", "DIN"],
        dtype=str,
        engine="python"
    )

    # Merge based on DIN
    merged = df.merge(
        drug_df,
        left_on="Marketing_authorisation_number",
        right_on="DIN",
        how="left"
    )

    # Create link column
    merged["dpd_info_url"] = BASE_URL + merged["Drug_number"].astype(str)

    # Remove unnecessary columns
    merged = merged.drop(columns=["DIN"])

    # Save result
    merged.to_csv(output_csv, index=False)

    print(f"Done. File saved at: {output_csv}")
    
    # Validation check
    assert len(merged["dpd_info_url"]) == len(merged["Marketing_authorisation_number"])
    
    return output_csv


# ==================== DOWNLOAD PDFs ====================

# Configuration
OUTPUT_PATH = Path("./data/HealthCanada/test")
OUTPUT_PATH.mkdir(parents=True, exist_ok=True)

INPUT_CSV = OUTPUT_PATH / "HEALTHCANADA_with_links.csv"
DOWNLOADS = OUTPUT_PATH / "downloads"
OUTPUT_CSV = OUTPUT_PATH / "scraping_results.csv"
DICT_JSON = OUTPUT_PATH / "pdf_dict.json"
CHECKPOINT = OUTPUT_PATH / "scraping_results.json"

DOWNLOADS.mkdir(parents=True, exist_ok=True)

# HTTP/Retry/Timing
TIMEOUT_S = 30
MAX_RETRIES = 5
BASE_DELAY = 1.5
PAUSE_RANGE = (0.3, 0.9)  # small random pause between requests

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}

PDF_HREF = re.compile(r"\.pdf($|\?)", re.I)


def random_delay(a=PAUSE_RANGE[0], b=PAUSE_RANGE[1]):
    time.sleep(random.uniform(a, b))


def make_session() -> requests.Session:
    s = requests.Session()
    s.headers.update(HEADERS)
    s.max_redirects = 5
    return s


def fetch(session: requests.Session, url: str) -> requests.Response | None:
    delay = BASE_DELAY
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            r = session.get(url, timeout=TIMEOUT_S, allow_redirects=True)
            if 200 <= r.status_code < 300:
                return r
            if r.status_code == 429:
                ra = r.headers.get("Retry-After")
                wait = int(ra) if ra and ra.isdigit() else delay
                time.sleep(wait)
            elif 500 <= r.status_code < 600:
                time.sleep(delay)
            else:
                print(f"[WARN] {r.status_code} {url}")
                return None
        except requests.RequestException as e:
            if attempt == MAX_RETRIES:
                print(f"[ERROR] {url} -> {e}")
                return None
            time.sleep(delay)
        delay *= 1.8
    return None


def extract_pdf_links(html: str, base_url: str) -> list[str]:
    soup = BeautifulSoup(html, "html.parser")
    urls = []
    for a in soup.find_all("a", href=True):
        href = a.get("href")
        if not href:
            continue
        if PDF_HREF.search(href):
            urls.append(urljoin(base_url, href))
    # Stable: preserve order but remove duplicates per page
    seen = set()
    deduped = []
    for u in urls:
        if u not in seen:
            deduped.append(u)
            seen.add(u)
    return deduped


def filename_from_url(pdf_url: str) -> str:
    """
    Extract filename from URL:
      last path segment (without query/fragment), everything before the last dot,
      and append '.pdf'.
      Examples:
        .../ABC123.PDF            -> ABC123.pdf
        .../doc-name.v1.pdf?x=1   -> doc-name.v1.pdf
        .../noext?x=1             -> noext.pdf
    """
    path = urlparse(pdf_url).path
    last = Path(path).name or "monograph"
    if "." in last:
        base = last.rsplit(".", 1)[0]
    else:
        base = last
    return f"{base}.pdf"


def save_binary(session: requests.Session, url: str, dest: Path) -> bool:
    if dest.exists() and dest.stat().st_size > 0:
        return True
    delay = BASE_DELAY
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            with session.get(url, timeout=TIMEOUT_S, stream=True) as r:
                if not (200 <= r.status_code < 300):
                    if r.status_code == 429:
                        ra = r.headers.get("Retry-After")
                        wait = int(ra) if ra and ra.isdigit() else delay
                        time.sleep(wait)
                        delay *= 1.8
                        continue
                    if 500 <= r.status_code < 600:
                        time.sleep(delay)
                        delay *= 1.8
                        continue
                    print(f"[WARN] Download {r.status_code}: {url}")
                    return False
                tmp = dest.with_suffix(".part")
                with open(tmp, "wb") as f:
                    for chunk in r.iter_content(chunk_size=1024 * 64):
                        if chunk:
                            f.write(chunk)
                tmp.replace(dest)
                return True
        except requests.RequestException as e:
            if attempt == MAX_RETRIES:
                print(f"[ERROR] Download failed: {url} -> {e}")
                return False
            time.sleep(delay)
            delay *= 1.8
    return False


def save_intermediate_results(results, filename="scraping_results.json"):
    Path(filename).write_text(json.dumps(results, indent=4), encoding="utf-8")


def download_pdfs():
    """Download PDF monographs from Health Canada DPD pages"""
    # Input
    if not INPUT_CSV.exists():
        print(f"Input file not found: {INPUT_CSV}", file=sys.stderr)
        sys.exit(1)
    df = pd.read_csv(INPUT_CSV, dtype=str)
    if "dpd_info_url" not in df.columns:
        print("Column 'dpd_info_url' missing in input CSV.", file=sys.stderr)
        sys.exit(1)

    # Load existing dictionary (to detect duplicates)
    if DICT_JSON.exists():
        try:
            PDF_DICT = json.loads(DICT_JSON.read_text(encoding="utf-8"))
        except Exception:
            PDF_DICT = {}
    else:
        PDF_DICT = {}

    # Load existing checkpoint/result list
    if CHECKPOINT.exists():
        try:
            results = json.loads(CHECKPOINT.read_text(encoding="utf-8"))
        except Exception:
            results = []
    else:
        results = []

    # Counters
    COUNTER = 0
    PDF_COUNTER = sum(1 for r in results if r.get("status") == "downloaded")
    UNIQUE_COUNTER = len(PDF_DICT)  # number of unique PDF URLs so far

    # Set for fast duplicate detection
    seen_pdf_urls = set(PDF_DICT.keys())

    session = make_session()

    for _, row in df.fillna("").iterrows():
        COUNTER += 1
        dpd_url = str(row["dpd_info_url"]).strip()
        din = str(row.get("Marketing_authorisation_number", "")).strip()  # optional

        if not dpd_url:
            results.append({
                "DIN": din,
                "PDF_URL": None,
                "PDF_NAME": None,
                "Status": None,
                "idx": COUNTER,
                "PDF_Counter": None,
                "PDF_Counter_Unique": None
            })
            save_intermediate_results(results, CHECKPOINT)
            continue

        random_delay()
        resp = fetch(session, dpd_url)
        if not resp:
            results.append({
                "DIN": din,
                "PDF_URL": None,
                "PDF_NAME": None,
                "Status": "page_fetch_failed",
                "idx": COUNTER,
                "PDF_Counter": PDF_COUNTER,
                "PDF_Counter_Unique": UNIQUE_COUNTER
            })
            save_intermediate_results(results, CHECKPOINT)
            continue

        pdf_urls = extract_pdf_links(resp.text, dpd_url)

        if not pdf_urls:
            results.append({
                "DIN": din,
                "PDF_URL": None,
                "PDF_NAME": None,
                "Status": "no_pdf_found",
                "idx": COUNTER,
                "PDF_Counter": PDF_COUNTER,
                "PDF_Counter_Unique": UNIQUE_COUNTER
            })
            save_intermediate_results(results, CHECKPOINT)
            continue

        for pdf_url in pdf_urls:
            # Filename
            save_name = filename_from_url(pdf_url)
            dest = DOWNLOADS / save_name

            if pdf_url in seen_pdf_urls:
                # already known -> don't download again, but append DIN
                lst = PDF_DICT.get(pdf_url, [])
                if din and din not in lst:
                    lst.append(din)
                    PDF_DICT[pdf_url] = lst
                    DICT_JSON.write_text(json.dumps(PDF_DICT, indent=4), encoding="utf-8")

                results.append({
                    "DIN": din,
                    "PDF_URL": pdf_url,
                    "PDF_NAME": Path(urlparse(pdf_url).path).name,
                    "Status": "already_downloaded",
                    "idx": COUNTER,
                    "PDF_Counter": PDF_COUNTER,
                    "PDF_Counter_Unique": UNIQUE_COUNTER
                })
                save_intermediate_results(results, CHECKPOINT)
                continue

            # New -> download
            random_delay()
            ok = save_binary(session, pdf_url, dest)
            if ok:
                PDF_COUNTER += 1
                UNIQUE_COUNTER += 1
                seen_pdf_urls.add(pdf_url)
                PDF_DICT[pdf_url] = [din] if din else []
                DICT_JSON.write_text(json.dumps(PDF_DICT, indent=4), encoding="utf-8")

            results.append({
                "DIN": din,
                "PDF_URL": pdf_url,
                "PDF_NAME": Path(urlparse(pdf_url).path).name,
                "Status": "downloaded" if ok else "download_failed",
                "idx": COUNTER,
                "PDF_Counter": PDF_COUNTER,
                "PDF_Counter_Unique": UNIQUE_COUNTER
            })
            save_intermediate_results(results, CHECKPOINT)

    # Completion
    pd.DataFrame(results).to_csv(OUTPUT_CSV, index=False)
    print(f"Done. Results: {OUTPUT_CSV}")
    print(f"PDF Dictionary: {DICT_JSON}")
    print(f"Downloads: {DOWNLOADS.resolve()}")


def main():
    """Main execution: generate links then download PDFs"""
    print("Step 1: Generating DPD info links...")
    generate_links()
    
    print("\nStep 2: Downloading PDFs...")
    download_pdfs()


if __name__ == "__main__":
    main()
