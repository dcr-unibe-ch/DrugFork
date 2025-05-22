import os

# Pfad zum Ordner mit den PDFs
pdf_folder = "DrugFork/data/EMA/EMA_downloads"
output_file = "DrugFork/data/EMA/EMA_list.txt"

# Alle .pdf-Dateien auflisten
pdf_files = [f for f in os.listdir(pdf_folder) if f.endswith(".pdf")]

# In eine .txt-Datei schreiben
with open(output_file, "w") as f:
    for pdf in pdf_files:
        f.write(f"{pdf}\n")

print(f"{len(pdf_files)} PDF-Dateien in '{output_file}' gespeichert.")