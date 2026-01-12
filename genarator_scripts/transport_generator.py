"""
GÉNÉRATEUR DE DONNÉES COHÉRENTES POUR TRANSPORT
Génère des données de véhicules avec cohérence totale (type, marque, modèle, prix, etc.)
"""

import json
import argparse
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

np.random.seed(42)

# ====================
# DONNÉES COHÉRENTES PAR TYPE DE VÉHICULE
# ====================
TRANSPORT_DATA = {
    "Voiture": {
        "marques": {
            "Toyota": ["Corolla", "Camry", "RAV4", "Yaris", "Land Cruiser"],
            "Mercedes": ["Classe A", "Classe C", "Classe E", "GLE", "GLA"],
            "BMW": ["Série 3", "Série 5", "X3", "X5", "i4"],
            "Volkswagen": ["Golf", "Polo", "Tiguan", "Passat", "T-Roc"],
            "Peugeot": ["208", "308", "3008", "5008", "2008"],
            "Renault": ["Clio", "Megane", "Captur", "Kadjar", "Talisman"],
            "Dacia": ["Sandero", "Duster", "Logan", "Spring"],
            "Audi": ["A3", "A4", "Q3", "Q5", "e-tron"]
        },
        "carburant": ["Essence", "Diesel", "Hybride", "Électrique"],
        "transmission": ["Manuelle", "Automatique"],
        "vitesse_max_range": (120, 250),
        "chevaux_range": (70, 350),
        "prix_range": (15000, 80000),
        "consommation_range": (4.0, 9.0),  # L/100km
        "capacite_reservoir": (40, 70),  # Litres
        "nb_places": [2, 4, 5, 7],
        "annee_range": (2015, 2024)
    },
    "Moto": {
        "marques": {
            "Honda": ["CBR 600", "Africa Twin", "CB 500", "PCX"],
            "Yamaha": ["MT-07", "R1", "TMAX", "YZF-R6"],
            "Kawasaki": ["Ninja 650", "Z900", "Versys"],
            "Suzuki": ["GSX-R", "V-Strom", "Burgman"],
            "Ducati": ["Panigale", "Monster", "Multistrada"],
            "BMW": ["F 850 GS", "S 1000 RR", "R 1250 GS"]
        },
        "carburant": ["Essence"],
        "transmission": ["Manuelle", "Automatique"],
        "vitesse_max_range": (150, 300),
        "chevaux_range": (35, 200),
        "prix_range": (5000, 30000),
        "consommation_range": (3.5, 6.5),
        "capacite_reservoir": (10, 22),
        "nb_places": [1, 2],
        "annee_range": (2015, 2024)
    },
    "Camion": {
        "marques": {
            "Mercedes": ["Actros", "Atego", "Axor"],
            "Volvo": ["FH", "FM", "FMX"],
            "Scania": ["R Series", "S Series", "P Series"],
            "MAN": ["TGX", "TGS", "TGL"],
            "Iveco": ["Stralis", "Eurocargo", "Daily"],
            "Renault": ["T High", "C", "K"]
        },
        "carburant": ["Diesel", "Électrique"],
        "transmission": ["Automatique"],
        "vitesse_max_range": (90, 130),
        "chevaux_range": (250, 600),
        "prix_range": (60000, 150000),
        "consommation_range": (25.0, 40.0),
        "capacite_reservoir": (300, 600),
        "nb_places": [2, 3],
        "annee_range": (2015, 2024),
        "charge_utile_range": (3500, 40000)  # kg
    },
    "Bus": {
        "marques": {
            "Mercedes": ["Citaro", "Sprinter", "Tourismo"],
            "Iveco": ["Crossway", "Urbanway", "Evadys"],
            "Volvo": ["7900", "9700", "9900"],
            "MAN": ["Lion's City", "Lion's Coach"],
            "Scania": ["Citywide", "Touring", "Interlink"]
        },
        "carburant": ["Diesel", "Électrique", "Hybride"],
        "transmission": ["Automatique"],
        "vitesse_max_range": (90, 120),
        "chevaux_range": (250, 450),
        "prix_range": (150000, 400000),
        "consommation_range": (25.0, 35.0),
        "capacite_reservoir": (200, 400),
        "nb_places": [30, 45, 55, 70],
        "annee_range": (2015, 2024)
    },
    "Avion": {
        "marques": {
            "Boeing": ["737", "747", "777", "787 Dreamliner"],
            "Airbus": ["A320", "A330", "A350", "A380"],
            "Embraer": ["E175", "E190", "E195"],
            "Bombardier": ["CRJ900", "CRJ1000"]
        },
        "carburant": ["Kérosène"],
        "transmission": ["Automatique"],
        "vitesse_max_range": (800, 950),  # km/h
        "chevaux_range": (20000, 100000),
        "prix_range": (50000000, 400000000),
        "consommation_range": (2500, 12000),  # L/h
        "capacite_reservoir": (100000, 250000),
        "nb_places": [150, 200, 300, 400, 550],
        "annee_range": (2010, 2024)
    },
    "Train": {
        "marques": {
            "Alstom": ["TGV", "AGV", "Coradia"],
            "Siemens": ["Velaro", "Desiro", "Vectron"],
            "Bombardier": ["Talent", "Zefiro"],
            "CAF": ["Civity", "Urbos"]
        },
        "carburant": ["Électrique", "Diesel-Électrique"],
        "transmission": ["Électrique"],
        "vitesse_max_range": (160, 320),
        "chevaux_range": (5000, 12000),
        "prix_range": (20000000, 50000000),
        "consommation_range": (0, 0),  # Électrique
        "capacite_reservoir": (0, 0),
        "nb_places": [200, 300, 400, 500, 600],
        "annee_range": (2010, 2024)
    }
}

# ====================
# CATÉGORIES SUPPLÉMENTAIRES
# ====================
TRANSPORT_CATEGORIES = {
    "couleur": ["Blanc", "Noir", "Gris", "Bleu", "Rouge", "Argent", "Vert", "Jaune"],
    "etat": ["Neuf", "Excellent", "Bon", "Moyen", "À réparer"],
    "statut": ["Disponible", "En maintenance", "En location", "Hors service"],
    "classe_avion": ["Économique", "Affaires", "Première"],
    "type_train": ["Grande vitesse", "Régional", "Intercités", "RER"],
    "ville": ["Paris", "Casablanca", "Lyon", "Marseille", "Rabat", "Marrakech", "Fès", "Tanger", "Toulouse", "Bordeaux"],
    "pays": ["France", "Maroc", "Allemagne", "Espagne", "Italie", "UK", "USA"]
}

# ====================
# GÉNÉRATEURS COHÉRENTS POUR TRANSPORT
# ====================
def gen_transport_data(n):
    """Génère des données de transport COHÉRENTES"""
    transports = []
    
    for _ in range(n):
        # Choisir type de véhicule
        type_vehicule = np.random.choice(list(TRANSPORT_DATA.keys()))
        data_type = TRANSPORT_DATA[type_vehicule]
        
        # Choisir marque
        marque = np.random.choice(list(data_type["marques"].keys()))
        
        # Choisir modèle cohérent avec la marque
        modele = np.random.choice(data_type["marques"][marque])
        
        # Année de fabrication
        annee_min, annee_max = data_type["annee_range"]
        annee = np.random.randint(annee_min, annee_max + 1)
        
        # Carburant
        carburant = np.random.choice(data_type["carburant"])
        
        # Transmission
        transmission = np.random.choice(data_type["transmission"])
        
        # Vitesse max
        vmin, vmax = data_type["vitesse_max_range"]
        vitesse_max = np.random.randint(vmin, vmax + 1)
        
        # Chevaux
        cmin, cmax = data_type["chevaux_range"]
        chevaux = np.random.randint(cmin, cmax + 1)
        
        # Prix
        pmin, pmax = data_type["prix_range"]
        # Prix diminue avec l'âge
        age = 2024 - annee
        depreciation = 0.9 ** age  # 10% par an
        prix = int(np.random.uniform(pmin, pmax) * depreciation)
        
        # Consommation
        cons_min, cons_max = data_type["consommation_range"]
        consommation = round(np.random.uniform(cons_min, cons_max), 1)
        
        # Capacité réservoir
        res_min, res_max = data_type["capacite_reservoir"]
        capacite_reservoir = np.random.randint(res_min, res_max + 1) if res_max > 0 else 0
        
        # Nombre de places
        nb_places = np.random.choice(data_type["nb_places"])
        
        # Kilométrage cohérent avec l'année
        km_par_an = np.random.randint(10000, 25000)
        kilometrage = age * km_par_an
        
        transport_dict = {
            "type_vehicule": type_vehicule,
            "marque_voiture": marque,
            "modele": modele,
            "annee_fabrication": annee,
            "carburant": carburant,
            "transmission": transmission,
            "vitesse_max": vitesse_max,
            "chevaux": chevaux,
            "prix": prix,
            "consommation": consommation,
            "capacite_reservoir": capacite_reservoir,
            "nb_places": nb_places,
            "kilometrage": kilometrage
        }
        
        # Ajout charge utile pour camions
        if type_vehicule == "Camion":
            charge_min, charge_max = data_type["charge_utile_range"]
            transport_dict["charge_utile"] = np.random.randint(charge_min, charge_max + 1)
        
        transports.append(transport_dict)
    
    return transports

def gen_immatriculation(n, pays="MA"):
    """Génère des plaques d'immatriculation"""
    immatriculations = []
    
    for _ in range(n):
        if pays == "MA":
            # Format marocain: 12345-أ-67
            num1 = np.random.randint(10000, 99999)
            lettre = np.random.choice(['A', 'B', 'D', 'W', 'H'])
            num2 = np.random.randint(10, 99)
            immat = f"{num1}-{lettre}-{num2}"
        elif pays == "FR":
            # Format français: AB-123-CD
            l1 = ''.join(np.random.choice(list('ABCDEFGHJKLMNPRSTUVWXYZ'), 2))
            num = np.random.randint(100, 999)
            l2 = ''.join(np.random.choice(list('ABCDEFGHJKLMNPRSTUVWXYZ'), 2))
            immat = f"{l1}-{num}-{l2}"
        else:
            # Format générique
            immat = f"{''.join(np.random.choice(list('ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 3))}-{np.random.randint(1000, 9999)}"
        
        immatriculations.append(immat)
    
    return immatriculations

def gen_date_achat(annees, current_date=None):
    """Génère des dates d'achat COHÉRENTES avec l'année de fabrication"""
    if current_date is None:
        current_date = datetime.now()
    
    dates_achat = []
    for annee in annees:
        # Achat entre l'année de fabrication et maintenant
        date_fabrication = datetime(annee, 1, 1)
        jours_depuis_fabrication = (current_date - date_fabrication).days
        
        if jours_depuis_fabrication > 0:
            jours_achat = np.random.randint(0, jours_depuis_fabrication + 1)
            date_achat = date_fabrication + timedelta(days=jours_achat)
        else:
            date_achat = date_fabrication
        
        dates_achat.append(date_achat.strftime("%Y-%m-%d"))
    
    return dates_achat

def gen_autonomie_coherente(carburants, capacites, consommations):
    """Génère l'autonomie cohérente avec le réservoir et la consommation"""
    autonomies = []
    for i, carburant in enumerate(carburants):
        if carburant == "Électrique":
            # Autonomie en km pour véhicules électriques
            autonomie = np.random.randint(200, 500)
        elif consommations[i] > 0:
            # Autonomie = capacité / consommation * 100
            autonomie = int((capacites[i] / consommations[i]) * 100)
        else:
            autonomie = 0
        
        autonomies.append(autonomie)
    
    return autonomies

def gen_id_transport(n, prefix="VEH"):
    """Génère des identifiants de véhicules"""
    return [f"{prefix}_{str(i+1).zfill(6)}" for i in range(n)]

# ====================
# DÉTECTION INTELLIGENTE POUR TRANSPORT
# ====================
def guess_transport_type(name):
    """Détecte automatiquement le type de colonne pour transport"""
    name_lower = name.lower()
    
    if name_lower in ["type_vehicule", "type", "moyen_transport", "categorie"]:
        return ("transport_type", {})
    
    if name_lower in ["marque", "marque_voiture", "fabricant"]:
        return ("transport_marque", {})
    
    if name_lower in ["modele", "modèle", "version"]:
        return ("transport_modele", {})
    
    if name_lower in ["annee", "année", "annee_fabrication"]:
        return ("transport_annee", {})
    
    if name_lower in ["carburant", "energie", "motorisation"]:
        return ("transport_carburant", {})
    
    if name_lower in ["transmission", "boite_vitesse"]:
        return ("transport_transmission", {})
    
    if name_lower in ["vitesse_max", "vitesse_maximale"]:
        return ("transport_vitesse", {})
    
    if name_lower in ["chevaux", "puissance", "cv"]:
        return ("transport_chevaux", {})
    
    if name_lower in ["prix", "prix_achat", "valeur"]:
        return ("transport_prix", {})
    
    if name_lower in ["consommation", "conso"]:
        return ("transport_consommation", {})
    
    if name_lower in ["capacite_reservoir", "reservoir", "capacité"]:
        return ("transport_reservoir", {})
    
    if name_lower in ["nb_places", "places", "capacite_passagers"]:
        return ("transport_places", {})
    
    if name_lower in ["kilometrage", "km", "kilométrage"]:
        return ("transport_kilometrage", {})
    
    if name_lower in ["charge_utile", "charge"]:
        return ("transport_charge", {})
    
    if name_lower in ["autonomie"]:
        return ("transport_autonomie", {})
    
    if name_lower in ["immatriculation", "plaque", "numero_serie"]:
        return ("transport_immat", {})
    
    if "date" in name_lower and ("achat" in name_lower or "acquisition" in name_lower):
        return ("transport_date_achat", {})
    
    if "id" in name_lower or "numero" in name_lower:
        return ("transport_id", {})
    
    # Catégories prédéfinies
    for key in TRANSPORT_CATEGORIES:
        if key in name_lower or name_lower in key:
            return ("categorical", {"categories": TRANSPORT_CATEGORIES[key]})
    
    # Fallback
    return ("categorical", {"categories": ["Option A", "Option B", "Option C"]})

# ====================
# CONSTRUCTION DU DATASET TRANSPORT
# ====================
def build_transport_dataset(schema, n=500):
    """Construit un dataset de transport avec données COHÉRENTES"""
    
    cols = []
    if isinstance(schema, list) and all(isinstance(x, str) for x in schema):
        for name in schema:
            t, params = guess_transport_type(name)
            cols.append({"name": name, "type": t, "params": params})
    else:
        for c in schema:
            name = c.get("name")
            if not name:
                raise ValueError("Chaque colonne doit avoir un 'name'")
            t = c.get("type")
            params = c.get("params", {})
            if not t:
                guessed_t, guessed_params = guess_transport_type(name)
                guessed_params.update(params)
                t = guessed_t
                params = guessed_params
            cols.append({"name": name, "type": t, "params": params})
    
    transports = gen_transport_data(n)
    
    types = [t["type_vehicule"] for t in transports]
    marques = [t["marque_voiture"] for t in transports]
    modeles = [t["modele"] for t in transports]
    annees = [t["annee_fabrication"] for t in transports]
    carburants = [t["carburant"] for t in transports]
    transmissions = [t["transmission"] for t in transports]
    vitesses = [t["vitesse_max"] for t in transports]
    chevaux = [t["chevaux"] for t in transports]
    prix = [t["prix"] for t in transports]
    consommations = [t["consommation"] for t in transports]
    reservoirs = [t["capacite_reservoir"] for t in transports]
    places = [t["nb_places"] for t in transports]
    kilometrages = [t["kilometrage"] for t in transports]
    
    # Données dérivées
    dates_achat = gen_date_achat(annees)
    immatriculations = gen_immatriculation(n, pays="MA")
    autonomies = gen_autonomie_coherente(carburants, reservoirs, consommations)
    ids = gen_id_transport(n)
    
    data = {}
    
    for col in cols:
        name = col["name"]
        t = col["type"]
        p = col.get("params", {})
        
        if t == "transport_type":
            data[name] = types
        elif t == "transport_marque":
            data[name] = marques
        elif t == "transport_modele":
            data[name] = modeles
        elif t == "transport_annee":
            data[name] = annees
        elif t == "transport_carburant":
            data[name] = carburants
        elif t == "transport_transmission":
            data[name] = transmissions
        elif t == "transport_vitesse":
            data[name] = vitesses
        elif t == "transport_chevaux":
            data[name] = chevaux
        elif t == "transport_prix":
            data[name] = prix
        elif t == "transport_consommation":
            data[name] = consommations
        elif t == "transport_reservoir":
            data[name] = reservoirs
        elif t == "transport_places":
            data[name] = places
        elif t == "transport_kilometrage":
            data[name] = kilometrages
        elif t == "transport_charge":
            # Générer charge utile seulement pour camions
            charges = []
            for i, type_v in enumerate(types):
                if type_v == "Camion":
                    charges.append(transports[i].get("charge_utile", 10000))
                else:
                    charges.append(0)
            data[name] = charges
        elif t == "transport_autonomie":
            data[name] = autonomies
        elif t == "transport_immat":
            data[name] = immatriculations
        elif t == "transport_date_achat":
            data[name] = dates_achat
        elif t == "transport_id":
            data[name] = ids
        elif t == "categorical":
            cats = p.get("categories", ["Option A", "Option B", "Option C"])
            data[name] = np.random.choice(cats, size=n)
        elif t == "int":
            data[name] = np.random.randint(int(p.get("low", 0)), int(p.get("high", 100)) + 1, n)
        elif t == "numeric":
            data[name] = np.random.uniform(p.get("low", 0), p.get("high", 100), n)
        elif t == "boolean":
            data[name] = np.random.rand(n) < float(p.get("p", 0.5))
        else:
            data[name] = np.random.choice(["Valeur 1", "Valeur 2", "Valeur 3"], n)
    
    return pd.DataFrame(data)

# ====================
# CLI
# ====================
def main():
    parser = argparse.ArgumentParser(
        description="🚗 Générateur COHÉRENT de datasets de transport",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
EXEMPLES POWERSHELL :

🚗 Dataset de véhicules simple :
  python transport_generator.py --name vehicles --cols id,type_vehicule,marque_voiture,modele,annee_fabrication,prix,kilometrage --n 2000

🚙 Dataset concession automobile :
  python transport_generator.py --name concession --cols id,type_vehicule,marque_voiture,modele,annee_fabrication,carburant,transmission,chevaux,prix,kilometrage,couleur,etat,statut --n 2000

✈️ Dataset transport complet :
  python transport_generator.py --name transport --cols id,type_vehicule,marque_voiture,modele,annee_fabrication,carburant,vitesse_max,chevaux,prix,consommation,nb_places,kilometrage,immatriculation,date_achat --n 2000

COLONNES DISPONIBLES :
  id, type_vehicule, marque_voiture, modele, annee_fabrication, carburant, transmission,
  vitesse_max, chevaux, prix, consommation, capacite_reservoir, nb_places, kilometrage,
  charge_utile, autonomie, immatriculation, date_achat, couleur, etat, statut, ville, pays
        """
    )
    
    parser.add_argument("--name", required=True, help="Nom du dataset")
    parser.add_argument("--schema", default=None, help="Colonnes JSON ou fichier.json")
    parser.add_argument("--cols", default=None, help="Colonnes séparées par virgules (RECOMMANDÉ)")
    parser.add_argument("--n", type=int, default=500, help="Nombre de lignes")
    parser.add_argument("--out", default=None, help="Fichier de sortie")
    parser.add_argument("--preview", type=int, default=10, help="Lignes à afficher")
    
    args = parser.parse_args()
    
    if not args.schema and not args.cols:
        print("❌ Erreur: Vous devez fournir --schema OU --cols")
        print("\n💡 Pour PowerShell, utilisez --cols :")
        print("   python transport_generator.py --name vehicles --cols id,type_vehicule,marque_voiture,modele,prix --n 2000")
        return
    
    try:
        if args.cols:
            schema = [col.strip() for col in args.cols.split(',')]
            print(f"✅ Colonnes détectées: {', '.join(schema)}\n")
        elif args.schema.endswith('.json'):
            with open(args.schema, 'r', encoding='utf-8') as f:
                schema = json.load(f)
        else:
            schema = json.loads(args.schema)
    except Exception as e:
        print(f"❌ Erreur schéma: {e}")
        return
    
    print(f"{'='*80}")
    print(f"🚗 GÉNÉRATION DU DATASET DE TRANSPORT '{args.name}'")
    print("="*80 + "\n")
    
    try:
        df = build_transport_dataset(schema, n=args.n)
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        return
    
    out = args.out or f"{args.name}_transport.csv"
    df.to_csv(out, index=False, encoding='utf-8-sig')
    
    print("="*80)
    print(f"✅ DATASET DE TRANSPORT GÉNÉRÉ")
    print("="*80)
    print(f"📁 Fichier : {out}")
    print(f"📊 Lignes  : {len(df)}")
    print(f"📊 Colonnes: {len(df.columns)}\n")
    
    print("👁️  APERÇU :")
    print(df.head(args.preview).to_string(index=False))
    
    print(f"\n{'='*80}")
    print("✅ VÉRIFICATIONS DE COHÉRENCE")
    print("="*80)
    
    if "type_vehicule" in df.columns and "marque_voiture" in df.columns and "modele" in df.columns:
        print("\n✓ Type, Marque et Modèle cohérents")
        sample = df.head(3)[["type_vehicule", "marque_voiture", "modele"]].to_string(index=False)
        print(sample)
    
    if "annee_fabrication" in df.columns and "prix" in df.columns:
        print("\n✓ Année et Prix cohérents (dépréciation)")
        sample = df.head(3)[["marque_voiture", "annee_fabrication", "prix", "kilometrage"]].to_string(index=False)
        print(sample)
    
    if "carburant" in df.columns and "consommation" in df.columns:
        print("\n✓ Carburant et Consommation cohérents")
        sample = df.head(3)[["type_vehicule", "carburant", "consommation"]].to_string(index=False)
        print(sample)
    
    print(f"\n✨ Génération terminée! Fichier sauvegardé: {out}\n")

if __name__ == "__main__":
    main()