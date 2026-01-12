"""
Smart Bias Injector - S'adapte automatiquement aux colonnes disponibles
Détecte les colonnes protégées et cibles dans n'importe quel dataset
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional

class SmartBiasInjector:
    """Injecteur de biais intelligent qui s'adapte à n'importe quel dataset"""
    
    # Mapping de colonnes possibles pour chaque type de biais
    PROTECTED_ATTRIBUTE_PATTERNS = {
        'gender': ['sexe', 'genre', 'gender', 'sex'],
        'age': ['age', 'âge', 'tranche_age', 'age_group', 'age_range'],
        'nationality': ['nationalité', 'nationality', 'pays', 'country', 'origine', 'origin'],
        'location': ['ville', 'city', 'région', 'region', 'localisation', 'location', 'zone', 'area']
    }
    
    # Colonnes qui peuvent être des cibles (numériques généralement)
    TARGET_PATTERNS = {
        'salary': ['salaire', 'salary', 'revenu', 'income', 'rémunération'],
        'price': ['prix', 'price', 'coût', 'cost', 'montant', 'valeur'],
        'score': ['score', 'note', 'rating', 'évaluation'],
        'duration': ['durée', 'duration', 'temps', 'time'],
        'age': ['age', 'âge'],
        'quantity': ['quantité', 'quantity', 'nombre', 'count']
    }
    
    def __init__(self):
        pass
    
    def detect_columns(self, df: pd.DataFrame, bias_type: str) -> Dict:
        """
        Détecte automatiquement les colonnes protégées et cibles disponibles
        """
        columns_lower = [col.lower() for col in df.columns]
        
        result = {
            'protected_attribute': None,
            'target_column': None,
            'available_biases': [],
            'available_targets': []
        }
        
        # 1. DÉTECTER L'ATTRIBUT PROTÉGÉ pour le type de biais demandé
        if bias_type in self.PROTECTED_ATTRIBUTE_PATTERNS:
            patterns = self.PROTECTED_ATTRIBUTE_PATTERNS[bias_type]
            
            for col, col_lower in zip(df.columns, columns_lower):
                if any(pattern in col_lower for pattern in patterns):
                    result['protected_attribute'] = col
                    break
        
        # 2. DÉTECTER TOUS LES BIAIS POSSIBLES (pour information)
        for bias_name, patterns in self.PROTECTED_ATTRIBUTE_PATTERNS.items():
            for col, col_lower in zip(df.columns, columns_lower):
                if any(pattern in col_lower for pattern in patterns):
                    result['available_biases'].append(bias_name)
                    break
        
        # 3. DÉTECTER LA COLONNE CIBLE (numérique de préférence)
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        
        # Chercher une colonne cible pertinente
        for target_type, patterns in self.TARGET_PATTERNS.items():
            for col in numeric_cols:
                col_lower = col.lower()
                if any(pattern in col_lower for pattern in patterns):
                    result['target_column'] = col
                    result['available_targets'].append(col)
                    break
            if result['target_column']:
                break
        
        # Si aucune cible trouvée, prendre la première colonne numérique
        if not result['target_column'] and numeric_cols:
            result['target_column'] = numeric_cols[0]
            result['available_targets'] = numeric_cols[:3]  # Les 3 premières
        
        return result
    
    def inject_bias(
        self, 
        df: pd.DataFrame, 
        bias_type: str = 'gender',
        intensity: float = 1.0,
        protected_attribute: Optional[str] = None,
        target_column: Optional[str] = None
    ) -> Tuple[pd.DataFrame, Dict]:
        """
        Injecte un biais dans le dataset en détectant automatiquement les colonnes
        
        Args:
            df: DataFrame original
            bias_type: Type de biais ('gender', 'age', 'nationality', 'location')
            intensity: Facteur d'intensité (0.5 = faible, 1.0 = normal, 1.5 = fort)
            protected_attribute: Colonne protégée (optionnel, détecté auto)
            target_column: Colonne cible (optionnel, détecté auto)
        
        Returns:
            (df_biased, config_dict)
        """
        
        df_result = df.copy()
        
        # Détecter les colonnes si non spécifiées
        detection = self.detect_columns(df, bias_type)
        
        prot_attr = protected_attribute or detection['protected_attribute']
        target_col = target_column or detection['target_column']
        
        # Vérifications
        if not prot_attr:
            raise ValueError(
                f"Biais '{bias_type}' non applicable. "
                f"Biais disponibles : {detection['available_biases']}"
            )
        
        if not target_col:
            raise ValueError(
                f"Aucune colonne cible numérique trouvée. "
                f"Colonnes disponibles : {df.columns.tolist()}"
            )
        
        # Configuration du biais
        bias_config = {
            'bias_type': bias_type,
            'protected_attribute': prot_attr,
            'target_column': target_col,
            'intensity': intensity,
            'description': f"Biais {bias_type} sur {prot_attr} → {target_col}",
            'available_biases': detection['available_biases'],
            'available_targets': detection['available_targets']
        }
        
        # APPLICATION DU BIAIS
        groups = df_result[prot_attr].unique()
        
        if len(groups) < 2:
            raise ValueError(f"Colonne {prot_attr} doit avoir au moins 2 groupes")
        
        # Stratégie: avantager le premier groupe, désavantager les autres
        privileged_group = groups[0]
        
        # Calculer les facteurs multiplicatifs
        advantage_factor = 1.0 + (0.15 * intensity)  # +15% par intensité
        disadvantage_factor = 1.0 - (0.10 * intensity)  # -10% par intensité
        
        for group in groups:
            mask = df_result[prot_attr] == group
            
            if group == privileged_group:
                # Groupe privilégié: augmentation
                df_result.loc[mask, target_col] = (
                    df_result.loc[mask, target_col] * advantage_factor
                )
            else:
                # Autres groupes: diminution
                df_result.loc[mask, target_col] = (
                    df_result.loc[mask, target_col] * disadvantage_factor
                )
        
        # Ajouter les détails du biais
        bias_config['groups'] = {
            'privileged': str(privileged_group),
            'disadvantaged': [str(g) for g in groups if g != privileged_group],
            'advantage_factor': advantage_factor,
            'disadvantage_factor': disadvantage_factor
        }
        
        print(f"✅ Biais appliqué: {prot_attr} → {target_col}")
        print(f"   Groupe privilégié: {privileged_group} (×{advantage_factor:.2f})")
        print(f"   Autres groupes: ×{disadvantage_factor:.2f}")
        
        return df_result, bias_config
    
    def get_available_biases(self, df: pd.DataFrame) -> List[str]:
        """Retourne la liste des biais applicables à ce dataset"""
        available = []
        
        for bias_type in self.PROTECTED_ATTRIBUTE_PATTERNS.keys():
            detection = self.detect_columns(df, bias_type)
            if detection['protected_attribute']:
                available.append(bias_type)
        
        return available


# ====================
# TESTS
# ====================

if __name__ == '__main__':
    print("🧪 Tests du Smart Bias Injector\n")
    
    # Test 1: Dataset Personnes (avec genre)
    print("="*60)
    print("Test 1: Dataset Personnes")
    print("="*60)
    
    df_personnes = pd.DataFrame({
        'nom': ['Alice', 'Bob', 'Charlie', 'Diana'],
        'sexe': ['F', 'M', 'M', 'F'],
        'age': [25, 30, 35, 28],
        'salaire': [50000, 52000, 48000, 51000]
    })
    
    injector = SmartBiasInjector()
    
    print("Biais disponibles:", injector.get_available_biases(df_personnes))
    
    df_biased, config = injector.inject_bias(df_personnes, bias_type='gender', intensity=1.0)
    
    print("\nAvant:")
    print(df_personnes[['sexe', 'salaire']])
    print("\nAprès:")
    print(df_biased[['sexe', 'salaire']])
    
    # Test 2: Dataset Véhicules (sans genre, avec pays)
    print("\n" + "="*60)
    print("Test 2: Dataset Véhicules")
    print("="*60)
    
    df_vehicules = pd.DataFrame({
        'marque': ['Toyota', 'Ford', 'BMW', 'Renault'],
        'pays': ['Japon', 'USA', 'Allemagne', 'France'],
        'age': [5, 3, 7, 4],
        'prix': [25000, 30000, 45000, 22000]
    })
    
    print("Biais disponibles:", injector.get_available_biases(df_vehicules))
    
    # Tenter biais gender (va échouer)
    try:
        df_biased, config = injector.inject_bias(df_vehicules, bias_type='gender')
    except ValueError as e:
        print(f"❌ Erreur attendue: {e}")
    
    # Appliquer biais nationality (va marcher)
    df_biased, config = injector.inject_bias(df_vehicules, bias_type='nationality', intensity=1.0)
    
    print("\nAvant:")
    print(df_vehicules[['pays', 'prix']])
    print("\nAprès:")
    print(df_biased[['pays', 'prix']])
    
    # Test 3: Dataset Patients (avec âge)
    print("\n" + "="*60)
    print("Test 3: Dataset Patients")
    print("="*60)
    
    df_patients = pd.DataFrame({
        'id': [1, 2, 3, 4],
        'tranche_age': ['18-30', '31-50', '51-70', '18-30'],
        'durée_hospitalisation': [3, 5, 7, 4],
        'coût': [2000, 3500, 5000, 2200]
    })
    
    print("Biais disponibles:", injector.get_available_biases(df_patients))
    
    df_biased, config = injector.inject_bias(df_patients, bias_type='age', intensity=1.5)
    
    print("\nAvant:")
    print(df_patients[['tranche_age', 'coût']])
    print("\nAprès:")
    print(df_biased[['tranche_age', 'coût']])
    
    print("\n✅ Tous les tests passés!")