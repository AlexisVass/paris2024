import sqlite3
import csv
from pathlib import Path

def load_pays(csv_path="data/pays.csv", db_path="data/paris2024.db"):
    if not Path(csv_path).exists():
        print(f" Fichier introuvable : {csv_path}")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Vider la table pays
    cursor.execute("DELETE FROM pays")

    with open(csv_path, newline='', encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = [(row["id_pays"].strip(), row["nom_pays"].strip()) for row in reader]

    cursor.executemany("""
        INSERT INTO pays (id_pays, nom_pays) VALUES (?, ?)
    """, rows)

    conn.commit()
    conn.close()
    print(f"Table pays vidée puis {len(rows)} lignes insérées.")

if __name__ == "__main__":
    load_pays()
