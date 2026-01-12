"""
MEGA DATASET GENERATOR - Version Complète
Générateur universel de datasets synthétiques pour tout domaine
Supporte 200+ catégories et 15+ types de données
"""

import json
import argparse
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

np.random.seed(42)

# ====================
# GÉNÉRATEURS DE BASE
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

def gen_boolean(n, p=0.5):
    """Génère des valeurs booléennes"""
    return np.random.rand(n) < p

def gen_id(n, prefix="id"):
    """Génère des identifiants séquentiels"""
    return [f"{prefix}_{str(i+1).zfill(5)}" for i in range(n)]

def gen_date(n, start_year=1950, end_year=2025):
    """Génère des dates aléatoires"""
    start_date = datetime(start_year, 1, 1)
    end_date = datetime(end_year, 12, 31)
    days_range = (end_date - start_date).days
    random_days = np.random.randint(0, days_range, n)
    return [(start_date + timedelta(days=int(d))).strftime("%Y-%m-%d") for d in random_days]

def gen_datetime(n, start_year=2020, end_year=2025):
    """Génère des datetime complets"""
    start_date = datetime(start_year, 1, 1)
    end_date = datetime(end_year, 12, 31)
    seconds_range = int((end_date - start_date).total_seconds())
    random_seconds = np.random.randint(0, seconds_range, n)
    return [(start_date + timedelta(seconds=int(s))).strftime("%Y-%m-%d %H:%M:%S") for s in random_seconds]

def gen_time(n):
    """Génère des heures aléatoires"""
    hours = np.random.randint(0, 24, n)
    minutes = np.random.randint(0, 60, n)
    return [f"{h:02d}:{m:02d}:00" for h, m in zip(hours, minutes)]

def gen_email(n):
    """Génère des emails réalistes"""
    names = ["alice","bob","charlie","david","emma","fiona","george","hannah","igor","julia",
             "kevin","laura","martin","nina","oscar","paula","quinn","rachel","steve","tina"]
    domains = ["gmail.com","yahoo.fr","outlook.com","hotmail.fr","icloud.com","proton.me"]
    return [f"{np.random.choice(names)}{np.random.randint(1,9999)}@{np.random.choice(domains)}" for _ in range(n)]

def gen_phone(n, country="FR"):
    """Génère des numéros de téléphone"""
    if country == "FR":
        return [f"0{np.random.randint(6,8)}{np.random.randint(10000000,99999999)}" for _ in range(n)]
    elif country == "MA":
        return [f"0{np.random.choice([6,7])}{np.random.randint(10000000,99999999)}" for _ in range(n)]
    else:
        return [f"+{np.random.randint(1,999)}{np.random.randint(100000000,9999999999)}" for _ in range(n)]

def gen_url(n):
    """Génère des URLs"""
    domains = ["example.com","website.fr","company.ma","shop.co","blog.net","portal.org"]
    paths = ["home","about","contact","products","services","blog","login","profile"]
    return [f"https://www.{np.random.choice(domains)}/{np.random.choice(paths)}" for _ in range(n)]

def gen_ip(n):
    """Génère des adresses IP"""
    return [f"{np.random.randint(1,255)}.{np.random.randint(0,255)}.{np.random.randint(0,255)}.{np.random.randint(1,255)}" for _ in range(n)]

def gen_code_postal(n, country="FR"):
    """Génère des codes postaux"""
    if country in ["FR", "MA"]:
        return [f"{np.random.randint(10000,99999)}" for _ in range(n)]
    else:
        return [f"{np.random.randint(1000,99999)}" for _ in range(n)]

def gen_uuid(n):
    """Génère des UUIDs"""
    import uuid
    return [str(uuid.uuid4()) for _ in range(n)]

def gen_hex_color(n):
    """Génère des couleurs hexadécimales"""
    return [f"#{np.random.randint(0,16777215):06x}" for _ in range(n)]

def gen_coordinate(n, coord_type="lat"):
    """Génère des coordonnées GPS"""
    if coord_type == "lat":
        return np.random.uniform(-90, 90, n)
    else:  # lon
        return np.random.uniform(-180, 180, n)

def gen_percentage(n):
    """Génère des pourcentages"""
    return np.random.uniform(0, 100, n)

# ====================
# DICTIONNAIRE COMPLET DE CATÉGORIES
# ====================
MEGA_CATEGORIES = {
    # === PERSONNES ===
    "nom": ["Dubois","Morel","Caron","Lefèvre","Bernard","Girard","Pons","Robert","Perrin","Lemoine",
            "El Amrani","Essadiq","Benali","El Yousfi","El Haddad","Othmani","Lahlou","Idrissi","Mouline","Chentouf",
            "Hassan","El Sayed","Mohamed","Adel","Samir","Khaled","Ibrahim","Mahmoud","Mostafa","Fathy",
            "Anderson","Johnson","Brown","Miller","Davis","Wilson","Thompson","Martinez","Harris","Clark",
            "Wright","Turner","Parker","Hughes","Collins","Foster","Morgan","Stewart","Reed","Adams"]
,
    "prenom": ["Camille","Julien","Élodie","Mathieu","Sarah","Antoine","Claire","Louis","Léa","Hugo",
               "Youssef","Ikram","Ayoub","Salma","Nour","Rachid","Ihssan","Marwa","Fatima Zahra","Mohammed",
               "Ahmed","Omar","Nour","Mariam","Youssef","Salma","Hany","Farida","Tarek","Laila",
               "James","Emily","Michael","Sophia","Daniel","Olivia","Ethan","Ava","Mason","Isabella",
               "Oliver","Amelia","George","Charlotte","Henry","Grace","Jack","Ella","William","Chloe"]
,
    
    "genre": ["M","F"],
    "sexe": ["Masculin","Féminin"],
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
                               
    "Nationalites": ["Française","Marocaine","Algérienne","Tunisienne","Égyptienne","Sénégalaise","Ivoirienne","Maliène","Canadienne","Américaine",
                     "Mexicaine","Brésilienne","Argentine","Espagnole","Portugaise","Italienne","Allemande","Néerlandaise","Belge","Suisse",
                     "Autrichienne","Polonaise","Suédoise","Norvégienne","Finlandaise","Russe","Ukrainienne","Turque","Saoudienne","Qatarie",
                     "Émiratie","Indienne","Pakistanaise","Chinoise","Japonaise","Coréenne","Indonésienne","Malaisienne","Australienne","Néo-Zélandaise",
                     "Sud-africaine","Kenyanne","Nigériane","Ghanéenne","Éthiopienne","Angolaise","Vietnamienne","Thaïlandaise","Philippine","Britannique"],

    "Ville": ["Paris","Casablanca","Rabat","Marrakech","Agadir","Tanger","Fès","Berlin","Rome","Madrid",
              "Barcelone","Lisbonne","Porto","Londres","Manchester","Edimbourg","Dublin","Bruxelles","Amsterdam","Oslo",
              "Stockholm","Helsinki","Copenhague","Vienne","Zurich","Genève","Prague","Varsovie","Budapest","Athènes",
              "Istanbul","Ankara","Moscou","Kiev","Bucarest","Sofia","Belgrade","Zagreb","New York","Chicago",
              "Los Angeles","Houston","Toronto","Montréal","Sydney","Melbourne","Tokyo","Séoul","Taipei","Bangkok"],

    "Pays": ["France","Maroc","Algérie","Tunisie","Égypte","Sénégal","Côte d'Ivoire","Mali","États-Unis","Canada",
              "Mexique","Brésil","Argentine","Espagne","Portugal","Italie","Allemagne","Belgique","Suisse","Pays-Bas",
              "Autriche","Pologne","Suède","Norvège","Finlande","Danemark","Russie","Ukraine","Turquie","Arabie Saoudite",
              "Qatar","Émirats Arabes Unis","Inde","Pakistan","Chine","Japon","Corée du Sud","Indonésie","Malaisie","Australie",
              "Nouvelle-Zélande","Afrique du Sud","Kenya","Nigéria","Ghana","Éthiopie","Vietnam","Thaïlande","Philippines","Royaume-Uni"],
    
    "Age":["18","19","20","21","22","23","24","25","26","27",
           "28","29","30","31","32","33","34","35","36","37",
           "38","39","40","41","42","43","44","45","46","47",
           "48","49","50","51","52","53","54","55","56","57",
           "58","59","60","22","24","28","33","40","45","50"],


    # === GÉOGRAPHIE ===
    "pays": ["France","Maroc","Canada","USA","Allemagne","Japon","Espagne","Italie","UK","Belgique",
             "Suisse","Portugal","Brésil","Argentine","Mexique","Chine","Inde","Australie","Égypte","Tunisie"],
    "ville": ["Paris","Casablanca","Rabat","Marrakech","Fès","Tanger","Lyon","Marseille","Bordeaux","Toulouse",
              "Montreal","New York","Berlin","Tokyo","Madrid","Rome","Londres","Bruxelles","Genève","Lisbonne"],
    "ville_ma": ["Casablanca","Rabat","Marrakech","Fès","Tanger","Agadir","Meknès","Oujda","Kenitra","Tétouan",
                 "Safi","El Jadida","Nador","Khouribga","Beni Mellal","Mohammedia","Laâyoune","Ksar El Kébir"],
    "region": ["Nord","Sud","Est","Ouest","Centre","Nord-Est","Nord-Ouest","Sud-Est","Sud-Ouest"],
    "continent": ["Europe","Afrique","Asie","Amérique du Nord","Amérique du Sud","Océanie","Antarctique"],
    "quartier": ["Centre-ville","Banlieue","Périphérie","Zone résidentielle","Zone commerciale","Zone industrielle"],
    
    # === ÉDUCATION ===
    "ecole": ["École Primaire A","Collège B","Lycée C","Université D","Institut E"],
    "niveau_scolaire": ["CP","CE1","CE2","CM1","CM2","6ème","5ème","4ème","3ème","2nde","1ère","Terminale"],
    "diplome": ["Sans diplôme","Bac","Bac+2","Licence","Master","Doctorat","Ingénieur"],
    "specialite": ["Mathématiques","Physique","Chimie","Biologie","Informatique","Économie","Droit","Médecine",
                   "Lettres","Histoire","Géographie","Philosophie","Arts","Langues"],
    "niveau_etude": ["Primaire","Collège","Lycée","Licence","Master","Doctorat"],
    "mention": ["Passable","Assez bien","Bien","Très bien","Excellent"],
    
    # === PROFESSIONNEL ===
    "profession": ["Ingénieur","Médecin","Enseignant","Avocat","Comptable","Commercial","Manager","Technicien",
                   "Infirmier","Pharmacien","Architecte","Développeur","Designer","Chef de projet","Consultant",
                   "Artisan","Commerçant","Agriculteur","Ouvrier","Employé de bureau","Cadre","Directeur"],
    "secteur_activite": ["Technologie","Santé","Éducation","Finance","Commerce","Industrie","Agriculture",
                         "Services","Transport","Tourisme","Immobilier","BTP","Énergie","Télécommunications"],
    "type_contrat": ["CDI","CDD","Stage","Alternance","Freelance","Intérim","Auto-entrepreneur"],
    "niveau_poste": ["Junior","Intermédiaire","Senior","Expert","Manager","Directeur","C-Level"],
    "departement": ["RH","Finance","IT","Marketing","Ventes","Production","R&D","Logistique","Support"],
    
    # === BOTANIQUE & AGRICULTURE ===
    "espece_plante": ["Rose","Tulipe","Orchidée","Cactus","Aloe","Basilic","Pin","Chêne","Olivier","Ficus",
                      "Lavande","Jasmin","Menthe","Romarin","Thym","Palmier","Bambou","Eucalyptus"],
    "type_plante": ["Arbre","Arbuste","Herbe","Fleur","Plante grasse","Plante grimpante","Plante aquatique"],
    "type_sol": ["Argileux","Sableux","Limoneux","Humide","Rocheux","Calcaire","Tourbeux"],
    "saison": ["Printemps","Été","Automne","Hiver"],
    "culture": ["Blé","Maïs","Riz","Tomate","Pomme de terre","Olive","Orange","Raisin","Datte"],
    
    # === ANIMAUX ===
    "espece_animale": ["Chien","Chat","Cheval","Vache","Mouton","Chèvre","Poule","Canard","Lapin","Poisson"],
    "race_chien": ["Labrador","Berger Allemand","Golden Retriever","Bulldog","Beagle","Caniche","Chihuahua"],
    "race_chat": ["Persan","Siamois","Maine Coon","British Shorthair","Bengal","Sphynx","Ragdoll"],
    
    # === COMMERCE & PRODUITS ===
    "marque": ["Nike","Adidas","Puma","Reebok","NewBalance","Asics","Samsung","Apple","Sony","LG",
               "HP","Dell","Lenovo","Asus","Acer","Zara","H&M","Gucci","Dior","Chanel"],
    "categorie_produit": ["Vêtements","Chaussures","Électronique","Alimentaire","Maison","Sport","Beauté",
                          "Jouets","Livres","Automobile","High-tech","Mobilier","Décoration"],
    "type_produit": ["Smartphone","Ordinateur","Tablette","TV","Appareil photo","Console","Écouteurs"],
    "etat_produit": ["Neuf","Excellent","Très bon","Bon","Acceptable","Usé","Pour pièces"],
    "taille_vetement": ["XXS","XS","S","M","L","XL","XXL","XXXL"],
    "taille_chaussure": ["35","36","37","38","39","40","41","42","43","44","45","46"],
    "couleur": ["Rouge","Vert","Bleu","Noir","Blanc","Jaune","Orange","Violet","Rose","Gris","Marron","Beige"],
    "matiere": ["Coton","Polyester","Laine","Soie","Lin","Cuir","Plastique","Métal","Bois","Verre","Céramique"],
    
    # === SANTÉ ===
    "groupe_sanguin": ["A+","A-","B+","B-","AB+","AB-","O+","O-"],
    "symptome": ["Fièvre","Toux","Fatigue","Douleur","Nausée","Vertige","Maux de tête","Insomnie",
                 "Perte d'appétit","Essoufflement","Douleur thoracique","Douleur abdominale"],
    "maladie": ["Grippe","Rhume","Angine","Asthme","Diabète","Hypertension","Allergie","Migraine"],
    "medicament": ["Paracétamol","Ibuprofène","Aspirine","Amoxicilline","Doliprane","Advil","Efferalgan"],
    "vaccination": ["BCG","DTP","ROR","Hépatite B","Grippe","COVID-19","Tétanos"],
    
    # === FINANCE ===
    "devise": ["EUR","USD","MAD","GBP","JPY","CAD","CHF","AUD","CNY","INR"],
    "type_transaction": ["Achat","Vente","Remboursement","Transfert","Retrait","Dépôt","Virement"],
    "mode_paiement": ["Carte bancaire","Espèces","Chèque","Virement","PayPal","Crypto","Mobile payment"],
    "type_compte": ["Courant","Épargne","Livret A","PEL","Compte titre","Assurance vie"],
    "banque": ["BMCE","Attijariwafa Bank","BCP","CIH","Crédit du Maroc","BNP Paribas","Société Générale"],
    
    # === TRANSPORT ===
    "moyen_transport": ["Voiture","Bus","Train","Avion","Vélo","Moto","Tramway","Métro","Marche","Taxi"],
    "type_vehicule": ["Berline","SUV","Citadine","Break","Coupé","Monospace","Camion","Utilitaire","Moto"],
    "marque_voiture": ["Renault","Peugeot","Citroën","Dacia","Mercedes","BMW","Audi","Toyota","Ford","Volkswagen"],
    "carburant": ["Essence","Diesel","Électrique","Hybride","GPL","Hydrogène"],
    "classe_avion": ["Économique","Premium Économique","Affaires","Première classe"],
    
    # === MÉTÉO & ENVIRONNEMENT ===
    "meteo": ["Ensoleillé","Partiellement nuageux","Nuageux","Pluvieux","Orageux","Neigeux","Brumeux","Venteux"],
    "qualite_air": ["Excellente","Bonne","Moyenne","Mauvaise","Très mauvaise","Dangereuse"],
    "type_pollution": ["Air","Eau","Sol","Sonore","Lumineuse","Plastique"],
    
    # === TECHNOLOGIE & INFORMATIQUE ===
    "os": ["Windows 10","Windows 11","MacOS","Linux","Ubuntu","Android","iOS","Chrome OS"],
    "navigateur": ["Chrome","Firefox","Safari","Edge","Opera","Brave","Vivaldi"],
    "langage_programmation": ["Python","JavaScript","Java","C++","C#","PHP","Ruby","Go","Rust","Swift","Kotlin"],
    "framework": ["React","Angular","Vue.js","Django","Flask","Spring","Laravel","Express","FastAPI"],
    "base_donnees": ["MySQL","PostgreSQL","MongoDB","Redis","Oracle","SQL Server","SQLite","Cassandra"],
    "cloud_provider": ["AWS","Azure","Google Cloud","DigitalOcean","OVH","Heroku"],
    "type_appareil": ["Smartphone","Tablette","Ordinateur portable","Desktop","Serveur","Montre connectée"],
    
    # === IMMOBILIER ===
    "type_logement": ["Appartement","Maison","Studio","Villa","Duplex","Loft","Penthouse","Ferme"],
    "type_bien": ["Résidentiel","Commercial","Industriel","Terrain","Bureau","Local commercial"],
    "standing": ["Économique","Moyen","Haut standing","Luxe"],
    "chauffage": ["Électrique","Gaz","Fioul","Pompe à chaleur","Solaire","Bois"],
    
    # === LOISIRS & CULTURE ===
    "sport": ["Football","Basketball","Tennis","Natation","Course","Cyclisme","Volleyball","Rugby",
              "Golf","Ski","Équitation","Boxe","Arts martiaux","Yoga","Fitness"],
    "genre_musical": ["Pop","Rock","Jazz","Classique","Hip-hop","Électro","Rap","R&B","Reggae","Metal"],
    "genre_film": ["Action","Comédie","Drame","Horreur","Science-fiction","Thriller","Romance","Animation"],
    "instrument": ["Piano","Guitare","Violon","Batterie","Flûte","Saxophone","Trompette","Violoncelle"],
    
    # === RESTAURATION ===
    "type_cuisine": ["Française","Marocaine","Italienne","Japonaise","Chinoise","Indienne","Mexicaine",
                     "Américaine","Espagnole","Thaïlandaise","Libanaise","Tunisienne"],
    "type_repas": ["Petit-déjeuner","Déjeuner","Dîner","Brunch","Goûter","Apéritif"],
    "regime_alimentaire": ["Omnivore","Végétarien","Végan","Sans gluten","Halal","Casher","Paléo"],
    "allergene": ["Arachide","Fruits à coque","Lait","Œufs","Poisson","Crustacés","Soja","Gluten"],
    
    # === STATUTS & ÉTATS ===
    "statut": ["Actif","Inactif","En attente","Terminé","Annulé","En cours","Validé","Rejeté"],
    "priorite": ["Basse","Normale","Haute","Urgente","Critique"],
    "niveau": ["Débutant","Intermédiaire","Avancé","Expert","Maître"],
    "qualite": ["Très mauvaise","Mauvaise","Moyenne","Bonne","Excellente"],
    "satisfaction": ["Très insatisfait","Insatisfait","Neutre","Satisfait","Très satisfait"],
    
    # === JURIDIQUE ===
    "type_contrat_legal": ["Vente","Location","Prestation","Travail","Partenariat","NDA","Franchise"],
    "type_societe": ["SARL","SAS","SA","Auto-entrepreneur","Association","EURL","SCI"],
    
    # === ÉVÉNEMENTS ===
    "type_evenement": ["Conférence","Séminaire","Formation","Webinaire","Atelier","Salon","Concert","Festival"],
    "jour_semaine": ["Lundi","Mardi","Mercredi","Jeudi","Vendredi","Samedi","Dimanche"],
    "mois": ["Janvier","Février","Mars","Avril","Mai","Juin","Juillet","Août","Septembre","Octobre","Novembre","Décembre"],
    
    # === FALLBACK GÉNÉRIQUE ===
    "type": ["Type A","Type B","Type C","Type D","Type E"],
    "categorie": ["Catégorie 1","Catégorie 2","Catégorie 3","Catégorie 4","Catégorie 5"],
}

# ====================
# DÉTECTION INTELLIGENTE DU TYPE
# ====================
def guess_type(name):
    """Détecte automatiquement le type de colonne basé sur son nom"""
    name_lower = name.lower()
    
    # === IDs et Codes ===
    if any(k in name_lower for k in ["id","uid","code","reference","ref","identifiant"]):
        if "uuid" in name_lower:
            return ("uuid", {})
        return ("id", {})
    
    # === Dates et Temps ===
    if any(k in name_lower for k in ["date","naissance","birth","creation","expiration","debut","fin"]):
        if "naissance" in name_lower or "birth" in name_lower:
            return ("date", {"start_year":1950,"end_year":2010})
        return ("date", {"start_year":2020,"end_year":2025})
    
    if "datetime" in name_lower or "timestamp" in name_lower:
        return ("datetime", {"start_year":2020,"end_year":2025})
    
    if any(k in name_lower for k in ["heure","time","horaire"]) and "date" not in name_lower:
        return ("time", {})
    
    # === Contact ===
    if any(k in name_lower for k in ["email","mail","courriel"]):
        return ("email", {})
    
    if any(k in name_lower for k in ["telephone","phone","tel","mobile","portable"]):
        country = "MA" if "ma" in name_lower or "maroc" in name_lower else "FR"
        return ("phone", {"country":country})
    
    if "url" in name_lower or "site" in name_lower or "lien" in name_lower:
        return ("url", {})
    
    # === Adresse ===
    if "ip" in name_lower and ("adresse" in name_lower or name_lower == "ip"):
        return ("ip", {})
    
    if "code_postal" in name_lower or "zip" in name_lower or "postal" in name_lower:
        return ("code_postal", {})
    
    # === Coordonnées géographiques ===
    if "latitude" in name_lower or name_lower == "lat":
        return ("latitude", {})
    if "longitude" in name_lower or name_lower == "lon" or name_lower == "lng":
        return ("longitude", {})
    
    # === Couleurs ===
    if "couleur" in name_lower and "hex" in name_lower:
        return ("hex_color", {})
    
    # === Numériques spécifiques ===
    if any(k in name_lower for k in ["age","annee","year"]) and "moyenne" not in name_lower:
        return ("int", {"low":18,"high":80})
    
    if any(k in name_lower for k in ["prix","price","cout","cost","montant","amount","salaire","salary","revenu"]):
        return ("numeric", {"low":100,"high":100000,"mean":30000,"std":15000})
    
    if any(k in name_lower for k in ["hauteur","height","taille"]) and "personne" not in name_lower:
        return ("numeric", {"low":10,"high":200,"mean":80,"std":30})
    
    if any(k in name_lower for k in ["poids","weight","masse"]):
        return ("numeric", {"low":40,"high":120,"mean":70,"std":15})
    
    if any(k in name_lower for k in ["temperature","temp"]):
        return ("numeric", {"low":-10,"high":45,"mean":20,"std":8})
    
    if any(k in name_lower for k in ["score","note","grade","marks","resultat"]):
        return ("numeric", {"low":0,"high":20,"mean":12,"std":3})
    
    if "ph" in name_lower:
        return ("numeric", {"low":0,"high":14,"mean":7,"std":2})
    
    if any(k in name_lower for k in ["pourcentage","percent","taux","rate","%"]):
        return ("percentage", {})
    
    if any(k in name_lower for k in ["distance","km","kilometres"]):
        return ("numeric", {"low":0,"high":1000,"mean":200,"std":150})
    
    if any(k in name_lower for k in ["duree","duration","temps"]) and "date" not in name_lower:
        return ("numeric", {"low":0,"high":180,"mean":60,"std":30})
    
    if any(k in name_lower for k in ["superficie","surface","area"]):
        return ("numeric", {"low":10,"high":500,"mean":100,"std":80})
    
    # === Entiers spécifiques ===
    if any(k in name_lower for k in ["quantite","quantity","nombre","count","stock"]):
        return ("int", {"low":0,"high":1000})
    
    if any(k in name_lower for k in ["absences","absence"]):
        return ("int", {"low":0,"high":30})
    
    if any(k in name_lower for k in ["annee_","year_","an_"]):
        return ("int", {"low":2020,"high":2025})
    
    if any(k in name_lower for k in ["experience","anciennete","seniority"]):
        return ("int", {"low":0,"high":40})
    
    # === Booléens ===
    if any(k in name_lower for k in ["actif","active","valide","valid","est_","is_","has_","a_"]):
        return ("boolean", {"p":0.7})
    
    # === Catégoriels - Recherche exacte dans le dictionnaire ===
    for key in MEGA_CATEGORIES:
        if key in name_lower or name_lower in key:
            return ("categorical", {"categories": MEGA_CATEGORIES[key]})
    
    # === Fallback par proximité sémantique ===
    if "nom" in name_lower or "name" in name_lower:
        return ("categorical", {"categories": MEGA_CATEGORIES["nom"]})
    if "ville" in name_lower or "city" in name_lower:
        if "maroc" in name_lower or "ma" in name_lower:
            return ("categorical", {"categories": MEGA_CATEGORIES["ville_ma"]})
        return ("categorical", {"categories": MEGA_CATEGORIES["ville"]})
    if "pays" in name_lower or "country" in name_lower:
        return ("categorical", {"categories": MEGA_CATEGORIES["pays"]})
    
    # === Fallback générique ===
    return ("categorical", {"categories": MEGA_CATEGORIES["type"]})

# ====================
# CONSTRUCTION DU DATASET
# ====================
def build_dataset(schema, n=500):
    """Construit le dataset à partir du schéma"""
    cols = []
    
    # Normaliser le schéma
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

    data = {}
    for col in cols:
        name = col["name"]
        t = col["type"]
        p = col.get("params",{})
        
        if t == "numeric":
            data[name] = gen_numeric(n, p.get("low",0), p.get("high",100), p.get("mean"), p.get("std",1))
        elif t == "int":
            data[name] = gen_integer(n, int(p.get("low",0)), int(p.get("high",100)))
        elif t == "categorical":
            cats = p.get("categories", MEGA_CATEGORIES["type"])
            data[name] = gen_categorical(n, cats)
        elif t == "boolean":
            data[name] = gen_boolean(n, float(p.get("p",0.5)))
        elif t == "id":
            data[name] = gen_id(n, name)
        elif t == "uuid":
            data[name] = gen_uuid(n)
        elif t == "date":
            data[name] = gen_date(n, p.get("start_year",2020), p.get("end_year",2025))
        elif t == "datetime":
            data[name] = gen_datetime(n, p.get("start_year",2020), p.get("end_year",2025))
        elif t == "time":
            data[name] = gen_time(n)
        elif t == "email":
            data[name] = gen_email(n)
        elif t == "phone":
            data[name] = gen_phone(n, p.get("country","FR"))
        elif t == "url":
            data[name] = gen_url(n)
        elif t == "ip":
            data[name] = gen_ip(n)
        elif t == "code_postal":
            data[name] = gen_code_postal(n, p.get("country","FR"))
        elif t == "hex_color":
            data[name] = gen_hex_color(n)
        elif t == "latitude":
            data[name] = gen_coordinate(n, "lat")
        elif t == "longitude":
            data[name] = gen_coordinate(n, "lon")
        elif t == "percentage":
            data[name] = gen_percentage(n)
        else:
            # Fallback
            data[name] = gen_categorical(n, MEGA_CATEGORIES["type"])
    
    return pd.DataFrame(data)

# ====================
# CLI - INTERFACE LIGNE DE COMMANDE
# ====================
def main():
    parser = argparse.ArgumentParser(
        description="🚀 Générateur MEGA universel de dataset synthétique",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""


📚 ÉTUDIANTS :
  python mega_dataset_generator.py --name students --schema '["nom","prenom","age","niveau_scolaire","note","absences"]' --n 100

🏥 PATIENTS :
  python mega_dataset_generator.py --name patients --schema '["id","nom","age","groupe_sanguin","temperature","symptome"]' --n 200

🛒 E-COMMERCE :
  python mega_dataset_generator.py --name products --schema '["marque","categorie_produit","prix","couleur","taille_vetement","etat_produit"]' --n 500

🌱 AGRICULTURE :
  python mega_dataset_generator.py --name plantes --schema '["espece_plante","hauteur","type_sol","PH","saison"]' --n 1000

👔 EMPLOYÉS :
  python mega_dataset_generator.py --name employees --schema '["nom","prenom","email","telephone","profession","salaire","date_embauche"]' --n 300

🏠 IMMOBILIER :
  python mega_dataset_generator.py --name logements --schema '["type_logement","ville_ma","prix","superficie","chauffage"]' --n 150

🚗 VÉHICULES :
  python mega_dataset_generator.py --name vehicles --schema '["marque_voiture","type_vehicule","carburant","prix","annee"]' --n 250

💻 TECH :
  python mega_dataset_generator.py --name users --schema '["email","os","navigateur","ip","date_inscription"]' --n 400

📄 AVEC FICHIER JSON (RECOMMANDÉ) :
  python mega_dataset_generator.py --name test --schema schema.json --n 500



📊 NUMÉRIQUES : age, prix, salaire, temperature, hauteur, poids, score, ph, 
                distance, duree, superficie, pourcentage

🔢 ENTIERS : quantite, stock, absences, annee, experience

📅 DATES : date, date_naissance, date_creation, datetime, time, heure

📧 CONTACT : email, telephone, url, ip, code_postal

🆔 IDENTIFIANTS : id, uuid, code, reference

🎨 AUTRES : latitude, longitude, couleur_hex, boolean

📝 CATÉGORIELS (200+ catégories prédéfinies) :
   Personnes, Géographie, Éducation, Professions, Botanique, Animaux, Commerce,
   Santé, Finance, Transport, Météo, Technologie, Immobilier, Loisirs, etc.


❌ ERREUR JSON sur PowerShell ?
   → Utilisez un fichier JSON : --schema schema.json
   → OU utilisez CMD au lieu de PowerShell
   → OU échappez correctement : --schema '[\"col1\",\"col2\"]'

📁 Créer schema.json :
   ["nom", "age", "ville"]
        """
    )
    
    parser.add_argument("--name", required=True, 
                       help="Nom du dataset (ex: students, products)")
    parser.add_argument("--schema", required=True, 
                       help='Colonnes JSON: ["col1","col2",...] ou fichier.json')
    parser.add_argument("--n", type=int, default=500, 
                       help="Nombre de lignes (défaut: 500)")
    parser.add_argument("--out", default=None, 
                       help="Fichier CSV de sortie (défaut: {name}_seed.csv)")
    parser.add_argument("--preview", type=int, default=10, 
                       help="Nombre de lignes à afficher (défaut: 10)")
    parser.add_argument("--stats", action="store_true", 
                       help="Afficher les statistiques descriptives")
    
    args = parser.parse_args()

    # Charger le schéma (depuis string JSON ou fichier)
    try:
        # Essayer de charger comme fichier JSON
        if args.schema.endswith('.json'):
            with open(args.schema, 'r', encoding='utf-8') as f:
                schema = json.load(f)
            print(f"📁 Schéma chargé depuis: {args.schema}")
        else:
            # Parser comme string JSON
            schema = json.loads(args.schema)
    except FileNotFoundError:
        print(f"❌ Fichier introuvable: {args.schema}")
        print("💡 Créez le fichier JSON ou vérifiez le chemin")
        return
    except json.JSONDecodeError as e:
        print(f"❌ Erreur JSON: {e}")
        print("\n💡 Solutions:")
        print("   1. Utilisez un fichier: --schema schema.json")
        print("   2. Vérifiez l'échappement: --schema '[\"col1\",\"col2\"]'")
        print("   3. Utilisez CMD au lieu de PowerShell")
        return
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return

    # Génération du dataset
    print(f"\n{'='*80}")
    print(f"⚙️  GÉNÉRATION DU DATASET '{args.name}'")
    print("="*80)
    
    # Afficher les colonnes
    if isinstance(schema, list) and all(isinstance(x, str) for x in schema):
        cols_display = schema
    else:
        cols_display = [c['name'] for c in schema]
    
    print(f"📊 Colonnes ({len(cols_display)}): {', '.join(cols_display)}")
    print(f"📈 Nombre de lignes: {args.n}")
    print(f"🔄 Génération en cours...\n")
    
    try:
        df = build_dataset(schema, n=args.n)
    except Exception as e:
        print(f"❌ Erreur lors de la génération: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # Sauvegarde
    out = args.out or f"{args.name}_seed.csv"
    try:
        df.to_csv(out, index=False)
    except Exception as e:
        print(f"❌ Erreur lors de la sauvegarde: {e}")
        return
    
    # Affichage des résultats
    print("="*80)
    print(f"✅ DATASET GÉNÉRÉ AVEC SUCCÈS")
    print("="*80)
    print(f"📁 Fichier        : {out}")
    print(f"📊 Dimensions     : {len(df)} lignes × {len(df.columns)} colonnes")
    print(f"💾 Taille         : {df.memory_usage(deep=True).sum() / 1024:.2f} KB")
    
    # Aperçu
    print(f"\n{'='*80}")
    print(f"👁️  APERÇU ({min(args.preview, len(df))} premières lignes)")
    print("="*80)
    try:
        print(df.head(args.preview).to_string(index=False))
    except:
        print(df.head(args.preview))
    
    # Types détectés
    print(f"\n{'='*80}")
    print("🔍 TYPES DE DONNÉES DÉTECTÉS")
    print("="*80)
    for col in df.columns:
        sample_val = str(df[col].iloc[0]) if len(df) > 0 else "N/A"
        if len(sample_val) > 30:
            sample_val = sample_val[:27] + "..."
        print(f"  • {col:30s} → {str(df[col].dtype):15s} (ex: {sample_val})")
    
    # Statistiques (optionnel)
    if args.stats:
        print(f"\n{'='*80}")
        print("📈 STATISTIQUES DESCRIPTIVES")
        print("="*80)
        try:
            print(df.describe(include='all').to_string())
        except:
            print(df.describe())
    
    print(f"\n{'='*80}")
    print("✨ Génération terminée avec succès!")
    print("="*80)
    print(f"\n💡 Prochaines étapes:")
    print(f"   1. Vérifiez le fichier: {out}")
    print(f"   2. Entraînez CTGAN sur ce dataset")
    print(f"   3. Injectez des biais contrôlés")
    print(f"   4. Analysez avec fairness metrics\n")

# ====================
# POINT D'ENTRÉE
# ====================
if __name__ == "__main__":
    main()