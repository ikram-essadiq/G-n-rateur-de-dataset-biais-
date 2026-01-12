"""
GÉNÉRATEUR DE DONNÉES MOLÉCULES CHIMIQUES
Génère des données cohérentes pour molécules, formules, propriétés
"""

import json
import argparse
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

np.random.seed(42)

# ====================
# BASE DE DONNÉES MOLÉCULES
# ====================

MOLECULES_DATABASE = {
    # ============ MOLÉCULES ORGANIQUES SIMPLES ============
    "Eau": {
        "formule": "H2O", "masse_molaire": 18.015, "categorie": "Inorganique",
        "point_fusion": 0, "point_ebullition": 100, "solubilite": "Miscible",
        "toxicite": "Non toxique", "usage": "Solvant universel"
    },
    "Méthane": {
        "formule": "CH4", "masse_molaire": 16.04, "categorie": "Hydrocarbure",
        "point_fusion": -182, "point_ebullition": -161, "solubilite": "Faible",
        "toxicite": "Faible", "usage": "Combustible"
    },
    "Éthanol": {
        "formule": "C2H5OH", "masse_molaire": 46.07, "categorie": "Alcool",
        "point_fusion": -114, "point_ebullition": 78, "solubilite": "Miscible",
        "toxicite": "Modérée", "usage": "Solvant, Désinfectant"
    },
    "Glucose": {
        "formule": "C6H12O6", "masse_molaire": 180.16, "categorie": "Glucide",
        "point_fusion": 146, "point_ebullition": None, "solubilite": "Très soluble",
        "toxicite": "Non toxique", "usage": "Métabolisme énergétique"
    },
    "Acide Acétique": {
        "formule": "CH3COOH", "masse_molaire": 60.05, "categorie": "Acide Carboxylique",
        "point_fusion": 16, "point_ebullition": 118, "solubilite": "Miscible",
        "toxicite": "Corrosif", "usage": "Conservateur alimentaire"
    },
    
    # ============ MÉDICAMENTS ============
    "Aspirine": {
        "formule": "C9H8O4", "masse_molaire": 180.16, "categorie": "Médicament",
        "point_fusion": 135, "point_ebullition": 140, "solubilite": "Modérée",
        "toxicite": "Modérée", "usage": "Antalgique, Anti-inflammatoire"
    },
    "Paracétamol": {
        "formule": "C8H9NO2", "masse_molaire": 151.16, "categorie": "Médicament",
        "point_fusion": 169, "point_ebullition": None, "solubilite": "Modérée",
        "toxicite": "Modérée", "usage": "Antalgique, Antipyrétique"
    },
    "Ibuprofène": {
        "formule": "C13H18O2", "masse_molaire": 206.28, "categorie": "Médicament",
        "point_fusion": 75, "point_ebullition": None, "solubilite": "Faible",
        "toxicite": "Modérée", "usage": "Anti-inflammatoire"
    },
    "Caféine": {
        "formule": "C8H10N4O2", "masse_molaire": 194.19, "categorie": "Alcaloïde",
        "point_fusion": 238, "point_ebullition": 178, "solubilite": "Modérée",
        "toxicite": "Faible", "usage": "Stimulant SNC"
    },
    
    # ============ ACIDES ET BASES ============
    "Acide Sulfurique": {
        "formule": "H2SO4", "masse_molaire": 98.08, "categorie": "Acide Fort",
        "point_fusion": 10, "point_ebullition": 337, "solubilite": "Miscible",
        "toxicite": "Très toxique", "usage": "Industrie chimique"
    },
    "Acide Chlorhydrique": {
        "formule": "HCl", "masse_molaire": 36.46, "categorie": "Acide Fort",
        "point_fusion": -114, "point_ebullition": -85, "solubilite": "Miscible",
        "toxicite": "Corrosif", "usage": "Décapage, Synthèse"
    },
    "Hydroxyde de Sodium": {
        "formule": "NaOH", "masse_molaire": 40.00, "categorie": "Base Forte",
        "point_fusion": 318, "point_ebullition": 1388, "solubilite": "Très soluble",
        "toxicite": "Corrosif", "usage": "Industrie, Savonnerie"
    },
    "Ammoniaque": {
        "formule": "NH3", "masse_molaire": 17.03, "categorie": "Base Faible",
        "point_fusion": -78, "point_ebullition": -33, "solubilite": "Très soluble",
        "toxicite": "Toxique", "usage": "Fertilisant, Réfrigérant"
    },
    
    # ============ SOLVANTS ============
    "Acétone": {
        "formule": "C3H6O", "masse_molaire": 58.08, "categorie": "Cétone",
        "point_fusion": -95, "point_ebullition": 56, "solubilite": "Miscible",
        "toxicite": "Faible", "usage": "Solvant industriel"
    },
    "Benzène": {
        "formule": "C6H6", "masse_molaire": 78.11, "categorie": "Hydrocarbure Aromatique",
        "point_fusion": 5, "point_ebullition": 80, "solubilite": "Faible",
        "toxicite": "Cancérigène", "usage": "Solvant, Synthèse"
    },
    "Toluène": {
        "formule": "C7H8", "masse_molaire": 92.14, "categorie": "Hydrocarbure Aromatique",
        "point_fusion": -95, "point_ebullition": 111, "solubilite": "Faible",
        "toxicite": "Modérée", "usage": "Solvant, Carburant"
    },
    
    # ============ POLYMÈRES ET MATÉRIAUX ============
    "Polyéthylène": {
        "formule": "(C2H4)n", "masse_molaire": 28.05, "categorie": "Polymère",
        "point_fusion": 130, "point_ebullition": None, "solubilite": "Insoluble",
        "toxicite": "Non toxique", "usage": "Plastique, Emballage"
    },
    "Polypropylène": {
        "formule": "(C3H6)n", "masse_molaire": 42.08, "categorie": "Polymère",
        "point_fusion": 160, "point_ebullition": None, "solubilite": "Insoluble",
        "toxicite": "Non toxique", "usage": "Plastique, Textile"
    },
    "PVC": {
        "formule": "(C2H3Cl)n", "masse_molaire": 62.50, "categorie": "Polymère",
        "point_fusion": 80, "point_ebullition": None, "solubilite": "Insoluble",
        "toxicite": "Modérée", "usage": "Tuyauterie, Construction"
    },
    
    # ============ GAZ ============
    "Dioxyde de Carbone": {
        "formule": "CO2", "masse_molaire": 44.01, "categorie": "Gaz",
        "point_fusion": -78, "point_ebullition": -78, "solubilite": "Modérée",
        "toxicite": "Asphyxiant", "usage": "Boissons gazeuses, Extincteur"
    },
    "Oxygène": {
        "formule": "O2", "masse_molaire": 32.00, "categorie": "Gaz",
        "point_fusion": -218, "point_ebullition": -183, "solubilite": "Faible",
        "toxicite": "Non toxique", "usage": "Respiration, Combustion"
    },
    "Azote": {
        "formule": "N2", "masse_molaire": 28.01, "categorie": "Gaz",
        "point_fusion": -210, "point_ebullition": -196, "solubilite": "Très faible",
        "toxicite": "Asphyxiant", "usage": "Atmosphère inerte"
    },
    
    # ============ MOLÉCULES BIOLOGIQUES ============
    "Vitamine C": {
        "formule": "C6H8O6", "masse_molaire": 176.12, "categorie": "Vitamine",
        "point_fusion": 190, "point_ebullition": None, "solubilite": "Très soluble",
        "toxicite": "Non toxique", "usage": "Antioxydant, Supplément"
    },
    "Cholestérol": {
        "formule": "C27H46O", "masse_molaire": 386.65, "categorie": "Stéroïde",
        "point_fusion": 148, "point_ebullition": 360, "solubilite": "Insoluble",
        "toxicite": "Non toxique", "usage": "Membrane cellulaire"
    },
}

def gen_molecules_data(n):
    """Génère des données cohérentes pour molécules"""
    molecules = list(MOLECULES_DATABASE.keys())
    data = []
    
    for i in range(n):
        # Choisir une molécule aléatoire
        molecule = np.random.choice(molecules)
        info = MOLECULES_DATABASE[molecule]
        
        # Concentration variable selon la catégorie
        if info["categorie"] in ["Acide Fort", "Base Forte"]:
            concentration = np.random.uniform(0.1, 12)  # Molarité
            unite_conc = "M"
        elif info["categorie"] == "Médicament":
            concentration = np.random.uniform(100, 1000)  # mg
            unite_conc = "mg"
        elif info["categorie"] in ["Gaz"]:
            concentration = np.random.uniform(1, 100)  # %vol
            unite_conc = "%vol"
        elif info["categorie"] == "Polymère":
            concentration = np.random.uniform(10, 100)  # g
            unite_conc = "g"
        else:
            concentration = np.random.uniform(0.01, 10)  # g/L
            unite_conc = "g/L"
        
        data.append({
            "nom_molecule": molecule,
            "formule_chimique": info["formule"],
            "masse_molaire": info["masse_molaire"],
            "categorie": info["categorie"],
            "concentration": round(concentration, 2),
        })
    
    return data

def build_molecules_dataset(schema, n=500):
    cols = []
    if isinstance(schema, list) and all(isinstance(x, str) for x in schema):
        cols = [{"name": name} for name in schema]
    else:
        cols = schema
    
    # Générer les données combinées
    combined_data = gen_molecules_data(n)
    
    data = {}
    
    for col in cols:
        name = col["name"]
        nl = name.lower()
        
        # Mapping des 5 colonnes principales
        if "nom" in nl and "molecule" in nl:
            data[name] = [d["nom_molecule"] for d in combined_data]
        elif "formule" in nl:
            data[name] = [d["formule_chimique"] for d in combined_data]
        elif "masse" in nl or "molaire" in nl:
            data[name] = [d["masse_molaire"] for d in combined_data]
        elif "categorie" in nl or "type" in nl:
            data[name] = [d["categorie"] for d in combined_data]
        elif "concentration" in nl or "quantite" in nl:
            data[name] = [d["concentration"] for d in combined_data]
        # Colonnes supplémentaires optionnelles
        elif nl in ["id", "id_molecule", "id_echantillon"]:
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
    parser = argparse.ArgumentParser(description="🧪 Générateur Molécules Chimiques")
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
    print(f"🧪 GÉNÉRATION DATASET MOLÉCULES '{args.name}'")
    print("="*80 + "\n")
    
    df = build_molecules_dataset(schema, n=args.n)
    
    out = args.out or f"{args.name}_molecules.csv"
    df.to_csv(out, index=False)
    
    print("="*80)
    print(f"✅ DATASET MOLÉCULES GÉNÉRÉ")
    print("="*80)
    print(f"📁 Fichier : {out}")
    print(f"📊 Lignes  : {len(df)}")
    print(f"📊 Colonnes: {len(df.columns)}\n")
    
    print("👁️  APERÇU :")
    print(df.head(args.preview).to_string(index=False))
    
    # Statistiques par catégorie
    if "categorie" in df.columns:
        print(f"\n{'='*80}")
        print("⚗️  RÉPARTITION PAR CATÉGORIE")
        print("="*80)
        print(df["categorie"].value_counts().to_string())
    
    # Statistiques masse molaire
    if "masse_molaire" in df.columns:
        print(f"\n{'='*80}")
        print("📊 STATISTIQUES MASSE MOLAIRE (g/mol)")
        print("="*80)
        print(df["masse_molaire"].describe().to_string())
    
    # Top molécules
    if "nom_molecule" in df.columns:
        print(f"\n{'='*80}")
        print("🔬 TOP 10 MOLÉCULES")
        print("="*80)
        print(df["nom_molecule"].value_counts().head(10).to_string())
    
    print(f"\n✨ Génération terminée!\n")

if __name__ == "__main__":
    main()