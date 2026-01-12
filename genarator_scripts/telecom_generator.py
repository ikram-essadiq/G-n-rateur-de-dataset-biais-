"""
GÉNÉRATEUR DE DONNÉES ABONNEMENTS TÉLÉPHONIQUES
Génère des données cohérentes pour abonnements, opérateurs, forfaits
"""

import json
import argparse
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

np.random.seed(42)

# ====================
# BASE DE DONNÉES TÉLÉCOMMUNICATIONS
# ====================

OPERATEURS_DATABASE = {
    # ============ OPÉRATEURS MAROC ============
    "Maroc Telecom": {
        "pays": "Maroc", "type": "Mobile & Fixe",
        "forfaits": {
            "Jawal 50 Go": {"data": "50 Go", "prix": 100, "appels": "Illimités", "sms": "Illimités"},
            "Jawal 100 Go": {"data": "100 Go", "prix": 150, "appels": "Illimités", "sms": "Illimités"},
            "Jawal Illimité": {"data": "Illimité", "prix": 250, "appels": "Illimités", "sms": "Illimités"},
            "Forfait Entreprise": {"data": "200 Go", "prix": 350, "appels": "Illimités", "sms": "Illimités"},
        }
    },
    "Orange Maroc": {
        "pays": "Maroc", "type": "Mobile & Fixe",
        "forfaits": {
            "Orange 40 Go": {"data": "40 Go", "prix": 89, "appels": "2h", "sms": "500"},
            "Orange 80 Go": {"data": "80 Go", "prix": 129, "appels": "Illimités", "sms": "Illimités"},
            "Orange Max": {"data": "Illimité", "prix": 299, "appels": "Illimités", "sms": "Illimités"},
            "Orange Pro": {"data": "150 Go", "prix": 399, "appels": "Illimités", "sms": "Illimités"},
        }
    },
    "Inwi": {
        "pays": "Maroc", "type": "Mobile",
        "forfaits": {
            "Inwi 30 Go": {"data": "30 Go", "prix": 79, "appels": "1h", "sms": "200"},
            "Inwi 60 Go": {"data": "60 Go", "prix": 119, "appels": "Illimités", "sms": "Illimités"},
            "Inwi Unlimited": {"data": "Illimité", "prix": 279, "appels": "Illimités", "sms": "Illimités"},
        }
    },
    
    # ============ OPÉRATEURS FRANCE ============
    "Orange France": {
        "pays": "France", "type": "Mobile & Fixe",
        "forfaits": {
            "Orange 5G 100 Go": {"data": "100 Go", "prix": 24.99, "appels": "Illimités", "sms": "Illimités"},
            "Orange 5G Unlimited": {"data": "Illimité", "prix": 49.99, "appels": "Illimités", "sms": "Illimités"},
        }
    },
    "SFR": {
        "pays": "France", "type": "Mobile & Fixe",
        "forfaits": {
            "SFR 80 Go": {"data": "80 Go", "prix": 19.99, "appels": "Illimités", "sms": "Illimités"},
            "SFR Power": {"data": "150 Go", "prix": 35.99, "appels": "Illimités", "sms": "Illimités"},
        }
    },
    "Free Mobile": {
        "pays": "France", "type": "Mobile",
        "forfaits": {
            "Free 2€": {"data": "50 Mo", "prix": 2.00, "appels": "2h", "sms": "Illimités"},
            "Free 5G": {"data": "300 Go", "prix": 19.99, "appels": "Illimités", "sms": "Illimités"},
        }
    },
    "Bouygues Telecom": {
        "pays": "France", "type": "Mobile & Fixe",
        "forfaits": {
            "B&YOU 100 Go": {"data": "100 Go", "prix": 14.99, "appels": "Illimités", "sms": "Illimités"},
            "Sensation": {"data": "200 Go", "prix": 29.99, "appels": "Illimités", "sms": "Illimités"},
        }
    },
    
    # ============ OPÉRATEURS INTERNATIONAUX ============
    "Vodafone": {
        "pays": "International", "type": "Mobile",
        "forfaits": {
            "Vodafone Red": {"data": "100 Go", "prix": 45.00, "appels": "Illimités", "sms": "Illimités"},
            "Vodafone Unlimited": {"data": "Illimité", "prix": 65.00, "appels": "Illimités", "sms": "Illimités"},
        }
    },
    "T-Mobile": {
        "pays": "USA", "type": "Mobile",
        "forfaits": {
            "Magenta": {"data": "100 Go", "prix": 70.00, "appels": "Illimités", "sms": "Illimités"},
            "Magenta Max": {"data": "Illimité", "prix": 85.00, "appels": "Illimités", "sms": "Illimités"},
        }
    },
}

# Prénoms et noms pour générer des identités réalistes
PRENOMS = [
    "Mohammed", "Fatima", "Ahmed", "Khadija", "Youssef", "Aïcha", "Hassan", "Zineb",
    "Omar", "Salma", "Ali", "Nora", "Karim", "Leila", "Mehdi", "Sofia",
    "Jean", "Marie", "Pierre", "Julie", "Michel", "Sophie", "Laurent", "Camille",
    "David", "Emma", "Thomas", "Léa", "Nicolas", "Chloé", "Alexandre", "Sarah",
    "John", "Emily", "Michael", "Jessica", "James", "Ashley", "Robert", "Lisa"
]

NOMS = [
    "Alaoui", "Benali", "El Amrani", "Idrissi", "Tazi", "Benjelloun", "Sefrioui", "Fassi",
    "Ouazzani", "Bennani", "Lazrak", "Chraibi", "Berrada", "El Fassi", "Filali", "Kettani",
    "Dupont", "Martin", "Bernard", "Dubois", "Thomas", "Robert", "Richard", "Petit",
    "Durand", "Leroy", "Moreau", "Simon", "Laurent", "Lefebvre", "Michel", "Garcia",
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis"
]

def gen_telecom_data(n):
    """Génère des données cohérentes pour abonnements téléphoniques"""
    data = []
    
    for i in range(n):
        # Générer ID unique
        id_abonne = f"ABN{str(i+1).zfill(8)}"
        
        # Générer nom personne
        prenom = np.random.choice(PRENOMS)
        nom = np.random.choice(NOMS)
        nom_complet = f"{prenom} {nom}"
        
        # Choisir opérateur
        operateur = np.random.choice(list(OPERATEURS_DATABASE.keys()))
        info_operateur = OPERATEURS_DATABASE[operateur]
        
        # Choisir forfait cohérent avec l'opérateur
        forfaits_disponibles = list(info_operateur["forfaits"].keys())
        forfait_nom = np.random.choice(forfaits_disponibles)
        forfait_info = info_operateur["forfaits"][forfait_nom]
        
        data.append({
            "id": id_abonne,
            "nom_personne": nom_complet,
            "operateur_telephonique": operateur,
            "forfait_abonnement": forfait_nom,
        })
    
    return data

def build_telecom_dataset(schema, n=500):
    cols = []
    if isinstance(schema, list) and all(isinstance(x, str) for x in schema):
        cols = [{"name": name} for name in schema]
    else:
        cols = schema
    
    # Générer les données combinées
    combined_data = gen_telecom_data(n)
    
    data = {}
    
    for col in cols:
        name = col["name"]
        nl = name.lower()
        
        # Mapping des 4 colonnes principales
        if nl == "id" or "id_abonne" in nl:
            data[name] = [d["id"] for d in combined_data]
        elif "nom" in nl and ("personne" in nl or "client" in nl or "abonne" in nl):
            data[name] = [d["nom_personne"] for d in combined_data]
        elif "operateur" in nl or "operator" in nl:
            data[name] = [d["operateur_telephonique"] for d in combined_data]
        elif "forfait" in nl or "plan" in nl or "abonnement" in nl:
            data[name] = [d["forfait_abonnement"] for d in combined_data]
        # Colonnes supplémentaires optionnelles
        elif "date" in nl and "debut" in nl:
            base = datetime(2023, 1, 1)
            dates = [base + timedelta(days=np.random.randint(0, 365)) for _ in range(n)]
            data[name] = [d.strftime("%Y-%m-%d") for d in dates]
        elif "date" in nl and "fin" in nl:
            base = datetime(2024, 1, 1)
            dates = [base + timedelta(days=np.random.randint(0, 730)) for _ in range(n)]
            data[name] = [d.strftime("%Y-%m-%d") for d in dates]
        elif "email" in nl:
            data[name] = [f"{d['nom_personne'].lower().replace(' ', '.')}@email.com" for d in combined_data]
        elif "telephone" in nl or "numero" in nl:
            data[name] = [f"+212{np.random.randint(600000000, 799999999)}" for _ in range(n)]
        elif "statut" in nl:
            data[name] = np.random.choice(["Actif", "Suspendu", "Résilié"], n, p=[0.85, 0.10, 0.05])
        else:
            print(f"⚠️  Colonne '{name}' non reconnue, valeurs par défaut")
            data[name] = ["N/A"] * n
    
    return pd.DataFrame(data)

def main():
    parser = argparse.ArgumentParser(description="📱 Générateur Abonnements Téléphoniques")
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
    print(f"📱 GÉNÉRATION DATASET ABONNEMENTS TÉLÉPHONIQUES '{args.name}'")
    print("="*80 + "\n")
    
    df = build_telecom_dataset(schema, n=args.n)
    
    out = args.out or f"{args.name}_abonnements.csv"
    df.to_csv(out, index=False)
    
    print("="*80)
    print(f"✅ DATASET ABONNEMENTS GÉNÉRÉ")
    print("="*80)
    print(f"📁 Fichier : {out}")
    print(f"📊 Lignes  : {len(df)}")
    print(f"📊 Colonnes: {len(df.columns)}\n")
    
    print("👁️  APERÇU :")
    print(df.head(args.preview).to_string(index=False))
    
    # Statistiques par opérateur
    if "operateur_telephonique" in df.columns:
        print(f"\n{'='*80}")
        print("📡 RÉPARTITION PAR OPÉRATEUR")
        print("="*80)
        print(df["operateur_telephonique"].value_counts().to_string())
    
    # Statistiques par forfait
    if "forfait_abonnement" in df.columns:
        print(f"\n{'='*80}")
        print("📊 TOP 10 FORFAITS")
        print("="*80)
        print(df["forfait_abonnement"].value_counts().head(10).to_string())
    
    print(f"\n✨ Génération terminée!\n")

if __name__ == "__main__":
    main()