import sqlite3
from pathlib import Path

def corriger_equipe_na(db_path="data/paris2024.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Vérification des correspondances existantes (equipe NULL et participant connu)
    cursor.execute("""
        SELECT COUNT(*)
        FROM resultat r
        JOIN pays p ON p.nom_pays = r.participant
        WHERE r.equipe IS NULL
    """)
    correspondances = cursor.fetchone()[0]
    print(f"{correspondances} lignes avec 'equipe = NULL' et participant reconnu dans la table pays.")

    if correspondances == 0:
        print("Aucune ligne à corriger.")
        conn.close()
        return

    # Mise à jour : remplacer NULL par id_pays
    cursor.execute("""
        UPDATE resultat
        SET equipe = (
            SELECT p.id_pays
            FROM pays p
            WHERE p.nom_pays = resultat.participant
        )
        WHERE equipe IS NULL
          AND EXISTS (
              SELECT 1 FROM pays p WHERE p.nom_pays = resultat.participant
          )
    """)

    conn.commit()
    print("Correction effectuée : les valeurs NULL ont été remplacées par le trigramme pays.")
    conn.close()

if __name__ == "__main__":
    corriger_equipe_na()
