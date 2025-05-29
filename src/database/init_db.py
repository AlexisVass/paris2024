import sqlite3
from pathlib import Path
import os

def init_db(db_path="data/paris2024.db"):
    Path("data").mkdir(exist_ok=True)

    # Supprimer la base si elle existe
    if Path(db_path).exists():
        os.remove(db_path)
        print("Base existante supprimée.")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Table sport
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sport (
            id_sport INTEGER PRIMARY KEY AUTOINCREMENT,
            nom_sport TEXT UNIQUE NOT NULL
        )
    """)

    # Table epreuve
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS epreuve (
            id_epreuve INTEGER PRIMARY KEY AUTOINCREMENT,
            nom_epreuve TEXT NOT NULL,
            id_sport INTEGER NOT NULL,
            FOREIGN KEY (id_sport) REFERENCES sport(id_sport)
        )
    """)

    # Table medaille
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS medaille (
            id_medaille TEXT PRIMARY KEY,
            nom_medaille TEXT NOT NULL,
            order_medaille INTEGER NOT NULL
        )
    """)

    # Table pays
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pays (
            id_pays TEXT NOT NULL,
            nom_pays TEXT NOT NULL
        )
    """)

    # Table resultat
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS resultat (
            id_resultat INTEGER PRIMARY KEY AUTOINCREMENT,
            id_epreuve INTEGER NOT NULL,
            classement TEXT,
            id_medaille TEXT,
            equipe TEXT,
            participant TEXT,
            resultats TEXT,
            note TEXT,
            FOREIGN KEY (id_epreuve) REFERENCES epreuve(id_epreuve),
            FOREIGN KEY (id_medaille) REFERENCES medaille(id_medaille),
            FOREIGN KEY (equipe) REFERENCES pays(id_pays)
        )
    """)

    # Peupler la table medaille
    cursor.executemany("""
        INSERT OR IGNORE INTO medaille (id_medaille, nom_medaille, order_medaille) VALUES (?, ?, ?)
    """, [
        ("O", "Or", 1),
        ("A", "Argent", 2),
        ("B", "Bronze", 3)
    ])

    conn.commit()
    conn.close()
    print("Base de données initialisée avec les tables, les médailles et la contrainte pays.")

if __name__ == "__main__":
    init_db()
