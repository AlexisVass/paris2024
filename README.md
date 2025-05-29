_________________________
 Projet Scraping & Base de Données
 =============
 J.O. Paris 2024
 =============
 
 ![Logo JO Paris 2024](/images/logo_jo_paris2024.png "Logo JO Paris 2024E")



|Alexis Vassalo| mai 2025 |
|:-------------- | --------:|
|![Logo ESIEE](/images/logo_esiee.png "logo ESIEE")| filière Data Science et Intelligence Artificielle 


# **INTRODUCTION**
Ce projet permet d'automatiser la collecte et l’exploration des résultats des épreuves des Jeux Olympiques de Paris 2024, disponibles sur le site officiel :
https://www.olympics.com/fr/olympic-games/paris-2024/results

Plus précisément, l’objectif est :

* de récupérer l’ensemble des résultats publiés sur le site pour chaque épreuve et chaque sport représenté ;
* de stocker ces données dans une base de données relationnelle;
* de permettre une restitution de ces données via un requêteur SQL interactif.

Le projet repose intégralement sur l’écosystème Python, avec :

* Playwright pour le scraping
* SQLite pour la base de données
* un ensemble de scripts Python pour assurer l'automatisation complète de la chaîne de traitement


# **I - USER GUIDE**

## I.1 Déploiement du projet
Tous les fichiers sources du projet sont contenus dans le répertoire GitHub : 
```sh
"https://github.com/AlexisVass/paris2024"
```
Ce répertoire est public et il contient l’ensemble du code strictement nécessaire pour exécuter le projet.

## I.2 Structure du projet
```
paris2024/
|──.gitignore
|── config.py                 # fichier de configuration
|── main.py                   # fichier principal permettant de lancer l'application
|── requirements.txt          # liste des packages additionnels requis
|── README.md
├── .venv/                    # Environnement virtuel (non inclus sur GitHub)
├── data/                     # les données
│   ├── rawdata.csv           # Résultats scrappés
│   └── paris2024.db          # Base de données SQLite
├── documentation/            # rapport
├── images/                   # images utilisées dans le README
├── src/                      # Code source de l'application
    ├── scrap/                # Code de la partie scraping
    ├── database/             # Code de la partie database
    └── utils/                # Fonctions utilitaires
```

 Le répertoire racine "paris2024" contient principalement :

- un fichier **"main.py"** à la racine du répertoire qui est le fichier python principal du projet
- le fichier **"requirements.txt"** qui comporte toutes les bibliothèques python pour recréer l'environnement
- le fichier **"config.py"** qui contient les paramètres globaux
- le répertoire **data/** contenant les données (database et fichiers csv) ;
- le répertoire **src/** contenant les sources du programme;

Pour déployer le projet sur une autre machine, il suffit de copier ce répertoire "paris2024" (et tout son contenu) sur la machine cible avec la commande:

```sh
$ git clone https://github.com/AlexisVass/paris2024
$ cd paris2024
```

## I.2 Installation locale à effectuer
**1. Créer un environnement virtuel** :
```bash
python -m venv .venv
```
**2. (Si erreur d’activation) Autoriser les scripts PowerShell**
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```
**3. Activer l'environnement** :
```powershell
.venv\Scripts\Activate.ps1  # Windows PowerShell**
source .venv/bin/activate  # Linux/macOS**
```
**4. (Optionnel) Télécharger les navigateurs via un miroir rapide :**
```powershell
$env:PLAYWRIGHT_DOWNLOAD_HOST = "https://playwright.azureedge.net"
```
**5. Installer les dépendances:**
```bash
pip install -r requirements.txt
```
/!\  Remarque : Si l'installation des dépendances échoue à cause d'une erreur SSL (CERTIFICATE_VERIFY_FAILED), on peut relancer la commande suivante pour contourner le problème :

```bash
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt
```

**6. (Optionnel) Si playwright est mal installé depuis requirements.txt : Ré-installer playwright:**
```bash
$env:NODE_TLS_REJECT_UNAUTHORIZED = "0"
python -m pip install playwright
```
**7. Installer les navigateurs pour Playwright:**
```bash
python -m playwright install
```  
## I.3 Exécution du projet
L'application est alors prête à être utilisée. Il suffit pour cela d'exécuter depuis une console active (dans l’environnement `.venv`) le fichier principal `main.py` qui se trouve à la racine du projet.

Assurez-vous que :

- Vous êtes bien dans le dossier du projet
- L’environnement virtuel `.venv` est **activé**

```bash
python main.py
```
Ce programme "main.py" exécute l'ensemble de la chaine de traitement : il parcourt le site web des jeux Olympiques pour extraire les données (scraping), génère une base de données, charge les données du scraping dans les tables de cette base et lance le requêteur qui permet de lancer des requêtes SQL pour interroger la base de données.

**/!\  Attention :**  
_Pendant l’exécution du programme, il est important de ne pas interagir manuellement avec les fenêtres du navigateur que le script ouvre automatiquement. Cliquer, fermer ou bouger quoi que ce soit peut perturber le déroulement du scraping, entraîner des erreurs, ou bloquer l’extraction de certaines données. Par précaution, il est également préférable de ne pas utiliser un autre navigateur en parallèle, surtout si vous êtes connecté au même site. Cela peut interférer avec les sessions en cours du script._

## I.4  Utilisation du Requêteur
### I.4.1 **Menu proposé**
Le fichier requeteur.py lance un menu interactif en console permettant d’interroger la base sqlite paris2024.db :

```
=== REQUETES J.O. PARIS 2024 ===

1 - Choisir une requête prédéfinie (répertoire src/database/requetes_sql)
2 - Saisir manuellement une requête SQL (sur une ligne sans retour à ligne)
3 - Voir le modèle de données
0 - Quitter
```

### I.4.2 **Choisir une requête prédéfinie**

Le choix 1 permet de sélectionner une requête prédéfinie stockée dans un des fichiers (.sql) situés dans le dossier "src/database/requetes_sql". Si la requête contient des paramètres nommés (:pays, :epreuve, etc.), ils sont automatiquement détectés et demandés à l'utilisateur.

Voici la liste des requêtes disponibles :

* Liste des sports et épreuves
* Résultats d’une épreuve
* Tableau des médailles par pays
* Nombre de médailles d’un pays
* Détail du podium d’une épreuve
* Liste des médaillés d’un pays
* Participation ou palmarès d’un athlète
* Nombre d'épreuves par sport

Il est possible de rajouter des requêtes prédéfinies supplémentaires. Pour cela, il suffit de mettre le SQL de la requête dans un fichier (.sql)  et de placer ce fichier dans le répertoire "src/database/requetes_sql/". La nouvelle requête apparaitra alors dans la liste des requêtes disponibles au choix 1 du menu.

### I.4.3 **Saisir manuellement une requête SQL**

Le choix 2 permet de saisir manuellement une requête SQL directement depuis la console (donc en une seule ligne).
La requête est exécutée et les résultats sont affichés dans la console.

<u>/!\ _Attention de ne pas oublier le point virgule en fin d'instruction SQL_</u>

### I.4.4 **Modèle de données**
Le choix 3 permet d'afficher la liste les tables de la base de données avec les différents champs et leur type pour aider à la rédaction des requêtes manuelles. Le graphique du schéma relationnel est disponible au paragraphe  II.4.1

_________________________
# **II - DEVELOPER GUIDE**
## II.1 - Packages
Les modules nécessaires au projet sont répertoriés dans le fichier `requirements.txt` situé dans le répertoire racine "paris2024" :

| Package            | Utilisation                                                                 |
|--------------------|------------------------------------------------------------------------------|
| greenlet           | Nécessaire pour le fonctionnement asynchrone de certains modules comme Playwright |
| playwright         | Bibliothèque de scraping permettant d'automatiser un navigateur |
| pyee               | Fournit un système d’événements utilisé en interne par Playwright              |
| typing_extensions  | Apporte des compléments de typage statique pour Python | 


## II.2 Architecture du code
### II.2.1 - Fichier main.py
 Le fichier main.py est le programme principal qui lance automatiquement et de façon séquentielle tous les traitements : 

   - un premier scraping du site pour en extraire les URL à parcourir (une par épreuve).
   - un second scraping su site qui parcourt ces URL et en extrait les données des résultats des épreuves.
   - la création de la base de données (tables)
   - le chargement des données du scraping dans la base
   - le lancement du requêteur SQL

### II.2.2 Enchainement des traitements
Le script main.py exécute séquentiellement 2 sous programmes qui correspondent aux deux grandes étapes du traitement :  le scraping et la mise à disposition des données dans la database :

|           |                      |
|------------:|:---------------------|
|**Etape 1**|--->  menu_scraping.py|
|**Etape 2**|--->  menu_database.py|
|           |                      |

**Détail de chacun de ces deux sous programmes :**

* **Étape 1 – Scraping**

menu_scraping.py lance séquentiellement les 2 programmes ci-dessous :
```
src/scrap/menu_scraping.py
├── scraping_des_url_a_parcourir.py       → Récupération des URL de chaque épreuve et chargement dans epreuves.csv
└── scraping_des_resultats_epreuves.py    → Récupération des résultats et chargement dans rawdata.csv
```

* **Étape 2 – Mise à disposition des données**

menu_datatbase.py lance séquentiellement les 4 programmes ci-dessous :
```
src/database/menu_database.py
├── init_db.py           → Création des tables
├── load_pays.py         → Chargement des pays depuis pays.csv
├── load_csv_to_db.py    → Insertion des résultats scrappés
├── fix_na_pays.py       → Complétion des codes pays manquants
└── requeteur.py         → Lancement du menu interactif pour les requêtes SQL
```

### II.2.3 Durée d'exécution

L'ensemble des traitements pour extraire les données et les mettre à disposition pour le requêteur prend 38 minutes environ. Voici le temps d'execution par programme :

|Sous programme| Durée d'exécution |
|:-------------- | -----------:|
|scraping_des_url_a_parcourir.py |  8 minutes   | 
|scraping_des_resultats_epreuves.py |  30 minutes   | 
|init_db.py |  3 secondes   | 
|load_pays.py |  1 secondes   |
|load_csv_to_db.py |  3 secondes   | 
|fix_na_pays.py |  2 secondes   |
|requeteur.py |  ouverture immédiate   |

## II.3 Détail de la partie Scraping

### II.3.1 Chemin de navigation sur le site
Le site officiel des Jeux Olympiques 2024 propose un point d’entrée unique pour les résultats :
https://www.olympics.com/fr/olympic-games/paris-2024/results. Depuis cette page, les blocs de résultats sont chargés dynamiquement via JavaScript au fur et à mesure du scroll.

La navigation vers les résultats d'une épreuve  suit cette logique :

**1. Page de départ (/results) :**

→ Il faut commencer par accepter les cookies à l'ouverture de la page.

![cookies](/images/cookies.png "cookies")

→ Affichage de la liste des sports en bas de page (il faut scroller vers le bas pour que tous les sports soient affichés)

![Liste des sports](/images/Liste_sports.png "Liste des sports")

**2. sélection par clic d'un sport (/results/athletisme)**

→ liste des épreuves correspondant au sport sélectionné.

![Liste des épreuves](/images/Liste_epreuves.png "Liste des épreuves")

Les épreuves se présentent sous la forme d'une liste de blocs repliés. Chaque bloc peut être déplié en cliquant sur son bouton "+" , ce qui permet de visualiser le podium de l'épreuve (les 3 médaillés avec leur photo) ainsi qu'un lien "Voir tous les résultats" qui nous intéresse particulièrement car c'est l'URL vers les résultats détaillés de l'épreuve que l'on veut récupérer dans la première phase de notre scraping.

Le problème, c'est que souvent certains blocs sont déjà développés (le premier en général) et d'autres sont réduits, ce qui masque leur bouton "Voir tous les résultats".

Plutôt que de développer un par un les blocs en cliquant sur les "+" (complexe car le nombrer d'épreuves est très variable d'un sport à un autre), j'ai choisi d'exploiter la possibilité offerte par le site de développer tous les blocs de la page en même temps. C'est possible en cliquant sur le lien "Tout Afficher" au dessus du premier bloc.

**3. Clic sur le lien "Tout afficher"**

→ Développement de tous les blocs d'épreuves de la page, ce qui rend visibles les liens "Voir tous les résultats" de toutes les épreuves du sport courant (ici Athlétisme).

![Tout afficher](/images/Tout_Afficher.png "Tout afficher")

Ce bouton binaire prend les valeurs "Tout réduire" (réduction de tous les blocs) ou "Tout afficher" (développement de tous les blocs)

**4. Clic sur le lien "Voir tous les résultats" pour chaque épreuve.** 

→ Affichage des résultats de l’épreuve sous forme de tableau.

![Résultats](/images/Voir_Tous_Les_Resultats.png "Résultats")

Ce sont les données de ces tableaux (un pour chaque épreuve de tous les sports) que je récupère lors de la phase de scraping des résultats.

### II.3.2 Pourquoi avoir utilisé Playwright ?

Le site officiel des JO Paris 2024 charge la majorité de ses données via JavaScript de manière dynamique.  Par exemple, les blocs de résultats (sports, épreuves, tableaux) n’apparaissent qu’après défilement ou clics sur certains boutons.

Or une solution de scraping classique (comme `BeautifulSoup`) ne permet pas de capturer ces éléments dynamiques. Playwright, à l’inverse, permet de complètement piloter le navigateur et de simuler un utilisateur humain qui effectue les actions nécessaires (cookies, clics, scroll, attente de chargement).  On peut ainsi récupérer l’ensemble du contenu HTML final tel qu’il est affiché dans le navigateur, après exécution du JavaScript.

Playwright, qui est aussi utilisé pour automatiser les tests de sites web, est donc incontournable pour réaliser le scraping du site des J.O.

### II.3.3 Récupération des URL à parcourir (scraping_des_url_a_parcourir.py)
Ce script effectue un scroll automatique de la page principale pour charger dynamiquement tous les blocs de sports. Il utilise Playwright pour :

* Cliquer automatiquement sur « Tout accepter » pour les cookies
* Simuler un scroll bas (avec evaluate() en JavaScript)
* Cliquer sur les boutons « Tout afficher » lorsque ils sont présents
* Extraire tous les liens vers les pages de résultats d’épreuves
* Écrire ces URLs dans un fichier epreuves.csv qui a pour format :
```
csv
Sport,Épreuve,URL
Athlétisme,100m femmes,https://www.olympics.com/fr/olympic-games/paris-2024/results/athletisme/100m-femmes
```
On récupère ainsi 329 URLs dans le fichier "epreuves.csv". Les doublons éventuels (liens identiques pour une même épreuve) sont supprimés via une conversion en set() avant enregistrement, afin de garantir l’unicité des lignes.

### II.3.4 Récupération des résultats des épreuves (scraping_des_resultats_epreuves.py)

Ce script lit séquentiellement toutes les URLs qui ont été stockées dans le fichier epreuves.csv, et pour chaque URL (donc pour chaque épreuve), voici ce qu'il fait :

1. Ouverture de la page d’épreuve avec page.goto(...)
2. Détection dynamique du tableau contenant les résultats.
Le script tente successivement trois sélecteurs CSS selon le type de compétition :
* [data-cy="single-athlete-result-row"] pour les épreuves individuelles
* [data-cy="team-result-row"] pour les sports collectifs
* [data-cy="doubles-result-row"] pour les duos

3. Si aucun tableau n’est trouvé sous 15 secondes, l’épreuve est ignorée avec un message d’erreur (mais le scraping continue).

**Extraction optimisée avec JavaScript :**

Une fois le bon tableau trouvé, toutes les lignes sont extraites en une seule fois grâce à evaluate_all(...), une fonction qui permet d’exécuter du JavaScript directement dans la page. Ce JS construit pour chaque ligne un objet contenant :

|Champ	|Source|
|-------|------|
|rank|	data-cy="rank" (ou index de la ligne si absent)
|medal|	data-cy="medal-main" (si une médaille est présente)
|country|	Code ISO détecté dans span[data-cy="XXX"]
|athlete|	Liste des noms dans [data-cy="athlete-name"], joints par /, ou nom de l’équipe
|result|	Temps, score, points (data-cy="result-info-content")
|note|	Champ facultatif comme "Disqualifié", "Égalité", etc.

```js
const athleteNodes = row.querySelectorAll('[data-cy="athlete-name"]');
const athleteNames = Array.from(athleteNodes).map(n => n.textContent.trim());
```
Les données sont ensuite collectées ligne par ligne en Python dans un tableau results, enrichies avec le nom du sport et de l’épreuve (dérivés de l’URL).

Puis chaque ligne extraite est formatée et écrite dans data/rawdata.csv :

```
csv
sport,epreuve,classement,medaille,equipe,participant,resultats,note
```

* Si le code pays n’est pas reconnu, "N/A" est utilisé (et corrigé plus tard par fix_na_pays.py)
* Les lignes vides ou incomplètes sont filtrées
* Les noms multiples (duos, relais) sont normalisés avec /


Ce traitement permet d’extraire 9294 résultats à partir des 329 épreuves listées dans le fichier epreuves.csv

## II 4 Partie Database
### II.4.1 Création du Modèle de données (init_db.py)
Ce script crée le schéma relationnel de la base SQLite paris2024.db.

J'ai identifié 5 entités : sport, epreuve, medaille, pays, resultat à partir desquelles j'ai défini un modèle conceptuel des données (MCD) de type meurisien (respect des 3 formes normales) pour bien structurer les données.

Les cardinalités du modèle conceptuel des données sont les suivantes:

* un résultat est lié à une et une seule épreuve (relation 1 → 1)
* une épreuve est liée à un ou plusieurs résultats (relation 1 → n)
* un résultat est lié à 0 ou une médaille (relation 0 → 1)
* une médaille peut être attribuée à plusieurs résultats (relation 1 → n)
* un résultat est lié à un et un seul pays (relation 1 → 1)
* un pays epeut être attribuée à plusieurs résultats (relation 1 → n)
* une épreuve est liée à un et un seul sport (relation 1 → 1)
* un sport regroupe plusieurs épreuves (relation 1 → n)


Lorsqu'on passe au modèle physique des données (MPD), chaque table correspond à une entité claire du site (sport, épreuve, résultat, etc.), ce qui évite les redondances et facilite les requêtes. La table "résultat" contient les données les plus détaillées, chaque ligne correspondant à une ligne du tableau des résultats pour une épreuve ainsi qu'à une ligne du fichier rawdata.csv

Les autres tables contiennent les données de référence (libellés des sports, épreuves, pays et médailles). Les liens entre les tables sont gérés par des clés étrangères qui respectent les règles d’intégrité référentielle. 

Enfin, les noms des colonnes ont été choisis pour être explicites et respecter les bonnes pratiques de nommage (codes préfixés par id et libellés préfixés par nom).
 
**Schéma du modèle physique de données :**

![mpd](/images/modele_bd.drawio.png "mpd")

* Table : sport
  - id_sport (INTEGER, PK)
  - nom_sport (TEXT)
* Table : epreuve
  - id_epreuve (INTEGER, PK)
  - nom_epreuve (TEXT)
  - id_sport (INTEGER, FK → sport.id_sport)
* Table : medaille
  - id_medaille (TEXT, PK) : "O", "A", "B"
  - nom_medaille (TEXT) : Or, Argent, Bronze
  - order_medaille (INTEGER) : 1 = Or, 2 = Argent, 3 = Bronze
* Table : pays
  - id_pays (TEXT, PK) : code pays (FRA, USA, etc.)
  - nom_pays (TEXT)
* Table : resultat
  - id_resultat (INTEGER, PK)
  - id_epreuve (INTEGER, FK → epreuve.id_epreuve)
  - classement (TEXT)
  - id_medaille (TEXT, FK → medaille.id_medaille)
  - equipe (TEXT, FK → pays.id_pays)
  - participant (TEXT)
  - resultats (TEXT)
  - note (TEXT)

**Remarque :** La table sqlite_sequence est une table système utilisée automatiquement par SQLite pour gérer l’autoincrémentation des clés primaires.

### II.4.2 – Chargement des données dans la base de données
Les scripts suivants assurent le chargement des données dans la base de données. Pour charger une table contenant des clés étrangères (FK), il faut préalablement charger la table de référence pour respecter l'intégrité référentielle. De ce fait, l'ordre de chargement des tables est le suivant : 

1. medaille 
2. pays 
3. sport, epreuve
3. résultat

**Remarques :** 

* La table médaille est une toute petite table. Elle est chargée dans la foulée de la création des tables dans init.db

* Les données des tables sport, epreuve et resultat sont directement extraites des données brutes du scraping (fichier rawdata.csv)

* Par contre, la table pays est chargée avec un fichier pays.csv complet avec des données récupérées sur le net. J'ai du procéder ainsi parce que pour les sports en équipe, le champ participant contient un nom de pays qui quelquefois n'était pas déjà répertorié dans les épreuves individuelles où dont le libéllé différait un peu. J'ai donc du construire une table pays plus complète.

#### II.4.2.1 – Chargement des pays (load_pays.py)
Ce programme lit le fichier pays.csv, contenant les couples (id_pays, nom_pays), et les insère dans la table pays qu'il
vide avant chargement.

#### II.4.2.2 – Chargement des résultats des épreuves (load_csv_to_db.py)
Ce script lit le fichier rawdata.csv et insère les résultats dans la base de données en complétant les tables sport, epreuve et resultat.

Pour garantir l’intégrité des données, les sports sont insérés dans la table sport uniquement s’ils n’existent pas déjà, avec une mise en cache en mémoire pour éviter les requêtes redondantes.

Les épreuves sont insérées dans la table epreuve en tenant compte du couple (nom_epreuve, id_sport) afin d’éviter les doublons liés à des intitulés identiques entre sports différents.
Chaque ligne du fichier est ensuite insérée dans la table resultat, avec conversion des médailles ("O", "A", "B") et liaison aux clés étrangères correspondantes.

Cette logique assure qu'il n'y ait pas de doublons, conformément au schéma relationnel normalisé du modèle.

#### II.4.2.3 – Récupération des pays manquants (fix_na_pays.py)
On a vu que certaines lignes ont le champ equipe à "N/A" (valeur par défaut lorsqu'aucun code pays n’a été détecté lors du scraping).
Ce script tente de corriger cela en croisant le champ participant (libellé) avec le nom des pays (pays.nom_pays).
S’il y a correspondance exacte (minuscule / insensible à la casse), le champ equipe est corrigé avec le bon code pays (id_pays) correspondant.

### II.4.3  Requêtes SQL prédéfinies
Le projet propose un ensemble de requêtes SQL prêtes à l’emploi pour interroger la base paris2024.db. Ces requêtes permettent d'explorer la base de données avec quelques restitutions basiques. Elles sont stockées dans le dossier src/database/requetes_sql/ et de ce fait sont détectées et proposées dans le menu du requêteur (choix 1).

Certaines requêtes contiennent des paramètres nommés (comme :pays ou :epreuve), qui sont demandés à l'utilisateur lors de l'exécution.

#### II.4.3.1 Liste des requêtes disponibles

| Fichier SQL                                | Description                                                             |
|-------------------------------------------|-------------------------------------------------------------------------|
| 1-Liste des sports et épreuves.sql        | Affiche la liste des sports et des épreuves associées                  |
| 2-Résultats par épreuve.sql               | Affiche les résultats d’une épreuve (classement, pays, performance...) |
| 3-Tableau des medailles par pays.sql      | Affiche un tableau croisé du nombre de médailles par pays              |
| 4-Nombre de médailles d'un pays.sql       | Affiche le nombre de médailles (or, argent, bronze) obtenues par un pays |
| 5-Podium d'une épreuve.sql                | Affiche le podium d’une épreuve (médaillés or/argent/bronze)           |
| 6-Liste des médaillés d'un pays.sql       | Affiche le détail des médailles (participant, épreuve, performance) d’un pays |
| 7-Résultats d'un athlète.sql              | Recherche les résultats d’un athlète donné dans toutes les épreuves    |
| 8-Nombre d'épreuves par sport             | Liste les sports par nombre d'épreuves décroissant   |


##### **Exemple de restitution obtenue avec la requête 6 pour le pays "France" :**

pays | medaille | participant | nom_sport | nom_epreuve | resultats | note
|:-----|:----|:-----|:-----|:-----|:-----|---:|
France | Or | Althea LAURIN | Taekwondo | Plus de 67kg f |  |
France | Or | Benjamin THOMAS | Cyclisme-sur-piste | Omnium hommes | 164 |
France | Or | Cassandre BEAUGRAND | Triathlon | Individuel femmes | 1:54:55 |
France | Or | France | Judo | Equipe mixte |  |
France | Or | France | Rugby-a-7 | Homme |  |
France | Or | France | Volleyball | Homme |  |
France | Or | Joris DAUDET | Cyclisme-bmx-racing | Homme | 31.422 |
France | Or | Kauli VAAST | Surf | Homme |  |
France | Or | Léon MARCHAND | Natation | 200m 4 nages individuel hommes | 1:54.06 |
France | Or | Léon MARCHAND | Natation | 200m brasse hommes | 2:05.85 |
France | Or | Léon MARCHAND | Natation | 200m papillon hommes | 1:51.21 |
France | Or | Léon MARCHAND | Natation | 400m 4 nages individuel hommes | 4:02.95 |
France | Or | Manon BRUNET | Escrime | Sabre individuel femmes |  |
France | Or | Nicolas GESTIN | Canoe-slalom | Canoe simple hommes | 91.36 |
France | Or | Pauline FERRAND-PREVOT | Vtt | Cross country femmes | 1:26:02 |
France | Or | Teddy RINER | Judo | Plus de 100kg h |  |
France | Argent | Anastasiia KIRPICHNIKOVA | Natation | 1500m nage libre femmes | 15:40.35 |
France | Argent | Angele HUG | Canoe-slalom | Kayak cross femmes |  |
France | Argent | Auriane MALLO | Escrime | Epee individuel femmes |  |
France | Argent | Billal BENNAMA | Boxe | 51kg hommes |  |
France | Argent | Camille JEDRZEJEWSKI | Tir | Pistolet 25m f | 37 |
France | Argent | Cyrena SAMBA-MAYELA | Athletisme | 100m haies femmes | 12.34 |
France | Argent | DANY | Breaking | B boys |  |
France | Argent | Elodie CLOUVEL | Pentathlon-moderne | Individuel femmes | 1452 |
France | Argent | France | Basketball | Femme |  |
France | Argent | France | Basketball | Homme |  |
France | Argent | France | Basketball-3x3 | Homme |  |
France | Argent | France | Equitation | Concours complet d equitation equipe | 103.60 |
France | Argent | France | Escrime | Epee par equipes femmes |  |
France | Argent | France | Football | Homme |  |
France | Argent | France | Handball | Femme |  |
France | Argent | France | Tir-a-l-arc | Par equipes hommes |  |
France | Argent | Joan-Benjamin GABA | Judo | 73kg h |  |
France | Argent | Lauriane NOLOT | Voile | Kitesurf femmes |  |
France | Argent | Luka MKHEIDZE | Judo | 60kg h |  |
France | Argent | Sara BALZER | Escrime | Sabre individuel femmes |  |
France | Argent | Sofiane OUMIHA | Boxe | 63 5kg hommes |  |
France | Argent | Sylvain ANDRE | Cyclisme-bmx-racing | Homme | 31.706 |
France | Argent | Titouan CASTRYCK | Canoe-slalom | Kayak simple hommes | 88.42 |
France | Argent | Valentin MADOUAS | Cyclisme-sur-route | Course sur route hommes | 6:20:45 |
France | Argent | Victor KORETZKY | Vtt | Cross country hommes | 1:26:31 |
France | Argent | Yannick BOREL | Escrime | Epee individuel hommes |  |
France | Bronze | Amandine BUCHARD | Judo | 52kg f |  |
France | Bronze | Anthony JEANJEAN | Cyclisme-bmx-freestyle | Park hommes | 93.76 |
France | Bronze | Christophe LAPORTE | Cyclisme-sur-route | Course sur route hommes | 6:20:50 |
France | Bronze | Clarisse AGBEGNENOU | Judo | 63kg f |  |
France | Bronze | Cyrian RAVET | Taekwondo | 58kg h |  |
France | Bronze | Djamili-Dini ABOUDOU MOINDZE | Boxe | Poids super lourds plus de 92kg hommes |  |
France | Bronze | Felix LEBRUN | Tennis-de-table | Simple hommes |  |
France | Bronze | France | Equitation | Saut d obstacles equipe | 7 |
France | Bronze | France | Escrime | Fleuret par equipes hommes |  |
France | Bronze | France | Escrime | Sabre par equipes hommes |  |
France | Bronze | France | Natation | Relais 4x100m 4 nages hommes | 3:28.38 |
France | Bronze | France | Tennis-de-table | Par equipes hommes |  |
France | Bronze | Johanne DEFAY | Surf | Femme |  |
France | Bronze | Leo BERGERE | Triathlon | Individuel hommes | 1:43:43 |
France | Bronze | Lisa BARBELIN | Tir-a-l-arc | Individuel femmes |  |
France | Bronze | Maxime-Gael NGAYAP HAMBOU | Judo | 90kg h |  |
France | Bronze | Romain MAHIEU | Cyclisme-bmx-racing | Homme | 32.022 |
France | Bronze | Romane DICKO | Judo | Plus de 78 kg f |  |
France | Bronze | Sarah Leonie CYSIQUE | Judo | 57 kg f |  |
France | Bronze | Sarah STEYAERT / Charline PICON | Voile | Skiff femmes | 79 |
France | Bronze | Shirine BOUKLI | Judo | 48kg f |  |


#### II.4.3.2 Ajouter une requête

Il est possible de rajouter une nouvelle requête pré définie tout simplement en saisissant la requête en SQL dans un nouveau fichier (.sql) et de placer ce fichier avec les autres dans le dossier "\paris2024\src\database\requetes_sql". Le nom du fichier sera automatiquement proposé dans le menu à son prochain lancement.


#### II.4.3.3 Recherches floues et insensibles à la casse

Pour certaines requêtes, les recherches sont volontairement rendues floues et insensibles à la casse. C’est le cas notamment pour la recherche d’épreuves ou de pays, où le paramètre saisi est comparé en minuscules à une concaténation de colonnes;

J'utilise pour cela une clause WHERE avec l’opérateur LIKE combiné à LOWER(...) afin de rendre la recherche floue (partielle) et insensible à la casse. 

Exemple pour retrouver une épreuve ou un sport à partir d’un unique mot-clé : je teste si la saisie est présente dans la concaténation du sport et de l'épreuve, ce qui permet de trouver par exemple tous les sports et toutes les épreuves contenant le mot "relais".
```
sql
WHERE LOWER(s.nom_sport || e.nom_epreuve) LIKE '%' || LOWER(:epreuve) || '%'
```
 Autre exemple pour re trouver un ensemble de pays à partir de son code ou son libellé :
```
sql
WHERE LOWER(p.id_pays || p.nom_pays) LIKE '%' || LOWER(:pays) || '%'
```

Cela permet de saisir par exemple :
```txt
pays = ANDE
```
Et d’obtenir tous les résultats comme :

| Pays              | Médaille | Nb |
|:------------------|:---------|---:|
| Grande-Bretagne   | Or       | 14 |
| Grande-Bretagne   | Argent   | 21 |
| Grande-Bretagne   | Bronze   | 29 |
| Irlande           | Or       |  4 |
| Irlande           | Bronze   |  3 |
| Nouvelle-Zélande  | Or       | 10 |
| Nouvelle-Zélande  | Argent   |  7 |
| Nouvelle-Zélande  | Bronze   |  3 |
| Thaïlande         | Or       |  1 |
| Thaïlande         | Argent   |  3 |
| Thaïlande         | Bronze   |  2 |



___________________
# III - Conclusion

Ce projet m’a permis d’explorer de bout en bout une problématique concrète de collecte et d’exploitation de données issues d’un site web moderne. L’objectif était de récupérer automatiquement les résultats des épreuves des Jeux Olympiques de Paris 2024, puis de structurer ces données dans une base relationnelle interrogeable. Pour cela, j’ai utilisé Playwright afin d’automatiser la navigation sur un site entièrement dynamique, ce qui m’a confronté à des problématiques comme le chargement différé des blocs, le scroll automatique ou encore la gestion des éléments interactifs. La suite du projet m’a conduit à modéliser les données sous forme de tables normalisées, puis à créer un requêteur SQL simple mais fonctionnel. 

Ce travail m’a permis de mobiliser des compétences en Python, JavaScript, modélisation relationnelle et manipulation de données, telles qu’enseignées dans le cadre du parcours Data Science & IA de l’ESIEE. De plus, cela m’a permis de franchir un cap avec l'utilisation de Playwright, ayant jusque-là principalement travaillé avec BeautifulSoup pour faire du scraping sur des pages statiques.

Des pistes d’amélioration du projet seraient d'ajouter une variable de configuration pour rendre le projet compatible avec d’autres éditions des Jeux Olympiques (Tokyo 2020, Londres 2012, etc.), ou intégrer un module de visualisation graphique pour compléter les requêtes SQL par des représentations plus conviviales qui pourraient de plus comparer les éditions entre elles.






