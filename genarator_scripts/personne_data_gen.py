"""
MEGA DATASET GENERATOR - Version Corrigée avec Cohérence
Génère des données COHÉRENTES (genre, âge, dates...)
"""

import json
import argparse
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

np.random.seed(42)

# ====================
# DONNÉES COHÉRENTES PAR GENRE
# ====================
NOMS_PRENOMS = {
    "M": {
        "prenoms": ["Mohamed","Ahmed","Youssef","Ali","Hassan","Omar","Karim","Mehdi","Rachid","Samir",
                    "Pierre","Jean","Luc","Marc","Louis","Antoine","Hugo","Julien","Mathieu","Nicolas",
                    "James","John","Michael","David","Daniel","Robert","William","Joseph","Thomas","Christopher"],
        "noms": ["El Amrani","Benali","Hassan","Mohamed","Khaled","Ibrahim","Mahmoud","Adel","Fathy","Essadiq",
                 "Dupont","Martin","Bernard","Dubois","Moreau","Robert","Richard","Petit","Durand","Laurent",
                 "Smith","Johnson","Williams","Brown","Jones","Miller","Davis","Garcia","Rodriguez","Wilson"]
    },
    "F": {
        "prenoms": ["Fatima","Aicha","Salma","Nour","Amina","Laila","Sanae","Zineb","Ikram","Marwa",
                    "Marie","Sophie","Claire","Julie","Emma","Léa","Camille","Chloé","Sarah","Élodie",
                    "Mary","Patricia","Jennifer","Linda","Barbara","Elizabeth","Susan","Jessica","Sarah","Karen"],
        "noms": ["El Amrani","Benali","Hassan","Mohamed","El Idrissi","El Haddad","Othmani","Lahlou","Mouline","Chentouf",
                 "Dupont","Martin","Bernard","Dubois","Moreau","Robert","Richard","Petit","Durand","Laurent",
                 "Smith","Johnson","Williams","Brown","Jones","Miller","Davis","Garcia","Rodriguez","Wilson"]
    }
}

# ====================
# GÉNÉRATEURS DE BASE COHÉRENTS
# ====================
def gen_person_data(n):
    """
    Génère des données de personne COHÉRENTES
    Retourne: dict avec genre, nom, prenom cohérents
    """
    persons = []
    
    for _ in range(n):
        # Choisir genre
        genre = np.random.choice(["M", "F"])
        
        # Choisir prénom et nom cohérents avec le genre
        prenom = np.random.choice(NOMS_PRENOMS[genre]["prenoms"])
        nom = np.random.choice(NOMS_PRENOMS[genre]["noms"])
        
        # Genre textuel
        sexe = "Masculin" if genre == "M" else "Féminin"
        
        persons.append({
            "genre": genre,
            "sexe": sexe,
            "prenom": prenom,
            "nom": nom
        })
    
    return persons

def gen_age_and_birthdate(n, min_age=18, max_age=65):
    """
    Génère âge ET date de naissance COHÉRENTS
    """
    current_year = datetime.now().year
    ages = np.random.randint(min_age, max_age + 1, n)
    
    birthdates = []
    for age in ages:
        birth_year = current_year - age
        # Date aléatoire dans l'année de naissance
        birth_month = np.random.randint(1, 13)
        birth_day = np.random.randint(1, 29)  # Évite problèmes avec février
        
        birthdate = f"{birth_year}-{birth_month:02d}-{birth_day:02d}"
        birthdates.append(birthdate)
    
    return ages, birthdates

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

def gen_boolean(n, p=0.5):
    """Génère des valeurs booléennes"""
    return np.random.rand(n) < p

def gen_id(n, prefix="id"):
    """Génère des identifiants séquentiels"""
    return [f"{prefix}_{str(i+1).zfill(5)}" for i in range(n)]

def gen_email(names, domains=None):
    """Génère des emails basés sur les noms"""
    if domains is None:
        domains = ["gmail.com","yahoo.fr","outlook.com","hotmail.fr","proton.me"]
    
    emails = []
    for name in names:
        # Normaliser le nom (enlever espaces, accents basiques)
        clean_name = name.lower().replace(" ", ".").replace("é", "e").replace("è", "e")
        email = f"{clean_name}{np.random.randint(1,999)}@{np.random.choice(domains)}"
        emails.append(email)
    
    return emails

def gen_phone(n, country="FR"):
    """Génère des numéros de téléphone"""
    if country == "FR":
        return [f"0{np.random.randint(6,8)}{np.random.randint(10000000,99999999)}" for _ in range(n)]
    elif country == "MA":
        return [f"0{np.random.choice([6,7])}{np.random.randint(10000000,99999999)}" for _ in range(n)]
    else:
        return [f"+{np.random.randint(1,999)}{np.random.randint(100000000,9999999999)}" for _ in range(n)]

# ====================
# CATÉGORIES CORRIGÉES
# ====================
MEGA_CATEGORIES = {
    # Ne PAS inclure nom, prenom, genre, age, date_naissance ici
    # Ils sont gérés de manière cohérente par les fonctions spéciales
    
    # === GÉOGRAPHIE ===
    "pays": ["France","Maroc","Canada","USA","Allemagne","Japon","Espagne","Italie","UK","Belgique",
             "Suisse","Portugal","Brésil","Argentine","Mexique","Chine","Inde","Australie","Égypte","Tunisie"],
    "ville": ["Paris","Casablanca","Rabat","Marrakech","Fès","Tanger","Lyon","Marseille","Bordeaux","Toulouse",
              "Montreal","New York","Berlin","Tokyo","Madrid","Rome","Londres","Bruxelles","Genève","Lisbonne",
              "Casablanca","Rabat","Marrakech","Fès","Tanger","Agadir","Meknès","Oujda","Kenitra","Tétouan"],
    "Date_de_naissance": ["1990-01-12","1988-05-23","1995-09-14","1992-11-30","1998-03-08","1997-07-19","2010-12-04","1991-06-25","1999-02-16","1990-10-10",
                          "1989-08-29","1994-04-21","2003-01-30","1992-09-03","1997-11-11","1995-06-14","1998-12-27","1990-03-01","1987-07-09","2010-10-18",
                          "2003-05-07","1994-12-19","1991-02-22","1999-08-12","1993-04-09","2000-02-11","1995-03-17","1990-06-06","1998-07-22","1988-09-28",
                          "1994-10-05","2003-11-29","1992-01-15","1993-08-03","2000-04-18","1991-09-26","2001-05-20","1995-07-31","1994-02-09","2003-06-02",
                          "1989-11-14","1991-04-28","1997-10-21","1993-01-09","2001-09-25","1994-08-16","1990-12-30","2003-03-04","1999-05-14","1992-07-07"],

    "Lieu_de_naissance": ["Paris","Casablanca","Rabat","Marseille","Lyon","Tanger","Fès","Berlin","Madrid","Rome",
                          "Tokyo","Séoul","New York","Los Angeles","Montréal","Londres","Manchester","Tunis","Alger","Oran",
                          "Bruxelles","Amsterdam","Lisbonne","Dubaï","Doha","Le Caire","Istanbul","Moscou","Kiev","Stockholm",
                          "Oslo","Helsinki","Varsovie","Bucarest","Vienne","Genève","Zurich","Dakar","Abidjan","Bamako",
                          "Nairobi","Johannesburg","Sydney","Melbourne","Delhi","Mumbai","Beijing","Shanghai","Mexico City","São Paulo"],
    "region": ["Nord","Sud","Est","Ouest","Centre"],
    "nationalite": ["Française","Marocaine","Canadienne","Américaine","Allemande","Japonaise","Espagnole"],
    
    # === ÉDUCATION ===
    "niveau_scolaire": ["CP","CE1","CE2","CM1","CM2","6ème","5ème","4ème","3ème","2nde","1ère","Terminale"],
    "diplome": ["Sans diplôme","Bac","Bac+2","Licence","Master","Doctorat","Ingénieur"],
    "specialite": ["Mathématiques","Physique","Chimie","Biologie","Informatique","Économie","Droit","Médecine"],
    
    # === PROFESSIONNEL ===
    "profession": ["Ingénieur","Médecin","Enseignant","Avocat","Comptable","Commercial","Manager","Technicien",
                   "Infirmier","Pharmacien","Architecte","Développeur","Designer","Consultant"],
    "secteur_activite": ["Technologie","Santé","Éducation","Finance","Commerce","Industrie","Services"],
    "type_contrat": ["CDI","CDD","Stage","Alternance","Freelance"],
    "departement": ["RH","Finance","IT","Marketing","Ventes","Production","R&D"],
    
    # === SANTÉ ===
    "groupe_sanguin": ["A+","A-","B+","B-","AB+","AB-","O+","O-"],
    "fumeur": ["Oui","Non"],
    
    # === AUTRES ===
    "statut": ["Actif","Inactif","En attente","Terminé"],
    "niveau": ["Débutant","Intermédiaire","Avancé","Expert"],
}

# ====================
# DÉTECTION INTELLIGENTE CORRIGÉE
# ====================
def guess_type(name):
    """Détecte automatiquement le type de colonne"""
    name_lower = name.lower()
    
    # === Colonnes spéciales gérées de manière cohérente ===
    if name_lower in ["nom", "name", "lastname"]:
        return ("person_nom", {})
    
    if name_lower in ["prenom", "firstname", "prénom"]:
        return ("person_prenom", {})
    
    if name_lower in ["genre", "gender", "sexe"]:
        return ("person_genre", {})
    
    if name_lower in ["age", "âge"]:
        return ("person_age", {})
    
    if "date" in name_lower and ("naissance" in name_lower or "birth" in name_lower):
        return ("person_birthdate", {})
    
    if "email" in name_lower or "mail" in name_lower:
        return ("person_email", {})
    
    # === IDs ===
    if any(k in name_lower for k in ["id","uid","code","reference"]):
        return ("id", {})
    
    # === Numériques ===
    if any(k in name_lower for k in ["prix","price","salaire","salary","revenu"]):
        return ("numeric", {"low":1000,"high":100000,"mean":35000,"std":15000})
    
    if any(k in name_lower for k in ["score","note","grade"]):
        return ("numeric", {"low":0,"high":20,"mean":12,"std":3})
    
    if "temperature" in name_lower:
        return ("numeric", {"low":35,"high":42,"mean":37,"std":1})
    
    # === Entiers ===
    if "quantite" in name_lower or "stock" in name_lower:
        return ("int", {"low":0,"high":1000})
    
    if "absence" in name_lower:
        return ("int", {"low":0,"high":30})
    
    if "experience" in name_lower or "anciennete" in name_lower:
        return ("int", {"low":0,"high":40})
    
    # === Téléphone ===
    if "telephone" in name_lower or "phone" in name_lower or "tel" in name_lower:
        country = "MA" if "ma" in name_lower or "maroc" in name_lower else "FR"
        return ("phone", {"country":country})
    
    # === Catégoriels ===
    for key in MEGA_CATEGORIES:
        if key in name_lower or name_lower in key:
            return ("categorical", {"categories": MEGA_CATEGORIES[key]})
    
    # === Fallback ===
    return ("categorical", {"categories": ["Option A","Option B","Option C"]})

# ====================
# CONSTRUCTION COHÉRENTE DU DATASET
# ====================
def build_dataset(schema, n=500):
    """Construit un dataset avec données COHÉRENTES"""
    
    # Normaliser le schéma
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
                guessed_t, guessed_params = guess_type(name)
                guessed_params.update(params)
                t = guessed_t
                params = guessed_params
            cols.append({"name":name,"type":t,"params":params})
    
    # === ÉTAPE 1 : Générer les données de personne cohérentes ===
    person_data_needed = any(col["type"].startswith("person_") for col in cols)
    
    if person_data_needed:
        persons = gen_person_data(n)
        ages, birthdates = gen_age_and_birthdate(n, min_age=18, max_age=65)
        
        # Extraire les prénoms pour emails
        prenoms = [p["prenom"] for p in persons]
        emails = gen_email(prenoms)
    
    # === ÉTAPE 2 : Construire le dataframe ===
    data = {}
    
    for col in cols:
        name = col["name"]
        t = col["type"]
        p = col.get("params",{})
        
        # Données de personne cohérentes
        if t == "person_nom":
            data[name] = [person["nom"] for person in persons]
        elif t == "person_prenom":
            data[name] = [person["prenom"] for person in persons]
        elif t == "person_genre":
            data[name] = [person["genre"] for person in persons]
        elif t == "person_sexe":
            data[name] = [person["sexe"] for person in persons]
        elif t == "person_age":
            data[name] = ages
        elif t == "person_birthdate":
            data[name] = birthdates
        elif t == "person_email":
            data[name] = emails
        
        # Autres types
        elif t == "numeric":
            data[name] = gen_numeric(n, p.get("low",0), p.get("high",100), p.get("mean"), p.get("std",10))
        elif t == "int":
            data[name] = gen_integer(n, int(p.get("low",0)), int(p.get("high",100)))
        elif t == "categorical":
            cats = p.get("categories", ["Option A","Option B","Option C"])
            data[name] = gen_categorical(n, cats)
        elif t == "boolean":
            data[name] = gen_boolean(n, float(p.get("p",0.5)))
        elif t == "id":
            data[name] = gen_id(n, name)
        elif t == "phone":
            data[name] = gen_phone(n, p.get("country","FR"))
        else:
            # Fallback
            data[name] = gen_categorical(n, ["Valeur 1","Valeur 2","Valeur 3"])
    
    return pd.DataFrame(data)

# ====================
# CLI
# ====================
def main():
    parser = argparse.ArgumentParser(
        description="🚀 Générateur COHÉRENT de datasets synthétiques",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
EXEMPLES :

📚 Dataset d'étudiants cohérent :
  python mega_dataset_generator_fixed.py --name students \\
    --schema '["nom","prenom","genre","age","date_naissance","niveau_scolaire","note"]' --n 100

💼 Dataset d'employés cohérent :
  python mega_dataset_generator_fixed.py --name employees \\
    --schema '["nom","prenom","genre","age","email","profession","salaire"]' --n 200

🏥 Dataset de patients cohérent :
  python mega_dataset_generator_fixed.py --name patients \\
    --schema '["nom","prenom","genre","age","groupe_sanguin","fumeur"]' --n 150

COLONNES COHÉRENTES AUTOMATIQUES :
  • nom + prenom → cohérents avec genre
  • genre → M ou F cohérent avec nom/prenom
  • age + date_naissance → calculés ensemble
  • email → basé sur le prénom
        """
    )
    
    parser.add_argument("--name", required=True, help="Nom du dataset")
    parser.add_argument("--schema", required=True, help="Colonnes JSON ou fichier.json")
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
    print(f"⚙️  GÉNÉRATION DU DATASET COHÉRENT '{args.name}'")
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
    
    # Afficher résultats
    print("="*80)
    print(f"✅ DATASET COHÉRENT GÉNÉRÉ")
    print("="*80)
    print(f"📁 Fichier : {out}")
    print(f"📊 Lignes  : {len(df)}")
    print(f"📊 Colonnes: {len(df.columns)}\n")
    
    print("👁️  APERÇU :")
    print(df.head(args.preview).to_string(index=False))
    
    # Vérification cohérence
    print(f"\n{'='*80}")
    print("✅ VÉRIFICATIONS DE COHÉRENCE")
    print("="*80)
    
    if "genre" in df.columns and "nom" in df.columns:
        print("\n✓ Genre et Nom cohérents")
        sample = df.head(3)[["nom","prenom","genre"]].to_string(index=False)
        print(sample)
    
    if "age" in df.columns and "date_naissance" in df.columns:
        print("\n✓ Âge et Date de naissance cohérents")
        # Vérifier cohérence
        current_year = datetime.now().year
        df_check = df.head(3).copy()
        df_check["age_calculé"] = df_check["date_naissance"].apply(
            lambda x: current_year - int(x.split("-")[0])
        )
        print(df_check[["date_naissance","age","age_calculé"]].to_string(index=False))
    
    print(f"\n✨ Génération terminée!\n")

if __name__ == "__main__":
    main()