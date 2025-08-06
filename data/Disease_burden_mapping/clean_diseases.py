# Eingabe- und Ausgabedateien
input_file = "data/Disease_burden_mapping/diseases.txt"
output_file = "data/Disease_burden_mapping/diseases_unique.txt"

# Datei einlesen
with open(input_file, "r", encoding="utf-8") as f:
    lines = f.readlines()

# Doppelte entfernen, Reihenfolge beibehalten
seen = set()
unique_lines = []
for line in lines:
    stripped_line = line.strip()
    if stripped_line not in seen:
        seen.add(stripped_line)
        unique_lines.append(stripped_line)

# Neue Datei speichern
with open(output_file, "w", encoding="utf-8") as f:
    for line in unique_lines:
        f.write(line + "\n")

print(f"{len(unique_lines)} eindeutige Einträge wurden in '{output_file}' gespeichert.")
