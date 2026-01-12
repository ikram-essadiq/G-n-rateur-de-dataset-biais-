"""
GÉNÉRATEUR DE DONNÉES SPORTS & ACTIVITÉS INTERNATIONAL
Génère des données cohérentes pour sports, équipes, athlètes, compétitions
"""

import json
import argparse
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

np.random.seed(42)

# ====================
# BASE DE DONNÉES SPORTS
# ====================

SPORTS_DATABASE = {
    # ============ FOOTBALL ============
    "Real Madrid": {
        "sport": "Football", "pays": "Espagne", "ville": "Madrid",
        "ligue": "La Liga", "stade": "Santiago Bernabéu", "capacite": 81044,
        "fondation": 1902, "continent": "Europe"
    },
    "FC Barcelona": {
        "sport": "Football", "pays": "Espagne", "ville": "Barcelone",
        "ligue": "La Liga", "stade": "Camp Nou", "capacite": 99354,
        "fondation": 1899, "continent": "Europe"
    },
    "Manchester United": {
        "sport": "Football", "pays": "Angleterre", "ville": "Manchester",
        "ligue": "Premier League", "stade": "Old Trafford", "capacite": 74879,
        "fondation": 1878, "continent": "Europe"
    },
    "Bayern Munich": {
        "sport": "Football", "pays": "Allemagne", "ville": "Munich",
        "ligue": "Bundesliga", "stade": "Allianz Arena", "capacite": 75024,
        "fondation": 1900, "continent": "Europe"
    },
    "Paris Saint-Germain": {
        "sport": "Football", "pays": "France", "ville": "Paris",
        "ligue": "Ligue 1", "stade": "Parc des Princes", "capacite": 47929,
        "fondation": 1970, "continent": "Europe"
    },
    "Raja Casablanca": {
        "sport": "Football", "pays": "Maroc", "ville": "Casablanca",
        "ligue": "Botola Pro", "stade": "Stade Mohamed V", "capacite": 45891,
        "fondation": 1949, "continent": "Afrique"
    },
    "Wydad Casablanca": {
        "sport": "Football", "pays": "Maroc", "ville": "Casablanca",
        "ligue": "Botola Pro", "stade": "Stade Mohamed V", "capacite": 45891,
        "fondation": 1937, "continent": "Afrique"
    },
    
    # ============ BASKETBALL ============
    "Los Angeles Lakers": {
        "sport": "Basketball", "pays": "USA", "ville": "Los Angeles",
        "ligue": "NBA", "stade": "Crypto.com Arena", "capacite": 18997,
        "fondation": 1947, "continent": "Amérique du Nord"
    },
    "Chicago Bulls": {
        "sport": "Basketball", "pays": "USA", "ville": "Chicago",
        "ligue": "NBA", "stade": "United Center", "capacite": 20917,
        "fondation": 1966, "continent": "Amérique du Nord"
    },
    "Golden State Warriors": {
        "sport": "Basketball", "pays": "USA", "ville": "San Francisco",
        "ligue": "NBA", "stade": "Chase Center", "capacite": 18064,
        "fondation": 1946, "continent": "Amérique du Nord"
    },
    
    # ============ TENNIS ============
    "Roland-Garros": {
        "sport": "Tennis", "pays": "France", "ville": "Paris",
        "ligue": "Grand Slam", "stade": "Stade Roland-Garros", "capacite": 15225,
        "fondation": 1891, "continent": "Europe"
    },
    "Wimbledon": {
        "sport": "Tennis", "pays": "Angleterre", "ville": "Londres",
        "ligue": "Grand Slam", "stade": "All England Club", "capacite": 15000,
        "fondation": 1877, "continent": "Europe"
    },
    "US Open": {
        "sport": "Tennis", "pays": "USA", "ville": "New York",
        "ligue": "Grand Slam", "stade": "USTA Billie Jean King", "capacite": 23771,
        "fondation": 1881, "continent": "Amérique du Nord"
    },
    
    # ============ RUGBY ============
    "All Blacks": {
        "sport": "Rugby", "pays": "Nouvelle-Zélande", "ville": "Wellington",
        "ligue": "International", "stade": "Sky Stadium", "capacite": 34500,
        "fondation": 1903, "continent": "Océanie"
    },
    "Springboks": {
        "sport": "Rugby", "pays": "Afrique du Sud", "ville": "Pretoria",
        "ligue": "International", "stade": "Loftus Versfeld", "capacite": 51762,
        "fondation": 1891, "continent": "Afrique"
    },
    
    # ============ ATHLÉTISME ============
    "Stade de France": {
        "sport": "Athlétisme", "pays": "France", "ville": "Paris",
        "ligue": "International", "stade": "Stade de France", "capacite": 80698,
        "fondation": 1998, "continent": "Europe"
    },
}

ATHLETES = {
    "Football": ["Mohamed Salah", "Kylian Mbappé", "Erling Haaland", "Achraf Hakimi", "Hakim Ziyech"],
    "Basketball": ["LeBron James", "Stephen Curry", "Kevin Durant", "Giannis Antetokounmpo"],
    "Tennis": ["Novak Djokovic", "Carlos Alcaraz", "Iga Świątek", "Aryna Sabalenka"],
    "Rugby": ["Antoine Dupont", "Beauden Barrett", "Cheslin Kolbe"],
    "Athlétisme": ["Usain Bolt", "Eliud Kipchoge", "Mondo Duplantis", "Faith Kipyegon"],
}

SPORTS_CATEGORIES = {
    "type_activite": ["Match", "Entraînement", "Tournoi", "Compétition", "Stage", "Amical"],
    "statut_match": ["Terminé", "En cours", "À venir", "Reporté", "Annulé"],
    "resultat": ["Victoire", "Défaite", "Nul", "Forfait"],
    "niveau": ["Amateur", "Semi-Pro", "Professionnel", "Elite", "International"],
    "categorie_age": ["U12", "U15", "U18", "U21", "Senior", "Vétéran"],
    "type_abonnement": ["Mensuel", "Trimestriel", "Annuel", "Illimité"],
    "surface": ["Pelouse", "Synthétique", "Parquet", "Terre Battue", "Gazon", "Tartan"],
}

def gen_combined_sports_data(n):
    """Génère des données cohérentes avec équipe/lieu + événement liés"""
    clubs = list(SPORTS_DATABASE.keys())
    data = []
    
    for i in range(n):
        # Choisir un club/lieu aléatoire
        club = np.random.choice(clubs)
        info = SPORTS_DATABASE[club]
        
        # Sport spécifique
        sport = info["sport"]
        
        # Type d'activité
        type_act = np.random.choice(SPORTS_CATEGORIES["type_activite"])
        statut = np.random.choice(SPORTS_CATEGORIES["statut_match"], 
                                 p=[0.6, 0.15, 0.2, 0.03, 0.02])
        
        # Scores selon le sport
        if sport == "Football":
            score_local = np.random.poisson(1.5)
            score_visiteur = np.random.poisson(1.2)
            duree = 90
            spectateurs = int(np.random.uniform(0.4, 0.95) * info["capacite"])
        elif sport == "Basketball":
            score_local = np.random.normal(105, 12)
            score_visiteur = np.random.normal(100, 12)
            duree = 48
            spectateurs = int(np.random.uniform(0.5, 1.0) * info["capacite"])
        elif sport == "Tennis":
            score_local = np.random.choice([0, 1, 2, 3])
            score_visiteur = np.random.choice([0, 1, 2, 3])
            duree = np.random.randint(90, 240)
            spectateurs = int(np.random.uniform(0.3, 0.9) * info["capacite"])
        elif sport == "Rugby":
            score_local = np.random.poisson(18)
            score_visiteur = np.random.poisson(15)
            duree = 80
            spectateurs = int(np.random.uniform(0.6, 1.0) * info["capacite"])
        else:
            score_local = np.random.randint(0, 100)
            score_visiteur = np.random.randint(0, 100)
            duree = np.random.randint(60, 120)
            spectateurs = int(np.random.uniform(0.3, 0.8) * info["capacite"])
        
        # Résultat
        if score_local > score_visiteur:
            resultat = "Victoire"
        elif score_local < score_visiteur:
            resultat = "Défaite"
        else:
            resultat = "Nul"
        
        # Prix selon le niveau
        if info["ligue"] in ["NBA", "Premier League", "La Liga"]:
            prix_billet = np.random.uniform(50, 250)
        elif info["ligue"] == "Grand Slam":
            prix_billet = np.random.uniform(80, 400)
        else:
            prix_billet = np.random.uniform(15, 100)
        
        # Athlète
        athlete = np.random.choice(ATHLETES.get(sport, ["Athlète Inconnu"]))
        
        # Niveau et catégorie
        niveau = np.random.choice(SPORTS_CATEGORIES["niveau"])
        categorie = np.random.choice(SPORTS_CATEGORIES["categorie_age"])
        
        data.append({
            "club": club,
            "sport": sport,
            "pays": info["pays"],
            "ville": info["ville"],
            "continent": info["continent"],
            "ligue": info["ligue"],
            "stade": info["stade"],
            "capacite": info["capacite"],
            "annee_fondation": info["fondation"],
            "type_activite": type_act,
            "statut": statut,
            "score_local": int(score_local),
            "score_visiteur": int(score_visiteur),
            "resultat": resultat,
            "duree_minutes": duree,
            "spectateurs": spectateurs,
            "prix_billet": round(prix_billet, 2),
            "athlete": athlete,
            "niveau": niveau,
            "categorie_age": categorie,
        })
    
    return data

def build_sports_dataset(schema, n=500):
    cols = []
    if isinstance(schema, list) and all(isinstance(x, str) for x in schema):
        cols = [{"name": name} for name in schema]
    else:
        cols = schema
    
    # Générer les données combinées
    combined_data = gen_combined_sports_data(n)
    
    data = {}
    
    for col in cols:
        name = col["name"]
        nl = name.lower()
        
        # Mapping des colonnes
        if "club" in nl or "equipe" in nl or "team" in nl:
            data[name] = [d["club"] for d in combined_data]
        elif nl == "sport" or "discipline" in nl:
            data[name] = [d["sport"] for d in combined_data]
        elif "ville" in nl or "city" in nl:
            data[name] = [d["ville"] for d in combined_data]
        elif "pays" in nl or "country" in nl:
            data[name] = [d["pays"] for d in combined_data]
        elif "continent" in nl or "region" in nl:
            data[name] = [d["continent"] for d in combined_data]
        elif "ligue" in nl or "championnat" in nl or "league" in nl:
            data[name] = [d["ligue"] for d in combined_data]
        elif "stade" in nl or "lieu" in nl or "venue" in nl:
            data[name] = [d["stade"] for d in combined_data]
        elif "capacite" in nl or "capacity" in nl:
            data[name] = [d["capacite"] for d in combined_data]
        elif "fondation" in nl or "creation" in nl:
            data[name] = [d["annee_fondation"] for d in combined_data]
        elif "type" in nl and ("activite" in nl or "event" in nl):
            data[name] = [d["type_activite"] for d in combined_data]
        elif "statut" in nl or "status" in nl:
            data[name] = [d["statut"] for d in combined_data]
        elif "score" in nl and "local" in nl:
            data[name] = [d["score_local"] for d in combined_data]
        elif "score" in nl and ("visiteur" in nl or "exterieur" in nl or "away" in nl):
            data[name] = [d["score_visiteur"] for d in combined_data]
        elif "resultat" in nl or "result" in nl:
            data[name] = [d["resultat"] for d in combined_data]
        elif "duree" in nl or "duration" in nl:
            data[name] = [d["duree_minutes"] for d in combined_data]
        elif "spectateur" in nl or "attendance" in nl or "public" in nl:
            data[name] = [d["spectateurs"] for d in combined_data]
        elif "prix" in nl or "tarif" in nl or "price" in nl:
            data[name] = [d["prix_billet"] for d in combined_data]
        elif "athlete" in nl or "joueur" in nl or "player" in nl:
            data[name] = [d["athlete"] for d in combined_data]
        elif "niveau" in nl or "level" in nl:
            data[name] = [d["niveau"] for d in combined_data]
        elif "categorie" in nl or "age" in nl:
            data[name] = [d["categorie_age"] for d in combined_data]
        # IDs
        elif nl in ["id", "id_match", "id_event", "id_membre", "id_inscription"]:
            data[name] = [f"{name}_{str(i+1).zfill(8)}" for i in range(n)]
        # Dates
        elif "date" in nl:
            base = datetime(2024, 1, 1)
            dates = [base + timedelta(days=int(i * 365 / n)) for i in range(n)]
            data[name] = [d.strftime("%Y-%m-%d") for d in dates]
        # Heure
        elif "heure" in nl or "time" in nl:
            heures = [f"{np.random.randint(10, 22)}:{np.random.choice(['00', '15', '30', '45'])}" for _ in range(n)]
            data[name] = heures
        else:
            # Valeur par défaut
            print(f"⚠️  Colonne '{name}' non reconnue, valeurs aléatoires générées")
            data[name] = np.random.uniform(0, 100, n)
    
    return pd.DataFrame(data)

def main():
    parser = argparse.ArgumentParser(description="⚽ Générateur Sports & Activités")
    parser.add_argument("--name", required=True, help="Nom dataset")
    parser.add_argument("--schema", required=True, help="Colonnes JSON")
    parser.add_argument("--n", type=int, default=500)
    parser.add_argument("--out", default=None)
    parser.add_argument("--preview", type=int, default=10)
    
    args = parser.parse_args()
    
    try:
        schema = json.loads(args.schema) if not args.schema.endswith('.json') else json.load(open(args.schema))
    except Exception as e:
        print(f"❌ Erreur schéma: {e}")
        return
    
    print(f"\n{'='*80}")
    print(f"⚽ GÉNÉRATION DATASET SPORTS '{args.name}'")
    print("="*80 + "\n")
    
    df = build_sports_dataset(schema, n=args.n)
    
    out = args.out or f"{args.name}_sports.csv"
    df.to_csv(out, index=False)
    
    print("="*80)
    print(f"✅ DATASET SPORTS GÉNÉRÉ")
    print("="*80)
    print(f"📁 Fichier : {out}")
    print(f"📊 Lignes  : {len(df)}")
    print(f"📊 Colonnes: {len(df.columns)}\n")
    
    print("👁️  APERÇU :")
    print(df.head(args.preview).to_string(index=False))
    
    # Statistiques par sport
    if "sport" in df.columns:
        print(f"\n{'='*80}")
        print("🏃 RÉPARTITION PAR SPORT")
        print("="*80)
        print(df["sport"].value_counts().to_string())
    
    # Statistiques par pays
    if "pays" in df.columns:
        print(f"\n{'='*80}")
        print("🌍 RÉPARTITION PAR PAYS")
        print("="*80)
        print(df["pays"].value_counts().to_string())
    
    # Statistiques par résultat
    if "resultat" in df.columns:
        print(f"\n{'='*80}")
        print("📊 RÉPARTITION PAR RÉSULTAT")
        print("="*80)
        print(df["resultat"].value_counts().to_string())
    
    print(f"\n✨ Génération terminée!\n")

if __name__ == "__main__":
    main()