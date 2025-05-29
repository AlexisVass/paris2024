import subprocess
import os

def run_script(script_name, use_shell=False):
    print(f"\n --> Exécution de {script_name}...")
    try:
        if use_shell:
            os.system(f'python {script_name}')
        else:
            subprocess.run(["python", script_name], check=True)
    except subprocess.CalledProcessError as e:
        print(f"\n Erreurs : {e}\n")

def main():
    print("=== Initialisation de la base JO Paris 2024 ===")

    scripts = [
        ("src/database/init_db.py", False),        # création de la base de données
        ("src/database/load_pays.py", False),      # chargement de la table des pays
        ("src/database/load_csv_to_db.py", False), # chargement de rawdata.csv dans la database
        ("src/database/fix_na_pays.py", False),    # récupération du code pays pour les pays N/A
        ("src/database/requeteur.py", True)        # menu interactif de Datavisualisation
    ]

    for script, interactive in scripts:
        run_script(script, use_shell=interactive)

if __name__ == "__main__":
    main()
