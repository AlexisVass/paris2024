import sqlite3
import csv
from pathlib import Path

def load_csv_to_db(conn, csv_path):
    cursor = conn.cursor()

    # Dictionnaires en mémoire pour éviter les doublons (cache)
    sports = {}         # { nom_sport : id_sport }
    epreuves = {}       # { (nom_epreuve, id_sport) : id_epreuve }

    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)

        for row in reader:
            sport = row["sport"].strip()
            epreuve = row["epreuve"].strip()
            classement = row["classement"]
            medaille = row["medaille"] if row["medaille"] in ["O", "A", "B"] else None
            equipe = row["equipe"]
            participant = row["participant"]
            resultats = row["resultats"]
            note = row["note"]

            # Insérer ou récupérer id_sport
            if sport not in sports:
                cursor.execute("INSERT OR IGNORE INTO sport (nom_sport) VALUES (?)", (sport,))
                cursor.execute("SELECT id_sport FROM sport WHERE nom_sport = ?", (sport,))
                sports[sport] = cursor.fetchone()[0]
            id_sport = sports[sport]

            # Insérer ou récupérer id_epreuve
            cle_epreuve = (epreuve, id_sport)
            if cle_epreuve not in epreuves:
                cursor.execute("""
                    INSERT OR IGNORE INTO epreuve (nom_epreuve, id_sport)
                    VALUES (?, ?)
                """, (epreuve, id_sport))
                cursor.execute("SELECT id_epreuve FROM epreuve WHERE nom_epreuve = ? AND id_sport = ?", (epreuve, id_sport))
                epreuves[cle_epreuve] = cursor.fetchone()[0]
            id_epreuve = epreuves[cle_epreuve]

            # Insérer le résultat
            cursor.execute("""
                INSERT INTO resultat (id_epreuve, classement, id_medaille, equipe, participant, resultats, note)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (id_epreuve, classement, medaille, equipe, participant, resultats, note))

    # Valider les insertions
    conn.commit()

def main():
    # Chemins vers la base de données et le fichier CSV
    db_path = Path("data/paris2024.db")
    csv_path = Path("data/rawdata.csv")

    # Connexion à la base et chargement des données
    conn = sqlite3.connect(db_path)
    load_csv_to_db(conn, csv_path)
    conn.close()
    print(f"[OK] Données importées depuis {csv_path} vers {db_path}")

if __name__ == "__main__":
    main()
