"""
GÉNÉRATEUR DE DONNÉES SECTEUR ALIMENTATION & AGRICULTURE
Génère des données cohérentes pour produits agricoles, exploitations, marchés
"""

import json
import argparse
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

np.random.seed(42)

# ====================
# BASE DE DONNÉES AGRICULTURE & ALIMENTATION
# ====================

AGRICULTURE_DATABASE = {
    # ============ EXPLOITATIONS AGRICOLES ============
    "Ferme Al Baraka": {
        "type": "Exploitation", "pays": "Maroc", "region": "Souss-Massa",
        "superficie_ha": 450, "bio": True, "specialite": "Agrumes"
    },
    "Domaine Saada": {
        "type": "Exploitation", "pays": "Maroc", "region": "Meknès-Fès",
        "superficie_ha": 320, "bio": False, "specialite": "Céréales"
    },
    "Green Valley Farm": {
        "type": "Exploitation", "pays": "USA", "region": "Californie",
        "superficie_ha": 2500, "bio": True, "specialite": "Légumes"
    },
    "Domaine Provence Bio": {
        "type": "Exploitation", "pays": "France", "region": "Provence",
        "superficie_ha": 180, "bio": True, "specialite": "Vignobles"
    },
    "Hacienda El Sol": {
        "type": "Exploitation", "pays": "Espagne", "region": "Andalousie",
        "superficie_ha": 600, "bio": False, "specialite": "Olives"
    },
    "Fattoria Toscana": {
        "type": "Exploitation", "pays": "Italie", "region": "Toscane",
        "superficie_ha": 280, "bio": True, "specialite": "Vignobles"
    },
    "Fazenda Brasil": {
        "type": "Exploitation", "pays": "Brésil", "region": "São Paulo",
        "superficie_ha": 8000, "bio": False, "specialite": "Café"
    },
    "Dairy Meadows": {
        "type": "Exploitation", "pays": "Nouvelle-Zélande", "region": "Canterbury",
        "superficie_ha": 450, "bio": True, "specialite": "Produits Laitiers"
    },
    
    # ============ COOPÉRATIVES ============
    "Coopérative Oasis": {
        "type": "Coopérative", "pays": "Maroc", "region": "Marrakech-Safi",
        "superficie_ha": 1200, "bio": True, "specialite": "Dattes"
    },
    "Union Agricole Méditerranée": {
        "type": "Coopérative", "pays": "Tunisie", "region": "Sfax",
        "superficie_ha": 800, "bio": False, "specialite": "Olives"
    },
    "Cooperative Grains Alliance": {
        "type": "Coopérative", "pays": "USA", "region": "Kansas",
        "superficie_ha": 5000, "bio": False, "specialite": "Céréales"
    },
    
    # ============ MARCHÉS ============
    "Marché Wholesale Agadir": {
        "type": "Marché", "pays": "Maroc", "region": "Souss-Massa",
        "superficie_ha": 15, "bio": False, "specialite": "Fruits & Légumes"
    },
    "Rungis International": {
        "type": "Marché", "pays": "France", "region": "Île-de-France",
        "superficie_ha": 234, "bio": False, "specialite": "Fruits & Légumes"
    },
    "Mercabarna": {
        "type": "Marché", "pays": "Espagne", "region": "Catalogne",
        "superficie_ha": 90, "bio": False, "specialite": "Fruits & Légumes"
    },
}

PRODUITS_AGRICOLES = {
    "Agrumes": ["Oranges", "Mandarines", "Citrons", "Pamplemousses"],
    "Céréales": ["Blé", "Orge", "Maïs", "Riz"],
    "Légumes": ["Tomates", "Pommes de terre", "Oignons", "Carottes", "Courgettes"],
    "Vignobles": ["Raisins de Table", "Raisins de Cuve"],
    "Olives": ["Olives de Table", "Olives à Huile"],
    "Café": ["Arabica", "Robusta"],
    "Produits Laitiers": ["Lait", "Fromage", "Yaourt", "Beurre"],
    "Dattes": ["Medjool", "Deglet Nour"],
    "Fruits & Légumes": ["Tomates", "Pommes", "Bananes", "Salades"],
}

QUALITES = ["Premium", "Standard", "Bio Certifié", "Commerce Équitable", "Label Rouge"]
CONDITIONNEMENTS = ["Vrac", "Cagettes 5kg", "Cartons 10kg", "Palettes", "Sacs 25kg", "Filets 2kg"]

def gen_agri_data(n):
    """Génère des données cohérentes pour agriculture & alimentation"""
    exploitations = list(AGRICULTURE_DATABASE.keys())
    data = []
    
    for i in range(n):
        # Choisir une exploitation aléatoire
        expl = np.random.choice(exploitations)
        info = AGRICULTURE_DATABASE[expl]
        
        # Produit cohérent avec la spécialité
        specialite = info["specialite"]
        produits_possibles = PRODUITS_AGRICOLES.get(specialite, ["Produit Agricole"])
        produit = np.random.choice(produits_possibles)
        
        # Quantité selon le type d'exploitation
        if info["type"] == "Coopérative":
            quantite_tonnes = np.random.uniform(50, 500)
        elif info["superficie_ha"] > 1000:
            quantite_tonnes = np.random.uniform(100, 1000)
        else:
            quantite_tonnes = np.random.uniform(10, 200)
        
        # Prix selon le produit et si bio
        prix_base = {
            "Oranges": 0.8, "Mandarines": 1.2, "Citrons": 1.0, "Pamplemousses": 0.9,
            "Blé": 0.25, "Orge": 0.22, "Maïs": 0.28, "Riz": 0.45,
            "Tomates": 1.5, "Pommes de terre": 0.4, "Oignons": 0.6, "Carottes": 0.7,
            "Raisins de Table": 2.5, "Raisins de Cuve": 1.2,
            "Olives de Table": 3.5, "Olives à Huile": 2.0,
            "Arabica": 4.5, "Robusta": 3.0,
            "Lait": 0.4, "Fromage": 8.0, "Yaourt": 2.5, "Beurre": 6.0,
            "Medjool": 12.0, "Deglet Nour": 6.0,
            "Pommes": 1.2, "Bananes": 1.0, "Salades": 2.0, "Courgettes": 1.3
        }
        
        prix_tonne = prix_base.get(produit, 1.5) * 1000  # Convertir en prix/tonne
        if info["bio"]:
            prix_tonne *= 1.4  # Prix bio +40%
        
        # Variation aléatoire du prix
        prix_tonne *= np.random.uniform(0.85, 1.15)
        
        # Qualité
        if info["bio"]:
            qualite = np.random.choice(["Bio Certifié", "Premium", "Commerce Équitable"], p=[0.6, 0.3, 0.1])
        else:
            qualite = np.random.choice(["Standard", "Premium"], p=[0.7, 0.3])
        
        conditionnement = np.random.choice(CONDITIONNEMENTS)
        
        data.append({
            "exploitation": expl,
            "type_exploitation": info["type"],
            "pays": info["pays"],
            "region": info["region"],
            "produit": produit,
            "quantite_tonnes": round(quantite_tonnes, 2),
            "prix_tonne_eur": round(prix_tonne, 2),
            "qualite": qualite,
        })
    
    return data

def build_agri_dataset(schema, n=500):
    cols = []
    if isinstance(schema, list) and all(isinstance(x, str) for x in schema):
        cols = [{"name": name} for name in schema]
    else:
        cols = schema
    
    # Générer les données combinées
    combined_data = gen_agri_data(n)
    
    data = {}
    
    for col in cols:
        name = col["name"]
        nl = name.lower()
        
        # Mapping des 8 colonnes principales
        if "exploitation" in nl or "ferme" in nl:
            data[name] = [d["exploitation"] for d in combined_data]
        elif "type" in nl and ("exploitation" in nl or "ferme" in nl):
            data[name] = [d["type_exploitation"] for d in combined_data]
        elif "pays" in nl:
            data[name] = [d["pays"] for d in combined_data]
        elif "region" in nl:
            data[name] = [d["region"] for d in combined_data]
        elif "produit" in nl:
            data[name] = [d["produit"] for d in combined_data]
        elif "quantite" in nl or "volume" in nl:
            data[name] = [d["quantite_tonnes"] for d in combined_data]
        elif "prix" in nl or "tarif" in nl:
            data[name] = [d["prix_tonne_eur"] for d in combined_data]
        elif "qualite" in nl or "label" in nl:
            data[name] = [d["qualite"] for d in combined_data]
        # Colonnes supplémentaires optionnelles
        elif nl in ["id", "id_transaction", "id_lot"]:
            data[name] = [f"{name}_{str(i+1).zfill(8)}" for i in range(n)]
        elif "date" in nl:
            base = datetime(2024, 1, 1)
            dates = [base + timedelta(days=int(i * 365 / n)) for i in range(n)]
            data[name] = [d.strftime("%Y-%m-%d") for d in dates]
        else:
            print(f"⚠️  Colonne '{name}' non reconnue, valeurs par défaut")
            data[name] = ["N/A"] * n
    
    return pd.DataFrame(data)

def main():
    parser = argparse.ArgumentParser(description="🌾 Générateur Agriculture & Alimentation")
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
    print(f"🌾 GÉNÉRATION DATASET AGRICULTURE '{args.name}'")
    print("="*80 + "\n")
    
    df = build_agri_dataset(schema, n=args.n)
    
    out = args.out or f"{args.name}_agriculture.csv"
    df.to_csv(out, index=False)
    
    print("="*80)
    print(f"✅ DATASET AGRICULTURE GÉNÉRÉ")
    print("="*80)
    print(f"📁 Fichier : {out}")
    print(f"📊 Lignes  : {len(df)}")
    print(f"📊 Colonnes: {len(df.columns)}\n")
    
    print("👁️  APERÇU :")
    print(df.head(args.preview).to_string(index=False))
    
    # Statistiques par pays
    if "pays" in df.columns:
        print(f"\n{'='*80}")
        print("🌍 RÉPARTITION PAR PAYS")
        print("="*80)
        print(df["pays"].value_counts().to_string())
    
    # Statistiques par produit
    if "produit" in df.columns:
        print(f"\n{'='*80}")
        print("🥕 RÉPARTITION PAR PRODUIT")
        print("="*80)
        print(df["produit"].value_counts().head(10).to_string())
    
    # Statistiques par qualité
    if "qualite" in df.columns:
        print(f"\n{'='*80}")
        print("⭐ RÉPARTITION PAR QUALITÉ")
        print("="*80)
        print(df["qualite"].value_counts().to_string())
    
    print(f"\n✨ Génération terminée!\n")

if __name__ == "__main__":
    main()