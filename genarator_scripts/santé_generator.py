"""
GÉNÉRATEUR DE DONNÉES DE SANTÉ
Génère des données médicales et de santé réalistes et cohérentes
"""

import json
import argparse
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

np.random.seed(42)

# ====================
# DONNÉES PATIENTS
# ====================

PRENOMS_H = ["Mohammed", "Ahmed", "Ali", "Hassan", "Youssef", "Omar", "Khalid", "Amine", "Mehdi", "Karim",
             "Jean", "Pierre", "Michel", "David", "Thomas", "Nicolas", "Alexandre", "Julien", "Antoine", "Lucas"]
PRENOMS_F = ["Fatima", "Aisha", "Khadija", "Amina", "Nour", "Sara", "Salma", "Yasmine", "Leila", "Zineb",
             "Marie", "Sophie", "Camille", "Emma", "Julie", "Laura", "Chloe", "Manon", "Léa", "Clara"]
NOMS = ["Alami", "Benali", "Idrissi", "Hassani", "Khalil", "Mansouri", "Tazi", "Fassi", "Filali", "Kadiri",
        "Martin", "Bernard", "Dubois", "Thomas", "Robert", "Richard", "Petit", "Durand", "Leroy", "Moreau"]

SEXES = ["M", "F"]
GROUPES_SANGUINS = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]
VILLES = ["Casablanca", "Rabat", "Marrakech", "Fès", "Tanger", "Agadir", "Meknès", "Oujda", "Kenitra", "Tétouan",
          "Paris", "Lyon", "Marseille", "Toulouse", "Nice", "Nantes", "Bordeaux", "Lille", "Strasbourg", "Rennes"]

# ====================
# DONNÉES MÉDICALES
# ====================

MALADIES_CHRONIQUES = [
    "Diabète Type 1", "Diabète Type 2", "Hypertension", "Asthme", "BPCO", 
    "Insuffisance cardiaque", "Maladie coronarienne", "Arthrite", "Ostéoporose",
    "Hypothyroïdie", "Hyperthyroïdie", "Maladie de Crohn", "Colite ulcéreuse",
    "Insuffisance rénale chronique", "Cirrhose", "Cancer (rémission)", "Épilepsie",
    "Maladie de Parkinson", "Alzheimer", "Sclérose en plaques", "Aucune"
]

SYMPTOMES = [
    "Fièvre", "Toux", "Fatigue", "Maux de tête", "Nausées", "Vomissements",
    "Douleur abdominale", "Douleur thoracique", "Essoufflement", "Vertiges",
    "Diarrhée", "Constipation", "Douleurs articulaires", "Douleurs musculaires",
    "Éruption cutanée", "Démangeaisons", "Palpitations", "Anxiété", "Insomnie",
    "Perte d'appétit", "Prise de poids", "Perte de poids", "Confusion", "Malaise"
]

DIAGNOSTICS = [
    "Grippe", "COVID-19", "Gastro-entérite", "Bronchite", "Pneumonie",
    "Infection urinaire", "Angine", "Otite", "Sinusite", "Migraine",
    "Hypertension", "Diabète", "Asthme", "Anémie", "Appendicite",
    "Fracture", "Entorse", "Tendinite", "Lombalgie", "Cervicalgie",
    "Dépression", "Anxiété", "Insomnie", "Allergie", "Eczéma",
    "Gastrite", "Reflux gastro-œsophagien", "Hémorroïdes", "Varicelle",
    "Zona", "Herpès", "Mycose", "Conjonctivite", "Cataracte"
]

MEDICAMENTS = [
    "Paracétamol", "Ibuprofène", "Aspirine", "Amoxicilline", "Azithromycine",
    "Omeprazole", "Metformine", "Insuline", "Atorvastatine", "Amlodipine",
    "Losartan", "Levothyroxine", "Salbutamol", "Prednisolone", "Methotrexate",
    "Warfarine", "Clopidogrel", "Furosémide", "Spironolactone", "Enalapril",
    "Sertraline", "Fluoxétine", "Lorazépam", "Zolpidem", "Cetirizine",
    "Ranitidine", "Domperidone", "Loperamide", "Diclofénac", "Tramadol"
]

TYPES_EXAMENS = [
    "Radiographie", "Scanner", "IRM", "Échographie", "ECG", "EEG",
    "Endoscopie", "Coloscopie", "Mammographie", "Densitométrie osseuse",
    "Test d'effort", "Holter", "Spirométrie", "Prise de sang", "Analyse d'urine",
    "Biopsie", "Ponction lombaire", "Doppler", "Scintigraphie", "PET Scan"
]

SPECIALITES = [
    "Médecine générale", "Cardiologie", "Pneumologie", "Gastro-entérologie",
    "Néphrologie", "Endocrinologie", "Rhumatologie", "Neurologie",
    "Psychiatrie", "Dermatologie", "Ophtalmologie", "ORL", "Urologie",
    "Gynécologie", "Pédiatrie", "Gériatrie", "Orthopédie", "Traumatologie",
    "Chirurgie générale", "Anesthésie", "Radiologie", "Oncologie"
]

HOPITAUX = [
    "CHU Ibn Sina", "Hôpital Cheikh Zaid", "Clinique Al Madina", "Hôpital des Spécialités",
    "Centre Hospitalier Universitaire", "Clinique du Parc", "Hôpital Avicenne",
    "Polyclinique de l'Atlas", "Hôpital Militaire", "Clinique Internationale",
    "Hôpital Pitié-Salpêtrière", "Hôpital Georges Pompidou", "Clinique Saint-Jean",
    "Centre Médical Universitaire", "Hôpital Américain"
]

TYPES_CONSULTATION = ["Urgence", "Consultation", "Suivi", "Contrôle", "Bilan"]
MODES_PAIEMENT = ["Espèces", "Carte bancaire", "Chèque", "Assurance", "Mutuelle"]

# ====================
# GÉNÉRATEURS
# ====================

def gen_patient(n):
    """Génère des données de patients"""
    patients = []
    
    for i in range(n):
        sexe = np.random.choice(SEXES)
        prenom = np.random.choice(PRENOMS_H if sexe == "M" else PRENOMS_F)
        nom = np.random.choice(NOMS)
        
        # Âge et date de naissance
        age = np.random.randint(0, 95)
        date_naissance = datetime.now() - timedelta(days=age*365 + np.random.randint(0, 365))
        
        # Informations de contact
        telephone = f"06{np.random.randint(10000000, 99999999)}"
        email = f"{prenom.lower()}.{nom.lower()}@email.com"
        ville = np.random.choice(VILLES)
        
        # Informations médicales de base
        groupe_sanguin = np.random.choice(GROUPES_SANGUINS, p=[0.35, 0.05, 0.20, 0.02, 0.05, 0.01, 0.30, 0.02])
        
        # Poids et taille selon l'âge
        if age < 18:
            poids = np.random.randint(10, 70)
            taille = np.random.randint(80, 175)
        else:
            poids = np.random.randint(45, 120)
            taille = np.random.randint(150, 195)
        
        imc = round(poids / ((taille/100) ** 2), 1)
        
        # Tension artérielle
        tension_systolique = np.random.randint(90, 180)
        tension_diastolique = np.random.randint(60, 120)
        tension = f"{tension_systolique}/{tension_diastolique}"
        
        # Fréquence cardiaque
        frequence_cardiaque = np.random.randint(50, 110)
        
        # Température
        temperature = round(np.random.uniform(36.0, 39.5), 1)
        
        # Maladies chroniques
        nb_maladies = np.random.choice([0, 1, 2, 3], p=[0.60, 0.25, 0.10, 0.05])
        if nb_maladies == 0:
            maladies_chroniques = "Aucune"
        else:
            maladies = np.random.choice([m for m in MALADIES_CHRONIQUES if m != "Aucune"], 
                                       size=nb_maladies, replace=False)
            maladies_chroniques = ", ".join(maladies)
        
        # Allergies
        allergies = np.random.choice([
            "Aucune", "Pénicilline", "Aspirine", "Pollen", "Acariens", 
            "Fruits de mer", "Lactose", "Gluten", "Iode", "Latex"
        ], p=[0.60, 0.08, 0.05, 0.07, 0.05, 0.05, 0.03, 0.03, 0.02, 0.02])
        
        # Fumeur
        fumeur = np.random.choice(["Non", "Oui", "Ancien fumeur"], p=[0.70, 0.20, 0.10])
        
        # Numéro de sécurité sociale
        num_secu = f"{1 if sexe == 'M' else 2}{str(date_naissance.year)[2:]}{date_naissance.month:02d}{np.random.randint(10000, 99999)}"
        
        patients.append({
            "nom": nom,
            "prenom": prenom,
            "sexe": sexe,
            "age": age,
            "date_naissance": date_naissance.strftime("%Y-%m-%d"),
            "telephone": telephone,
            "email": email,
            "ville": ville,
            "groupe_sanguin": groupe_sanguin,
            "poids": poids,
            "taille": taille,
            "imc": imc,
            "tension": tension,
            "frequence_cardiaque": frequence_cardiaque,
            "temperature": temperature,
            "maladies_chroniques": maladies_chroniques,
            "allergies": allergies,
            "fumeur": fumeur,
            "num_secu": num_secu
        })
    
    return patients

def gen_consultation(n):
    """Génère des données de consultations"""
    consultations = []
    
    for i in range(n):
        # Date consultation (dernier an)
        date_consultation = datetime.now() - timedelta(days=np.random.randint(0, 365))
        
        # Type et durée
        type_consultation = np.random.choice(TYPES_CONSULTATION, p=[0.15, 0.50, 0.20, 0.10, 0.05])
        duree = np.random.choice([15, 20, 30, 45, 60], p=[0.20, 0.30, 0.30, 0.15, 0.05])
        
        # Symptômes
        nb_symptomes = np.random.randint(1, 5)
        symptomes = ", ".join(np.random.choice(SYMPTOMES, size=nb_symptomes, replace=False))
        
        # Diagnostic
        diagnostic = np.random.choice(DIAGNOSTICS)
        
        # Spécialité et hôpital
        specialite = np.random.choice(SPECIALITES)
        hopital = np.random.choice(HOPITAUX)
        
        # Examens
        nb_examens = np.random.choice([0, 1, 2, 3], p=[0.40, 0.35, 0.20, 0.05])
        if nb_examens == 0:
            examens = "Aucun"
        else:
            exams = np.random.choice(TYPES_EXAMENS, size=nb_examens, replace=False)
            examens = ", ".join(exams)
        
        # Prescription
        nb_medicaments = np.random.randint(0, 6)
        if nb_medicaments == 0:
            prescription = "Aucune"
        else:
            medics = np.random.choice(MEDICAMENTS, size=nb_medicaments, replace=False)
            prescription = ", ".join(medics)
        
        # Arrêt de travail
        arret_travail = np.random.choice([0, 3, 7, 14, 21, 30], p=[0.70, 0.10, 0.10, 0.05, 0.03, 0.02])
        
        # Coût
        if type_consultation == "Urgence":
            cout = np.random.randint(500, 3000)
        elif type_consultation == "Consultation":
            cout = np.random.randint(200, 800)
        else:
            cout = np.random.randint(150, 600)
        
        mode_paiement = np.random.choice(MODES_PAIEMENT, p=[0.20, 0.30, 0.10, 0.25, 0.15])
        
        # Suivi
        suivi_necessaire = np.random.choice(["Oui", "Non"], p=[0.40, 0.60])
        date_prochain_rdv = ""
        if suivi_necessaire == "Oui":
            jours_suivi = np.random.choice([7, 14, 30, 60, 90])
            date_prochain_rdv = (date_consultation + timedelta(days=jours_suivi)).strftime("%Y-%m-%d")
        
        consultations.append({
            "date_consultation": date_consultation.strftime("%Y-%m-%d"),
            "heure": f"{np.random.randint(8, 19):02d}:{np.random.choice(['00', '15', '30', '45'])}",
            "type_consultation": type_consultation,
            "duree": duree,
            "specialite": specialite,
            "hopital": hopital,
            "symptomes": symptomes,
            "diagnostic": diagnostic,
            "examens": examens,
            "prescription": prescription,
            "arret_travail": arret_travail,
            "cout": cout,
            "mode_paiement": mode_paiement,
            "suivi_necessaire": suivi_necessaire,
            "date_prochain_rdv": date_prochain_rdv
        })
    
    return consultations

def gen_hospitalisation(n):
    """Génère des données d'hospitalisations"""
    hospitalisations = []
    
    for i in range(n):
        # Dates
        date_entree = datetime.now() - timedelta(days=np.random.randint(0, 365))
        duree_sejour = np.random.choice([1, 2, 3, 5, 7, 10, 14, 21, 30], p=[0.15, 0.20, 0.15, 0.15, 0.15, 0.10, 0.05, 0.03, 0.02])
        date_sortie = date_entree + timedelta(days=duree_sejour)
        
        # Type
        type_hospitalisation = np.random.choice(["Programmée", "Urgence"], p=[0.60, 0.40])
        
        # Service
        service = np.random.choice([
            "Chirurgie", "Médecine", "Cardiologie", "Réanimation", "Pédiatrie",
            "Gynécologie", "Orthopédie", "Neurologie", "Oncologie", "Urgences"
        ])
        
        # Diagnostic et intervention
        motif = np.random.choice(DIAGNOSTICS)
        intervention = np.random.choice([
            "Aucune", "Appendicectomie", "Césarienne", "Prothèse hanche", "Prothèse genou",
            "Cholécystectomie", "Hernie", "Cathétérisme", "Angioplastie", "Pontage",
            "Ablation tumeur", "Chimiothérapie", "Pose pacemaker", "Chirurgie colonne"
        ], p=[0.30, 0.08, 0.08, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.04, 0.06, 0.06, 0.04, 0.04])
        
        # Chambre
        type_chambre = np.random.choice(["Commune", "Double", "Individuelle", "VIP"], p=[0.50, 0.25, 0.20, 0.05])
        
        # Coûts
        cout_journalier = np.random.randint(500, 5000)
        cout_total = cout_journalier * duree_sejour
        if intervention != "Aucune":
            cout_total += np.random.randint(5000, 50000)
        
        # État sortie
        etat_sortie = np.random.choice(["Guéri", "Amélioration", "Stable", "Transfert", "Décès"], 
                                      p=[0.60, 0.25, 0.10, 0.04, 0.01])
        
        hospitalisations.append({
            "date_entree": date_entree.strftime("%Y-%m-%d"),
            "date_sortie": date_sortie.strftime("%Y-%m-%d"),
            "duree_sejour": duree_sejour,
            "type_hospitalisation": type_hospitalisation,
            "service": service,
            "motif": motif,
            "intervention": intervention,
            "type_chambre": type_chambre,
            "cout_journalier": cout_journalier,
            "cout_total": cout_total,
            "etat_sortie": etat_sortie
        })
    
    return hospitalisations

def gen_analyse_sang(n):
    """Génère des résultats d'analyses de sang"""
    analyses = []
    
    for i in range(n):
        date_analyse = (datetime.now() - timedelta(days=np.random.randint(0, 365))).strftime("%Y-%m-%d")
        
        # Hémogramme
        globules_rouges = round(np.random.uniform(3.5, 6.0), 2)
        hemoglobine = round(np.random.uniform(11.0, 18.0), 1)
        hematocrite = round(np.random.uniform(35.0, 55.0), 1)
        globules_blancs = round(np.random.uniform(4.0, 11.0), 2)
        plaquettes = np.random.randint(150, 450)
        
        # Bilan lipidique
        cholesterol_total = round(np.random.uniform(1.5, 3.0), 2)
        hdl = round(np.random.uniform(0.4, 2.0), 2)
        ldl = round(np.random.uniform(0.5, 2.0), 2)
        triglycérides = round(np.random.uniform(0.5, 2.5), 2)
        
        # Glycémie
        glycemie = round(np.random.uniform(0.7, 1.4), 2)
        
        # Fonction rénale
        creatinine = round(np.random.uniform(60, 120), 0)
        uree = round(np.random.uniform(2.5, 7.5), 1)
        
        # Fonction hépatique
        alat = np.random.randint(10, 50)
        asat = np.random.randint(10, 50)
        
        analyses.append({
            "date_analyse": date_analyse,
            "globules_rouges": globules_rouges,
            "hemoglobine": hemoglobine,
            "hematocrite": hematocrite,
            "globules_blancs": globules_blancs,
            "plaquettes": plaquettes,
            "cholesterol_total": cholesterol_total,
            "hdl": hdl,
            "ldl": ldl,
            "triglycérides": triglycérides,
            "glycemie": glycemie,
            "creatinine": creatinine,
            "uree": uree,
            "alat": alat,
            "asat": asat
        })
    
    return analyses

def gen_id(n, prefix="PAT"):
    """Génère des identifiants"""
    return [f"{prefix}_{str(i+1).zfill(6)}" for i in range(n)]

# ====================
# CONSTRUCTION DATASET
# ====================

def build_dataset(dataset_type, cols, n):
    """Construit le dataset selon le type"""
    
    if dataset_type == "patients":
        data_list = gen_patient(n)
        id_prefix = "PAT"
    elif dataset_type == "consultations":
        data_list = gen_consultation(n)
        id_prefix = "CONS"
    elif dataset_type == "hospitalisations":
        data_list = gen_hospitalisation(n)
        id_prefix = "HOSP"
    elif dataset_type == "analyses":
        data_list = gen_analyse_sang(n)
        id_prefix = "ANAL"
    else:
        raise ValueError(f"Type de dataset inconnu: {dataset_type}")
    
    ids = gen_id(n, id_prefix)
    
    # Construire dataframe
    data = {}
    
    for col in cols:
        col_lower = col.lower()
        
        if col_lower in ["id", "id_patient", "id_consultation", "id_hospitalisation", "id_analyse"]:
            data[col] = ids
        elif col_lower in data_list[0]:
            data[col] = [item[col_lower] for item in data_list]
        else:
            # Chercher avec underscores
            col_check = col_lower.replace("_", "")
            found = False
            for key in data_list[0].keys():
                if key.replace("_", "") == col_check:
                    data[col] = [item[key] for item in data_list]
                    found = True
                    break
            if not found:
                data[col] = ["N/A"] * n
    
    return pd.DataFrame(data)

# ====================
# CLI
# ====================

def main():
    parser = argparse.ArgumentParser(
        description="🏥 Générateur de données de santé",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
EXEMPLES D'UTILISATION :

👤 Dataset patients :
  python health_gen.py --type patients --name patients --cols id,nom,prenom,age,sexe,groupe_sanguin,poids,taille,imc,tension --n 1000

🩺 Dataset consultations :
  python health_gen.py --type consultations --name consultations --cols id,date_consultation,type_consultation,specialite,diagnostic,prescription,cout --n 500

🏥 Dataset hospitalisations :
  python health_gen.py --type hospitalisations --name hospitalisations --cols id,date_entree,date_sortie,duree_sejour,service,motif,cout_total --n 200

🧪 Dataset analyses de sang :
  python health_gen.py --type analyses --name analyses --cols id,date_analyse,hemoglobine,globules_blancs,cholesterol_total,glycemie --n 300

TYPES DE DATASETS :
  • patients         → Données des patients
  • consultations    → Consultations médicales
  • hospitalisations → Séjours hospitaliers
  • analyses         → Résultats d'analyses sanguines

COLONNES DISPONIBLES PAR TYPE :

PATIENTS :
  nom, prenom, sexe, age, date_naissance, telephone, email, ville,
  groupe_sanguin, poids, taille, imc, tension, frequence_cardiaque,
  temperature, maladies_chroniques, allergies, fumeur, num_secu

CONSULTATIONS :
  date_consultation, heure, type_consultation, duree, specialite,
  hopital, symptomes, diagnostic, examens, prescription, arret_travail,
  cout, mode_paiement, suivi_necessaire, date_prochain_rdv

HOSPITALISATIONS :
  date_entree, date_sortie, duree_sejour, type_hospitalisation,
  service, motif, intervention, type_chambre, cout_journalier,
  cout_total, etat_sortie

ANALYSES :
  date_analyse, globules_rouges, hemoglobine, hematocrite,
  globules_blancs, plaquettes, cholesterol_total, hdl, ldl,
  triglycérides, glycemie, creatinine, uree, alat, asat
        """
    )
    
    parser.add_argument("--type", required=True, choices=["patients", "consultations", "hospitalisations", "analyses"],
                       help="Type de dataset à générer")
    parser.add_argument("--name", required=True, help="Nom du dataset")
    parser.add_argument("--cols", required=True, help="Colonnes séparées par des virgules")
    parser.add_argument("--n", type=int, default=500, help="Nombre de lignes")
    parser.add_argument("--out", default=None, help="Fichier de sortie")
    parser.add_argument("--preview", type=int, default=10, help="Lignes à prévisualiser")
    
    args = parser.parse_args()
    
    cols = [c.strip() for c in args.cols.split(",")]
    
    print(f"\n{'='*80}")
    print(f"🏥 GÉNÉRATION DATASET SANTÉ : {args.type.upper()}")
    print("="*80 + "\n")
    print(f"📊 Nombre de lignes : {args.n}")
    print(f"📋 Colonnes : {', '.join(cols)}\n")
    
    try:
        df = build_dataset(args.type, cols, args.n)
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        return
    
    out = args.out or f"{args.name}.csv"
    df.to_csv(out, index=False, encoding='utf-8-sig')
    
    print("="*80)
    print(f"✅ DATASET GÉNÉRÉ")
    print("="*80)
    print(f"📁 Fichier : {out}")
    print(f"📊 Lignes  : {len(df)}")
    print(f"📊 Colonnes: {len(df.columns)}\n")
    
    print("👁️  APERÇU :")
    print(df.head(args.preview).to_string(index=False))
    
    print(f"\n✨ Terminé!\n")

if __name__ == "__main__":
    main()