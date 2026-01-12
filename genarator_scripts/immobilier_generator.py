"""
GÉNÉRATEUR DE DONNÉES IMMOBILIÈRES - Version Générale
Génère des données immobilières réalistes pour tout type de marché
"""

import json
import argparse
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

np.random.seed(42)

# ====================
# DONNÉES IMMOBILIÈRES GÉNÉRALES
# ====================

TYPES_LOGEMENT = ["Appartement", "Maison", "Villa", "Studio", "Duplex", "Loft", "Penthouse", "Terrain"]

# Types de transaction
TYPES_TRANSACTION = ["Vente", "Location", "Location saisonnière"]

# États du bien
ETATS = ["Neuf", "Excellent état", "Bon état", "À rénover", "À restaurer"]

# Type de chauffage
TYPES_CHAUFFAGE = ["Gaz", "Électrique", "Fioul", "Pompe à chaleur", "Climatisation réversible", "Chauffage central", "Aucun", "Autre"]

# Classe énergétique
CLASSES_ENERGIE = ["A", "B", "C", "D", "E", "F", "G", "Non renseigné"]

# Exposition/Orientation
ORIENTATIONS = ["Nord", "Sud", "Est", "Ouest", "Nord-Est", "Nord-Ouest", "Sud-Est", "Sud-Ouest"]

# Type de cuisine
TYPES_CUISINE = ["Équipée", "Semi-équipée", "Non équipée", "Américaine", "Indépendante"]

# Standing
STANDINGS = ["Standard", "Moyen", "Haut standing", "Luxe"]

# Disponibilité
DISPONIBILITES = ["Immédiate", "1 mois", "3 mois", "À convenir"]

# ====================
# GÉNÉRATEURS
# ====================

def gen_bien_immobilier(n):
    """Génère des données de biens immobiliers cohérentes"""
    biens = []
    
    for _ in range(n):
        # Type de logement
        type_logement = np.random.choice(TYPES_LOGEMENT, p=[0.40, 0.20, 0.15, 0.12, 0.06, 0.03, 0.02, 0.02])
        
        # Surface selon le type
        if type_logement == "Studio":
            surface = np.random.randint(20, 40)
            chambres = 0
            pieces = 1
        elif type_logement == "Appartement":
            surface = np.random.randint(45, 180)
            chambres = np.random.randint(1, 5)
            pieces = chambres + np.random.randint(1, 3)
        elif type_logement in ["Maison", "Villa"]:
            surface = np.random.randint(80, 400)
            chambres = np.random.randint(2, 6)
            pieces = chambres + np.random.randint(2, 4)
        elif type_logement == "Duplex":
            surface = np.random.randint(70, 200)
            chambres = np.random.randint(2, 4)
            pieces = chambres + np.random.randint(1, 3)
        elif type_logement == "Loft":
            surface = np.random.randint(60, 150)
            chambres = np.random.randint(1, 3)
            pieces = chambres + 1
        elif type_logement == "Penthouse":
            surface = np.random.randint(100, 300)
            chambres = np.random.randint(2, 5)
            pieces = chambres + np.random.randint(2, 4)
        else:  # Terrain
            surface = np.random.randint(200, 5000)
            chambres = 0
            pieces = 0
        
        # Salles de bain (cohérent avec chambres)
        if chambres == 0:
            salles_bain = 1 if type_logement != "Terrain" else 0
        else:
            salles_bain = max(1, min(chambres, np.random.randint(1, chambres + 2)))
        
        # WC séparés
        wc = np.random.randint(0, salles_bain + 2) if type_logement != "Terrain" else 0
        
        # Étage (pour appartements/studios/duplex/loft)
        if type_logement in ["Appartement", "Studio", "Duplex", "Loft"]:
            etage = np.random.randint(0, 20)
            total_etages = max(etage + np.random.randint(1, 10), etage + 1)
            ascenseur = etage > 2 and np.random.rand() > 0.2
        elif type_logement == "Penthouse":
            total_etages = np.random.randint(10, 30)
            etage = total_etages - 1  # Dernier étage
            ascenseur = True
        else:
            etage = None
            total_etages = None
            ascenseur = False
        
        # État
        etat = np.random.choice(ETATS, p=[0.15, 0.25, 0.35, 0.20, 0.05])
        
        # Année construction
        annee_construction = np.random.randint(1950, 2025)
        if etat == "Neuf":
            annee_construction = np.random.randint(2020, 2025)
        elif etat == "Excellent état":
            annee_construction = np.random.randint(2000, 2024)
        
        # Prix base (entre 50k et 5M pour simplifier)
        prix_base = np.random.randint(50000, 5000000)
        
        # Ajustement prix selon caractéristiques
        facteur_prix = 1.0
        
        if etat == "Neuf":
            facteur_prix *= 1.20
        elif etat == "Excellent état":
            facteur_prix *= 1.10
        elif etat == "À rénover":
            facteur_prix *= 0.70
        elif etat == "À restaurer":
            facteur_prix *= 0.50
        
        if type_logement == "Penthouse":
            facteur_prix *= 1.50
        elif type_logement == "Villa":
            facteur_prix *= 1.30
        
        prix_total = int(prix_base * facteur_prix)
        prix_m2 = int(prix_total / surface) if surface > 0 else 0
        
        # Type transaction
        type_transaction = np.random.choice(TYPES_TRANSACTION, p=[0.60, 0.35, 0.05])
        
        # Si location, calculer loyer mensuel
        if type_transaction == "Location":
            loyer_mensuel = int(prix_total * np.random.uniform(0.003, 0.006))
            prix_affiche = loyer_mensuel
        elif type_transaction == "Location saisonnière":
            loyer_mensuel = int(prix_total * np.random.uniform(0.008, 0.015))
            prix_affiche = loyer_mensuel
        else:
            loyer_mensuel = None
            prix_affiche = prix_total
        
        # Chauffage
        chauffage = np.random.choice(TYPES_CHAUFFAGE, p=[0.25, 0.20, 0.15, 0.15, 0.10, 0.10, 0.03, 0.02])
        
        # Classe énergétique
        if annee_construction >= 2015:
            classe_energie = np.random.choice(CLASSES_ENERGIE[:5], p=[0.15, 0.30, 0.35, 0.15, 0.05])
        elif annee_construction >= 2000:
            classe_energie = np.random.choice(CLASSES_ENERGIE[2:7], p=[0.20, 0.35, 0.30, 0.10, 0.05])
        else:
            classe_energie = np.random.choice(CLASSES_ENERGIE[4:], p=[0.25, 0.35, 0.30, 0.10])
        
        # Équipements
        parking = (type_logement in ["Maison", "Villa", "Penthouse"]) or (np.random.rand() > 0.4)
        nb_parking = np.random.randint(1, 4) if parking else 0
        
        cave = type_logement in ["Appartement", "Duplex", "Loft"] and np.random.rand() > 0.5
        balcon = type_logement != "Terrain" and type_logement != "Maison" and np.random.rand() > 0.4
        terrasse = (type_logement in ["Maison", "Villa", "Penthouse"]) or (np.random.rand() > 0.6)
        jardin = type_logement in ["Maison", "Villa"] and np.random.rand() > 0.4
        surface_jardin = np.random.randint(20, 500) if jardin else None
        piscine = type_logement in ["Villa", "Maison"] and np.random.rand() > 0.8
        gardien = type_logement in ["Villa", "Penthouse"] and np.random.rand() > 0.7
        
        # Cuisine
        cuisine = np.random.choice(TYPES_CUISINE, p=[0.35, 0.25, 0.15, 0.15, 0.10])
        
        # Standing
        if type_logement in ["Penthouse", "Villa"]:
            standing = np.random.choice(STANDINGS, p=[0.05, 0.15, 0.40, 0.40])
        elif type_logement == "Loft":
            standing = np.random.choice(STANDINGS, p=[0.10, 0.30, 0.45, 0.15])
        else:
            standing = np.random.choice(STANDINGS, p=[0.30, 0.40, 0.25, 0.05])
        
        # Meublé
        meuble = type_transaction != "Vente" and np.random.rand() > 0.5
        
        # Disponibilité
        disponibilite = np.random.choice(DISPONIBILITES, p=[0.50, 0.20, 0.15, 0.15])
        
        # Charges mensuelles (pour appartements principalement)
        charges = None
        if type_logement in ["Appartement", "Duplex", "Loft", "Penthouse"]:
            charges = np.random.randint(50, 500)
        
        # Taxe foncière annuelle
        taxe_fonciere = int(prix_total * np.random.uniform(0.001, 0.003)) if type_transaction == "Vente" else None
        
        # Description auto-générée
        desc_parts = [f"{type_logement} {etat.lower()}"]
        if chambres > 0:
            desc_parts.append(f"{chambres} chambre{'s' if chambres > 1 else ''}")
        desc_parts.append(f"{surface} m²")
        if jardin:
            desc_parts.append("avec jardin")
        if piscine:
            desc_parts.append("et piscine")
        
        description = ", ".join(desc_parts)
        
        biens.append({
            "type_logement": type_logement,
            "type_bien": type_logement,  # Alias
            "surface": surface,
            "pieces": pieces,
            "chambres": chambres,
            "salles_bain": salles_bain,
            "wc": wc,
            "etage": etage,
            "total_etages": total_etages,
            "ascenseur": ascenseur,
            "prix_m2": prix_m2,
            "prix_total": prix_total,
            "prix": prix_total,  # Alias
            "type_transaction": type_transaction,
            "loyer_mensuel": loyer_mensuel,
            "prix_affiche": prix_affiche,
            "etat": etat,
            "annee_construction": annee_construction,
            "chauffage": chauffage,
            "classe_energie": classe_energie,
            "parking": parking,
            "nb_parking": nb_parking,
            "cave": cave,
            "balcon": balcon,
            "terrasse": terrasse,
            "jardin": jardin,
            "surface_jardin": surface_jardin,
            "piscine": piscine,
            "gardien": gardien,
            "orientation": np.random.choice(ORIENTATIONS),
            "cuisine": cuisine,
            "standing": standing,
            "meuble": meuble,
            "disponibilite": disponibilite,
            "charges": charges,
            "taxe_fonciere": taxe_fonciere,
            "description": description
        })
    
    return biens

def gen_id(n, prefix="BIEN"):
    """Génère des identifiants immobiliers"""
    return [f"{prefix}_{str(i+1).zfill(6)}" for i in range(n)]

# ====================
# CONSTRUCTION DU DATASET
# ====================

def build_dataset(cols, n=500):
    """Construit le dataset immobilier"""
    
    # Générer données de base
    biens = gen_bien_immobilier(n)
    ids = gen_id(n, "BIEN")
    
    # Construire dataframe
    data = {}
    
    for col in cols:
        col_lower = col.lower()
        
        if col_lower in ["id", "id_bien", "reference"]:
            data[col] = ids
        elif col_lower in ["type", "type_bien", "type_logement"]:
            data[col] = [b["type_logement"] for b in biens]
        elif col_lower in ["surface", "surface_m2", "surface_habitable"]:
            data[col] = [b["surface"] for b in biens]
        elif col_lower in ["pieces", "nb_pieces"]:
            data[col] = [b["pieces"] for b in biens]
        elif col_lower in ["chambres", "nb_chambres"]:
            data[col] = [b["chambres"] for b in biens]
        elif col_lower in ["salles_bain", "nb_salles_bain", "sdb"]:
            data[col] = [b["salles_bain"] for b in biens]
        elif col_lower in ["wc", "nb_wc"]:
            data[col] = [b["wc"] for b in biens]
        elif col_lower == "etage":
            data[col] = [b["etage"] if b["etage"] is not None else "" for b in biens]
        elif col_lower in ["total_etages", "nb_etages"]:
            data[col] = [b["total_etages"] if b["total_etages"] is not None else "" for b in biens]
        elif col_lower == "ascenseur":
            data[col] = ["Oui" if b["ascenseur"] else "Non" for b in biens]
        elif col_lower in ["prix_m2", "prix_au_m2"]:
            data[col] = [b["prix_m2"] for b in biens]
        elif col_lower in ["prix", "prix_total"]:
            data[col] = [b["prix_total"] for b in biens]
        elif col_lower == "prix_affiche":
            data[col] = [b["prix_affiche"] for b in biens]
        elif col_lower in ["type_transaction", "transaction"]:
            data[col] = [b["type_transaction"] for b in biens]
        elif col_lower in ["loyer", "loyer_mensuel"]:
            data[col] = [b["loyer_mensuel"] if b["loyer_mensuel"] else "" for b in biens]
        elif col_lower == "etat":
            data[col] = [b["etat"] for b in biens]
        elif col_lower in ["annee_construction", "annee", "construction"]:
            data[col] = [b["annee_construction"] for b in biens]
        elif col_lower == "chauffage":
            data[col] = [b["chauffage"] for b in biens]
        elif col_lower in ["classe_energie", "dpe", "energie"]:
            data[col] = [b["classe_energie"] for b in biens]
        elif col_lower == "parking":
            data[col] = ["Oui" if b["parking"] else "Non" for b in biens]
        elif col_lower in ["nb_parking", "places_parking"]:
            data[col] = [b["nb_parking"] for b in biens]
        elif col_lower == "cave":
            data[col] = ["Oui" if b["cave"] else "Non" for b in biens]
        elif col_lower == "balcon":
            data[col] = ["Oui" if b["balcon"] else "Non" for b in biens]
        elif col_lower == "terrasse":
            data[col] = ["Oui" if b["terrasse"] else "Non" for b in biens]
        elif col_lower == "jardin":
            data[col] = ["Oui" if b["jardin"] else "Non" for b in biens]
        elif col_lower in ["surface_jardin", "jardin_m2"]:
            data[col] = [b["surface_jardin"] if b["surface_jardin"] else "" for b in biens]
        elif col_lower == "piscine":
            data[col] = ["Oui" if b["piscine"] else "Non" for b in biens]
        elif col_lower == "gardien":
            data[col] = ["Oui" if b["gardien"] else "Non" for b in biens]
        elif col_lower == "orientation":
            data[col] = [b["orientation"] for b in biens]
        elif col_lower == "cuisine":
            data[col] = [b["cuisine"] for b in biens]
        elif col_lower == "standing":
            data[col] = [b["standing"] for b in biens]
        elif col_lower == "meuble":
            data[col] = ["Oui" if b["meuble"] else "Non" for b in biens]
        elif col_lower == "disponibilite":
            data[col] = [b["disponibilite"] for b in biens]
        elif col_lower in ["charges", "charges_mensuelles"]:
            data[col] = [b["charges"] if b["charges"] else "" for b in biens]
        elif col_lower in ["taxe_fonciere", "taxe"]:
            data[col] = [b["taxe_fonciere"] if b["taxe_fonciere"] else "" for b in biens]
        elif col_lower == "description":
            data[col] = [b["description"] for b in biens]
        else:
            # Colonne non reconnue, remplir avec valeurs par défaut
            data[col] = ["N/A"] * n
    
    return pd.DataFrame(data)

# ====================
# CLI
# ====================

def main():
    parser = argparse.ArgumentParser(
        description="🏠 Générateur de données immobilières - Version Générale",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
EXEMPLES D'UTILISATION :

🏢 Dataset complet :
  python immobilier_gen.py --name biens --cols id,type_logement,surface,chambres,prix,etat,chauffage --n 1000

🏡 Dataset avec équipements :
  python immobilier_gen.py --name properties --cols id,type_bien,surface,pieces,prix,parking,jardin,piscine,standing --n 500

📊 Dataset locations :
  python immobilier_gen.py --name locations --cols id,type_logement,surface,type_transaction,loyer_mensuel,meuble,charges --n 300

COLONNES DISPONIBLES (comme dans l'image + autres) :
  • id, reference                → Identifiant unique
  • type_logement, type_bien     → Type (Appartement, Maison, Villa, etc.)
  • surface, surface_m2          → Surface en m²
  • pieces, nb_pieces            → Nombre de pièces
  • chambres, nb_chambres        → Nombre de chambres
  • salles_bain, sdb             → Salles de bain
  • wc, nb_wc                    → WC séparés
  • etage                        → Étage
  • total_etages, nb_etages      → Nombre d'étages total
  • ascenseur                    → Oui/Non
  • prix, prix_total             → Prix total
  • prix_m2                      → Prix au m²
  • type_transaction             → Vente/Location
  • loyer_mensuel                → Loyer mensuel
  • etat                         → État du bien
  • annee_construction           → Année de construction
  • chauffage                    → Type de chauffage
  • classe_energie, dpe          → Classe énergétique (A-G)
  • parking                      → Parking Oui/Non
  • nb_parking                   → Nombre de places
  • cave, balcon, terrasse       → Équipements Oui/Non
  • jardin                       → Jardin Oui/Non
  • surface_jardin               → Surface du jardin
  • piscine, gardien             → Oui/Non
  • orientation                  → Orientation
  • cuisine                      → Type de cuisine
  • standing                     → Standing du bien
  • meuble                       → Meublé Oui/Non
  • disponibilite                → Disponibilité
  • charges                      → Charges mensuelles
  • taxe_fonciere                → Taxe foncière annuelle
  • description                  → Description auto-générée
        """
    )
    
    parser.add_argument("--name", required=True, help="Nom du dataset")
    parser.add_argument("--cols", required=True, help="Colonnes séparées par des virgules")
    parser.add_argument("--n", type=int, default=500, help="Nombre de lignes")
    parser.add_argument("--out", default=None, help="Fichier de sortie (défaut: {name}.csv)")
    parser.add_argument("--preview", type=int, default=10, help="Lignes à prévisualiser")
    
    args = parser.parse_args()
    
    # Parser les colonnes
    cols = [c.strip() for c in args.cols.split(",")]
    
    # Générer dataset
    print(f"\n{'='*80}")
    print(f"🏠 GÉNÉRATION DU DATASET '{args.name}'")
    print("="*80 + "\n")
    print(f"📊 Nombre de biens : {args.n}")
    print(f"📋 Colonnes : {', '.join(cols)}\n")
    
    try:
        df = build_dataset(cols, n=args.n)
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # Sauvegarder
    out = args.out or f"{args.name}.csv"
    df.to_csv(out, index=False, encoding='utf-8-sig')
    
    # Afficher résultats
    print("="*80)
    print(f"✅ DATASET GÉNÉRÉ")
    print("="*80)
    print(f"📁 Fichier : {out}")
    print(f"📊 Lignes  : {len(df)}")
    print(f"📊 Colonnes: {len(df.columns)}\n")
    
    print("👁️  APERÇU :")
    print(df.head(args.preview).to_string(index=False))
    
    # Statistiques
    print(f"\n{'='*80}")
    print("📈 STATISTIQUES")
    print("="*80)
    
    if "type_logement" in df.columns or "type_bien" in df.columns:
        col = "type_logement" if "type_logement" in df.columns else "type_bien"
        print(f"\n🏢 Répartition par type :")
        print(df[col].value_counts().to_string())
    
    if "prix" in df.columns or "prix_total" in df.columns:
        prix_col = "prix" if "prix" in df.columns else "prix_total"
        print(f"\n💰 Prix :")
        print(f"   Min  : {df[prix_col].min():,.0f}")
        print(f"   Max  : {df[prix_col].max():,.0f}")
        print(f"   Moy  : {df[prix_col].mean():,.0f}")
        print(f"   Med  : {df[prix_col].median():,.0f}")
    
    if "surface" in df.columns:
        print(f"\n📐 Surface (m²) :")
        print(f"   Min  : {df['surface'].min()}")
        print(f"   Max  : {df['surface'].max()}")
        print(f"   Moy  : {df['surface'].mean():.1f}")
    
    print(f"\n✨ Terminé!\n")

if __name__ == "__main__":
    main()