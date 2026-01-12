"""
GÉNÉRATEUR DE DONNÉES SECTEUR ÉNERGIE
Génère des données cohérentes pour installations énergétiques, consommation, production
"""

import json
import argparse
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

np.random.seed(42)

# ====================
# BASE DE DONNÉES INSTALLATIONS ÉNERGÉTIQUES
# ====================

ENERGY_DATABASE = {
    # Format: "site": {"type": "...", "pays": "...", "ville": "...", "capacite_mw": ..., ...}
    
    # ============ SOLAIRE ============
    
    # Afrique
    "Parc Solaire Noor": {
        "type": "Solaire", "pays": "Maroc", "ville": "Ouarzazate",
        "latitude": 30.9335, "longitude": -6.9063, "capacite_mw": 580,
        "region": "Drâa-Tafilalet", "mise_service": 2016
    },
    "Parc Solaire Benban": {
        "type": "Solaire", "pays": "Égypte", "ville": "Assouan",
        "latitude": 24.0889, "longitude": 32.8998, "capacite_mw": 1650,
        "region": "Assouan", "mise_service": 2019
    },
    "Centrale Solaire Jasper": {
        "type": "Solaire", "pays": "Afrique du Sud", "ville": "Kimberley",
        "latitude": -28.7321, "longitude": 24.7623, "capacite_mw": 96,
        "region": "Northern Cape", "mise_service": 2014
    },
    
    # Europe
    "Centrale Solaire Cestas": {
        "type": "Solaire", "pays": "France", "ville": "Cestas",
        "latitude": 44.7447, "longitude": -0.6764, "capacite_mw": 300,
        "region": "Nouvelle-Aquitaine", "mise_service": 2015
    },
    "Parc Solaire Núñez de Balboa": {
        "type": "Solaire", "pays": "Espagne", "ville": "Usagre",
        "latitude": 38.4500, "longitude": -6.2833, "capacite_mw": 500,
        "region": "Extremadura", "mise_service": 2020
    },
    "Centrale Solaire Weesow-Willmersdorf": {
        "type": "Solaire", "pays": "Allemagne", "ville": "Werneuchen",
        "latitude": 52.6333, "longitude": 13.7333, "capacite_mw": 187,
        "region": "Brandenburg", "mise_service": 2020
    },
    
    # Asie
    "Parc Solaire Bhadla": {
        "type": "Solaire", "pays": "Inde", "ville": "Bhadla",
        "latitude": 27.5833, "longitude": 71.9167, "capacite_mw": 2245,
        "region": "Rajasthan", "mise_service": 2020
    },
    "Parc Solaire Tengger Desert": {
        "type": "Solaire", "pays": "Chine", "ville": "Zhongwei",
        "latitude": 37.5500, "longitude": 105.1667, "capacite_mw": 1547,
        "region": "Ningxia", "mise_service": 2017
    },
    
    # Amériques
    "Topaz Solar Farm": {
        "type": "Solaire", "pays": "USA", "ville": "San Luis Obispo",
        "latitude": 35.3833, "longitude": -120.0833, "capacite_mw": 550,
        "region": "California", "mise_service": 2014
    },
    "Villanueva Solar Park": {
        "type": "Solaire", "pays": "Mexique", "ville": "Viesca",
        "latitude": 25.3333, "longitude": -102.8000, "capacite_mw": 828,
        "region": "Coahuila", "mise_service": 2018
    },
    
    # ============ ÉOLIEN ============
    
    # Afrique
    "Parc Éolien Tanger I": {
        "type": "Éolien", "pays": "Maroc", "ville": "Tanger",
        "latitude": 35.7595, "longitude": -5.8340, "capacite_mw": 140,
        "region": "Tanger-Tétouan-Al Hoceïma", "mise_service": 2014
    },
    "Lake Turkana Wind Power": {
        "type": "Éolien", "pays": "Kenya", "ville": "Loiyangalani",
        "latitude": 2.7667, "longitude": 36.7000, "capacite_mw": 310,
        "region": "Marsabit", "mise_service": 2019
    },
    
    # Europe
    "Parc Éolien Hornsea One": {
        "type": "Éolien", "pays": "Royaume-Uni", "ville": "Yorkshire",
        "latitude": 53.8833, "longitude": 1.7833, "capacite_mw": 1218,
        "region": "England", "mise_service": 2020
    },
    "Parc Éolien London Array": {
        "type": "Éolien", "pays": "Royaume-Uni", "ville": "Thames Estuary",
        "latitude": 51.6500, "longitude": 1.4833, "capacite_mw": 630,
        "region": "England", "mise_service": 2013
    },
    "Parc Éolien Markbygden": {
        "type": "Éolien", "pays": "Suède", "ville": "Piteå",
        "latitude": 65.8167, "longitude": 21.4833, "capacite_mw": 1101,
        "region": "Norrbotten", "mise_service": 2022
    },
    "Parc Éolien Courseulles": {
        "type": "Éolien", "pays": "France", "ville": "Courseulles-sur-Mer",
        "latitude": 49.3333, "longitude": -0.4500, "capacite_mw": 450,
        "region": "Normandie", "mise_service": 2024
    },
    
    # Asie
    "Gansu Wind Farm": {
        "type": "Éolien", "pays": "Chine", "ville": "Jiuquan",
        "latitude": 39.7667, "longitude": 98.5000, "capacite_mw": 7965,
        "region": "Gansu", "mise_service": 2021
    },
    
    # Amériques
    "Alta Wind Energy Center": {
        "type": "Éolien", "pays": "USA", "ville": "Tehachapi",
        "latitude": 34.9500, "longitude": -118.2167, "capacite_mw": 1548,
        "region": "California", "mise_service": 2013
    },
    "Shepherds Flat Wind Farm": {
        "type": "Éolien", "pays": "USA", "ville": "Arlington",
        "latitude": 45.6667, "longitude": -120.0000, "capacite_mw": 845,
        "region": "Oregon", "mise_service": 2012
    },
    "Enel Green Power Delfina": {
        "type": "Éolien", "pays": "Brésil", "ville": "Casa Nova",
        "latitude": -9.1667, "longitude": -40.9667, "capacite_mw": 300,
        "region": "Bahia", "mise_service": 2018
    },
    
    # ============ HYDRAULIQUE ============
    
    # Afrique
    "Barrage Bin El Ouidane": {
        "type": "Hydraulique", "pays": "Maroc", "ville": "Azilal",
        "latitude": 32.1167, "longitude": -6.5167, "capacite_mw": 135,
        "region": "Béni Mellal-Khénifra", "mise_service": 1953
    },
    "Grand Ethiopian Renaissance Dam": {
        "type": "Hydraulique", "pays": "Éthiopie", "ville": "Guba",
        "latitude": 11.2167, "longitude": 35.0917, "capacite_mw": 6450,
        "region": "Benishangul-Gumuz", "mise_service": 2022
    },
    "Barrage d'Assouan": {
        "type": "Hydraulique", "pays": "Égypte", "ville": "Assouan",
        "latitude": 23.9667, "longitude": 32.8833, "capacite_mw": 2100,
        "region": "Assouan", "mise_service": 1970
    },
    
    # Asie
    "Barrage des Trois Gorges": {
        "type": "Hydraulique", "pays": "Chine", "ville": "Yichang",
        "latitude": 30.8239, "longitude": 111.0031, "capacite_mw": 22500,
        "region": "Hubei", "mise_service": 2012
    },
    "Barrage d'Itaipu": {
        "type": "Hydraulique", "pays": "Brésil", "ville": "Foz do Iguaçu",
        "latitude": -25.4083, "longitude": -54.5889, "capacite_mw": 14000,
        "region": "Paraná", "mise_service": 1984
    },
    "Barrage de Xiluodu": {
        "type": "Hydraulique", "pays": "Chine", "ville": "Yongshan",
        "latitude": 28.2500, "longitude": 103.6333, "capacite_mw": 13860,
        "region": "Yunnan", "mise_service": 2014
    },
    
    # Amériques
    "Grand Coulee Dam": {
        "type": "Hydraulique", "pays": "USA", "ville": "Coulee Dam",
        "latitude": 47.9547, "longitude": -119.0033, "capacite_mw": 6809,
        "region": "Washington", "mise_service": 1942
    },
    "Barrage Daniel-Johnson": {
        "type": "Hydraulique", "pays": "Canada", "ville": "Baie-Comeau",
        "latitude": 49.2833, "longitude": -68.7167, "capacite_mw": 2596,
        "region": "Québec", "mise_service": 1968
    },
    
    # Europe
    "Grande Dixence": {
        "type": "Hydraulique", "pays": "Suisse", "ville": "Hérémence",
        "latitude": 46.0833, "longitude": 7.4000, "capacite_mw": 2069,
        "region": "Valais", "mise_service": 1961
    },
    
    # ============ NUCLÉAIRE ============
    
    # Europe
    "Centrale Nucléaire de Gravelines": {
        "type": "Nucléaire", "pays": "France", "ville": "Gravelines",
        "latitude": 51.0133, "longitude": 2.1331, "capacite_mw": 5460,
        "region": "Hauts-de-France", "mise_service": 1980
    },
    "Centrale Nucléaire du Tricastin": {
        "type": "Nucléaire", "pays": "France", "ville": "Pierrelatte",
        "latitude": 44.3286, "longitude": 4.7319, "capacite_mw": 3660,
        "region": "Auvergne-Rhône-Alpes", "mise_service": 1980
    },
    "Zaporizhzhia Nuclear Power Plant": {
        "type": "Nucléaire", "pays": "Ukraine", "ville": "Enerhodar",
        "latitude": 47.5108, "longitude": 34.5858, "capacite_mw": 6000,
        "region": "Zaporizhzhia", "mise_service": 1984
    },
    
    # Asie
    "Kashiwazaki-Kariwa": {
        "type": "Nucléaire", "pays": "Japon", "ville": "Kashiwazaki",
        "latitude": 37.4281, "longitude": 138.5958, "capacite_mw": 8212,
        "region": "Niigata", "mise_service": 1985
    },
    "Kori Nuclear Power Plant": {
        "type": "Nucléaire", "pays": "Corée du Sud", "ville": "Busan",
        "latitude": 35.3167, "longitude": 129.2917, "capacite_mw": 5881,
        "region": "Busan", "mise_service": 1978
    },
    
    # Amériques
    "Palo Verde Nuclear": {
        "type": "Nucléaire", "pays": "USA", "ville": "Tonopah",
        "latitude": 33.3917, "longitude": -112.8642, "capacite_mw": 3937,
        "region": "Arizona", "mise_service": 1986
    },
    "Bruce Nuclear Generating Station": {
        "type": "Nucléaire", "pays": "Canada", "ville": "Tiverton",
        "latitude": 44.3333, "longitude": -81.6000, "capacite_mw": 6384,
        "region": "Ontario", "mise_service": 1977
    },
    
    # ============ THERMIQUE ============
    
    # Afrique
    "Centrale Thermique Jorf Lasfar": {
        "type": "Thermique", "pays": "Maroc", "ville": "El Jadida",
        "latitude": 33.1333, "longitude": -8.6333, "capacite_mw": 1356,
        "region": "Casablanca-Settat", "mise_service": 1984
    },
    "Medupi Power Station": {
        "type": "Thermique", "pays": "Afrique du Sud", "ville": "Lephalale",
        "latitude": -23.8500, "longitude": 27.6500, "capacite_mw": 4764,
        "region": "Limpopo", "mise_service": 2015
    },
    
    # Asie
    "Taichung Power Plant": {
        "type": "Thermique", "pays": "Taïwan", "ville": "Longjing",
        "latitude": 24.2122, "longitude": 120.4819, "capacite_mw": 5500,
        "region": "Taichung", "mise_service": 1992
    },
    "Vindhyachal Thermal Power Station": {
        "type": "Thermique", "pays": "Inde", "ville": "Vindhyanagar",
        "latitude": 24.0833, "longitude": 82.6167, "capacite_mw": 4760,
        "region": "Madhya Pradesh", "mise_service": 1987
    },
    
    # Amériques
    "W.A. Parish Generating Station": {
        "type": "Thermique", "pays": "USA", "ville": "Thompsons",
        "latitude": 29.4833, "longitude": -95.6333, "capacite_mw": 3653,
        "region": "Texas", "mise_service": 1977
    },
    
    # Europe
    "Bełchatów Power Station": {
        "type": "Thermique", "pays": "Pologne", "ville": "Bełchatów",
        "latitude": 51.2667, "longitude": 19.3333, "capacite_mw": 5298,
        "region": "Łódź", "mise_service": 1981
    },
}

# ====================
# CATÉGORIES ÉNERGIE
# ====================

ENERGY_CATEGORIES = {
    "type_energie": ["Solaire", "Éolien", "Hydraulique", "Nucléaire", "Thermique", "Biomasse", "Géothermique"],
    "statut_installation": ["Opérationnelle", "Maintenance", "Construction", "Planification", "Démantèlement"],
    "type_client": ["Résidentiel", "Commercial", "Industriel", "Public", "Agricole"],
    "qualite_reseau": ["Excellent", "Bon", "Moyen", "Faible"],
    "type_equipement": ["Panneau Solaire", "Éolienne", "Turbine", "Transformateur", "Onduleur", "Batterie"],
    "classe_efficacite": ["A+++", "A++", "A+", "A", "B", "C", "D"],
    "type_compteur": ["Linky", "Intelligent", "Électromécanique", "Électronique"],
}

# ====================
# GÉNÉRATEURS DONNÉES ÉNERGIE
# ====================

def gen_energy_installations(n):
    """Génère des données d'installations énergétiques cohérentes"""
    installations_disponibles = list(ENERGY_DATABASE.keys())
    installations_choisies = np.random.choice(installations_disponibles, size=n, replace=True)
    
    data = []
    for installation in installations_choisies:
        info = ENERGY_DATABASE[installation]
        
        # Variation géographique mineure
        lat_var = np.random.uniform(-0.01, 0.01)
        lon_var = np.random.uniform(-0.01, 0.01)
        
        data.append({
            "installation": installation,
            "type_energie": info["type"],
            "pays": info["pays"],
            "ville": info["ville"],
            "region": info["region"],
            "latitude": round(info["latitude"] + lat_var, 6),
            "longitude": round(info["longitude"] + lon_var, 6),
            "capacite_mw": info["capacite_mw"],
            "annee_mise_service": info["mise_service"]
        })
    
    return data

def gen_production_energy(n, type_energie=None):
    """Génère des données de production énergétique réalistes"""
    data = []
    
    for i in range(n):
        if type_energie is None:
            type_e = np.random.choice(ENERGY_CATEGORIES["type_energie"])
        else:
            type_e = type_energie
        
        # Production basée sur le type d'énergie (MW)
        if type_e == "Solaire":
            production = np.random.uniform(50, 800)
            facteur_charge = np.random.uniform(0.15, 0.25)  # 15-25%
        elif type_e == "Éolien":
            production = np.random.uniform(100, 1200)
            facteur_charge = np.random.uniform(0.25, 0.40)  # 25-40%
        elif type_e == "Hydraulique":
            production = np.random.uniform(100, 2000)
            facteur_charge = np.random.uniform(0.40, 0.60)  # 40-60%
        elif type_e == "Nucléaire":
            production = np.random.uniform(900, 5500)
            facteur_charge = np.random.uniform(0.75, 0.90)  # 75-90%
        elif type_e == "Thermique":
            production = np.random.uniform(200, 1500)
            facteur_charge = np.random.uniform(0.50, 0.70)  # 50-70%
        else:
            production = np.random.uniform(50, 500)
            facteur_charge = np.random.uniform(0.30, 0.50)
        
        data.append({
            "type_energie": type_e,
            "production_mw": round(production, 2),
            "facteur_charge": round(facteur_charge, 3),
            "production_annuelle_gwh": round(production * facteur_charge * 8760 / 1000, 2)
        })
    
    return data

def gen_consumption_data(n):
    """Génère des données de consommation énergétique"""
    data = []
    
    for i in range(n):
        type_client = np.random.choice(ENERGY_CATEGORIES["type_client"])
        
        # Consommation basée sur le type de client (kWh/mois)
        if type_client == "Résidentiel":
            conso = np.random.normal(250, 80)
        elif type_client == "Commercial":
            conso = np.random.normal(2500, 800)
        elif type_client == "Industriel":
            conso = np.random.normal(50000, 15000)
        elif type_client == "Public":
            conso = np.random.normal(5000, 1500)
        else:  # Agricole
            conso = np.random.normal(1500, 500)
        
        conso = max(50, conso)  # Minimum 50 kWh
        
        data.append({
            "type_client": type_client,
            "consommation_kwh": round(conso, 2),
            "cout_total_dh": round(conso * np.random.uniform(1.2, 1.8), 2),
            "pic_puissance_kw": round(conso / 730 * np.random.uniform(1.5, 2.5), 2)
        })
    
    return data

def gen_tarif_energie():
    """Génère des tarifs énergétiques réalistes (DH/kWh)"""
    return {
        "Résidentiel": round(np.random.uniform(1.15, 1.35), 3),
        "Commercial": round(np.random.uniform(1.25, 1.50), 3),
        "Industriel": round(np.random.uniform(0.95, 1.20), 3),
        "Public": round(np.random.uniform(1.10, 1.30), 3),
        "Agricole": round(np.random.uniform(0.85, 1.10), 3)
    }

def gen_emissions_co2(production_gwh, type_energie):
    """Calcule les émissions CO2 (tonnes) basées sur la production"""
    # Facteurs d'émission en kg CO2/kWh
    facteurs = {
        "Solaire": 0.05,
        "Éolien": 0.02,
        "Hydraulique": 0.01,
        "Nucléaire": 0.006,
        "Thermique": 0.85,
        "Biomasse": 0.10,
        "Géothermique": 0.05
    }
    
    facteur = facteurs.get(type_energie, 0.5)
    emissions = production_gwh * 1000000 * facteur / 1000  # tonnes CO2
    
    return round(emissions, 2)

# ====================
# CONSTRUCTION DU DATASET
# ====================

def build_energy_dataset(schema, n=500):
    """Construit un dataset énergie avec données cohérentes"""
    
    # Normaliser schéma
    cols = []
    if isinstance(schema, list) and all(isinstance(x, str) for x in schema):
        cols = [{"name": name, "type": None, "params": {}} for name in schema]
    else:
        cols = schema
    
    # Détecter si besoin de données d'installations
    needs_installation = any(
        col["name"].lower() in ["installation", "type_energie", "ville", "pays", "capacite_mw"]
        for col in cols
    )
    
    if needs_installation:
        installations = gen_energy_installations(n)
    
    # Détecter si besoin de données de production
    needs_production = any(
        col["name"].lower() in ["production_mw", "facteur_charge", "production_annuelle_gwh"]
        for col in cols
    )
    
    if needs_production:
        production = gen_production_energy(n)
    
    # Détecter si besoin de données de consommation
    needs_consumption = any(
        col["name"].lower() in ["consommation_kwh", "type_client", "cout_total_dh"]
        for col in cols
    )
    
    if needs_consumption:
        consumption = gen_consumption_data(n)
    
    # Construire le dataframe
    data = {}
    
    for col in cols:
        name = col["name"]
        name_lower = name.lower()
        
        # Données d'installations
        if needs_installation:
            if "installation" in name_lower:
                data[name] = [inst["installation"] for inst in installations]
            elif "type_energie" in name_lower or name_lower == "type":
                data[name] = [inst["type_energie"] for inst in installations]
            elif "ville" in name_lower:
                data[name] = [inst["ville"] for inst in installations]
            elif "pays" in name_lower:
                data[name] = [inst["pays"] for inst in installations]
            elif "region" in name_lower:
                data[name] = [inst["region"] for inst in installations]
            elif "latitude" in name_lower:
                data[name] = [inst["latitude"] for inst in installations]
            elif "longitude" in name_lower:
                data[name] = [inst["longitude"] for inst in installations]
            elif "capacite" in name_lower:
                data[name] = [inst["capacite_mw"] for inst in installations]
            elif "annee" in name_lower or "mise_service" in name_lower:
                data[name] = [inst["annee_mise_service"] for inst in installations]
        
        # Données de production
        if needs_production and name not in data:
            if "production_mw" in name_lower:
                data[name] = [prod["production_mw"] for prod in production]
            elif "facteur_charge" in name_lower:
                data[name] = [prod["facteur_charge"] for prod in production]
            elif "production_annuelle" in name_lower or "gwh" in name_lower:
                data[name] = [prod["production_annuelle_gwh"] for prod in production]
        
        # Données de consommation
        if needs_consumption and name not in data:
            if "type_client" in name_lower:
                data[name] = [cons["type_client"] for cons in consumption]
            elif "consommation" in name_lower:
                data[name] = [cons["consommation_kwh"] for cons in consumption]
            elif "cout" in name_lower or "prix" in name_lower:
                data[name] = [cons["cout_total_dh"] for cons in consumption]
            elif "pic" in name_lower or "puissance" in name_lower:
                data[name] = [cons["pic_puissance_kw"] for cons in consumption]
        
        # Émissions CO2
        if "emission" in name_lower or "co2" in name_lower:
            if needs_production:
                emissions = [
                    gen_emissions_co2(prod["production_annuelle_gwh"], prod["type_energie"])
                    for prod in production
                ]
                data[name] = emissions
            else:
                data[name] = np.random.uniform(100, 10000, n)
        
        # Statut
        if "statut" in name_lower and name not in data:
            data[name] = np.random.choice(ENERGY_CATEGORIES["statut_installation"], n)
        
        # Qualité réseau
        if "qualite" in name_lower and name not in data:
            data[name] = np.random.choice(ENERGY_CATEGORIES["qualite_reseau"], n)
        
        # ID
        if name_lower in ["id", "id_installation", "id_client"]:
            data[name] = [f"{name}_{str(i+1).zfill(6)}" for i in range(n)]
        
        # Date
        if "date" in name_lower and name not in data:
            base = datetime(2024, 1, 1)
            dates = [base + timedelta(days=int(i * 365 / n)) for i in range(n)]
            data[name] = [d.strftime("%Y-%m-%d") for d in dates]
        
        # Si colonne non traitée
        if name not in data:
            data[name] = np.random.uniform(0, 100, n)
    
    return pd.DataFrame(data)

# ====================
# CLI
# ====================

def main():
    parser = argparse.ArgumentParser(
        description="⚡ Générateur de Données SECTEUR ÉNERGIE",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
EXEMPLES :

⚡ Dataset installations énergétiques :
  python energy_data_generator.py --name installations \\
    --schema '["id","installation","type_energie","ville","pays","capacite_mw","production_annuelle_gwh"]' --n 300

📊 Dataset consommation clients :
  python energy_data_generator.py --name consommation \\
    --schema '["id_client","type_client","consommation_kwh","cout_total_dh","date"]' --n 500

🌍 Dataset production par région :
  python energy_data_generator.py --name production \\
    --schema '["region","type_energie","production_mw","facteur_charge","emissions_co2"]' --n 200

TYPES DE DONNÉES GÉNÉRÉES :
  • Installations : Solaire, Éolien, Hydraulique, Nucléaire, Thermique
  • Production : MW, GWh, Facteur de charge
  • Consommation : kWh, Coûts, Pics de puissance
  • Émissions : CO2 basées sur type d'énergie
  • Géolocalisation : Coordonnées GPS exactes des installations
        """
    )
    
    parser.add_argument("--name", required=True, help="Nom du dataset")
    parser.add_argument("--schema", required=True, help="Colonnes JSON")
    parser.add_argument("--n", type=int, default=500, help="Nombre de lignes")
    parser.add_argument("--out", default=None, help="Fichier de sortie")
    parser.add_argument("--preview", type=int, default=10, help="Lignes à afficher")
    
    args = parser.parse_args()
    
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
    print(f"⚡ GÉNÉRATION DATASET ÉNERGIE '{args.name}'")
    print("="*80 + "\n")
    
    try:
        df = build_energy_dataset(schema, n=args.n)
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # Sauvegarder
    out = args.out or f"{args.name}_energy.csv"
    df.to_csv(out, index=False)
    
    # Résultats
    print("="*80)
    print(f"✅ DATASET ÉNERGIE GÉNÉRÉ")
    print("="*80)
    print(f"📁 Fichier : {out}")
    print(f"📊 Lignes  : {len(df)}")
    print(f"📊 Colonnes: {len(df.columns)}\n")
    
    print("👁️  APERÇU :")
    print(df.head(args.preview).to_string(index=False))
    
    # Statistiques
    if "type_energie" in df.columns:
        print(f"\n{'='*80}")
        print("📈 RÉPARTITION PAR TYPE D'ÉNERGIE")
        print("="*80)
        print(df["type_energie"].value_counts().to_string())
    
    if "production_annuelle_gwh" in df.columns:
        print(f"\n📊 Production totale : {df['production_annuelle_gwh'].sum():.2f} GWh")
    
    if "emissions_co2" in df.columns:
        print(f"🌍 Émissions CO2 totales : {df['emissions_co2'].sum():.2f} tonnes")
    
    print(f"\n✨ Génération terminée!\n")

if __name__ == "__main__":
    main()