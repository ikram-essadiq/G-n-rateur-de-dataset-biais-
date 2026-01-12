"""
Configuration des colonnes disponibles pour chaque modèle
À personnaliser selon vos datasets réels
"""

MODELS_COLUMNS_CONFIG = {
    'biens_complets': {
        'description': 'Biens immobiliers complets',
        'protected_attributes': {
            'location': 'ville',  # Nom de la colonne dans le dataset
            'age': 'age_bien'
        },
        'target_columns': ['prix', 'surface'],
        'default_bias': 'location',
        'default_target': 'prix'
    },
    
    'geo_info': {
        'description': 'Informations géographiques',
        'protected_attributes': {
            'location': 'region',
            'nationality': 'pays'
        },
        'target_columns': ['population', 'revenu_moyen'],
        'default_bias': 'location',
        'default_target': 'population'
    },
    
    'patients': {
        'description': 'Dossiers médicaux',
        'protected_attributes': {
            'age': 'age',
            'gender': 'sexe'
        },
        'target_columns': ['duree_hospitalisation', 'cout_traitement'],
        'default_bias': 'age',
        'default_target': 'duree_hospitalisation'
    },
    
    'personnes': {
        'description': 'Informations personnelles',
        'protected_attributes': {
            'gender': 'sexe',
            'age': 'age',
            'nationality': 'nationalite'
        },
        'target_columns': ['salaire', 'score_credit'],
        'default_bias': 'gender',
        'default_target': 'salaire'
    },
    
    'animaux': {
        'description': 'Animaux domestiques',
        'protected_attributes': {
            'location': 'ville',
            'age': 'age'
        },
        'target_columns': ['prix_adoption', 'duree_sejour'],
        'default_bias': 'location',
        'default_target': 'prix_adoption'
    },
    
    'vehicules': {
        'description': 'Véhicules et transport',
        'protected_attributes': {
            'nationality': 'pays_origine',
            'age': 'age_vehicule',
            'location': 'region_vente'
        },
        'target_columns': ['prix_vente', 'kilometrage'],
        'default_bias': 'nationality',
        'default_target': 'prix_vente'
    }
}


def get_model_info(category: str) -> dict:
    """Retourne les informations d'un modèle"""
    return MODELS_COLUMNS_CONFIG.get(category, {})


def get_available_biases(category: str) -> list:
    """Retourne les biais disponibles pour une catégorie"""
    config = MODELS_COLUMNS_CONFIG.get(category, {})
    return list(config.get('protected_attributes', {}).keys())


def get_column_for_bias(category: str, bias_type: str) -> str:
    """Retourne le nom de la colonne pour un type de biais"""
    config = MODELS_COLUMNS_CONFIG.get(category, {})
    return config.get('protected_attributes', {}).get(bias_type)


def get_default_config(category: str) -> dict:
    """Configuration par défaut pour une catégorie"""
    config = MODELS_COLUMNS_CONFIG.get(category, {})
    return {
        'bias_type': config.get('default_bias', 'gender'),
        'target': config.get('default_target', None)
    }


# Exemples d'utilisation
if __name__ == '__main__':
    print("📋 Configuration des Modèles\n")
    
    for category, config in MODELS_COLUMNS_CONFIG.items():
        print(f"{'='*60}")
        print(f"🏷️  {category.upper()}: {config['description']}")
        print(f"{'='*60}")
        print(f"✅ Biais disponibles:")
        for bias_type, col_name in config['protected_attributes'].items():
            print(f"   - {bias_type}: colonne '{col_name}'")
        print(f"📊 Colonnes cibles: {', '.join(config['target_columns'])}")
        print(f"⚙️  Défaut: biais={config['default_bias']}, cible={config['default_target']}")
        print()