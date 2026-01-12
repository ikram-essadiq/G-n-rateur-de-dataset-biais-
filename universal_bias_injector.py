

import pandas as pd
import numpy as np
from datetime import datetime
import json
import os

class UniversalBiasInjector:
    """
    Module universel d'injection de biais
    Fonctionne avec n'importe quel dataset
    """
    
    # Bibliothèque de types de biais universels
    BIAS_TYPES = {
        "gender": {
            "description": "Biais basé sur le genre (M/F)",
            "required_columns": ["genre"],
            "target_numeric": True,
            "examples": ["salaire", "note", "score", "revenu", "age"]
        },
        "age": {
            "description": "Biais basé sur l'âge (seuil)",
            "required_columns": ["age"],
            "target_numeric": True,
            "examples": ["salaire", "taux_embauche", "score"]
        },
        "nationality": {
            "description": "Biais basé sur la nationalité",
            "required_columns": ["nationalite"],
            "target_numeric": True,
            "examples": ["salaire", "acces", "score"]
        },
        "location": {
            "description": "Biais géographique (ville/pays)",
            "required_columns": ["ville", "pays"],
            "target_numeric": True,
            "examples": ["salaire", "acces", "opportunites"]
        }
    }
    
    def __init__(self):
        self.applied_biases = []
    
    def detect_applicable_biases(self, df):
        """
        Détecte automatiquement quels biais peuvent être appliqués
        en fonction des colonnes disponibles
        """
        available_biases = {}
        columns = df.columns.tolist()
        
        for bias_type, config in self.BIAS_TYPES.items():
            # Vérifier si les colonnes requises existent
            required = config["required_columns"]
            
            if all(any(req.lower() in col.lower() for col in columns) for req in required):
                # Trouver les colonnes numériques cibles possibles
                numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
                
                available_biases[bias_type] = {
                    "description": config["description"],
                    "protected_attributes": [col for col in columns 
                                            if any(req.lower() in col.lower() 
                                                  for req in required)],
                    "possible_targets": numeric_cols,
                    "applicable": True
                }
        
        return available_biases
    
    def inject_bias(self, df, bias_type, target_column=None, 
                   intensity=1.0, custom_config=None):
        """
        Injecte un biais de manière universelle
        
        Args:
            df: DataFrame
            bias_type: Type de biais ("gender", "age", "nationality", etc.)
            target_column: Colonne cible (auto-détectée si None)
            intensity: Intensité (0.5=faible, 1.0=normal, 2.0=fort)
            custom_config: Configuration personnalisée
        """
        
        df_biased = df.copy()
        
        # Détecter les biais applicables
        applicable = self.detect_applicable_biases(df)
        
        if bias_type not in applicable:
            raise ValueError(
                f"Biais '{bias_type}' non applicable. "
                f"Biais disponibles : {list(applicable.keys())}"
            )
        
        # Configuration du biais
        config = {
            "bias_type": bias_type,
            "intensity": intensity,
            "timestamp": datetime.now().isoformat()
        }
        
        # Appliquer selon le type
        if bias_type == "gender":
            df_biased, details = self._apply_gender_bias(
                df_biased, target_column, intensity, custom_config
            )
            config.update(details)
        
        elif bias_type == "age":
            df_biased, details = self._apply_age_bias(
                df_biased, target_column, intensity, custom_config
            )
            config.update(details)
        
        elif bias_type == "nationality":
            df_biased, details = self._apply_nationality_bias(
                df_biased, target_column, intensity, custom_config
            )
            config.update(details)
        
        elif bias_type == "location":
            df_biased, details = self._apply_location_bias(
                df_biased, target_column, intensity, custom_config
            )
            config.update(details)
        
        self.applied_biases.append(config)
        
        return df_biased, config
    
    def _find_column(self, df, keywords):
        """Trouve une colonne basée sur des mots-clés"""
        for col in df.columns:
            if any(kw.lower() in col.lower() for kw in keywords):
                return col
        return None
    
    def _apply_gender_bias(self, df, target_col, intensity, custom_config):
        """Applique un biais de genre"""
        
        # Trouver la colonne genre
        gender_col = self._find_column(df, ["genre", "gender", "sexe"])
        
        if not gender_col:
            raise ValueError("Colonne 'genre' non trouvée")
        
        # Auto-détecter la colonne cible si non spécifiée
        if not target_col:
            # Chercher des colonnes comme age, score, etc.
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            
            # Priorité : age en premier (car présent dans votre dataset)
            for priority in ["age", "score", "note", "salaire"]:
                target_col = self._find_column(df, [priority])
                if target_col:
                    break
            
            # Sinon prendre la première colonne numérique
            if not target_col and len(numeric_cols) > 0:
                target_col = numeric_cols[0]
        
        if not target_col or target_col not in df.columns:
            raise ValueError(f"Colonne cible '{target_col}' non trouvée")
        
        # Configuration
        privileged_group = custom_config.get("privileged_group", "M") if custom_config else "M"
        base_factor = custom_config.get("factor", 1.15) if custom_config else 1.15
        
        # Ajuster avec l'intensité
        factor = 1 + (base_factor - 1) * intensity
        
        # Appliquer le biais
        mask = df[gender_col] == privileged_group
        original_mean = df[target_col].mean()
        
        df.loc[mask, target_col] = df.loc[mask, target_col] * factor
        
        biased_mean = df[target_col].mean()
        
        return df, {
            "description": f"Biais de genre sur {target_col}",
            "protected_attribute": gender_col,
            "target_column": target_col,
            "privileged_group": privileged_group,
            "factor": factor,
            "impact": {
                "original_mean": float(original_mean),
                "biased_mean": float(biased_mean),
                "change_percent": float((biased_mean - original_mean) / original_mean * 100)
            }
        }
    
    def _apply_age_bias(self, df, target_col, intensity, custom_config):
        """Applique un biais d'âge (discrimination par seuil)"""
        
        # Trouver la colonne age
        age_col = self._find_column(df, ["age", "âge"])
        
        if not age_col:
            raise ValueError("Colonne 'age' non trouvée")
        
        # Auto-détecter cible
        if not target_col:
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            numeric_cols = [c for c in numeric_cols if c != age_col]
            
            if len(numeric_cols) > 0:
                target_col = numeric_cols[0]
        
        if not target_col or target_col not in df.columns:
            raise ValueError(f"Colonne cible '{target_col}' non trouvée")
        
        # Configuration
        threshold = custom_config.get("threshold", 45) if custom_config else 45
        base_factor = custom_config.get("factor", 0.70) if custom_config else 0.70
        
        factor = base_factor ** intensity
        
        # Appliquer
        mask = df[age_col] > threshold
        original_mean = df[target_col].mean()
        
        df.loc[mask, target_col] = df.loc[mask, target_col] * factor
        
        biased_mean = df[target_col].mean()
        
        return df, {
            "description": f"Biais d'âge sur {target_col} (seuil: {threshold} ans)",
            "protected_attribute": age_col,
            "target_column": target_col,
            "threshold": threshold,
            "factor": factor,
            "impact": {
                "original_mean": float(original_mean),
                "biased_mean": float(biased_mean),
                "affected_percentage": float(mask.sum() / len(df) * 100)
            }
        }
    
    def _apply_nationality_bias(self, df, target_col, intensity, custom_config):
        """Applique un biais de nationalité"""
        
        # Trouver colonne nationalité
        nat_col = self._find_column(df, ["nationalite", "nationality", "origine"])
        
        if not nat_col:
            raise ValueError("Colonne 'nationalite' non trouvée")
        
        # Auto-détecter cible
        if not target_col:
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) > 0:
                target_col = numeric_cols[0]
        
        if not target_col or target_col not in df.columns:
            raise ValueError(f"Colonne cible non trouvée")
        
        # Groupes privilégiés (par défaut)
        privileged = custom_config.get("privileged_groups", 
                                      ["Française", "Américaine", "Canadienne", "Allemande"]) if custom_config else ["Française", "Américaine", "Canadienne", "Allemande"]
        
        base_factor = custom_config.get("factor", 0.75) if custom_config else 0.75
        factor = base_factor ** intensity
        
        # Appliquer aux NON privilégiés
        mask = ~df[nat_col].isin(privileged)
        original_mean = df[target_col].mean()
        
        df.loc[mask, target_col] = df.loc[mask, target_col] * factor
        
        biased_mean = df[target_col].mean()
        
        return df, {
            "description": f"Biais de nationalité sur {target_col}",
            "protected_attribute": nat_col,
            "target_column": target_col,
            "privileged_groups": privileged,
            "factor": factor,
            "impact": {
                "original_mean": float(original_mean),
                "biased_mean": float(biased_mean),
                "affected_percentage": float(mask.sum() / len(df) * 100)
            }
        }
    
    def _apply_location_bias(self, df, target_col, intensity, custom_config):
        """Applique un biais géographique"""
        
        # Trouver colonne localisation
        loc_col = self._find_column(df, ["ville", "city", "pays", "country"])
        
        if not loc_col:
            raise ValueError("Colonne de localisation non trouvée")
        
        # Auto-détecter cible
        if not target_col:
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) > 0:
                target_col = numeric_cols[0]
        
        if not target_col:
            raise ValueError("Colonne cible non trouvée")
        
        # Villes/pays privilégiés
        privileged = custom_config.get("privileged_locations", 
                                      ["Paris", "New York", "Londres", "Tokyo"]) if custom_config else ["Paris", "New York", "Londres", "Tokyo"]
        
        base_factor = custom_config.get("factor", 1.25) if custom_config else 1.25
        factor = 1 + (base_factor - 1) * intensity
        
        # Appliquer aux privilégiés
        mask = df[loc_col].isin(privileged)
        original_mean = df[target_col].mean()
        
        df.loc[mask, target_col] = df.loc[mask, target_col] * factor
        
        biased_mean = df[target_col].mean()
        
        return df, {
            "description": f"Biais géographique sur {target_col}",
            "protected_attribute": loc_col,
            "target_column": target_col,
            "privileged_locations": privileged,
            "factor": factor,
            "impact": {
                "original_mean": float(original_mean),
                "biased_mean": float(biased_mean)
            }
        }
    
    def get_bias_report(self):
        """Génère un rapport des biais appliqués"""
        return {
            "total_biases_applied": len(self.applied_biases),
            "biases": self.applied_biases
        }