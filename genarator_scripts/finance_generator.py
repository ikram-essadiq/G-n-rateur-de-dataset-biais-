"""
GÉNÉRATEUR DE DONNÉES SECTEUR FINANCE INTERNATIONAL
Génère des données cohérentes pour transactions, marchés, institutions financières
"""

import json
import argparse
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

np.random.seed(42)

# ====================
# BASE DE DONNÉES INSTITUTIONS FINANCIÈRES
# ====================

FINANCE_DATABASE = {
    # ============ BANQUES CENTRALES ============
    "Banque Al-Maghrib": {
        "type": "Banque Centrale", "pays": "Maroc", "ville": "Rabat",
        "code_pays": "MAR", "devise": "MAD", "crea": 1959,
        "region": "Afrique du Nord"
    },
    "Federal Reserve": {
        "type": "Banque Centrale", "pays": "USA", "ville": "Washington DC",
        "code_pays": "USA", "devise": "USD", "crea": 1913,
        "region": "Amérique du Nord"
    },
    "Banque Centrale Européenne": {
        "type": "Banque Centrale", "pays": "UE", "ville": "Francfort",
        "code_pays": "EUR", "devise": "EUR", "crea": 1998,
        "region": "Europe"
    },
    "Bank of England": {
        "type": "Banque Centrale", "pays": "Royaume-Uni", "ville": "Londres",
        "code_pays": "GBR", "devise": "GBP", "crea": 1694,
        "region": "Europe"
    },
    "Banque du Japon": {
        "type": "Banque Centrale", "pays": "Japon", "ville": "Tokyo",
        "code_pays": "JPN", "devise": "JPY", "crea": 1882,
        "region": "Asie"
    },
    "Banque Populaire de Chine": {
        "type": "Banque Centrale", "pays": "Chine", "ville": "Pékin",
        "code_pays": "CHN", "devise": "CNY", "crea": 1948,
        "region": "Asie"
    },
    
    # ============ BANQUES COMMERCIALES ============
    "Attijariwafa Bank": {
        "type": "Banque Commerciale", "pays": "Maroc", "ville": "Casablanca",
        "code_pays": "MAR", "devise": "MAD", "crea": 2003,
        "region": "Afrique du Nord"
    },
    "JPMorgan Chase": {
        "type": "Banque Commerciale", "pays": "USA", "ville": "New York",
        "code_pays": "USA", "devise": "USD", "crea": 2000,
        "region": "Amérique du Nord"
    },
    "HSBC Holdings": {
        "type": "Banque Commerciale", "pays": "Royaume-Uni", "ville": "Londres",
        "code_pays": "GBR", "devise": "GBP", "crea": 1865,
        "region": "Europe"
    },
    "BNP Paribas": {
        "type": "Banque Commerciale", "pays": "France", "ville": "Paris",
        "code_pays": "FRA", "devise": "EUR", "crea": 2000,
        "region": "Europe"
    },
    "Deutsche Bank": {
        "type": "Banque Commerciale", "pays": "Allemagne", "ville": "Francfort",
        "code_pays": "DEU", "devise": "EUR", "crea": 1870,
        "region": "Europe"
    },
    "ICBC": {
        "type": "Banque Commerciale", "pays": "Chine", "ville": "Pékin",
        "code_pays": "CHN", "devise": "CNY", "crea": 1984,
        "region": "Asie"
    },
    "Mitsubishi UFJ": {
        "type": "Banque Commerciale", "pays": "Japon", "ville": "Tokyo",
        "code_pays": "JPN", "devise": "JPY", "crea": 2005,
        "region": "Asie"
    },
    "Standard Bank": {
        "type": "Banque Commerciale", "pays": "Afrique du Sud", "ville": "Johannesburg",
        "code_pays": "ZAF", "devise": "ZAR", "crea": 1862,
        "region": "Afrique"
    },
    
    # ============ BOURSES ============
    "Bourse de Casablanca": {
        "type": "Bourse", "pays": "Maroc", "ville": "Casablanca",
        "code_pays": "MAR", "devise": "MAD", "crea": 1929,
        "region": "Afrique du Nord", "indice": "MASI"
    },
    "NYSE": {
        "type": "Bourse", "pays": "USA", "ville": "New York",
        "code_pays": "USA", "devise": "USD", "crea": 1792,
        "region": "Amérique du Nord", "indice": "NYSE"
    },
    "London Stock Exchange": {
        "type": "Bourse", "pays": "Royaume-Uni", "ville": "Londres",
        "code_pays": "GBR", "devise": "GBP", "crea": 1801,
        "region": "Europe", "indice": "FTSE"
    },
    "Euronext Paris": {
        "type": "Bourse", "pays": "France", "ville": "Paris",
        "code_pays": "FRA", "devise": "EUR", "crea": 2000,
        "region": "Europe", "indice": "CAC40"
    },
    "Tokyo Stock Exchange": {
        "type": "Bourse", "pays": "Japon", "ville": "Tokyo",
        "code_pays": "JPN", "devise": "JPY", "crea": 1878,
        "region": "Asie", "indice": "NIKKEI"
    },
}

CURRENCIES = {
    "MAD": {"nom": "Dirham Marocain", "taux_usd": 10.15},
    "USD": {"nom": "Dollar Américain", "taux_usd": 1.00},
    "EUR": {"nom": "Euro", "taux_usd": 1.08},
    "GBP": {"nom": "Livre Sterling", "taux_usd": 1.27},
    "JPY": {"nom": "Yen Japonais", "taux_usd": 0.0067},
    "CNY": {"nom": "Yuan Chinois", "taux_usd": 0.14},
    "ZAR": {"nom": "Rand Sud-Africain", "taux_usd": 0.053},
}

FINANCE_CATEGORIES = {
    "type_transaction": ["Virement", "Prélèvement", "Dépôt", "Retrait", "Carte", "Virement International"],
    "statut_transaction": ["Complétée", "En attente", "Rejetée", "En cours"],
    "type_compte": ["Courant", "Épargne", "Professionnel", "Joint"],
    "secteur_activite": ["Technologie", "Finance", "Santé", "Énergie", "Commerce", "Industrie"],
    "type_produit": ["Crédit Immobilier", "Crédit Auto", "Crédit Consommation", "Compte Épargne"],
    "risque_credit": ["Très Faible", "Faible", "Moyen", "Élevé", "Très Élevé"],
}

def gen_combined_data(n):
    """Génère des données cohérentes avec institution + transaction liées"""
    institutions = list(FINANCE_DATABASE.keys())
    data = []
    
    for i in range(n):
        # Choisir une institution aléatoire
        inst = np.random.choice(institutions)
        info = FINANCE_DATABASE[inst]
        
        # Capital selon le type
        if info["type"] == "Banque Centrale":
            capital = np.random.uniform(50000, 500000)
        elif info["type"] == "Banque Commerciale":
            capital = np.random.uniform(5000, 100000)
        else:
            capital = np.random.uniform(1000, 50000)
        
        # Transaction avec la même devise que l'institution
        type_trans = np.random.choice(FINANCE_CATEGORIES["type_transaction"])
        statut = np.random.choice(FINANCE_CATEGORIES["statut_transaction"], 
                                p=[0.85, 0.08, 0.04, 0.03])
        
        if type_trans == "Carte":
            montant = np.random.lognormal(4, 1.5)
        elif type_trans == "Virement International":
            montant = np.random.lognormal(8, 2)
        else:
            montant = np.random.lognormal(6, 1.5)
        
        montant = max(10, montant)
        frais = montant * np.random.uniform(0, 0.03) if type_trans == "Virement International" else np.random.uniform(0, 10)
        
        # Données de marché
        if info["type"] == "Bourse":
            prix_ouv = np.random.uniform(50, 500)
            variation = np.random.normal(0, 0.02)
            prix_ferm = prix_ouv * (1 + variation)
            volume = np.random.lognormal(15, 2)
            indice = info.get("indice", "N/A")
        else:
            prix_ouv = None
            prix_ferm = None
            variation = None
            volume = None
            indice = None
        
        data.append({
            "institution": inst,
            "type": info["type"],
            "pays": info["pays"],
            "ville": info["ville"],
            "region": info["region"],
            "devise": info["devise"],
            "annee_creation": info["crea"],
            "capital_millions": round(capital, 2),
            "type_transaction": type_trans,
            "montant": round(montant, 2),
            "frais": round(frais, 2),
            "statut": statut,
            "bourse": inst if info["type"] == "Bourse" else None,
            "indice": indice,
            "prix_ouverture": round(prix_ouv, 2) if prix_ouv else None,
            "prix_fermeture": round(prix_ferm, 2) if prix_ferm else None,
            "variation_pct": round(variation * 100, 2) if variation else None,
            "volume_millions": round(volume, 2) if volume else None,
        })
    
    return data

def build_finance_dataset(schema, n=500):
    cols = []
    if isinstance(schema, list) and all(isinstance(x, str) for x in schema):
        cols = [{"name": name} for name in schema]
    else:
        cols = schema
    
    # Générer les données combinées
    combined_data = gen_combined_data(n)
    
    data = {}
    
    for col in cols:
        name = col["name"]
        nl = name.lower()
        
        # Mapping des colonnes
        if "institution" in nl or "banque" in nl:
            data[name] = [d["institution"] for d in combined_data]
        elif "type_transaction" in nl:
            data[name] = [d["type_transaction"] for d in combined_data]
        elif nl == "type" and any("transaction" in c["name"].lower() for c in cols):
            data[name] = [d["type_transaction"] for d in combined_data]
        elif nl == "type":
            data[name] = [d["type"] for d in combined_data]
        elif "ville" in nl:
            data[name] = [d["ville"] for d in combined_data]
        elif "pays" in nl:
            data[name] = [d["pays"] for d in combined_data]
        elif "region" in nl:
            data[name] = [d["region"] for d in combined_data]
        elif "devise" in nl or "currency" in nl:
            data[name] = [d["devise"] for d in combined_data]
        elif "capital" in nl:
            data[name] = [d["capital_millions"] for d in combined_data]
        elif "montant" in nl:
            data[name] = [d["montant"] for d in combined_data]
        elif "frais" in nl:
            data[name] = [d["frais"] for d in combined_data]
        elif "statut" in nl:
            data[name] = [d["statut"] for d in combined_data]
        elif "bourse" in nl and nl != "bourse":
            data[name] = [d["bourse"] for d in combined_data]
        elif "indice" in nl:
            data[name] = [d["indice"] for d in combined_data]
        elif "variation" in nl:
            data[name] = [d["variation_pct"] for d in combined_data]
        elif "volume" in nl:
            data[name] = [d["volume_millions"] for d in combined_data]
        elif "prix" in nl and "ouverture" in nl:
            data[name] = [d["prix_ouverture"] for d in combined_data]
        elif "prix" in nl and "fermeture" in nl:
            data[name] = [d["prix_fermeture"] for d in combined_data]
        # IDs
        elif nl in ["id", "id_transaction", "id_client", "id_compte"]:
            data[name] = [f"{name}_{str(i+1).zfill(8)}" for i in range(n)]
        # Dates
        elif "date" in nl:
            base = datetime(2024, 1, 1)
            dates = [base + timedelta(days=int(i * 365 / n)) for i in range(n)]
            data[name] = [d.strftime("%Y-%m-%d") for d in dates]
        else:
            # Valeur par défaut
            print(f"⚠️  Colonne '{name}' non reconnue, valeurs aléatoires générées")
            data[name] = np.random.uniform(0, 1000, n)
    
    return pd.DataFrame(data)

def main():
    parser = argparse.ArgumentParser(description="💰 Générateur Finance International")
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
    print(f"💰 GÉNÉRATION DATASET FINANCE '{args.name}'")
    print("="*80 + "\n")
    
    df = build_finance_dataset(schema, n=args.n)
    
    out = args.out or f"{args.name}_finance.csv"
    df.to_csv(out, index=False)
    
    print("="*80)
    print(f"✅ DATASET FINANCE GÉNÉRÉ")
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
    
    # Statistiques par devise
    if "devise" in df.columns:
        print(f"\n{'='*80}")
        print("💱 RÉPARTITION PAR DEVISE")
        print("="*80)
        print(df["devise"].value_counts().to_string())
    
    if "type_transaction" in df.columns:
        print(f"\n{'='*80}")
        print("📈 RÉPARTITION PAR TYPE DE TRANSACTION")
        print("="*80)
        print(df["type_transaction"].value_counts().to_string())
    
    print(f"\n✨ Génération terminée!\n")

if __name__ == "__main__":
    main()