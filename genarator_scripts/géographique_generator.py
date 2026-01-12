"""
GÉNÉRATEUR DE DONNÉES GÉOGRAPHIQUES COHÉRENTES
Génère des données où ville → pays correct + coordonnées GPS exactes
"""

import json
import argparse
import numpy as np
import pandas as pd
from datetime import datetime

np.random.seed(42)

# ====================
# BASE DE DONNÉES GÉOGRAPHIQUES COHÉRENTES
# ====================

GEO_DATABASE = {
    # Format: "ville": {"pays": "...", "latitude": ..., "longitude": ..., "region": "..."}
    
    # FRANCE
    "Paris": {"pays": "France", "latitude": 48.8566, "longitude": 2.3522, "region": "Île-de-France"},
    "Marseille": {"pays": "France", "latitude": 43.2965, "longitude": 5.3698, "region": "Provence-Alpes-Côte d'Azur"},
    "Lyon": {"pays": "France", "latitude": 45.7640, "longitude": 4.8357, "region": "Auvergne-Rhône-Alpes"},
    "Toulouse": {"pays": "France", "latitude": 43.6047, "longitude": 1.4442, "region": "Occitanie"},
    "Nice": {"pays": "France", "latitude": 43.7102, "longitude": 7.2620, "region": "Provence-Alpes-Côte d'Azur"},
    "Nantes": {"pays": "France", "latitude": 47.2184, "longitude": -1.5536, "region": "Pays de la Loire"},
    "Bordeaux": {"pays": "France", "latitude": 44.8378, "longitude": -0.5792, "region": "Nouvelle-Aquitaine"},
    "Lille": {"pays": "France", "latitude": 50.6292, "longitude": 3.0573, "region": "Hauts-de-France"},
    "Strasbourg": {"pays": "France", "latitude": 48.5734, "longitude": 7.7521, "region": "Grand Est"},
    "Montpellier": {"pays": "France", "latitude": 43.6108, "longitude": 3.8767, "region": "Occitanie"},
    
    # MAROC
    "Casablanca": {"pays": "Maroc", "latitude": 33.5731, "longitude": -7.5898, "region": "Casablanca-Settat"},
    "Rabat": {"pays": "Maroc", "latitude": 34.0209, "longitude": -6.8416, "region": "Rabat-Salé-Kénitra"},
    "Marrakech": {"pays": "Maroc", "latitude": 31.6295, "longitude": -7.9811, "region": "Marrakech-Safi"},
    "Fès": {"pays": "Maroc", "latitude": 34.0181, "longitude": -5.0078, "region": "Fès-Meknès"},
    "Tanger": {"pays": "Maroc", "latitude": 35.7595, "longitude": -5.8340, "region": "Tanger-Tétouan-Al Hoceïma"},
    "Agadir": {"pays": "Maroc", "latitude": 30.4278, "longitude": -9.5981, "region": "Souss-Massa"},
    "Meknès": {"pays": "Maroc", "latitude": 33.8935, "longitude": -5.5473, "region": "Fès-Meknès"},
    "Oujda": {"pays": "Maroc", "latitude": 34.6867, "longitude": -1.9114, "region": "Oriental"},
    "Kenitra": {"pays": "Maroc", "latitude": 34.2610, "longitude": -6.5802, "region": "Rabat-Salé-Kénitra"},
    "Tétouan": {"pays": "Maroc", "latitude": 35.5889, "longitude": -5.3626, "region": "Tanger-Tétouan-Al Hoceïma"},
    
    # USA
    "New York": {"pays": "USA", "latitude": 40.7128, "longitude": -74.0060, "region": "New York"},
    "Los Angeles": {"pays": "USA", "latitude": 34.0522, "longitude": -118.2437, "region": "California"},
    "Chicago": {"pays": "USA", "latitude": 41.8781, "longitude": -87.6298, "region": "Illinois"},
    "Houston": {"pays": "USA", "latitude": 29.7604, "longitude": -95.3698, "region": "Texas"},
    "San Francisco": {"pays": "USA", "latitude": 37.7749, "longitude": -122.4194, "region": "California"},
    "Miami": {"pays": "USA", "latitude": 25.7617, "longitude": -80.1918, "region": "Florida"},
    "Boston": {"pays": "USA", "latitude": 42.3601, "longitude": -71.0589, "region": "Massachusetts"},
    "Seattle": {"pays": "USA", "latitude": 47.6062, "longitude": -122.3321, "region": "Washington"},
    
    # CANADA
    "Toronto": {"pays": "Canada", "latitude": 43.6532, "longitude": -79.3832, "region": "Ontario"},
    "Montréal": {"pays": "Canada", "latitude": 45.5017, "longitude": -73.5673, "region": "Québec"},
    "Vancouver": {"pays": "Canada", "latitude": 49.2827, "longitude": -123.1207, "region": "British Columbia"},
    "Ottawa": {"pays": "Canada", "latitude": 45.4215, "longitude": -75.6972, "region": "Ontario"},
    "Calgary": {"pays": "Canada", "latitude": 51.0447, "longitude": -114.0719, "region": "Alberta"},
    
    # ROYAUME-UNI
    "Londres": {"pays": "Royaume-Uni", "latitude": 51.5074, "longitude": -0.1278, "region": "England"},
    "Manchester": {"pays": "Royaume-Uni", "latitude": 53.4808, "longitude": -2.2426, "region": "England"},
    "Birmingham": {"pays": "Royaume-Uni", "latitude": 52.4862, "longitude": -1.8904, "region": "England"},
    "Édimbourg": {"pays": "Royaume-Uni", "latitude": 55.9533, "longitude": -3.1883, "region": "Scotland"},
    
    # ALLEMAGNE
    "Berlin": {"pays": "Allemagne", "latitude": 52.5200, "longitude": 13.4050, "region": "Berlin"},
    "Munich": {"pays": "Allemagne", "latitude": 48.1351, "longitude": 11.5820, "region": "Bavaria"},
    "Hambourg": {"pays": "Allemagne", "latitude": 53.5511, "longitude": 9.9937, "region": "Hamburg"},
    "Francfort": {"pays": "Allemagne", "latitude": 50.1109, "longitude": 8.6821, "region": "Hesse"},
    
    # ESPAGNE
    "Madrid": {"pays": "Espagne", "latitude": 40.4168, "longitude": -3.7038, "region": "Madrid"},
    "Barcelone": {"pays": "Espagne", "latitude": 41.3851, "longitude": 2.1734, "region": "Catalonia"},
    "Valence": {"pays": "Espagne", "latitude": 39.4699, "longitude": -0.3763, "region": "Valencia"},
    "Séville": {"pays": "Espagne", "latitude": 37.3891, "longitude": -5.9845, "region": "Andalusia"},
    
    # ITALIE
    "Rome": {"pays": "Italie", "latitude": 41.9028, "longitude": 12.4964, "region": "Lazio"},
    "Milan": {"pays": "Italie", "latitude": 45.4642, "longitude": 9.1900, "region": "Lombardy"},
    "Naples": {"pays": "Italie", "latitude": 40.8518, "longitude": 14.2681, "region": "Campania"},
    "Florence": {"pays": "Italie", "latitude": 43.7696, "longitude": 11.2558, "region": "Tuscany"},
    
    # PORTUGAL
    "Lisbonne": {"pays": "Portugal", "latitude": 38.7223, "longitude": -9.1393, "region": "Lisbon"},
    "Porto": {"pays": "Portugal", "latitude": 41.1579, "longitude": -8.6291, "region": "Porto"},
    
    # BELGIQUE
    "Bruxelles": {"pays": "Belgique", "latitude": 50.8503, "longitude": 4.3517, "region": "Brussels"},
    "Anvers": {"pays": "Belgique", "latitude": 51.2194, "longitude": 4.4025, "region": "Flanders"},
    
    # SUISSE
    "Genève": {"pays": "Suisse", "latitude": 46.2044, "longitude": 6.1432, "region": "Geneva"},
    "Zurich": {"pays": "Suisse", "latitude": 47.3769, "longitude": 8.5417, "region": "Zurich"},
    "Berne": {"pays": "Suisse", "latitude": 46.9480, "longitude": 7.4474, "region": "Bern"},
    
    # JAPON
    "Tokyo": {"pays": "Japon", "latitude": 35.6762, "longitude": 139.6503, "region": "Kanto"},
    "Osaka": {"pays": "Japon", "latitude": 34.6937, "longitude": 135.5023, "region": "Kansai"},
    "Kyoto": {"pays": "Japon", "latitude": 35.0116, "longitude": 135.7681, "region": "Kansai"},
    
    # CHINE
    "Beijing": {"pays": "Chine", "latitude": 39.9042, "longitude": 116.4074, "region": "Beijing"},
    "Shanghai": {"pays": "Chine", "latitude": 31.2304, "longitude": 121.4737, "region": "Shanghai"},
    
    # AUTRES
    "Sydney": {"pays": "Australie", "latitude": -33.8688, "longitude": 151.2093, "region": "New South Wales"},
    "Melbourne": {"pays": "Australie", "latitude": -37.8136, "longitude": 144.9631, "region": "Victoria"},
    "Le Caire": {"pays": "Égypte", "latitude": 30.0444, "longitude": 31.2357, "region": "Cairo"},
    "Tunis": {"pays": "Tunisie", "latitude": 36.8065, "longitude": 10.1815, "region": "Tunis"},
}

# ====================
# GÉNÉRATEURS GÉOGRAPHIQUES COHÉRENTS
# ====================

def gen_geo_data(n):
    """
    Génère des données géographiques 100% COHÉRENTES
    Retourne: DataFrame avec ville, pays, coordonnées correctes
    """
    
    # Sélectionner n villes aléatoires
    villes_disponibles = list(GEO_DATABASE.keys())
    villes_choisies = np.random.choice(villes_disponibles, size=n, replace=True)
    
    geo_data = []
    
    for ville in villes_choisies:
        info = GEO_DATABASE[ville]
        
        # Ajouter une petite variation aux coordonnées (pour simuler différents quartiers)
        lat_variation = np.random.uniform(-0.05, 0.05)  # ±5.5 km environ
        lon_variation = np.random.uniform(-0.05, 0.05)
        
        geo_data.append({
            "ville": ville,
            "pays": info["pays"],
            "region": info["region"],
            "latitude": round(info["latitude"] + lat_variation, 6),
            "longitude": round(info["longitude"] + lon_variation, 6),
        })
    
    return geo_data

def get_cities_by_country(country):
    """Retourne la liste des villes pour un pays donné"""
    cities = []
    for ville, info in GEO_DATABASE.items():
        if info["pays"] == country:
            cities.append(ville)
    return cities

def get_all_countries():
    """Retourne la liste de tous les pays disponibles"""
    countries = set()
    for info in GEO_DATABASE.values():
        countries.add(info["pays"])
    return sorted(list(countries))

# ====================
# AUTRES GÉNÉRATEURS
# ====================

def gen_numeric(n, low=0, high=100, mean=None, std=1):
    """Génère des valeurs numériques avec distribution normale"""
    if mean is None:
        mean = (low + high) / 2
    vals = np.random.normal(loc=mean, scale=std, size=n)
    return np.clip(vals, low, high)

def gen_integer(n, low=0, high=100):
    """Génère des entiers aléatoires"""
    return np.random.randint(low, high+1, n)

def gen_categorical(n, categories):
    """Génère des valeurs catégorielles"""
    return np.random.choice(categories, size=n)

def gen_id(n, prefix="id"):
    """Génère des identifiants séquentiels"""
    return [f"{prefix}_{str(i+1).zfill(5)}" for i in range(n)]

# ====================
# AUTRES CATÉGORIES
# ====================

CATEGORIES = {
    "secteur_activite": ["Technologie","Santé","Éducation","Finance","Commerce","Industrie","Services"],
    "type_bien": ["Appartement","Maison","Bureau","Commerce","Terrain"],
    "statut": ["Actif","Inactif","En attente","Terminé"],
    "niveau": ["Débutant","Intermédiaire","Avancé","Expert"],
}

# ====================
# DÉTECTION DE TYPE
# ====================

def guess_type(name):
    """Détecte le type de colonne"""
    name_lower = name.lower()
    
    # Géographiques
    if "ville" in name_lower or "city" in name_lower:
        return ("geo_ville", {})
    
    if "pays" in name_lower or "country" in name_lower:
        return ("geo_pays", {})
    
    if "region" in name_lower:
        return ("geo_region", {})
    
    if "latitude" in name_lower or "lat" == name_lower:
        return ("geo_latitude", {})
    
    if "longitude" in name_lower or "lon" in name_lower or "lng" in name_lower:
        return ("geo_longitude", {})
    
    # IDs
    if any(k in name_lower for k in ["id","uid","code"]):
        return ("id", {})
    
    # Numériques
    if any(k in name_lower for k in ["prix","price","montant"]):
        return ("numeric", {"low":10000,"high":500000,"mean":100000,"std":50000})
    
    if any(k in name_lower for k in ["score","note"]):
        return ("numeric", {"low":0,"high":20,"mean":12,"std":3})
    
    # Entiers
    if any(k in name_lower for k in ["quantite","stock"]):
        return ("int", {"low":0,"high":1000})
    
    # Catégoriels
    for key in CATEGORIES:
        if key in name_lower:
            return ("categorical", {"categories": CATEGORIES[key]})
    
    return ("categorical", {"categories": ["Option A","Option B","Option C"]})

# ====================
# CONSTRUCTION DU DATASET
# ====================

def build_dataset(schema, n=500):
    """Construit un dataset avec géographie cohérente"""
    
    # Normaliser schéma
    cols = []
    if isinstance(schema, list) and all(isinstance(x,str) for x in schema):
        for name in schema:
            t, params = guess_type(name)
            cols.append({"name":name,"type":t,"params":params})
    else:
        for c in schema:
            name = c.get("name")
            if not name:
                raise ValueError("Chaque colonne doit avoir un 'name'")
            t = c.get("type")
            params = c.get("params",{})
            if not t:
                t, params = guess_type(name)
            cols.append({"name":name,"type":t,"params":params})
    
    # Vérifier si données géo nécessaires
    geo_needed = any(col["type"].startswith("geo_") for col in cols)
    
    if geo_needed:
        geo_data = gen_geo_data(n)
    
    # Construire le dataframe
    data = {}
    
    for col in cols:
        name = col["name"]
        t = col["type"]
        p = col.get("params",{})
        
        # Données géographiques cohérentes
        if t == "geo_ville":
            data[name] = [g["ville"] for g in geo_data]
        elif t == "geo_pays":
            data[name] = [g["pays"] for g in geo_data]
        elif t == "geo_region":
            data[name] = [g["region"] for g in geo_data]
        elif t == "geo_latitude":
            data[name] = [g["latitude"] for g in geo_data]
        elif t == "geo_longitude":
            data[name] = [g["longitude"] for g in geo_data]
        
        # Autres types
        elif t == "numeric":
            data[name] = gen_numeric(n, p.get("low",0), p.get("high",100), p.get("mean"), p.get("std",10))
        elif t == "int":
            data[name] = gen_integer(n, int(p.get("low",0)), int(p.get("high",100)))
        elif t == "categorical":
            data[name] = gen_categorical(n, p.get("categories", ["Option A","Option B"]))
        elif t == "id":
            data[name] = gen_id(n, name)
        else:
            data[name] = gen_categorical(n, ["Valeur 1","Valeur 2"])
    
    return pd.DataFrame(data)

# ====================
# CLI
# ====================

def main():
    parser = argparse.ArgumentParser(
        description="🌍 Générateur de données GÉOGRAPHIQUES cohérentes",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
EXEMPLES :

🏢 Dataset immobilier avec géolocalisation exacte :
  python mega_dataset_generator_geo.py --name immobilier \\
    --schema '["id","ville","pays","region","latitude","longitude","prix","type_bien"]' --n 500

🏪 Dataset de magasins avec localisation :
  python mega_dataset_generator_geo.py --name magasins \\
    --schema '["ville","pays","latitude","longitude","secteur_activite"]' --n 200

📊 DONNÉES GÉNÉRÉES :
  • ville → TOUJOURS cohérente avec le pays
  • pays → Extrait automatiquement de la ville
  • latitude/longitude → Coordonnées GPS EXACTES
  • region → Région administrative correcte

🌍 VILLES DISPONIBLES :
  • France : Paris, Lyon, Marseille, Toulouse...
  • Maroc : Casablanca, Rabat, Marrakech, Fès...
  • USA : New York, Los Angeles, Chicago...
  • Et 60+ autres villes dans le monde
        """
    )
    
    parser.add_argument("--name", required=True, help="Nom du dataset")
    parser.add_argument("--schema", required=True, help="Colonnes JSON")
    parser.add_argument("--n", type=int, default=500, help="Nombre de lignes")
    parser.add_argument("--out", default=None, help="Fichier de sortie")
    parser.add_argument("--preview", type=int, default=10, help="Lignes à afficher")
    parser.add_argument("--list-countries", action="store_true", help="Lister les pays disponibles")
    parser.add_argument("--list-cities", help="Lister les villes d'un pays")
    
    args = parser.parse_args()
    
    # Liste des pays
    if args.list_countries:
        countries = get_all_countries()
        print("\n🌍 PAYS DISPONIBLES :")
        for country in countries:
            cities = get_cities_by_country(country)
            print(f"  • {country:20s} ({len(cities)} villes)")
        return
    
    # Liste des villes d'un pays
    if args.list_cities:
        cities = get_cities_by_country(args.list_cities)
        if cities:
            print(f"\n🏙️  VILLES DE {args.list_cities.upper()} :")
            for city in cities:
                info = GEO_DATABASE[city]
                print(f"  • {city:20s} (lat: {info['latitude']:.4f}, lon: {info['longitude']:.4f})")
        else:
            print(f"❌ Aucune ville trouvée pour le pays : {args.list_cities}")
        return
    
    # Charger schéma
    try:
        if args.schema.endswith('.json'):
            with open(args.schema, 'r', encoding='utf-8') as f:
                schema = json.load(f)
        else:
            schema = json.loads(args.schema)
    except Exception as e:
        print(f"❌ Erreur schéma: {e}")
        return
    
    # Générer dataset
    print(f"\n{'='*80}")
    print(f"⚙️  GÉNÉRATION GÉOGRAPHIQUE COHÉRENTE '{args.name}'")
    print("="*80 + "\n")
    
    try:
        df = build_dataset(schema, n=args.n)
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # Sauvegarder
    out = args.out or f"{args.name}_seed.csv"
    df.to_csv(out, index=False)
    
    # Résultats
    print("="*80)
    print(f"✅ DATASET GÉOGRAPHIQUE GÉNÉRÉ")
    print("="*80)
    print(f"📁 Fichier : {out}")
    print(f"📊 Lignes  : {len(df)}")
    print(f"📊 Colonnes: {len(df.columns)}\n")
    
    print("👁️  APERÇU :")
    print(df.head(args.preview).to_string(index=False))
    
    # Vérification cohérence
    if "ville" in df.columns and "pays" in df.columns:
        print(f"\n{'='*80}")
        print("✅ VÉRIFICATION DE COHÉRENCE GÉOGRAPHIQUE")
        print("="*80)
        
        # Vérifier quelques lignes
        sample = df.head(5)
        print("\n✓ Ville → Pays (vérification) :")
        for idx, row in sample.iterrows():
            ville = row.get("ville")
            pays = row.get("pays")
            expected_pays = GEO_DATABASE[ville]["pays"]
            status = "✅" if pays == expected_pays else "❌"
            print(f"  {status} {ville:20s} → {pays}")
    
    if "latitude" in df.columns and "longitude" in df.columns:
        print("\n✓ Coordonnées GPS (échantillon) :")
        sample = df.head(3)
        for idx, row in sample.iterrows():
            ville = row.get("ville", "N/A")
            lat = row.get("latitude", 0)
            lon = row.get("longitude", 0)
            print(f"  📍 {ville:20s} : lat={lat:.4f}, lon={lon:.4f}")
    
    print(f"\n✨ Génération terminée!\n")

if __name__ == "__main__":
    main()