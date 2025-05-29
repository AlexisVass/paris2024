import sqlite3
import csv
from pathlib import Path

def load_csv_to_db(conn, csv_path):
    cursor = conn.cursor()

    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)

        for row in reader:
            sport = row["sport"]
            epreuve = row["epreuve"]
            classement = row["classement"]
            medaille = row["medaille"] if row["medaille"] in ["O", "A", "B"] else None
            equipe = row["equipe"]
            participant = row["participant"]
            resultats = row["resultats"]
            note = row["note"]

            # Insérer ou récupérer id_sport
            cursor.execute("INSERT OR IGNORE INTO sport (nom_sport) VALUES (?)", (sport,))
            cursor.execute("SELECT id_sport FROM sport WHERE nom_sport = ?", (sport,))
            id_sport = cursor.fetchone()[0]

            # Insérer ou récupérer id_epreuve
            cursor.execute("""
                INSERT OR IGNORE INTO epreuve (nom_epreuve, id_sport)
                VALUES (?, ?)
            """, (epreuve, id_sport))
            cursor.execute("SELECT id_epreuve FROM epreuve WHERE nom_epreuve = ? AND id_sport = ?", (epreuve, id_sport))
            id_epreuve = cursor.fetchone()[0]

            # Insérer le résultat
            cursor.execute("""
                INSERT INTO resultat (id_epreuve, classement, id_medaille, equipe, participant, resultats, note)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (id_epreuve, classement, medaille, equipe, participant, resultats, note))

    conn.commit()

def main():
    db_path = Path("data/paris2024.db")
    csv_path = Path("data/rawdata.csv")

    conn = sqlite3.connect(db_path)
    load_csv_to_db(conn, csv_path)
    conn.close()
    print(f" Données importées depuis {csv_path} vers {db_path}")

if __name__ == "__main__":
    main()
