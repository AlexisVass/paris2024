from playwright.sync_api import sync_playwright
import csv
from pathlib import Path
from urllib.parse import urljoin, unquote, urlparse

# Fonction pour extraire un libellé d’épreuve à partir de l’URL (remplacement des tirets)
def extraire_nom_epreuve_depuis_url(url):
    path = urlparse(url).path
    return unquote(path.split('/')[-1]).replace('-', ' ').capitalize()

def scrap_epreuves_par_blocs():
    base_url = "https://www.olympics.com"
    main_url = f"{base_url}/fr/olympic-games/paris-2024/results"
    all_data = []  # Contiendra la liste des (sport, épreuve, URL)

    # Création du dossier data/ et du fichier epreuves.csv (entêtes uniquement)
    Path("data").mkdir(exist_ok=True)
    csv_path = Path("data/epreuves.csv")
    with open(csv_path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Sport", "Épreuve", "URL"])

    # Lancement de Playwright (navigateur Chromium)
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Mode non-headless pour observer
        page = browser.new_page()
        page.goto(main_url)

        # Acceptation automatique des cookies
        try:
            page.locator('button:has-text("Tout accepter")').click(timeout=3000)
            print("[OK] Cookies acceptés")
        except:
            print("[INFO] Pas de popup cookies")

        # Scroll automatique de la page pour charger dynamiquement tous les blocs de sports
        page.evaluate("""
            () => {
                return new Promise((resolve) => {
                    let totalHeight = 0;
                    const distance = 100;
                    const timer = setInterval(() => {
                        const scrollHeight = document.body.scrollHeight;
                        window.scrollBy(0, distance);
                        totalHeight += distance;
                        if (totalHeight >= scrollHeight) {
                            clearInterval(timer);
                            resolve();
                        }
                    }, 100);
                });
            }
        """)
        page.wait_for_timeout(2000)

        # Récupération de tous les liens vers les sports
        try:
            sport_links = page.locator('a[href^="/fr/olympic-games/paris-2024/results/"]')
            count = sport_links.count()
            print(f"[INFO] {count} sports détectés\n")
        except:
            print("[ERREUR] Aucun lien de sport détecté.")
            browser.close()
            return

        # Parcours de chaque lien de sport
        for i in range(count):
            link = sport_links.nth(i)
            href = link.get_attribute("href")
            sport_name = link.text_content().strip()
            sport_url = urljoin(base_url, href)
            print(f"=> {sport_name} ➜ {sport_url}")

            # Ouverture d’une nouvelle page pour le sport
            sport_page = browser.new_page()
            try:
                sport_page.goto(sport_url, timeout=45000, wait_until="domcontentloaded")
            except:
                print(f"(!) Timeout sur {sport_url}, tentative sans `wait_until`")
                try:
                    sport_page.goto(sport_url, timeout=45000)
                except Exception as e:
                    print(f"[ERREUR] Erreur ouverture {sport_url} : {e}")
                    sport_page.close()
                    continue

            # Si le bouton "Tout afficher" est présent, on le clique
            try:
                btn = sport_page.locator('button[data-cy="collapse-button"]')
                if btn.is_visible():
                    text = btn.text_content().strip().lower()
                    if "tout afficher" in text:
                        btn.click()
                        print(f"[OK] Tous les blocs affichés pour {sport_name}")
            except:
                pass  # Pas bloquant si le bouton n’existe pas

            sport_page.wait_for_timeout(2000)

            # Extraction des liens "Voir tous les résultats" (un par épreuve)
            result_links = sport_page.locator('a:has-text("Voir tous les résultats")')
            nb_epreuves = result_links.count()
            print(f"[INFO] {nb_epreuves} épreuves détectées pour {sport_name}")

            for j in range(nb_epreuves):
                try:
                    a_tag = result_links.nth(j)
                    url = a_tag.get_attribute("href")
                    if url:
                        full_url = urljoin(base_url, url)

                        # Récupération du libellé de l’épreuve à partir du bloc parent
                        label = a_tag.evaluate("""
                            el => el.closest('section')?.querySelector('h3')?.textContent?.trim()
                        """)
                        if not label:
                            label = extraire_nom_epreuve_depuis_url(full_url)

                        print(f"[OK] {sport_name} | {label} ➜ {full_url}")
                        all_data.append([sport_name, label, full_url])
                except Exception as e:
                    print(f"[ERREUR] Erreur bouton {j+1}/{nb_epreuves} : {e}")

            sport_page.close()

        browser.close()

    # Suppression des doublons éventuels (ligne identique sur les 3 colonnes)
    unique_data = list({tuple(row) for row in all_data})

    # Écriture des lignes dans le fichier CSV
    with open(csv_path, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(unique_data)

    print(f"\n[OK] Export terminé dans {csv_path}")

# Point d’entrée du script
if __name__ == "__main__":
    scrap_epreuves_par_blocs()