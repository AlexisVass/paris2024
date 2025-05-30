import pandas as pd
import sqlite3
from pathlib import Path

def load_dataframes_and_insert():
    # Définition des chemins
    csv_path = Path("data/rawdata.csv")
    db_path = Path("data/paris2024.db")

    # Chargement des données brutes
    df = pd.read_csv(csv_path)

    # Nettoyage des champs
    df["sport"] = df["sport"].astype(str).str.strip()
    df["epreuve"] = df["epreuve"].astype(str).str.strip()

    # Création de la table sport avec id_sport
    df_sport = df[["sport"]].drop_duplicates().reset_index(drop=True)
    df_sport["id_sport"] = df_sport.index + 1
    df = df.merge(df_sport, on="sport", how="left")

    # Création de la table epreuve avec id_epreuve
    df_epreuve = df[["epreuve", "id_sport"]].drop_duplicates().reset_index(drop=True)
    df_epreuve["id_epreuve"] = df_epreuve.index + 1
    df = df.merge(df_epreuve, on=["epreuve", "id_sport"], how="left")

    # Préparation de la table resultat
    # Normalisation des médailles : seules "O", "A", "B" sont conservées
    df["id_medaille"] = df["medaille"].where(df["medaille"].isin(["O", "A", "B"]), None)

    df_resultat = df[[
        "id_epreuve", "classement", "id_medaille", "equipe",
        "participant", "resultats", "note"
    ]]

    # Connexion SQLite
    conn = sqlite3.connect(db_path)

    # Insertion des tables dans la base
    df_sport.rename(columns={"sport": "nom_sport"}).to_sql("sport", conn, if_exists="append", index=False)
    df_epreuve.rename(columns={"epreuve": "nom_epreuve"}).to_sql("epreuve", conn, if_exists="append", index=False)
    df_resultat.to_sql("resultat", conn, if_exists="append", index=False)

    conn.close()
    print(f"[OK] Données insérées dans {db_path}")

if __name__ == "__main__":
    load_dataframes_and_insert()
