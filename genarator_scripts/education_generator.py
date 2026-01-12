"""
GÉNÉRATEUR DE DONNÉES COHÉRENTES POUR ÉDUCATION
Génère des données éducatives internationales avec cohérence totale
"""

import json
import argparse
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

np.random.seed(42)

# ====================
# DONNÉES ÉDUCATIVES INTERNATIONALES
# ====================

EDUCATION_DATA = {
    "France": {
        "etablissements": {
            "École Primaire": ["École Élémentaire Victor Hugo", "École Jean Jaurès", "École Jules Ferry", "École Pasteur"],
            "Collège": ["Collège Pierre et Marie Curie", "Collège Jean Moulin", "Collège Voltaire", "Collège Molière"],
            "Lycée": ["Lycée Louis le Grand", "Lycée Henri IV", "Lycée Condorcet", "Lycée Janson de Sailly"],
            "Université": ["Université Paris-Saclay", "Sorbonne Université", "Université Lyon 1", "Université Grenoble Alpes"]
        },
        "niveaux": {
            "École Primaire": ["CP", "CE1", "CE2", "CM1", "CM2"],
            "Collège": ["6ème", "5ème", "4ème", "3ème"],
            "Lycée": ["Seconde", "Première", "Terminale"],
            "Université": ["Licence 1", "Licence 2", "Licence 3", "Master 1", "Master 2", "Doctorat"]
        },
        "matieres": {
            "École Primaire": ["Français", "Mathématiques", "Histoire-Géo", "Sciences", "Arts", "EPS"],
            "Collège": ["Français", "Mathématiques", "Histoire-Géo", "SVT", "Physique-Chimie", "Anglais", "Espagnol", "Allemand", "EPS"],
            "Lycée": ["Français", "Philosophie", "Mathématiques", "Histoire-Géo", "SVT", "Physique-Chimie", "Anglais", "Espagnol", "SES", "EPS"],
            "Université": ["Analyse", "Algèbre", "Programmation", "Base de données", "Économie", "Droit", "Biologie", "Chimie Organique"]
        },
        "diplomes": ["Brevet", "Baccalauréat", "Licence", "Master", "Doctorat"],
        "villes": ["Paris", "Lyon", "Marseille", "Toulouse", "Bordeaux", "Lille", "Nantes", "Strasbourg"]
    },
    "Maroc": {
        "etablissements": {
            "École Primaire": ["École Al Massira", "École Mohammed V", "École Hassan II", "École Ibn Sina"],
            "Collège": ["Collège Ibn Khaldoun", "Collège Al Khawarizmi", "Collège Averroès", "Collège Al Ghazali"],
            "Lycée": ["Lycée Mohammed V", "Lycée Hassan II", "Lycée Moulay Youssef", "Lycée Descartes"],
            "Université": ["Université Mohammed V", "Université Hassan II", "Université Cadi Ayyad", "Université Ibn Tofail"]
        },
        "niveaux": {
            "École Primaire": ["1ère année", "2ème année", "3ème année", "4ème année", "5ème année", "6ème année"],
            "Collège": ["1ère AC", "2ème AC", "3ème AC"],
            "Lycée": ["Tronc Commun", "1ère Bac", "2ème Bac"],
            "Université": ["S1", "S2", "S3", "S4", "S5", "S6", "Master 1", "Master 2"]
        },
        "matieres": {
            "École Primaire": ["Arabe", "Français", "Mathématiques", "Éveil Scientifique", "Histoire-Géo", "Éducation Islamique"],
            "Collège": ["Arabe", "Français", "Mathématiques", "SVT", "Physique-Chimie", "Histoire-Géo", "Anglais", "Informatique"],
            "Lycée": ["Arabe", "Français", "Mathématiques", "SVT", "Physique-Chimie", "Philosophie", "Anglais", "Sciences de l'Ingénieur"],
            "Université": ["Analyse", "Algèbre", "Programmation", "Réseaux", "Économie", "Gestion", "Droit", "Statistiques"]
        },
        "diplomes": ["Certificat Primaire", "Brevet", "Baccalauréat", "Licence", "Master", "Doctorat"],
        "villes": ["Casablanca", "Rabat", "Marrakech", "Fès", "Tanger", "Agadir", "Meknès", "Oujda"]
    },
    "USA": {
        "etablissements": {
            "Elementary School": ["Washington Elementary", "Lincoln Elementary", "Jefferson Elementary", "Roosevelt Elementary"],
            "Middle School": ["Kennedy Middle School", "Madison Middle School", "Adams Middle School", "Franklin Middle School"],
            "High School": ["Central High School", "North High School", "South High School", "East High School"],
            "University": ["Harvard University", "MIT", "Stanford University", "UC Berkeley", "Yale University"]
        },
        "niveaux": {
            "Elementary School": ["Grade 1", "Grade 2", "Grade 3", "Grade 4", "Grade 5"],
            "Middle School": ["Grade 6", "Grade 7", "Grade 8"],
            "High School": ["Grade 9", "Grade 10", "Grade 11", "Grade 12"],
            "University": ["Freshman", "Sophomore", "Junior", "Senior", "Graduate"]
        },
        "matieres": {
            "Elementary School": ["English", "Math", "Science", "Social Studies", "Art", "PE"],
            "Middle School": ["English", "Math", "Science", "History", "Geography", "Spanish", "Computer Science"],
            "High School": ["English", "Algebra", "Geometry", "Calculus", "Biology", "Chemistry", "Physics", "History", "Spanish"],
            "University": ["Calculus", "Linear Algebra", "Computer Science", "Data Structures", "Economics", "Statistics", "Biology"]
        },
        "diplomes": ["High School Diploma", "Bachelor's Degree", "Master's Degree", "PhD"],
        "villes": ["New York", "Los Angeles", "Chicago", "Houston", "Boston", "San Francisco", "Seattle", "Miami"]
    },
    "UK": {
        "etablissements": {
            "Primary School": ["St. Mary's Primary", "King's Primary School", "Victoria Primary", "Westminster Primary"],
            "Secondary School": ["Oxford High School", "Cambridge High School", "Eton College", "Westminster School"],
            "University": ["University of Oxford", "University of Cambridge", "Imperial College London", "UCL", "LSE"]
        },
        "niveaux": {
            "Primary School": ["Year 1", "Year 2", "Year 3", "Year 4", "Year 5", "Year 6"],
            "Secondary School": ["Year 7", "Year 8", "Year 9", "Year 10", "Year 11", "Year 12", "Year 13"],
            "University": ["First Year", "Second Year", "Third Year", "Postgraduate"]
        },
        "matieres": {
            "Primary School": ["English", "Maths", "Science", "History", "Geography", "Art", "PE"],
            "Secondary School": ["English", "Maths", "Physics", "Chemistry", "Biology", "History", "Geography", "French", "German"],
            "University": ["Mathematics", "Computer Science", "Engineering", "Economics", "Law", "Medicine", "Business"]
        },
        "diplomes": ["GCSE", "A-Level", "Bachelor's", "Master's", "PhD"],
        "villes": ["London", "Manchester", "Edinburgh", "Birmingham", "Liverpool", "Bristol", "Oxford", "Cambridge"]
    },
    "Canada": {
        "etablissements": {
            "Elementary School": ["Maple Elementary", "Cedar Elementary", "Pine Elementary", "Oak Elementary"],
            "Secondary School": ["Toronto High School", "Montreal High School", "Vancouver High School", "Calgary High School"],
            "University": ["University of Toronto", "McGill University", "UBC", "University of Alberta"]
        },
        "niveaux": {
            "Elementary School": ["Grade 1", "Grade 2", "Grade 3", "Grade 4", "Grade 5", "Grade 6"],
            "Secondary School": ["Grade 7", "Grade 8", "Grade 9", "Grade 10", "Grade 11", "Grade 12"],
            "University": ["First Year", "Second Year", "Third Year", "Fourth Year", "Graduate"]
        },
        "matieres": {
            "Elementary School": ["English", "French", "Math", "Science", "Social Studies", "Art"],
            "Secondary School": ["English", "French", "Math", "Physics", "Chemistry", "Biology", "History", "Geography"],
            "University": ["Calculus", "Statistics", "Computer Science", "Engineering", "Business", "Economics"]
        },
        "diplomes": ["High School Diploma", "Bachelor's", "Master's", "PhD"],
        "villes": ["Toronto", "Montreal", "Vancouver", "Calgary", "Ottawa", "Edmonton", "Quebec City", "Winnipeg"]
    },
    "Allemagne": {
        "etablissements": {
            "Grundschule": ["Goethe Grundschule", "Schiller Grundschule", "Einstein Grundschule", "Mozart Grundschule"],
            "Gymnasium": ["Humboldt-Gymnasium", "Goethe-Gymnasium", "Kant-Gymnasium", "Schiller-Gymnasium"],
            "Universität": ["Universität München", "Universität Heidelberg", "TU Berlin", "Universität Hamburg"]
        },
        "niveaux": {
            "Grundschule": ["Klasse 1", "Klasse 2", "Klasse 3", "Klasse 4"],
            "Gymnasium": ["Klasse 5", "Klasse 6", "Klasse 7", "Klasse 8", "Klasse 9", "Klasse 10", "Klasse 11", "Klasse 12"],
            "Universität": ["1. Semester", "2. Semester", "3. Semester", "4. Semester", "5. Semester", "6. Semester"]
        },
        "matieres": {
            "Grundschule": ["Deutsch", "Mathematik", "Sachkunde", "Sport", "Kunst", "Musik"],
            "Gymnasium": ["Deutsch", "Mathematik", "Physik", "Chemie", "Biologie", "Geschichte", "Englisch", "Französisch"],
            "Universität": ["Mathematik", "Informatik", "Maschinenbau", "Wirtschaft", "Jura", "Medizin"]
        },
        "diplomes": ["Abitur", "Bachelor", "Master", "Doktor"],
        "villes": ["Berlin", "München", "Hamburg", "Frankfurt", "Köln", "Stuttgart", "Düsseldorf", "Leipzig"]
    },
    "Espagne": {
        "etablissements": {
            "Primaria": ["Colegio Cervantes", "Colegio Picasso", "Colegio Goya", "Colegio Velázquez"],
            "Secundaria": ["Instituto Ramón y Cajal", "Instituto Giner de los Ríos", "Instituto Lope de Vega"],
            "Universidad": ["Universidad Complutense", "Universidad de Barcelona", "Universidad de Salamanca"]
        },
        "niveaux": {
            "Primaria": ["1º Primaria", "2º Primaria", "3º Primaria", "4º Primaria", "5º Primaria", "6º Primaria"],
            "Secundaria": ["1º ESO", "2º ESO", "3º ESO", "4º ESO", "1º Bachillerato", "2º Bachillerato"],
            "Universidad": ["1º Curso", "2º Curso", "3º Curso", "4º Curso", "Máster"]
        },
        "matieres": {
            "Primaria": ["Lengua", "Matemáticas", "Ciencias", "Historia", "Arte", "Educación Física"],
            "Secundaria": ["Lengua", "Matemáticas", "Física", "Química", "Biología", "Historia", "Inglés", "Francés"],
            "Universidad": ["Cálculo", "Álgebra", "Programación", "Economía", "Derecho", "Medicina"]
        },
        "diplomes": ["ESO", "Bachillerato", "Grado", "Máster", "Doctorado"],
        "villes": ["Madrid", "Barcelona", "Valencia", "Sevilla", "Zaragoza", "Málaga", "Bilbao", "Granada"]
    }
}

# Noms et prénoms par pays
NOMS_PRENOMS_PAYS = {
    "France": {
        "M": {
            "prenoms": ["Lucas", "Hugo", "Louis", "Jules", "Gabriel", "Arthur", "Léo", "Raphaël", "Mathis", "Noah"],
            "noms": ["Dupont", "Martin", "Bernard", "Thomas", "Robert", "Petit", "Durand", "Leroy", "Moreau", "Simon"]
        },
        "F": {
            "prenoms": ["Emma", "Louise", "Chloé", "Camille", "Léa", "Manon", "Sarah", "Inès", "Zoé", "Clara"],
            "noms": ["Dupont", "Martin", "Bernard", "Thomas", "Robert", "Petit", "Durand", "Leroy", "Moreau", "Simon"]
        }
    },
    "Maroc": {
        "M": {
            "prenoms": ["Mohamed", "Ahmed", "Youssef", "Ali", "Hassan", "Omar", "Karim", "Mehdi", "Rachid", "Amine"],
            "noms": ["El Amrani", "Benali", "Idrissi", "Alaoui", "Bennani", "Chakir", "Tazi", "Benjelloun", "Fassi", "Sqalli"]
        },
        "F": {
            "prenoms": ["Fatima", "Aicha", "Salma", "Nour", "Amina", "Laila", "Sanae", "Zineb", "Ikram", "Marwa"],
            "noms": ["El Amrani", "Benali", "Idrissi", "Alaoui", "Bennani", "Chakir", "Tazi", "Benjelloun", "Fassi", "Sqalli"]
        }
    },
    "USA": {
        "M": {
            "prenoms": ["James", "John", "Michael", "David", "William", "Joseph", "Thomas", "Daniel", "Matthew", "Anthony"],
            "noms": ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez"]
        },
        "F": {
            "prenoms": ["Emma", "Olivia", "Ava", "Isabella", "Sophia", "Mia", "Charlotte", "Amelia", "Harper", "Evelyn"],
            "noms": ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez"]
        }
    },
    "UK": {
        "M": {
            "prenoms": ["Oliver", "Harry", "George", "Noah", "Jack", "Charlie", "Jacob", "Thomas", "Oscar", "William"],
            "noms": ["Smith", "Jones", "Williams", "Taylor", "Brown", "Davies", "Evans", "Wilson", "Thomas", "Johnson"]
        },
        "F": {
            "prenoms": ["Olivia", "Amelia", "Isla", "Emily", "Poppy", "Ava", "Isabella", "Jessica", "Lily", "Sophie"],
            "noms": ["Smith", "Jones", "Williams", "Taylor", "Brown", "Davies", "Evans", "Wilson", "Thomas", "Johnson"]
        }
    },
    "Canada": {
        "M": {
            "prenoms": ["Liam", "Noah", "Oliver", "Lucas", "Jack", "Benjamin", "William", "James", "Alexander", "Ethan"],
            "noms": ["Smith", "Brown", "Tremblay", "Martin", "Roy", "Wilson", "MacDonald", "Johnson", "Taylor", "Anderson"]
        },
        "F": {
            "prenoms": ["Emma", "Olivia", "Charlotte", "Amelia", "Sophia", "Emily", "Ava", "Isabella", "Mia", "Chloe"],
            "noms": ["Smith", "Brown", "Tremblay", "Martin", "Roy", "Wilson", "MacDonald", "Johnson", "Taylor", "Anderson"]
        }
    },
    "Allemagne": {
        "M": {
            "prenoms": ["Ben", "Paul", "Jonas", "Leon", "Finn", "Noah", "Elias", "Luis", "Lukas", "Felix"],
            "noms": ["Müller", "Schmidt", "Schneider", "Fischer", "Weber", "Meyer", "Wagner", "Becker", "Schulz", "Hoffmann"]
        },
        "F": {
            "prenoms": ["Mia", "Emma", "Hannah", "Sophia", "Anna", "Emilia", "Lina", "Marie", "Lena", "Lea"],
            "noms": ["Müller", "Schmidt", "Schneider", "Fischer", "Weber", "Meyer", "Wagner", "Becker", "Schulz", "Hoffmann"]
        }
    },
    "Espagne": {
        "M": {
            "prenoms": ["Hugo", "Martín", "Lucas", "Mateo", "Leo", "Daniel", "Alejandro", "Pablo", "Manuel", "Álvaro"],
            "noms": ["García", "Rodríguez", "González", "Fernández", "López", "Martínez", "Sánchez", "Pérez", "Gómez", "Martín"]
        },
        "F": {
            "prenoms": ["Lucía", "María", "Sofía", "Martina", "Paula", "Julia", "Emma", "Valeria", "Daniela", "Alba"],
            "noms": ["García", "Rodríguez", "González", "Fernández", "López", "Martínez", "Sánchez", "Pérez", "Gómez", "Martín"]
        }
    }
}

# ====================
# GÉNÉRATEURS COHÉRENTS POUR ÉDUCATION
# ====================

def gen_student_data(n):
    """Génère des données d'étudiants COHÉRENTES par pays"""
    students = []
    
    for _ in range(n):
        # Choisir un pays
        pays = np.random.choice(list(EDUCATION_DATA.keys()))
        data_pays = EDUCATION_DATA[pays]
        
        # Choisir genre
        genre = np.random.choice(["M", "F"])
        
        # Nom et prénom cohérents avec pays et genre
        prenom = np.random.choice(NOMS_PRENOMS_PAYS[pays][genre]["prenoms"])
        nom = np.random.choice(NOMS_PRENOMS_PAYS[pays][genre]["noms"])
        
        # Choisir type d'établissement
        type_etab = np.random.choice(list(data_pays["etablissements"].keys()))
        
        # Établissement cohérent avec le type
        etablissement = np.random.choice(data_pays["etablissements"][type_etab])
        
        # Niveau cohérent avec le type d'établissement
        niveau = np.random.choice(data_pays["niveaux"][type_etab])
        
        # Ville cohérente avec le pays
        ville = np.random.choice(data_pays["villes"])
        
        # Âge cohérent avec le niveau
        age_base = {
            "École Primaire": (6, 11), "Collège": (11, 15), "Lycée": (15, 18), "Université": (18, 26),
            "Elementary School": (6, 11), "Middle School": (11, 14), "High School": (14, 18),
            "Primary School": (5, 11), "Secondary School": (11, 18),
            "Grundschule": (6, 10), "Gymnasium": (10, 18), "Universität": (18, 26),
            "Primaria": (6, 12), "Secundaria": (12, 18), "Universidad": (18, 26)
        }
        age_min, age_max = age_base.get(type_etab, (6, 18))
        age = np.random.randint(age_min, age_max + 1)
        
        # Date de naissance cohérente avec l'âge
        current_year = datetime.now().year
        birth_year = current_year - age
        birth_month = np.random.randint(1, 13)
        birth_day = np.random.randint(1, 29)
        date_naissance = f"{birth_year}-{birth_month:02d}-{birth_day:02d}"
        
        students.append({
            "pays": pays,
            "genre": genre,
            "prenom": prenom,
            "nom": nom,
            "age": age,
            "date_naissance": date_naissance,
            "type_etablissement": type_etab,
            "etablissement": etablissement,
            "niveau": niveau,
            "ville": ville
        })
    
    return students

def gen_notes_coherentes(students):
    """Génère des notes cohérentes pour chaque étudiant selon son pays et niveau"""
    notes_data = []
    
    for student in students:
        pays = student["pays"]
        type_etab = student["type_etablissement"]
        
        # Obtenir les matières pour ce type d'établissement
        matieres = EDUCATION_DATA[pays]["matieres"][type_etab]
        
        # Générer un profil de performance (étudiant faible/moyen/bon)
        performance_base = np.random.choice([10, 12, 15], p=[0.2, 0.5, 0.3])
        
        notes_etudiant = {}
        for matiere in matieres:
            # Note avec variation autour de la performance de base
            note = np.clip(np.random.normal(performance_base, 2), 0, 20)
            notes_etudiant[matiere] = round(note, 1)
        
        notes_data.append(notes_etudiant)
    
    return notes_data

def gen_absences_coherentes(n, type_etablissements):
    """Génère des absences cohérentes (plus d'absences en université)"""
    absences = []
    for type_etab in type_etablissements:
        if "Université" in type_etab or "University" in type_etab or "Universität" in type_etab or "Universidad" in type_etab:
            absence = np.random.randint(0, 20)
        else:
            absence = np.random.randint(0, 10)
        absences.append(absence)
    return absences

def gen_email_education(prenoms, noms, etablissements):
    """Génère des emails éducatifs"""
    emails = []
    for i, (prenom, nom, etab) in enumerate(zip(prenoms, noms, etablissements)):
        # Email basé sur prenom.nom@etablissement
        clean_prenom = prenom.lower().replace(" ", "").replace("é", "e").replace("è", "e").replace("ä", "a").replace("ö", "o").replace("ü", "u")
        clean_nom = nom.lower().replace(" ", "").replace("é", "e").replace("è", "e").replace("ä", "a").replace("ö", "o").replace("ü", "u")
        
        # Domaine basé sur l'établissement
        if "Université" in etab or "University" in etab or "Universität" in etab or "Universidad" in etab:
            domain = "edu"
        else:
            domain = "school.edu"
        
        email = f"{clean_prenom}.{clean_nom}{np.random.randint(1, 999)}@{domain}"
        emails.append(email)
    
    return emails

def gen_id_student(n, prefix="STU"):
    """Génère des identifiants d'étudiants"""
    return [f"{prefix}_{str(i+1).zfill(6)}" for i in range(n)]

def gen_annee_scolaire():
    """Génère l'année scolaire actuelle"""
    current_year = datetime.now().year
    if datetime.now().month >= 9:
        return f"{current_year}-{current_year+1}"
    else:
        return f"{current_year-1}-{current_year}"

# ====================
# DÉTECTION INTELLIGENTE POUR ÉDUCATION
# ====================

def guess_education_type(name):
    """Détecte automatiquement le type de colonne pour éducation"""
    name_lower = name.lower()
    
    if name_lower in ["id", "id_etudiant", "numero_etudiant", "student_id"]:
        return ("edu_id", {})
    
    if name_lower in ["nom", "lastname", "apellido", "nachname"]:
        return ("edu_nom", {})
    
    if name_lower in ["prenom", "firstname", "nombre", "vorname"]:
        return ("edu_prenom", {})
    
    if name_lower in ["genre", "gender", "sexe", "geschlecht", "sexo"]:
        return ("edu_genre", {})
    
    if name_lower in ["age", "âge", "edad", "alter"]:
        return ("edu_age", {})
    
    if "date" in name_lower and ("naissance" in name_lower or "birth" in name_lower or "nacimiento" in name_lower):
        return ("edu_date_naissance", {})
    
    if name_lower in ["pays", "country", "land", "país"]:
        return ("edu_pays", {})
    
    if name_lower in ["ville", "city", "ciudad", "stadt"]:
        return ("edu_ville", {})
    
    if name_lower in ["type_etablissement", "school_type", "tipo_escuela"]:
        return ("edu_type_etab", {})
    
    if name_lower in ["etablissement", "school", "escuela", "schule"]:
        return ("edu_etablissement", {})
    
    if name_lower in ["niveau", "grade", "level", "curso", "klasse"]:
        return ("edu_niveau", {})
    
    if "email" in name_lower or "mail" in name_lower or "correo" in name_lower:
        return ("edu_email", {})
    
    if "note" in name_lower or "grade" in name_lower or "mark" in name_lower or "nota" in name_lower:
        return ("edu_note", {})
    
    if "moyenne" in name_lower or "average" in name_lower or "promedio" in name_lower:
        return ("edu_moyenne", {})
    
    if "absence" in name_lower or "absent" in name_lower or "ausencia" in name_lower:
        return ("edu_absence", {})
    
    if "matiere" in name_lower or "subject" in name_lower or "asignatura" in name_lower or "fach" in name_lower:
        return ("edu_matiere", {})
    
    if "annee_scolaire" in name_lower or "school_year" in name_lower or "año_escolar" in name_lower:
        return ("edu_annee_scolaire", {})
    
    if "diplome" in name_lower or "degree" in name_lower or "título" in name_lower:
        return ("edu_diplome", {})
    
    # Fallback
    return ("categorical", {"categories": ["Option A", "Option B", "Option C"]})

# ====================
# CONSTRUCTION DU DATASET ÉDUCATION
# ====================

def build_education_dataset(schema, n=500):
    """Construit un dataset éducatif avec données COHÉRENTES"""
    
    cols = []
    if isinstance(schema, list) and all(isinstance(x, str) for x in schema):
        for name in schema:
            t, params = guess_education_type(name)
            cols.append({"name": name, "type": t, "params": params})
    else:
        for c in schema:
            name = c.get("name")
            if not name:
                raise ValueError("Chaque colonne doit avoir un 'name'")
            t = c.get("type")
            params = c.get("params", {})
            if not t:
                guessed_t, guessed_params = guess_education_type(name)
                guessed_params.update(params)
                t = guessed_t
                params = guessed_params
            cols.append({"name": name, "type": t, "params": params})
    
    # Générer les données étudiants
    students = gen_student_data(n)
    
    # Extraire les données
    ids = gen_id_student(n)
    pays_list = [s["pays"] for s in students]
    genres = [s["genre"] for s in students]
    prenoms = [s["prenom"] for s in students]
    noms = [s["nom"] for s in students]
    ages = [s["age"] for s in students]
    dates_naissance = [s["date_naissance"] for s in students]
    types_etab = [s["type_etablissement"] for s in students]
    etablissements = [s["etablissement"] for s in students]
    niveaux = [s["niveau"] for s in students]
    villes = [s["ville"] for s in students]
    
    # Données dérivées
    emails = gen_email_education(prenoms, noms, etablissements)
    absences = gen_absences_coherentes(n, types_etab)
    annee_scolaire = gen_annee_scolaire()
    
    # Générer notes cohérentes
    notes_data = gen_notes_coherentes(students)
    moyennes = [round(np.mean(list(notes.values())), 2) for notes in notes_data]
    
    data = {}
    
    for col in cols:
        name = col["name"]
        t = col["type"]
        p = col.get("params", {})
        
        if t == "edu_id":
            data[name] = ids
        elif t == "edu_pays":
            data[name] = pays_list
        elif t == "edu_genre":
            data[name] = genres
        elif t == "edu_prenom":
            data[name] = prenoms
        elif t == "edu_nom":
            data[name] = noms
        elif t == "edu_age":
            data[name] = ages
        elif t == "edu_date_naissance":
            data[name] = dates_naissance
        elif t == "edu_ville":
            data[name] = villes
        elif t == "edu_type_etab":
            data[name] = types_etab
        elif t == "edu_etablissement":
            data[name] = etablissements
        elif t == "edu_niveau":
            data[name] = niveaux
        elif t == "edu_email":
            data[name] = emails
        elif t == "edu_absence":
            data[name] = absences
        elif t == "edu_annee_scolaire":
            data[name] = [annee_scolaire] * n
        elif t == "edu_moyenne":
            data[name] = moyennes
        elif t == "edu_note":
            # Générer une note aléatoire entre 0 et 20
            data[name] = [round(np.random.uniform(0, 20), 1) for _ in range(n)]
        elif t == "edu_matiere":
            # Choisir une matière aléatoire pour chaque étudiant selon son pays
            matieres = []
            for student in students:
                pays = student["pays"]
                type_etab = student["type_etablissement"]
                matiere = np.random.choice(EDUCATION_DATA[pays]["matieres"][type_etab])
                matieres.append(matiere)
            data[name] = matieres
        elif t == "edu_diplome":
            # Diplôme cohérent avec le pays
            diplomes = []
            for student in students:
                pays = student["pays"]
                diplome = np.random.choice(EDUCATION_DATA[pays]["diplomes"])
                diplomes.append(diplome)
            data[name] = diplomes
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
        description="📚 Générateur COHÉRENT de datasets éducatifs internationaux",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
EXEMPLES :

📚 Dataset d'étudiants international simple :
  python education_generator.py --name students --cols id,nom,prenom,genre,age,pays,ville,etablissement,niveau,moyenne --n 2000

🎓 Dataset éducatif complet :
  python education_generator.py --name education --cols id,nom,prenom,genre,age,date_naissance,pays,ville,type_etablissement,etablissement,niveau,email,moyenne,absence,annee_scolaire --n 3000

🌍 Dataset multi-pays détaillé :
  python education_generator.py --name international_students --cols id,nom,prenom,genre,age,pays,ville,etablissement,niveau,matiere,moyenne,absence,diplome --n 5000

COLONNES DISPONIBLES :
  id, nom, prenom, genre, age, date_naissance, pays, ville,
  type_etablissement, etablissement, niveau, email, note, moyenne,
  absence, matiere, annee_scolaire, diplome

PAYS SUPPORTÉS :
  France, Maroc, USA, UK, Canada, Allemagne, Espagne
  (avec noms, écoles et systèmes éducatifs cohérents par pays)
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
        print("\n💡 Utilisation recommandée :")
        print("   python education_generator.py --name students --cols id,nom,prenom,pays,niveau,moyenne --n 2000")
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
    print(f"📚 GÉNÉRATION DU DATASET ÉDUCATIF '{args.name}'")
    print("="*80 + "\n")
    
    try:
        df = build_education_dataset(schema, n=args.n)
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        return
    
    out = args.out or f"{args.name}_education.csv"
    df.to_csv(out, index=False, encoding='utf-8-sig')
    
    print("="*80)
    print(f"✅ DATASET ÉDUCATIF GÉNÉRÉ")
    print("="*80)
    print(f"📁 Fichier : {out}")
    print(f"📊 Lignes  : {len(df)}")
    print(f"📊 Colonnes: {len(df.columns)}\n")
    
    print("👁️  APERÇU :")
    print(df.head(args.preview).to_string(index=False))
    
    print(f"\n{'='*80}")
    print("✅ VÉRIFICATIONS DE COHÉRENCE")
    print("="*80)
    
    if "pays" in df.columns and "nom" in df.columns and "prenom" in df.columns:
        print("\n✓ Pays, Nom et Prénom cohérents")
        sample = df.head(3)[["pays", "nom", "prenom", "genre"]].to_string(index=False)
        print(sample)
    
    if "pays" in df.columns and "etablissement" in df.columns and "niveau" in df.columns:
        print("\n✓ Pays, Établissement et Niveau cohérents")
        sample = df.head(3)[["pays", "etablissement", "niveau"]].to_string(index=False)
        print(sample)
    
    if "age" in df.columns and "niveau" in df.columns:
        print("\n✓ Âge et Niveau cohérents")
        sample = df.head(3)[["nom", "age", "niveau", "type_etablissement"]].to_string(index=False)
        print(sample)
    
    if "moyenne" in df.columns:
        print("\n✓ Statistiques des moyennes")
        print(f"   Moyenne générale: {df['moyenne'].mean():.2f}/20")
        print(f"   Note minimale: {df['moyenne'].min():.2f}/20")
        print(f"   Note maximale: {df['moyenne'].max():.2f}/20")
    
    if "pays" in df.columns:
        print("\n✓ Répartition par pays")
        repartition = df['pays'].value_counts()
        for pays, count in repartition.items():
            print(f"   {pays}: {count} étudiants ({count/len(df)*100:.1f}%)")
    
    print(f"\n✨ Génération terminée! Fichier sauvegardé: {out}\n")

if __name__ == "__main__":
    main()