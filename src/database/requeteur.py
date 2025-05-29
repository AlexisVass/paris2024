import sqlite3
import re
from pathlib import Path

def execute_sql_from_file(file_path, db_path, params=None):
    with open(file_path, "r", encoding="utf-8") as f:
        query = f.read()
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(query, params or {})
    results = cursor.fetchall()
    conn.close()
    return results

def display_results(results):
    if not results:
        print("Aucun résultat.\n")
        return
    headers = results[0].keys()
    print("\n" + " | ".join(headers))
    print("-" * (len(headers) * 20))
    for row in results:
        print(" | ".join(str(row[h]) if row[h] is not None else "" for h in headers))
    print()

def list_tables_and_columns(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    for t in tables:
        print(f"\n## Table : {t[0]} ##")
        cursor.execute(f"PRAGMA table_info({t[0]})")
        for col in cursor.fetchall():
            print(f"  - {col[1]} ({col[2]})")
    conn.close()

def run_manual_query(db_path):
    query = input("Saisissez votre requête SQL (sur une ligne) :\n> ")
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    try:
        cursor.execute(query)
        results = cursor.fetchall()
        display_results(results)
    except Exception as e:
        print(f" Erreur : {e}")
    finally:
        conn.close()

def run_predefined_query(db_path):
    base_sql_path = Path("src/database/requetes_sql")
    sql_files = list(base_sql_path.glob("*.sql"))
    if not sql_files:
        print(" Aucun fichier SQL trouvé.")
        return

    print("\n REQUETES DISPONIBLES :\n")
    for i, f in enumerate(sql_files, 1):
        print(f"{f.name}")

    print()
    try:
        choice = int(input("Numéro de la requête à exécuter : ").strip())
        if 1 <= choice <= len(sql_files):
            file_path = sql_files[choice - 1]
            with open(file_path, encoding="utf-8") as f:
                sql = f.read()
            print("\n >> Requête sélectionnée :\n\n" + sql.strip()+"\n")

            params_names = re.findall(r":(\w+)", sql)
            params = {}
            for name in params_names:
                val = input(f"  Valeur pour '{name}' : ").strip()
                print()
                params[name] = val

            results = execute_sql_from_file(file_path, db_path, params)
            display_results(results)
        else:
            print(" Numéro invalide.")
    except ValueError:
        print(" Entrée non valide.")

def menu():
    db_path = "data/paris2024.db"
    while True:
        print("\n=== MENU REQUETES J.O. PARIS 2024 ===")
        print()
        print("1 - Choisir une requête prédéfinie (répertoire database/requetes_sql)")
        print("2 - Saisir manuellement une requête SQL (sur une seule ligne)")
        print("3 - Voir le modèle de données")
        print()
        print("0 - Quitter")
        print()
        choice = input("Votre choix : ").strip()

        if choice == "3":
            list_tables_and_columns(db_path)
        elif choice == "1":
            run_predefined_query(db_path)
        elif choice == "2":
            run_manual_query(db_path)
        elif choice == "0":
            print("Fin du programme.")
            break
        else:
            print(" Choix invalide.")

if __name__ == "__main__":
    menu()