import subprocess
import sys
from pathlib import Path

def run_script(script_path):
    print(f"\n --> Exécution de {script_path}...")
    try:
        subprocess.run([sys.executable, script_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"\n Erreur lors de l'exécution : {e}\n")

def main():
    print("=== Initialisation de la base JO Paris 2024 ===")
    
    scripts = [
        "src/scrap/scraping_des_url_a_parcourir.py",
        "src/scrap/scraping_des_resultats_epreuves.py"
    ]
    for script in scripts:
        run_script(script)

if __name__ == "__main__":
    main()
