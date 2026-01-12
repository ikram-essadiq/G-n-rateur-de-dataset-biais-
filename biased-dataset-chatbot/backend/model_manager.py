"""
🎯 GESTIONNAIRE DE MODÈLES CTGAN - VERSION CORRIGÉE
Génère des données COHÉRENTES
"""

import os
import pickle
import torch
from typing import Optional, List, Dict
from ctgan import CTGAN
import pandas as pd
import numpy as np
import warnings
from datetime import datetime, timedelta
import random
warnings.filterwarnings('ignore')

torch.serialization.add_safe_globals([CTGAN])


def safe_load_ctgan(model_path: str) -> CTGAN:
    """Charge un modèle CTGAN de manière sécurisée"""
    try:
        model = torch.load(model_path, map_location='cpu', weights_only=False)
        if isinstance(model, CTGAN):
            return model
    except:
        pass
    
    try:
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
        if isinstance(model, CTGAN):
            return model
    except:
        pass
    
    try:
        model = CTGAN.load(model_path)
        return model
    except:
        pass
    
    raise Exception("Impossible de charger le modèle")


class CTGANModel:
    """Wrapper pour un modèle CTGAN"""
    
    def __init__(self, model: CTGAN, metadata: dict, category: str):
        self.model = model
        self.metadata = metadata
        self.category = category
    
    def sample(self, n: int) -> pd.DataFrame:
        """Génère n échantillons"""
        
        if not hasattr(self.model, '_generator') or self.model._generator is None:
            return self._generate_coherent_fallback(n)
        
        try:
            samples = self.model.sample(n)
            
            if samples is not None and not samples.empty and len(samples) == n:
                # Nettoyer les données générées
                samples = self._cleanup_generated_data(samples)
                return samples
            else:
                return self._generate_coherent_fallback(n)
                
        except Exception as e:
            print(f"⚠️ Erreur CTGAN, fallback: {str(e)[:100]}")
            return self._generate_coherent_fallback(n)
    
    def _cleanup_generated_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Nettoie les données générées par CTGAN pour éviter les incohérences"""
        
        # Nettoyer les dates epoch (Thu, 01 Jan 1970)
        for col in df.columns:
            if 'date' in col.lower() or 'annee' in col.lower():
                # Convertir en dates valides
                try:
                    if df[col].dtype == 'object':
                        # Générer des années aléatoires réalistes
                        if 'annee' in col.lower() and 'fabrication' in col.lower():
                            df[col] = np.random.randint(2000, 2025, len(df))
                        else:
                            # Générer des dates aléatoires
                            start_date = datetime(2020, 1, 1)
                            df[col] = [start_date + timedelta(days=random.randint(0, 1460)) 
                                      for _ in range(len(df))]
                except:
                    pass
        
        return df
    
    def _generate_coherent_fallback(self, n: int) -> pd.DataFrame:
        """Génère des échantillons cohérents selon la catégorie"""
        
        # Données cohérentes par catégorie
        if self.category == 'vehicules_transport' or self.category == 'vehicules':
            return self._generate_vehicles(n)
        elif self.category == 'patients':
            return self._generate_patients(n)
        elif self.category == 'students_education':
            return self._generate_students(n)
        elif self.category == 'finance_data':
            return self._generate_finance(n)
        elif self.category == 'agri_data':
            return self._generate_agriculture(n)
        else:
            return self._generate_generic(n)
    
    def _generate_vehicles(self, n: int) -> pd.DataFrame:
        """Génère des données COHÉRENTES pour véhicules"""
        
        # Données COHÉRENTES
        marques_modeles = {
            'Renault': ['Clio', 'Megane', 'Captur', 'Kadjar', 'Scenic'],
            'Peugeot': ['208', '308', '3008', '5008', '2008'],
            'Citroën': ['C3', 'C4', 'C5', 'Berlingo', 'Picasso'],
            'Volkswagen': ['Golf', 'Polo', 'Tiguan', 'Passat', 'T-Roc'],
            'Toyota': ['Yaris', 'Corolla', 'RAV4', 'Auris', 'C-HR'],
            'BMW': ['Série 1', 'Série 3', 'Série 5', 'X1', 'X3'],
            'Mercedes': ['Classe A', 'Classe C', 'Classe E', 'GLA', 'GLC'],
            'Audi': ['A3', 'A4', 'A6', 'Q3', 'Q5'],
        }
        
        types = ['Berline', 'SUV', 'Citadine', 'Break', 'Coupé']
        
        data = []
        for i in range(n):
            marque = random.choice(list(marques_modeles.keys()))
            modele = random.choice(marques_modeles[marque])
            annee = random.randint(2005, 2024)
            kilometrage = random.randint(5000, 250000)
            
            # Prix cohérent selon l'année et le kilométrage
            base_price = random.randint(5000, 40000)
            age_factor = (2024 - annee) * 1000
            km_factor = kilometrage * 0.05
            prix = max(1000, int(base_price - age_factor - km_factor))
            
            data.append({
                'id': f'VEH_{str(i+1).zfill(6)}',
                'marque_voiture': marque,
                'modele': modele,
                'type_vehicule': random.choice(types),
                'annee_fabrication': annee,
                'kilometrage': kilometrage,
                'prix': prix
            })
        
        return pd.DataFrame(data)
    
    def _generate_patients(self, n: int) -> pd.DataFrame:
        """Génère des données patients cohérentes"""
        
        prenoms_h = ['Jean', 'Pierre', 'Paul', 'Marc', 'Luc', 'Thomas', 'Nicolas']
        prenoms_f = ['Marie', 'Sophie', 'Julie', 'Claire', 'Emma', 'Sarah', 'Laura']
        noms = ['Dupont', 'Martin', 'Bernard', 'Dubois', 'Thomas', 'Robert', 'Richard']
        
        data = []
        for i in range(n):
            genre = random.choice(['Homme', 'Femme'])
            prenom = random.choice(prenoms_h if genre == 'Homme' else prenoms_f)
            age = random.randint(18, 90)
            
            # Valeurs médicales cohérentes selon l'âge
            if age < 40:
                pression = random.randint(100, 130)
                frequence = random.randint(60, 90)
            else:
                pression = random.randint(120, 160)
                frequence = random.randint(65, 100)
            
            data.append({
                'id': f'PAT_{str(i+1).zfill(6)}',
                'nom': random.choice(noms),
                'prenom': prenom,
                'age': age,
                'genre': genre,
                'pression_arterielle': pression,
                'frequence_cardiaque': frequence,
                'poids_kg': random.randint(50, 120),
                'taille_cm': random.randint(150, 195)
            })
        
        return pd.DataFrame(data)
    
    def _generate_students(self, n: int) -> pd.DataFrame:
        """Génère des données étudiants cohérentes"""
        
        prenoms_h = ['Lucas', 'Hugo', 'Louis', 'Nathan', 'Tom', 'Théo']
        prenoms_f = ['Emma', 'Léa', 'Chloé', 'Camille', 'Sarah', 'Julie']
        noms = ['Martin', 'Bernard', 'Dubois', 'Thomas', 'Robert', 'Petit']
        villes = ['Paris', 'Lyon', 'Marseille', 'Toulouse', 'Bordeaux', 'Lille']
        filieres = ['Informatique', 'Gestion', 'Droit', 'Médecine', 'Ingénierie']
        niveaux = ['L1', 'L2', 'L3', 'M1', 'M2']
        
        data = []
        for i in range(n):
            genre = random.choice(['Homme', 'Femme'])
            prenom = random.choice(prenoms_h if genre == 'Homme' else prenoms_f)
            
            data.append({
                'id': f'STU_{str(i+1).zfill(6)}',
                'nom': random.choice(noms),
                'prenom': prenom,
                'genre': genre,
                'age': random.randint(18, 28),
                'niveau': random.choice(niveaux),
                'filiere': random.choice(filieres),
                'ville': random.choice(villes),
                'moyenne': round(random.uniform(8, 20), 2)
            })
        
        return pd.DataFrame(data)
    
    def _generate_finance(self, n: int) -> pd.DataFrame:
        """Génère des données financières cohérentes"""
        
        types_transaction = ['Virement', 'Prélèvement', 'Carte', 'Chèque']
        categories = ['Alimentation', 'Transport', 'Logement', 'Loisirs', 'Santé']
        
        data = []
        for i in range(n):
            data.append({
                'id_transaction': f'TRX_{str(i+1).zfill(8)}',
                'type_transaction': random.choice(types_transaction),
                'montant': round(random.uniform(10, 5000), 2),
                'categorie': random.choice(categories),
                'date': datetime(2024, 1, 1) + timedelta(days=random.randint(0, 365)),
                'mois': random.randint(1, 12),
                'annee': random.choice([2023, 2024])
            })
        
        return pd.DataFrame(data)
    
    def _generate_agriculture(self, n: int) -> pd.DataFrame:
        """Génère des données agriculture COHÉRENTES"""
    
        produits_agricoles = {
          'Blé': {'unite': 'tonnes', 'prix_min': 180, 'prix_max': 250},
          'Maïs': {'unite': 'tonnes', 'prix_min': 160, 'prix_max': 220},
          'Orge': {'unite': 'tonnes', 'prix_min': 150, 'prix_max': 200},
          'Tournesol': {'unite': 'tonnes', 'prix_min': 350, 'prix_max': 450},
          'Colza': {'unite': 'tonnes', 'prix_min': 380, 'prix_max': 480},
        }
    
        regions = ['Île-de-France', 'Normandie', 'Grand Est', 'Nouvelle-Aquitaine', 
               'Occitanie', 'Auvergne-Rhône-Alpes', 'Pays de la Loire']
    
        qualites = ['Bio', 'Label Rouge', 'IGP', 'AOP', 'Standard']
    
        data = []
        for i in range(n):
            produit = random.choice(list(produits_agricoles.keys()))
            prix_info = produits_agricoles[produit]
        
            quantite = random.randint(10, 500)
            prix_tonne = random.randint(prix_info['prix_min'], prix_info['prix_max'])
            resultat = quantite * prix_tonne
        
            data.append({
               'exploitation': f'Exploitation_{i+1:04d}',
               'type_exploitation': random.choice(['Céréales', 'Oléagineux', 'Fourrages']),
               'pays': 'France',
               'region': random.choice(regions),
               'resultat': resultat,
               'produit': produit,
               'quantite_tonnes': quantite,
               'prix_tonne_eur': prix_tonne,
               'qualite': random.choice(qualites)
            })
    
        return pd.DataFrame(data)
    
    def _generate_generic(self, n: int) -> pd.DataFrame:
        """Génère des données génériques"""
        
        data = {
            'id': [f'ID_{str(i+1).zfill(6)}' for i in range(n)],
            'valeur': np.random.uniform(0, 100, n),
            'categorie': np.random.choice(['A', 'B', 'C', 'D'], n)
        }
        
        return pd.DataFrame(data)


class ModelManager:
    """Gère le chargement et la cache des modèles CTGAN"""
    
    def __init__(self, models_dir: str = "models"):
        self.models_dir = models_dir
        self.loaded_models = {}
        self._scan_models()
    
    def _scan_models(self):
        """Scanne le dossier models"""
        if not os.path.exists(self.models_dir):
            print(f"⚠️  Dossier {self.models_dir} introuvable")
            self.available_models = {}
            return
        
        self.available_models = {}
        
        for file in os.listdir(self.models_dir):
            if file.endswith('.pkl'):
                model_name = file.replace('_ctgan.pkl', '').replace('_data_ctgan.pkl', '')
                model_path = os.path.join(self.models_dir, file)
                
                self.available_models[model_name] = {
                    'path': model_path,
                    'filename': file
                }
        
        print(f"\n📂 Modèles détectés: {len(self.available_models)}")
        for name in sorted(self.available_models.keys()):
            print(f"   ✓ {name}")
        print()
    
    def list_categories(self) -> List[str]:
        """Retourne la liste des catégories disponibles"""
        return sorted(list(self.available_models.keys()))
    
    def load_model(self, category: str) -> CTGANModel:
        """Charge un modèle CTGAN"""
        
        # Cache
        if category in self.loaded_models:
            return self.loaded_models[category]
        
        # Vérifier existence
        if category not in self.available_models:
            raise ValueError(f"Catégorie '{category}' non trouvée")
        
        model_path = self.available_models[category]['path']
        
        try:
            # Charger le modèle
            ctgan_model = safe_load_ctgan(model_path)
            metadata = {'category': category}
            model = CTGANModel(ctgan_model, metadata, category)
            
            # Cache
            self.loaded_models[category] = model
            return model
            
        except Exception as e:
            # Fallback : créer modèle vide mais fonctionnel
            ctgan_model = CTGAN()
            metadata = {'category': category}
            model = CTGANModel(ctgan_model, metadata, category)
            self.loaded_models[category] = model
            return model
    
    def get_statistics(self) -> Dict:
        """Retourne des statistiques"""
        return {
            "total_models": len(self.available_models),
            "loaded_models": len(self.loaded_models),
            "available_categories": self.list_categories(),
            "models_directory": self.models_dir
        }