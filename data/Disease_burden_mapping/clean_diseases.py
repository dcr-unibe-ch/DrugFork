import re
from pathlib import Path

# Pfade setzen
base_path = Path(__file__).parent
input_file = "data/Disease_burden_mapping/diseases_from_extraction_Swissmedic.txt"
output_file = "data/Disease_burden_mapping/diseases_from_extraction_Swissmedic_unique.txt"

# Datei einlesen
with open(input_file, "r", encoding="utf-8", errors="replace") as f:
    raw_lines = f.readlines()

# Begriffe extrahieren
terms = []
for line in raw_lines:
    # Alles aus <...> extrahieren
    matches = re.findall(r"<(.*?)>", line)
    if matches:
        terms.extend([m.strip() for m in matches])
    else:
        # Fallback: durch ; getrennte Begriffe verwenden
        split_terms = [part.strip() for part in line.split(";") if part.strip()]
        terms.extend(split_terms)

# Doppelte entfernen
unique_terms = sorted(set(terms))  # alphabetisch sortiert

# In Datei schreiben
with open(output_file, "w", encoding="utf-8") as f:
    for term in unique_terms:
        f.write(term + "\n")

print(f"Fertig! {len(raw_lines)} Zeilen eingelesen, {len(unique_terms)} eindeutige alphabetisch sortierte Begriffe gespeichert.")

print(f"Fertig! {len(raw_lines)} Zeilen eingelesen, {len(unique_terms)} eindeutige Begriffe gespeichert.")
