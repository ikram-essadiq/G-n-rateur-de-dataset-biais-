"""
GÉNÉRATEUR DE DONNÉES SECTEUR COMMERCE & CONSOMMATION
Génère des données cohérentes pour produits, prix, promotions, tendances
"""

import json
import argparse
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

np.random.seed(42)

# ====================
# BASE DE DONNÉES COMMERCE & CONSOMMATION
# ====================

COMMERCE_DATABASE = {
    # ============ ÉLECTRONIQUE ============
    "Samsung Galaxy S24": {
        "categorie": "Électronique", "sous_categorie": "Smartphones",
        "marque": "Samsung", "prix_base": 899, "unite": "pièce",
        "tendance": "Forte", "saisonnalite": "Stable"
    },
    "iPhone 15 Pro": {
        "categorie": "Électronique", "sous_categorie": "Smartphones",
        "marque": "Apple", "prix_base": 1199, "unite": "pièce",
        "tendance": "Très Forte", "saisonnalite": "Stable"
    },
    "MacBook Air M3": {
        "categorie": "Électronique", "sous_categorie": "Ordinateurs",
        "marque": "Apple", "prix_base": 1299, "unite": "pièce",
        "tendance": "Forte", "saisonnalite": "Rentrée"
    },
    "PlayStation 5": {
        "categorie": "Électronique", "sous_categorie": "Consoles",
        "marque": "Sony", "prix_base": 499, "unite": "pièce",
        "tendance": "Forte", "saisonnalite": "Noël"
    },
    "AirPods Pro": {
        "categorie": "Électronique", "sous_categorie": "Audio",
        "marque": "Apple", "prix_base": 249, "unite": "pièce",
        "tendance": "Forte", "saisonnalite": "Stable"
    },
    
    # ============ MODE & VÊTEMENTS ============
    "Nike Air Max": {
        "categorie": "Mode", "sous_categorie": "Chaussures",
        "marque": "Nike", "prix_base": 140, "unite": "pièce",
        "tendance": "Forte", "saisonnalite": "Stable"
    },
    "Zara Veste Hiver": {
        "categorie": "Mode", "sous_categorie": "Vêtements",
        "marque": "Zara", "prix_base": 89, "unite": "pièce",
        "tendance": "Moyenne", "saisonnalite": "Hiver"
    },
    "H&M T-Shirt": {
        "categorie": "Mode", "sous_categorie": "Vêtements",
        "marque": "H&M", "prix_base": 19, "unite": "pièce",
        "tendance": "Moyenne", "saisonnalite": "Été"
    },
    "Adidas Survêtement": {
        "categorie": "Mode", "sous_categorie": "Sport",
        "marque": "Adidas", "prix_base": 75, "unite": "pièce",
        "tendance": "Moyenne", "saisonnalite": "Stable"
    },
    
    # ============ ALIMENTATION ============
    "Huile d'Olive Bio": {
        "categorie": "Alimentation", "sous_categorie": "Épicerie",
        "marque": "Terra Bio", "prix_base": 12, "unite": "litre",
        "tendance": "Forte", "saisonnalite": "Stable"
    },
    "Café Arabica": {
        "categorie": "Alimentation", "sous_categorie": "Boissons",
        "marque": "Lavazza", "prix_base": 8, "unite": "kg",
        "tendance": "Forte", "saisonnalite": "Stable"
    },
    "Chocolat Lindt": {
        "categorie": "Alimentation", "sous_categorie": "Confiserie",
        "marque": "Lindt", "prix_base": 15, "unite": "kg",
        "tendance": "Moyenne", "saisonnalite": "Fêtes"
    },
    "Yaourt Nature": {
        "categorie": "Alimentation", "sous_categorie": "Produits Laitiers",
        "marque": "Danone", "prix_base": 3, "unite": "pack 8",
        "tendance": "Moyenne", "saisonnalite": "Stable"
    },
    
    # ============ MAISON & DÉCORATION ============
    "Aspirateur Dyson V15": {
        "categorie": "Maison", "sous_categorie": "Électroménager",
        "marque": "Dyson", "prix_base": 649, "unite": "pièce",
        "tendance": "Forte", "saisonnalite": "Stable"
    },
    "Canapé IKEA Ektorp": {
        "categorie": "Maison", "sous_categorie": "Meubles",
        "marque": "IKEA", "prix_base": 499, "unite": "pièce",
        "tendance": "Moyenne", "saisonnalite": "Stable"
    },
    "Lampe Philips Hue": {
        "categorie": "Maison", "sous_categorie": "Éclairage",
        "marque": "Philips", "prix_base": 59, "unite": "pièce",
        "tendance": "Forte", "saisonnalite": "Stable"
    },
    
    # ============ BEAUTÉ & COSMÉTIQUES ============
    "Parfum Chanel N°5": {
        "categorie": "Beauté", "sous_categorie": "Parfums",
        "marque": "Chanel", "prix_base": 120, "unite": "100ml",
        "tendance": "Forte", "saisonnalite": "Fêtes"
    },
    "Crème L'Oréal": {
        "categorie": "Beauté", "sous_categorie": "Soins",
        "marque": "L'Oréal", "prix_base": 25, "unite": "50ml",
        "tendance": "Moyenne", "saisonnalite": "Stable"
    },
    
    # ============ SPORT & LOISIRS ============
    "Vélo Décathlon": {
        "categorie": "Sport", "sous_categorie": "Vélos",
        "marque": "Décathlon", "prix_base": 399, "unite": "pièce",
        "tendance": "Moyenne", "saisonnalite": "Printemps"
    },
    "Ballon Nike": {
        "categorie": "Sport", "sous_categorie": "Équipement",
        "marque": "Nike", "prix_base": 35, "unite": "pièce",
        "tendance": "Moyenne", "saisonnalite": "Stable"
    },
}

TYPES_PROMOTIONS = {
    "Aucune": 0,
    "Soldes -20%": 0.20,
    "Soldes -30%": 0.30,
    "Soldes -50%": 0.50,
    "Black Friday -40%": 0.40,
    "Cyber Monday -35%": 0.35,
    "Promo Flash -25%": 0.25,
    "2ème à -50%": 0.25,  # Moyenne
    "3 pour 2": 0.33,
}

SEGMENTS_CLIENTS = ["Premium", "Standard", "Budget", "Luxe", "Première Commande"]
CANAUX_VENTE = ["E-commerce", "Magasin Physique", "Application Mobile", "Marketplace", "Réseaux Sociaux"]

def gen_commerce_data(n):
    """Génère des données cohérentes pour commerce & consommation"""
    produits = list(COMMERCE_DATABASE.keys())
    data = []
    
    for i in range(n):
        # Choisir un produit aléatoire
        produit = np.random.choice(produits)
        info = COMMERCE_DATABASE[produit]
        
        # Prix avec variation
        prix_base = info["prix_base"]
        variation_marche = np.random.uniform(0.90, 1.10)
        prix_actuel = prix_base * variation_marche
        
        # Promotion (plus probable en certaines périodes)
        proba_promo = 0.35 if info["saisonnalite"] in ["Noël", "Fêtes"] else 0.20
        
        if np.random.random() < proba_promo:
            promotion = np.random.choice(list(TYPES_PROMOTIONS.keys())[1:], 
                                        p=[0.25, 0.20, 0.10, 0.15, 0.10, 0.15, 0.03, 0.02])
            reduction = TYPES_PROMOTIONS[promotion]
            prix_final = prix_actuel * (1 - reduction)
        else:
            promotion = "Aucune"
            prix_final = prix_actuel
        
        # Volume de ventes selon tendance et promo
        volume_base = {
            "Très Forte": np.random.uniform(500, 2000),
            "Forte": np.random.uniform(200, 800),
            "Moyenne": np.random.uniform(50, 300),
            "Faible": np.random.uniform(10, 100)
        }
        
        volume = volume_base.get(info["tendance"], 100)
        if promotion != "Aucune":
            volume *= np.random.uniform(1.5, 2.5)  # Boost promo
        
        volume = int(volume)
        
        # Segment client
        if info["categorie"] in ["Électronique", "Beauté"] and prix_base > 500:
            segment = np.random.choice(["Premium", "Luxe"], p=[0.6, 0.4])
        elif prix_base < 50:
            segment = np.random.choice(["Budget", "Standard"], p=[0.6, 0.4])
        else:
            segment = np.random.choice(SEGMENTS_CLIENTS, p=[0.2, 0.4, 0.2, 0.1, 0.1])
        
        # Canal de vente
        if info["categorie"] in ["Électronique", "Beauté"]:
            canal = np.random.choice(CANAUX_VENTE, p=[0.4, 0.2, 0.25, 0.10, 0.05])
        else:
            canal = np.random.choice(CANAUX_VENTE, p=[0.3, 0.4, 0.15, 0.10, 0.05])
        
        data.append({
            "produit": produit,
            "categorie": info["categorie"],
            "marque": info["marque"],
            "prix_unitaire": round(prix_final, 2),
            "promotion": promotion,
            "volume_ventes": volume,
            "segment_client": segment,
            "canal_vente": canal,
        })
    
    return data

def build_commerce_dataset(schema, n=500):
    cols = []
    if isinstance(schema, list) and all(isinstance(x, str) for x in schema):
        cols = [{"name": name} for name in schema]
    else:
        cols = schema
    
    # Générer les données combinées
    combined_data = gen_commerce_data(n)
    
    data = {}
    
    for col in cols:
        name = col["name"]
        nl = name.lower()
        
        # Mapping des 8 colonnes principales
        if "produit" in nl and "categorie" not in nl:
            data[name] = [d["produit"] for d in combined_data]
        elif "categorie" in nl:
            data[name] = [d["categorie"] for d in combined_data]
        elif "marque" in nl or "brand" in nl:
            data[name] = [d["marque"] for d in combined_data]
        elif "prix" in nl or "tarif" in nl or "price" in nl:
            data[name] = [d["prix_unitaire"] for d in combined_data]
        elif "promotion" in nl or "promo" in nl or "reduction" in nl:
            data[name] = [d["promotion"] for d in combined_data]
        elif "volume" in nl or "vente" in nl or "quantite" in nl:
            data[name] = [d["volume_ventes"] for d in combined_data]
        elif "segment" in nl or "client" in nl:
            data[name] = [d["segment_client"] for d in combined_data]
        elif "canal" in nl or "channel" in nl:
            data[name] = [d["canal_vente"] for d in combined_data]
        # Colonnes supplémentaires optionnelles
        elif nl in ["id", "id_transaction", "id_commande"]:
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
    parser = argparse.ArgumentParser(description="🛒 Générateur Commerce & Consommation")
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
    print(f"🛒 GÉNÉRATION DATASET COMMERCE '{args.name}'")
    print("="*80 + "\n")
    
    df = build_commerce_dataset(schema, n=args.n)
    
    out = args.out or f"{args.name}_commerce.csv"
    df.to_csv(out, index=False)
    
    print("="*80)
    print(f"✅ DATASET COMMERCE GÉNÉRÉ")
    print("="*80)
    print(f"📁 Fichier : {out}")
    print(f"📊 Lignes  : {len(df)}")
    print(f"📊 Colonnes: {len(df.columns)}\n")
    
    print("👁️  APERÇU :")
    print(df.head(args.preview).to_string(index=False))
    
    # Statistiques par catégorie
    if "categorie" in df.columns:
        print(f"\n{'='*80}")
        print("📦 RÉPARTITION PAR CATÉGORIE")
        print("="*80)
        print(df["categorie"].value_counts().to_string())
    
    # Statistiques promotions
    if "promotion" in df.columns:
        print(f"\n{'='*80}")
        print("🎁 RÉPARTITION DES PROMOTIONS")
        print("="*80)
        print(df["promotion"].value_counts().to_string())
    
    # Statistiques canaux
    if "canal_vente" in df.columns:
        print(f"\n{'='*80}")
        print("📱 RÉPARTITION PAR CANAL DE VENTE")
        print("="*80)
        print(df["canal_vente"].value_counts().to_string())
    
    # Top marques
    if "marque" in df.columns:
        print(f"\n{'='*80}")
        print("⭐ TOP 10 MARQUES")
        print("="*80)
        print(df["marque"].value_counts().head(10).to_string())
    
    print(f"\n✨ Génération terminée!\n")

if __name__ == "__main__":
    main()