import subprocess
import sys

def run_script(script_path):
    print(f"\n --> Exécution de {script_path}...")
    try:
        subprocess.run([sys.executable, script_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"\n[ERREUR] Erreur lors de l'exécution : {e}\n")

def main():
    scripts = [
        "src/scrap/menu_scraping.py",      # étape 1 : scraping
        "src/database/menu_database.py"    # étape 2 : base de données
    ]

    for script in scripts:
        run_script(script)

if __name__ == "__main__":
    main()
