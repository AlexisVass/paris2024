from playwright.sync_api import sync_playwright
import csv
from pathlib import Path
from urllib.parse import urlparse

# Fonction principale qui scrape les résultats d’une épreuve donnée (URL)
# Le paramètre first permet de savoir si on doit créer le fichier CSV ou juste l’ajouter
def scrap_resultats_epreuve(url, first=False):
    results = []  # Contiendra les lignes de résultats à écrire dans le CSV

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Mode non-headless pour observation
        context = browser.new_context()
        page = context.new_page()

        # Accès à la page de l’épreuve
        try:
            page.goto(url, wait_until="domcontentloaded", timeout=30000)
        except:
            print("(!) domcontentloaded échoué, tentative sans wait_until")
            page.goto(url, timeout=30000)

        # Accepter les cookies si présents
        try:
            page.locator('button:has-text("Tout accepter")').click(timeout=3000)
            print("[OK] Cookies acceptés automatiquement")
        except:
            pass

        # Déduire les noms du sport et de l’épreuve à partir de l’URL
        parts = url.split("/results/")[-1].split("/")
        sport = parts[0].capitalize()
        epreuve = parts[1].replace("-", " ").capitalize() if len(parts) > 1 else "Inconnue"

        # Sélection du bon type de tableau de résultats (3 cas possibles)
        row_selector = '[data-cy="single-athlete-result-row"]'
        if page.locator(row_selector).count() == 0:
            row_selector = '[data-cy="team-result-row"]'
        if page.locator(row_selector).count() == 0:
            row_selector = '[data-cy="doubles-result-row"]'

        # Attendre l’apparition du tableau
        try:
            page.wait_for_selector(row_selector, timeout=15000, state="attached")
        except:
            print(f"[ERREUR] Aucun tableau détecté pour {epreuve} ({url})")
            browser.close()
            return

        rows = page.locator(row_selector)

        # Récupération optimisée de toutes les lignes via JavaScript
        rows_data = rows.evaluate_all("""
        rows => rows.map((row, index) => {
            // Fonction utilitaire pour récupérer et nettoyer le texte d'un élément
            const getText = (sel) => row.querySelector(sel)?.textContent?.trim() || "";

            // Récupération du code pays (ex: FRA, USA, etc.) depuis les balises <span data-cy="XXX">
            const spans = row.querySelectorAll("span[data-cy]");
            let country = "N/A";
            for (const el of spans) {
                const code = el.getAttribute("data-cy");
                if (code && /^[A-Z]{3}$/.test(code)) {  // Vérifie que c'est bien un trigramme pays
                    country = code;
                    break;
                }
            }

            // Récupération de la médaille (O, A, B) depuis l’icône visuelle
            const medal = getText('span[data-cy="medal-main"]');

            // Récupération du rang (classement)
            let rank = getText('[data-cy="rank"]');
            if (!rank) rank = (index + 1).toString(); // Si vide, utiliser l’indice dans la liste comme fallback

            // Récupération des noms d’athlètes (plusieurs balises possibles par ligne)
            const athleteNodes = row.querySelectorAll('[data-cy="athlete-name"]');
            const athleteNames = Array.from(athleteNodes).map(n => n.textContent.trim());

            // Si plusieurs noms trouvés, les joindre avec /
            const athlete = athleteNames.join(" / ") || 
                            getText('[data-cy^="team-members-row-"]') || // sinon : nom des membres de l’équipe
                            getText('[data-cy^="country-name-row-"]');   // sinon : juste le nom du pays

            // Retourne l’objet représentant une ligne de résultat
            return {
                athlete,
                result: getText('[data-cy="result-info-content"]'), // temps / score
                note: getText('[data-cy="result-notes"]'),           // ex: Disqualifié
                rank,
                country,
                medal
            };
        })

        """)

        print(f"[INFO] {len(rows_data)} lignes détectées pour {sport} - {epreuve}")

        # Parcours des lignes extraites pour affichage + insertion dans results
        for row in rows_data:
            print(f"[OK] {epreuve} | Rang {row['rank']} | {row['medal']} | {row['country']} | {row['athlete']} | {row['result']} | {row['note']}")
            results.append({
                "sport": sport,
                "epreuve": epreuve,
                "classement": row["rank"],
                "medaille": row["medal"],
                "equipe": row["country"],
                "participant": row["athlete"],
                "resultats": row["result"],
                "note": row["note"]
            })

        browser.close()
        print("[CLEAN] Navigateur fermé.")

    # Écriture dans le fichier CSV
    Path("data").mkdir(parents=True, exist_ok=True)
    mode = "w" if first else "a"
    with open("data/rawdata.csv", mode=mode, newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "sport", "epreuve", "classement", "medaille", "equipe", "participant", "resultats", "note"
        ])
        if first:
            writer.writeheader()
        writer.writerows(results)

    print(f"[OK] {len(results)} lignes ajoutées depuis {epreuve}")


# Fonction main : lecture du fichier epreuves.csv et appel de scrap_resultats_epreuve pour chaque URL
def main():
    csv_path = "data/epreuves.csv" 
    urls = []

    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        seen = set()
        for row in reader:
            url = row["URL"]
            if url not in seen:
                seen.add(url)
                urls.append(url)

    # Traitement de toutes les épreuves
    for i, url in enumerate(urls):
        scrap_resultats_epreuve(url, first=(i == 0))

if __name__ == "__main__":
    main()
