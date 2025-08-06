import os

# Absoluter Pfad zur Datei
input_file = "/Users/jacquelinedort/Documents/DrugFork/data/Disease_burden_mapping/diseases.txt"
output_file = "/Users/jacquelinedort/Documents/DrugFork/data/Disease_burden_mapping/diseases_unique.txt"

# Prüfen, ob Datei existiert
if not os.path.exists(input_file):
    print(f"❌ Datei nicht gefunden: {input_file}")
    exit()

# Datei lesen und leere Zeilen entfernen
with open(input_file, "r", encoding="utf-8", errors="replace") as f:
    lines = [line.strip() for line in f if line.strip()]

# Doppelte Einträge entfernen
seen = set()
unique_lines = []
for line in lines:
    if line not in seen:
        seen.add(line)
        unique_lines.append(line)

# Ergebnis schreiben
with open(output_file, "w", encoding="utf-8") as f:
    f.write("\n".join(unique_lines))

print(f"📄 {len(lines)} Zeilen eingelesen, {len(unique_lines)} eindeutige Einträge gespeichert.")
