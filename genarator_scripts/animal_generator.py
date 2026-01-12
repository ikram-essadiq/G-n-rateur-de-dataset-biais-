"""
GÉNÉRATEUR DE DONNÉES COHÉRENTES POUR ANIMAUX - VERSION POWERSHELL
Génère des données d'animaux avec cohérence totale (espèce, race, âge, poids, etc.)
Compatible PowerShell avec --cols
"""

import json
import argparse
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

np.random.seed(42)

# ====================
# DONNÉES COHÉRENTES PAR ESPÈCE
# ====================
ANIMAUX_DATA = {
    "Chien": {
        "races": ["Berger Allemand", "Labrador", "Golden Retriever", "Bulldog Français", "Beagle", 
                  "Chihuahua", "Yorkshire", "Caniche", "Husky", "Boxer", "Rottweiler"],
        "noms": ["Max", "Bella", "Rocky", "Luna", "Charlie", "Daisy", "Rex", "Milo", "Buddy", "Lola",
                 "Zeus", "Maya", "Duke", "Ruby", "Oscar", "Nala", "Simba", "Coco", "Thor", "Stella"],
        "poids_min": 5, "poids_max": 50,
        "esperance_vie": 12,
        "regime": "Omnivore",
        "habitat": "Domestique"
    },
    "Chat": {
        "races": ["Persan", "Maine Coon", "Siamois", "Bengal", "Européen", "British Shorthair",
                  "Ragdoll", "Sphynx", "Chartreux", "Scottish Fold"],
        "noms": ["Minou", "Felix", "Tigrou", "Simba", "Nala", "Whiskers", "Shadow", "Mittens", 
                 "Gizmo", "Luna", "Oliver", "Cleo", "Leo", "Bella", "Charlie", "Lucy"],
        "poids_min": 3, "poids_max": 8,
        "esperance_vie": 15,
        "regime": "Carnivore",
        "habitat": "Domestique"
    },
    "Cheval": {
        "races": ["Pur-sang Arabe", "Frison", "Quarter Horse", "Appaloosa", "Mustang", 
                  "Andalou", "Percheron", "Shetland"],
        "noms": ["Spirit", "Thunder", "Shadow", "Blaze", "Storm", "Star", "Flash", "Apollo",
                 "Bella", "Luna", "Phoenix", "Maximus", "Pegasus", "Tornado"],
        "poids_min": 400, "poids_max": 800,
        "esperance_vie": 25,
        "regime": "Herbivore",
        "habitat": "Ferme/Écurie"
    },
    "Lapin": {
        "races": ["Nain", "Bélier", "Angora", "Rex", "Géant des Flandres"],
        "noms": ["Fluffy", "Thumper", "Snowball", "Cotton", "Bugs", "Cottontail", "Oreo",
                 "Peter", "Clover", "Honey", "Bunny", "Marshmallow"],
        "poids_min": 1, "poids_max": 6,
        "esperance_vie": 8,
        "regime": "Herbivore",
        "habitat": "Domestique"
    },
    "Oiseau": {
        "races": ["Perroquet Ara", "Canari", "Perruche", "Cacatoès", "Inséparable", "Calopsitte"],
        "noms": ["Tweety", "Kiwi", "Sky", "Rio", "Sunny", "Blue", "Coco", "Pepper",
                 "Angel", "Buddy", "Charlie", "Mango"],
        "poids_min": 0.05, "poids_max": 1.5,
        "esperance_vie": 15,
        "regime": "Granivore",
        "habitat": "Cage/Volière"
    },
    "Poisson": {
        "races": ["Poisson Rouge", "Betta", "Guppy", "Néon", "Discus", "Carpe Koï"],
        "noms": ["Nemo", "Goldie", "Bubbles", "Flash", "Splash", "Finn", "Blue", "Rainbow"],
        "poids_min": 0.01, "poids_max": 0.5,
        "esperance_vie": 5,
        "regime": "Omnivore",
        "habitat": "Aquarium"
    }
}

# ====================
# CATÉGORIES SUPPLÉMENTAIRES
# ====================
ANIMAUX_CATEGORIES = {
    "couleur_pelage": ["Noir", "Blanc", "Marron", "Gris", "Roux", "Beige", "Tacheté", "Rayé", "Tricolore"],
    "statut_sante": ["Excellent", "Bon", "Moyen", "À surveiller"],
    "vaccination": ["À jour", "En retard", "Non vacciné"],
    "sterilise": ["Oui", "Non"],
    "sexe_animal": ["Mâle", "Femelle"],
    "caractere": ["Calme", "Joueur", "Timide", "Énergique", "Affectueux", "Indépendant", "Agressif"],
    "niveau_activite": ["Très actif", "Actif", "Modéré", "Calme", "Très calme"],
    "veterinaire": ["Dr. Martin", "Dr. Dubois", "Dr. Benali", "Dr. Laurent", "Clinique Vétérinaire Centre"],
    "ville": ["Paris", "Casablanca", "Lyon", "Marseille", "Rabat", "Marrakech", "Fès", "Tanger", "Toulouse", "Bordeaux"]
}

# ====================
# GÉNÉRATEURS COHÉRENTS POUR ANIMAUX
# ====================
def gen_animal_data(n):
    """Génère des données d'animaux COHÉRENTES"""
    animals = []
    
    for _ in range(n):
        espece = np.random.choice(list(ANIMAUX_DATA.keys()))
        data_espece = ANIMAUX_DATA[espece]
        
        race = np.random.choice(data_espece["races"])
        nom = np.random.choice(data_espece["noms"])
        
        age_max = data_espece["esperance_vie"]
        age = np.random.randint(0, age_max + 1)
        
        poids_min = data_espece["poids_min"]
        poids_max = data_espece["poids_max"]
        poids = round(np.random.uniform(poids_min, poids_max), 2)
        
        regime = data_espece["regime"]
        habitat = data_espece["habitat"]
        
        animals.append({
            "espece": espece,
            "race": race,
            "nom": nom,
            "age": age,
            "poids": poids,
            "regime_alimentaire": regime,
            "habitat": habitat
        })
    
    return animals

def gen_date_adoption(ages, current_date=None):
    """Génère des dates d'adoption COHÉRENTES avec l'âge"""
    if current_date is None:
        current_date = datetime.now()
    
    dates_adoption = []
    for age in ages:
        # Pour les animaux très jeunes (0-1 an), adoption entre 2 et 6 mois
        if age == 0:
            age_adoption_mois = np.random.randint(2, 7)  # 2 à 6 mois
        else:
            # Pour les autres, adoption à n'importe quel moment de leur vie
            max_mois = age * 12
            age_adoption_mois = np.random.randint(2, max(3, max_mois + 1))
        
        date_adoption = current_date - timedelta(days=age * 365) + timedelta(days=age_adoption_mois * 30)
        dates_adoption.append(date_adoption.strftime("%Y-%m-%d"))
    
    return dates_adoption

def gen_date_naissance_animal(ages, current_date=None):
    """Génère des dates de naissance COHÉRENTES avec l'âge"""
    if current_date is None:
        current_date = datetime.now()
    
    dates_naissance = []
    for age in ages:
        date_naissance = current_date - timedelta(days=age * 365 + np.random.randint(0, 365))
        dates_naissance.append(date_naissance.strftime("%Y-%m-%d"))
    
    return dates_naissance

def gen_taille_coherente(especes, poids):
    """Génère des tailles cohérentes avec l'espèce et le poids"""
    tailles = []
    for i, espece in enumerate(especes):
        p = poids[i]
        if espece == "Chien":
            taille = int(20 + (p * 0.8))
        elif espece == "Chat":
            taille = int(20 + (p * 2))
        elif espece == "Cheval":
            taille = int(120 + (p * 0.1))
        elif espece == "Lapin":
            taille = int(15 + (p * 5))
        elif espece == "Oiseau":
            taille = int(5 + (p * 20))
        elif espece == "Poisson":
            taille = int(2 + (p * 30))
        else:
            taille = 30
        
        tailles.append(taille)
    
    return tailles

def gen_prix_coherent(especes, races):
    """Génère des prix d'achat cohérents avec l'espèce et la race"""
    prix_base = {
        "Chien": 800,
        "Chat": 500,
        "Cheval": 5000,
        "Lapin": 50,
        "Oiseau": 150,
        "Poisson": 20
    }
    
    races_premium = ["Pur-sang Arabe", "Persan", "Bengal", "Perroquet Ara", "Frison"]
    
    prix = []
    for i, espece in enumerate(especes):
        base = prix_base.get(espece, 100)
        race = races[i]
        
        if race in races_premium:
            base *= 2
        
        prix_final = int(base * np.random.uniform(0.7, 1.3))
        prix.append(prix_final)
    
    return prix

def gen_id_animal(n, prefix="ANI"):
    """Génère des identifiants d'animaux"""
    return [f"{prefix}_{str(i+1).zfill(6)}" for i in range(n)]

# ====================
# DÉTECTION INTELLIGENTE POUR ANIMAUX
# ====================
def guess_animal_type(name):
    """Détecte automatiquement le type de colonne pour animaux"""
    name_lower = name.lower()
    
    if name_lower in ["espece", "espèce", "type_animal"]:
        return ("animal_espece", {})
    
    if name_lower in ["race"]:
        return ("animal_race", {})
    
    if name_lower in ["nom", "nom_animal", "prenom"]:
        return ("animal_nom", {})
    
    if name_lower in ["age", "âge"]:
        return ("animal_age", {})
    
    if name_lower in ["poids", "poid"]:
        return ("animal_poids", {})
    
    if name_lower in ["taille", "hauteur"]:
        return ("animal_taille", {})
    
    if name_lower in ["regime", "régime", "regime_alimentaire"]:
        return ("animal_regime", {})
    
    if name_lower in ["habitat"]:
        return ("animal_habitat", {})
    
    if "date" in name_lower and ("naissance" in name_lower or "birth" in name_lower):
        return ("animal_date_naissance", {})
    
    if "date" in name_lower and ("adoption" in name_lower):
        return ("animal_date_adoption", {})
    
    if "prix" in name_lower or "price" in name_lower or "cout" in name_lower:
        return ("animal_prix", {})
    
    if "id" in name_lower or "numero" in name_lower:
        return ("animal_id", {})
    
    if name_lower in ["sexe", "genre"]:
        return ("categorical", {"categories": ANIMAUX_CATEGORIES["sexe_animal"]})
    
    for key in ANIMAUX_CATEGORIES:
        if key in name_lower or name_lower in key:
            return ("categorical", {"categories": ANIMAUX_CATEGORIES[key]})
    
    return ("categorical", {"categories": ["Option A", "Option B", "Option C"]})

# ====================
# CONSTRUCTION DU DATASET ANIMAUX
# ====================
def build_animal_dataset(schema, n=500):
    """Construit un dataset d'animaux avec données COHÉRENTES"""
    
    cols = []
    if isinstance(schema, list) and all(isinstance(x, str) for x in schema):
        for name in schema:
            t, params = guess_animal_type(name)
            cols.append({"name": name, "type": t, "params": params})
    else:
        for c in schema:
            name = c.get("name")
            if not name:
                raise ValueError("Chaque colonne doit avoir un 'name'")
            t = c.get("type")
            params = c.get("params", {})
            if not t:
                guessed_t, guessed_params = guess_animal_type(name)
                guessed_params.update(params)
                t = guessed_t
                params = guessed_params
            cols.append({"name": name, "type": t, "params": params})
    
    animals = gen_animal_data(n)
    
    especes = [a["espece"] for a in animals]
    races = [a["race"] for a in animals]
    noms = [a["nom"] for a in animals]
    ages = [a["age"] for a in animals]
    poids = [a["poids"] for a in animals]
    regimes = [a["regime_alimentaire"] for a in animals]
    habitats = [a["habitat"] for a in animals]
    
    dates_naissance = gen_date_naissance_animal(ages)
    dates_adoption = gen_date_adoption(ages)
    tailles = gen_taille_coherente(especes, poids)
    prix = gen_prix_coherent(especes, races)
    ids = gen_id_animal(n)
    
    data = {}
    
    for col in cols:
        name = col["name"]
        t = col["type"]
        p = col.get("params", {})
        
        if t == "animal_espece":
            data[name] = especes
        elif t == "animal_race":
            data[name] = races
        elif t == "animal_nom":
            data[name] = noms
        elif t == "animal_age":
            data[name] = ages
        elif t == "animal_poids":
            data[name] = poids
        elif t == "animal_taille":
            data[name] = tailles
        elif t == "animal_regime":
            data[name] = regimes
        elif t == "animal_habitat":
            data[name] = habitats
        elif t == "animal_date_naissance":
            data[name] = dates_naissance
        elif t == "animal_date_adoption":
            data[name] = dates_adoption
        elif t == "animal_prix":
            data[name] = prix
        elif t == "animal_id":
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
        description="🐾 Générateur COHÉRENT de datasets d'animaux",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
EXEMPLES POWERSHELL :

🐕 Dataset simple (MÉTHODE RECOMMANDÉE) :
  python animal_generator.py --name pets --cols id,nom,espece,race,age,poids,sexe,couleur_pelage --n 2000

🏥 Dataset vétérinaire :
  python animal_generator.py --name veterinaire --cols id,nom,espece,race,age,poids,taille,date_naissance,vaccination,veterinaire,ville --n 2000

🐴 Dataset refuge :
  python animal_generator.py --name refuge --cols id,nom,espece,race,age,date_adoption,caractere,sterilise,statut_sante --n 2000

📄 Ou utiliser un fichier JSON :
  python animal_generator.py --name pets --schema schema.json --n 2000

COLONNES DISPONIBLES :
  id, nom, espece, race, age, poids, taille, date_naissance, date_adoption,
  sexe, couleur_pelage, vaccination, sterilise, caractere, niveau_activite,
  statut_sante, veterinaire, ville, prix, regime_alimentaire, habitat
        """
    )
    
    parser.add_argument("--name", required=True, help="Nom du dataset")
    parser.add_argument("--schema", default=None, help="Colonnes JSON ou fichier.json")
    parser.add_argument("--cols", default=None, help="Colonnes séparées par virgules (RECOMMANDÉ pour PowerShell)")
    parser.add_argument("--n", type=int, default=500, help="Nombre de lignes")
    parser.add_argument("--out", default=None, help="Fichier de sortie")
    parser.add_argument("--preview", type=int, default=10, help="Lignes à afficher")
    
    args = parser.parse_args()
    
    # Charger schéma
    if not args.schema and not args.cols:
        print("❌ Erreur: Vous devez fournir --schema OU --cols")
        print("\n💡 Pour PowerShell, utilisez --cols :")
        print("   python animal_generator.py --name pets --cols id,nom,espece,race,age,poids --n 2000")
        return
    
    try:
        if args.cols:
            # Format simple pour PowerShell
            schema = [col.strip() for col in args.cols.split(',')]
            print(f"✅ Colonnes détectées: {', '.join(schema)}\n")
        elif args.schema.endswith('.json'):
            with open(args.schema, 'r', encoding='utf-8') as f:
                schema = json.load(f)
        else:
            schema = json.loads(args.schema)
    except Exception as e:
        print(f"❌ Erreur schéma: {e}")
        print("\n💡 Utilisez plutôt --cols pour éviter les problèmes de guillemets :")
        print("   python animal_generator.py --name pets --cols id,nom,espece,race,age,poids --n 2000")
        return
    
    print(f"{'='*80}")
    print(f"🐾 GÉNÉRATION DU DATASET D'ANIMAUX '{args.name}'")
    print("="*80 + "\n")
    
    try:
        df = build_animal_dataset(schema, n=args.n)
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        return
    
    out = args.out or f"{args.name}_animaux.csv"
    df.to_csv(out, index=False, encoding='utf-8-sig')
    
    print("="*80)
    print(f"✅ DATASET D'ANIMAUX GÉNÉRÉ")
    print("="*80)
    print(f"📁 Fichier : {out}")
    print(f"📊 Lignes  : {len(df)}")
    print(f"📊 Colonnes: {len(df.columns)}\n")
    
    print("👁️  APERÇU :")
    print(df.head(args.preview).to_string(index=False))
    
    print(f"\n{'='*80}")
    print("✅ VÉRIFICATIONS DE COHÉRENCE")
    print("="*80)
    
    if "espece" in df.columns and "race" in df.columns and "poids" in df.columns:
        print("\n✓ Espèce, Race et Poids cohérents")
        sample = df.head(3)[["espece", "race", "poids"]].to_string(index=False)
        print(sample)
    
    if "age" in df.columns and "date_naissance" in df.columns:
        print("\n✓ Âge et Date de naissance cohérents")
        df_check = df.head(3).copy()
        current_year = datetime.now().year
        df_check["age_calculé"] = df_check["date_naissance"].apply(
            lambda x: current_year - int(x.split("-")[0])
        )
        print(df_check[["nom", "date_naissance", "age", "age_calculé"]].to_string(index=False))
    
    if "espece" in df.columns and "taille" in df.columns:
        print("\n✓ Espèce et Taille cohérentes")
        sample = df.head(3)[["nom", "espece", "taille", "poids"]].to_string(index=False)
        print(sample)
    
    print(f"\n✨ Génération terminée! Fichier sauvegardé: {out}\n")

if __name__ == "__main__":
    main()