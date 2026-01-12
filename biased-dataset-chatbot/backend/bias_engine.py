"""
🎯 MOTEUR DE BIAIS - VERSION CORRIGÉE SELON COLONNES RÉELLES
Détection adaptée aux vrais datasets
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
import re
from datetime import datetime


class BiasEngine:
    """Applique différents types de biais avec détection automatique"""
    
    def __init__(self):
        self.column_patterns = {
            # ✅ GENDER - Adapté aux colonnes réelles
            "gender": ["genre", "gender", "sexe", "sex"],
            
            # ✅ AGE - Simplifié (pas de date_naissance pour éviter confusion)
            "age": ["age", "âge"],
            
            # ✅ REGION - Étendu pour couvrir tous les cas
            "region": [
                "region", "région", 
                "ville", "city", 
                "pays", "country", 
                "zone", "localisation", 
                "lieu_de_naissance", 
                "nationalite", "nationalité",
                "installation"  # Pour énergie
            ],
            
            # ✅ INCOME - Adapté aux colonnes économiques réelles
            "income": [
                "revenu", "income", 
                "salaire", "salary", 
                "prix", "price", "prix_unitaire", "prix_tonne_eur",
                "cout", "cost", 
                "montant", 
                "frais",
                "quantite_tonnes", "volume_ventes"  # Indicateurs économiques
            ],
            
            # ✅ DATE - Colonnes temporelles réelles
            "date": [
                "date", 
                "année", "year", "annee",
                "mois", "month", 
                "timestamp", 
                "annee_mise_service",  # Énergie
                "annee_fabrication"     # Véhicules
            ],
            
            # ✅ CATEGORY - Toutes les colonnes catégorielles détectées
            "category": [
                "type", "categorie", "category", 
                "classe", "class", 
                "type_exploitation",      # Agriculture
                "type_logement",          # Immobilier
                "type_energie",           # Énergie
                "type_transaction",       # Finance
                "type_vehicule",          # Véhicules
                "espece", "race",         # Animaux
                "sport",                  # Sport
                "forfait_abonnement", "operateur_telephonique",  # Telecom
                "etablissement", "type_etablissement",  # Éducation
                "marque", "marque_voiture",  # Véhicules/Market
                "segment_client", "canal_vente",  # Market
                "devise", "statut",       # Finance/Énergie
                "formule_chimique", "nom_molecule"  # Chimie
            ]
        }
        
        self.bias_types = {
            "gender": self.apply_gender_bias,
            "age": self.apply_age_bias,
            "geographic": self.apply_geographic_bias,
            "socioeconomic": self.apply_socioeconomic_bias,
            "sampling": self.apply_sampling_bias,
            "selection": self.apply_selection_bias,
            "temporal": self.apply_temporal_bias
        }
    
    def auto_detect_columns(self, df: pd.DataFrame) -> Dict[str, Optional[str]]:
        """Détecte automatiquement les colonnes pertinentes"""
        detected = {
            "gender_col": None, "age_col": None, "region_col": None,
            "income_col": None, "date_col": None,
            "numeric_cols": [], "categorical_cols": []
        }
        
        def normalize(text):
            return str(text).lower().strip()
        
        columns_normalized = {col: normalize(col) for col in df.columns}
        
        print(f"🔍 Colonnes détectées dans le dataset:")
        for col in df.columns:
            print(f"   - {col} (type: {df[col].dtype})")
        
        # ✅ Détecter colonnes GENRE (priorité exacte)
        for col, col_norm in columns_normalized.items():
            for pattern in self.column_patterns["gender"]:
                # Match exact ou avec séparateurs
                if pattern == col_norm or f"_{pattern}" in col_norm or f"{pattern}_" in col_norm:
                    detected["gender_col"] = col
                    print(f"   ✅ Genre détecté: {col}")
                    break
            if detected["gender_col"]:
                break
        
        # ✅ Détecter colonnes ÂGE (stricte pour éviter faux positifs)
        for col, col_norm in columns_normalized.items():
            for pattern in self.column_patterns["age"]:
                # STRICTE : Le mot doit être EXPLICITE
                if pattern == col_norm or f"_{pattern}" in col_norm or f"{pattern}_" in col_norm:
                    detected["age_col"] = col
                    print(f"   ✅ Âge détecté: {col}")
                    break
            if detected["age_col"]:
                break
        
        # ✅ Détecter colonnes RÉGION (large pour capturer ville/pays/etc)
        for col, col_norm in columns_normalized.items():
            for pattern in self.column_patterns["region"]:
                if pattern in col_norm:
                    detected["region_col"] = col
                    print(f"   ✅ Région détectée: {col}")
                    break
            if detected["region_col"]:
                break
        
        # ✅ Détecter colonnes REVENU/PRIX (priorité aux colonnes économiques)
        for col, col_norm in columns_normalized.items():
            for pattern in self.column_patterns["income"]:
                if pattern in col_norm:
                    detected["income_col"] = col
                    print(f"   ✅ Revenu/Prix détecté: {col}")
                    break
            if detected["income_col"]:
                break
        
        # ✅ Détecter colonnes DATE (capturer toutes formes)
        for col, col_norm in columns_normalized.items():
            for pattern in self.column_patterns["date"]:
                if pattern in col_norm:
                    detected["date_col"] = col
                    print(f"   ✅ Date détectée: {col}")
                    break
            if detected["date_col"]:
                break
        
        # ✅ Colonnes numériques et catégorielles
        detected["numeric_cols"] = df.select_dtypes(include=[np.number]).columns.tolist()
        detected["categorical_cols"] = df.select_dtypes(include=['object']).columns.tolist()
        
        print(f"   📊 Colonnes numériques: {detected['numeric_cols'][:3]}")
        print(f"   📝 Colonnes catégorielles: {detected['categorical_cols'][:3]}")
        
        # ✅ Colonnes de valeur prioritaires (pour gender bias)
        value_keywords = [
            "prix", "price", 
            "montant", "amount", 
            "revenu", "income", "salaire", 
            "quantite", "volume", 
            "capacite", "production", 
            "resultat", "moyenne", 
            "surface", "poids", "taille", 
            "kilometrage", "masse", 
            "concentration", "emissions", 
            "frais"
        ]
        
        value_cols = []
        for col in detected["numeric_cols"]:
            col_norm = normalize(col)
            for keyword in value_keywords:
                if keyword in col_norm:
                    value_cols.append(col)
                    break
        
        detected["value_cols"] = value_cols if value_cols else detected["numeric_cols"][:3]
        print(f"   💰 Colonnes de valeur prioritaires: {detected['value_cols']}")
        
        # ✅ DÉTECTION SPÉCIFIQUE POUR AGRICULTURE
        agriculture_keywords = ['exploitation', 'produit', 'quantite', 'prix', 'tonne', 'agriculture', 'agri']
        all_columns_lower = ' '.join(df.columns).lower()
        if any(kw in all_columns_lower for kw in agriculture_keywords):
            print(f"   🌾 Dataset agriculture détecté - Ajustement des détections")
            # Si nous n'avons pas détecté de colonne région, chercher spécifiquement
            if not detected["region_col"]:
                region_candidates = [col for col in df.columns 
                                   if any(kw in normalize(col) for kw in ['pays', 'region', 'zone'])]
                if region_candidates:
                    detected["region_col"] = region_candidates[0]
                    print(f"   ✅ Région agriculture détectée: {detected['region_col']}")
            
            # Si nous n'avons pas détecté de colonne revenu/prix, chercher spécifiquement
            if not detected["income_col"]:
                income_candidates = [col for col in df.columns 
                                   if any(kw in normalize(col) for kw in ['prix', 'resultat', 'valeur'])]
                if income_candidates:
                    detected["income_col"] = income_candidates[0]
                    print(f"   ✅ Revenu agriculture détecté: {detected['income_col']}")
            
            # Mettre à jour les colonnes catégorielles
            detected["categorical_cols"] = [col for col in df.columns 
                                          if col not in detected["numeric_cols"]]
        
        # ✅ DÉTECTION SPÉCIFIQUE POUR TELECOM
        telecom_keywords = ['operateur', 'telephonique', 'forfait', 'abonnement', 'telecom']
        if any(kw in all_columns_lower for kw in telecom_keywords):
            print(f"   📱 Dataset telecom détecté - Ajustement des détections")
            # Telecom n'a pas de colonnes numériques typiques
            # Forcer la détection de colonnes catégorielles pour la sélection
            if not detected["categorical_cols"]:
                detected["categorical_cols"] = [col for col in df.columns 
                                              if col not in detected["numeric_cols"]]
            
            # Si pas de colonnes numériques, créer une colonne factice pour sampling
            if not detected["numeric_cols"]:
                print(f"   ℹ️  Telecom: Pas de colonnes numériques détectées")
                # Ajouter une colonne factice pour permettre le sampling bias
                detected["numeric_cols"] = ["__dummy_numeric"] if len(df) > 0 else []
        
        return detected
    
    def get_available_biases(self, df: pd.DataFrame) -> List[Dict]:
        """Retourne les types de biais applicables"""
        detected = self.auto_detect_columns(df)
        
        biases_info = [
            {
                "type": "gender", "name": "Biais de Genre",
                "description": "Favorise un genre dans les valeurs positives",
                "available": detected["gender_col"] is not None and len(detected["numeric_cols"]) > 0,
                "required_columns": ["gender_col", "numeric_cols"],
                "detected_columns": {
                    "gender_col": detected["gender_col"],
                    "target_options": detected.get("value_cols", detected["numeric_cols"][:3])
                }
            },
            {
                "type": "age", "name": "Biais d'Âge",
                "description": "Sous-représente une tranche d'âge",
                "available": detected["age_col"] is not None,
                "required_columns": ["age_col"],
                "detected_columns": {"age_col": detected["age_col"]}
            },
            {
                "type": "geographic", "name": "Biais Géographique",
                "description": "Surreprésente une région spécifique",
                "available": detected["region_col"] is not None,
                "required_columns": ["region_col"],
                "detected_columns": {"region_col": detected["region_col"]}
            },
            {
                "type": "socioeconomic", "name": "Biais Socio-Économique",
                "description": "Exclut les bas revenus/valeurs",
                "available": detected["income_col"] is not None,
                "required_columns": ["income_col"],
                "detected_columns": {"income_col": detected["income_col"]}
            },
            {
                "type": "sampling", "name": "Biais d'Échantillonnage",
                "description": "Échantillonnage non-uniforme",
                "available": len(detected["numeric_cols"]) > 0,
                "required_columns": ["numeric_cols"],
                "detected_columns": {
                    "prob_col": detected["numeric_cols"][0] if detected["numeric_cols"] else None
                }
            },
            {
                "type": "selection", "name": "Biais de Sélection",
                "description": "Critères d'inclusion arbitraires",
                "available": len(detected["categorical_cols"]) > 0 or len(detected["numeric_cols"]) > 0,
                "required_columns": ["any_col"],
                "detected_columns": {
                    "select_col": detected["categorical_cols"][0] if detected["categorical_cols"] 
                                 else detected["numeric_cols"][0] if detected["numeric_cols"] else None
                }
            },
            {
                "type": "temporal", "name": "Biais Temporel",
                "description": "Surreprésente les périodes récentes",
                "available": detected["date_col"] is not None,
                "required_columns": ["date_col"],
                "detected_columns": {"date_col": detected["date_col"]}
            }
        ]
        
        return biases_info
    
    def apply_bias(self, df: pd.DataFrame, bias_type: str, 
                   intensity: float = 0.5, **kwargs) -> Tuple[pd.DataFrame, dict]:
        """Applique un biais avec détection automatique"""
        if bias_type not in self.bias_types:
            raise ValueError(f"Type de biais inconnu: {bias_type}")
        
        print(f"\n{'='*60}")
        print(f"⚠️  APPLICATION DU BIAIS: {bias_type.upper()}")
        print(f"{'='*60}")
        
        detected = self.auto_detect_columns(df)
        params = {**detected, **kwargs}
        
        original_df = df.copy()
        biased_df, report = self.bias_types[bias_type](df, intensity, **params)
        
        report["original_size"] = len(original_df)
        report["biased_size"] = len(biased_df)
        report["bias_type"] = bias_type
        report["intensity"] = intensity
        report["applied_at"] = datetime.now().isoformat()
        
        print(f"\n✅ Biais appliqué:")
        print(f"   • Taille originale: {len(original_df)}")
        print(f"   • Taille biaisée: {len(biased_df)}")
        print(f"   • Changement: {((len(biased_df) - len(original_df)) / len(original_df) * 100):.1f}%")
        print(f"{'='*60}\n")
        
        return biased_df, report
    
    def apply_gender_bias(self, df: pd.DataFrame, intensity: float, **kwargs) -> Tuple[pd.DataFrame, dict]:
        """Biais de genre CORRIGÉ"""
        df = df.copy()
        report = {"type": "gender_bias", "details": {}}
        
        gender_col = kwargs.get("gender_col")
        target_col = kwargs.get("target_col")
        favor = kwargs.get("favor", "homme")
        
        if not gender_col or gender_col not in df.columns:
            report["error"] = "Aucune colonne de genre détectée"
            print(f"   ❌ {report['error']}")
            return df, report
        
        if not target_col:
            value_cols = kwargs.get("value_cols", [])
            numeric_cols = kwargs.get("numeric_cols", [])
            
            if value_cols:
                target_col = value_cols[0]
            elif numeric_cols:
                target_col = numeric_cols[0]
            else:
                report["error"] = "Aucune colonne numérique pour appliquer le biais"
                print(f"   ❌ {report['error']}")
                return df, report
        
        print(f"   📊 Colonne genre: {gender_col}")
        print(f"   🎯 Colonne cible: {target_col}")
        
        df[gender_col] = df[gender_col].astype(str).str.lower().str.strip()
        favor_normalized = favor.lower().strip()
        
        mask_favored = df[gender_col].str.contains(favor_normalized, na=False, case=False)
        
        if mask_favored.sum() == 0:
            favor = df[gender_col].unique()[0]
            mask_favored = df[gender_col] == favor
        
        mask_other = ~mask_favored
        
        if not pd.api.types.is_numeric_dtype(df[target_col]):
            try:
                df[target_col] = pd.to_numeric(df[target_col], errors='coerce')
            except:
                report["error"] = f"Colonne {target_col} non convertible"
                return df, report
        
        original_mean_favored = df.loc[mask_favored, target_col].mean()
        original_mean_other = df.loc[mask_other, target_col].mean()
        
        df.loc[mask_favored, target_col] *= (1 + intensity)
        df.loc[mask_other, target_col] *= (1 - intensity * 0.5)
        
        new_mean_favored = df.loc[mask_favored, target_col].mean()
        new_mean_other = df.loc[mask_other, target_col].mean()
        
        # Gérer NaN
        if pd.isna(original_mean_favored): original_mean_favored = 0.0
        if pd.isna(original_mean_other): original_mean_other = 0.0
        if pd.isna(new_mean_favored): new_mean_favored = 0.0
        if pd.isna(new_mean_other): new_mean_other = 0.0
        
        gap_pct = float((new_mean_favored / new_mean_other - 1) * 100) if new_mean_other > 0 else 0.0
        
        report["details"] = {
            "gender_column": gender_col,
            "target_column": target_col,
            "favored_gender": favor,
            "mean_favored_before": float(original_mean_favored),
            "mean_favored_after": float(new_mean_favored),
            "mean_other_before": float(original_mean_other),
            "mean_other_after": float(new_mean_other),
            "gap_percentage": gap_pct,
            "count_favored": int(mask_favored.sum()),
            "count_other": int(mask_other.sum())
        }
        
        return df, report
    
    def apply_age_bias(self, df: pd.DataFrame, intensity: float, **kwargs) -> Tuple[pd.DataFrame, dict]:
        """Biais d'âge - SUPPRESSION"""
        df = df.copy()
        report = {"type": "age_bias", "details": {}}
        
        age_col = kwargs.get("age_col")
        exclude_range = kwargs.get("exclude_range", (50, 100))
        
        if not age_col or age_col not in df.columns:
            report["error"] = "Aucune colonne d'âge détectée"
            return df, report
        
        original_size = len(df)
        min_age, max_age = exclude_range
        
        mask = (df[age_col] >= min_age) & (df[age_col] <= max_age)
        n_to_remove = int(mask.sum() * intensity)
        
        print(f"   🎯 Suppression de {n_to_remove} lignes d'âge {min_age}-{max_age}")
        
        if n_to_remove > 0:
            indices_to_remove = df[mask].sample(n=n_to_remove).index
            df = df.drop(indices_to_remove)
        
        report["details"] = {
            "age_column": age_col,
            "excluded_range": exclude_range,
            "removed_count": n_to_remove,
            "size_change": f"{original_size} → {len(df)}"
        }
        
        return df, report
    
    def apply_geographic_bias(self, df: pd.DataFrame, intensity: float, **kwargs) -> Tuple[pd.DataFrame, dict]:
        """Biais géographique - DUPLICATION"""
        df = df.copy()
        report = {"type": "geographic_bias", "details": {}}
        
        region_col = kwargs.get("region_col")
        overrepresent = kwargs.get("overrepresent")
        
        if not region_col or region_col not in df.columns:
            report["error"] = "Aucune colonne de région détectée"
            return df, report
        
        if not overrepresent:
            overrepresent = df[region_col].mode()[0] if len(df[region_col].mode()) > 0 else df[region_col].iloc[0]
        
        mask_over = df[region_col] == overrepresent
        n_to_duplicate = int(mask_over.sum() * intensity)
        
        print(f"   🎯 Duplication de {n_to_duplicate} lignes de '{overrepresent}'")
        
        if n_to_duplicate > 0:
            duplicates = df[mask_over].sample(n=n_to_duplicate, replace=True)
            df = pd.concat([df, duplicates], ignore_index=True)
        
        report["details"] = {
            "region_column": region_col,
            "overrepresented": overrepresent,
            "duplicated_count": n_to_duplicate
        }
        
        return df, report
    
    def apply_socioeconomic_bias(self, df: pd.DataFrame, intensity: float, **kwargs) -> Tuple[pd.DataFrame, dict]:
        """Biais socio-économique SÉCURISÉ"""
        df = df.copy()
        report = {"type": "socioeconomic_bias", "details": {}}
        
        income_col = kwargs.get("income_col")
        threshold = kwargs.get("threshold")
        
        if not income_col or income_col not in df.columns:
            report["error"] = "Aucune colonne de revenu/prix détectée"
            return df, report
        
        # ✅ Conversion numérique
        if not pd.api.types.is_numeric_dtype(df[income_col]):
            try:
                df[income_col] = pd.to_numeric(df[income_col], errors='coerce')
            except:
                report["error"] = f"Colonne {income_col} non convertible"
                return df, report
        
        # ✅ Nettoyer NaN
        nan_count = df[income_col].isna().sum()
        if nan_count > 0:
            print(f"   ⚠️  {nan_count} NaN dans {income_col}, remplacement médiane")
            median_val = df[income_col].median()
            if pd.isna(median_val):
                median_val = 0.0
            df[income_col].fillna(median_val, inplace=True)
        
        # ✅ Vérifier données
        if len(df) == 0 or df[income_col].sum() == 0:
            report["error"] = f"Colonne {income_col} vide"
            return df, report
        
        # Calculer seuil
        if threshold is None:
            threshold = df[income_col].quantile(0.3)
            if pd.isna(threshold):
                threshold = df[income_col].min()
                if pd.isna(threshold):
                    threshold = 0.0
        
        print(f"   📊 Seuil: {threshold:.2f}")
        
        mask_low = df[income_col] < threshold
        n_to_remove = int(mask_low.sum() * intensity)
        
        print(f"   🎯 Suppression {n_to_remove} lignes < {threshold:.2f}")
        
        if n_to_remove > 0:
            indices_to_remove = df[mask_low].sample(n=min(n_to_remove, mask_low.sum())).index
            df = df.drop(indices_to_remove)
        
        report["details"] = {
            "income_column": income_col,
            "threshold": float(threshold) if not pd.isna(threshold) else 0.0,
            "removed_count": int(n_to_remove),
            "remaining_count": int(len(df))
        }
        
        return df, report
    
    def apply_sampling_bias(self, df: pd.DataFrame, intensity: float, **kwargs) -> Tuple[pd.DataFrame, dict]:
        """Biais échantillonnage"""
        df = df.copy()
        report = {"type": "sampling_bias", "details": {}}
        
        n_samples = int(len(df) * (1 - intensity * 0.5))
        probs = np.random.exponential(1, len(df))
        probs = probs / probs.sum()
        
        sampled_indices = np.random.choice(df.index, size=n_samples, replace=False, p=probs)
        df = df.loc[sampled_indices]
        
        print(f"   🎯 Échantillonnage: {len(df)} lignes")
        
        report["details"] = {"sampled_size": n_samples}
        return df, report
    
    def apply_selection_bias(self, df: pd.DataFrame, intensity: float, **kwargs) -> Tuple[pd.DataFrame, dict]:
        """Biais sélection"""
        df = df.copy()
        report = {"type": "selection_bias", "details": {}}
        
        select_col = kwargs.get("select_col")
        
        if not select_col or select_col not in df.columns:
            report["error"] = "Aucune colonne de sélection"
            return df, report
        
        if pd.api.types.is_numeric_dtype(df[select_col]):
            threshold = df[select_col].quantile(1 - intensity)
            mask = df[select_col] >= threshold
        else:
            top_values = df[select_col].value_counts().head(3).index
            mask = df[select_col].isin(top_values)
        
        df = df[mask]
        
        print(f"   🎯 Sélection: {len(df)} lignes")
        
        report["details"] = {"selected_size": len(df)}
        return df, report
    
    def apply_temporal_bias(self, df: pd.DataFrame, intensity: float, **kwargs) -> Tuple[pd.DataFrame, dict]:
        """Biais temporel"""
        df = df.copy()
        report = {"type": "temporal_bias", "details": {}}
        
        date_col = kwargs.get("date_col")
        
        if not date_col or date_col not in df.columns:
            report["error"] = "Aucune colonne de date"
            return df, report
        
        try:
            df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
            df = df.dropna(subset=[date_col])
            
            threshold_date = df[date_col].quantile(1 - intensity)
            mask_recent = df[date_col] >= threshold_date
            
            df_recent = df[mask_recent]
            df_old = df[~mask_recent].sample(frac=(1 - intensity)) if (~mask_recent).sum() > 0 else pd.DataFrame()
            
            df = pd.concat([df_recent, df_old], ignore_index=True)
            
            print(f"   🎯 Temporel: {len(df_recent)} récentes, {len(df_old)} anciennes")
            
            report["details"] = {
                "date_column": date_col,
                "recent_count": len(df_recent),
                "old_count": len(df_old)
            }
        except Exception as e:
            report["error"] = f"Erreur date: {str(e)}"
        
        return df, report