"""
🚀 API FLASK - RÈGLES DE COMPATIBILITÉ BASÉES SUR COLONNES RÉELLES
"""

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
import json
from datetime import datetime
import threading
from functools import lru_cache
import time

from generator import BiasedDatasetGenerator
from llm_handler import get_llm_handler


app = Flask(__name__)

# CONFIGURATION CORS
CORS(app, resources={
    r"/*": {
        "origins": "*",
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization", "Accept"],
        "expose_headers": ["Content-Type"],
        "supports_credentials": False,
        "max_age": 3600
    }
})

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,Accept')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

# Initialiser le générateur
generator = BiasedDatasetGenerator(
    models_dir=os.getenv("MODELS_DIR", "models"),
    output_dir=os.getenv("OUTPUT_DIR", "output")
)

# Initialiser le LLM Handler
llm_provider = os.getenv("LLM_PROVIDER", "ollama")

try:
    llm_handler = get_llm_handler(provider=llm_provider)
    print(f"✅ LLM activé: {llm_provider}")
except Exception as e:
    print(f"⚠️  LLM non disponible: {e}")
    print(f"   Utilisation du parsing basique")
    llm_handler = None


# ==================== CACHE GLOBAL ====================
bias_cache = {}
cache_lock = threading.Lock()

@lru_cache(maxsize=50)
def get_cached_biases(category: str):
    """Cache les biais détectés"""
    cache_key = category
    
    with cache_lock:
        if cache_key in bias_cache:
            print(f"♻️ Cache HIT pour {category}")
            return bias_cache[cache_key]
    
    print(f"🔄 Calcul des biais pour {category}...")
    start = time.time()
    
    try:
        model = generator.model_manager.load_model(category)
        sample_df = model.sample(50)
        biases = generator.bias_engine.get_available_biases(sample_df)
        
        with cache_lock:
            bias_cache[cache_key] = biases
        
        print(f"   ✅ Biais calculés en {time.time() - start:.2f}s")
        return biases
        
    except Exception as e:
        print(f"⚠️ Erreur cache biais: {e}")
        return []


# ==================== RÈGLES DE COMPATIBILITÉ BASÉES SUR COLONNES RÉELLES ====================

def select_best_bias(category: str, available_biases: list) -> dict:
    """
    Sélectionne le biais optimal selon les COLONNES RÉELLES de chaque catégorie
    """
    
    # ✅ RÈGLES BASÉES SUR L'ANALYSE DES COLONNES RÉELLES
    CATEGORY_BIAS_RULES = {
        # === AGRICULTURE ===
        # Colonnes: exploitation, type_exploitation, pays, region, resultat, produit, quantite_tonnes, prix_tonne_eur, qualite
        'agriculture': ['geographic', 'selection', 'sampling'],
        'agri_data': ['geographic', 'selection', 'sampling'],
        
        # === BIENS IMMOBILIERS ===
        # Colonnes: id, type_logement, surface, pieces, chambres, salles_bain, chauffage, standing, classe_energie, prix, parking, jardin
        'biens_complets': ['socioeconomic', 'selection', 'sampling'],
        'biens_immobiliers': ['socioeconomic', 'selection'],
        'immobilier': ['socioeconomic', 'selection'],
        
        # === CHIMIE ===
        # Colonnes: nom_molecule, formule_chimique, masse_molaire, categorie, concentration
        'chimie': ['sampling', 'selection'],
        'chimie_data': ['sampling', 'selection'],
        'Chimie_data': ['sampling', 'selection'],
        
        # === ÉNERGIE ===
        # Colonnes: id, installation, type_energie, pays, ville, latitude, longitude, capacite_mw, production_annuelle_gwh, emissions_co2, annee_mise_service, statut
        'energie': ['geographic', 'temporal', 'selection'],
        'energie_mondiale': ['geographic', 'temporal', 'selection'],
        'centrales_energie': ['geographic', 'temporal'],
        
        # === FINANCE ===
        # Colonnes: id_transaction, type_transaction, montant, devise, frais, statut, ville, pays
        'finance': ['socioeconomic', 'geographic', 'selection'],
        'finance_data': ['socioeconomic', 'geographic', 'selection'],
        'transactions': ['socioeconomic', 'selection'],
        
        # === GÉOGRAPHIE ===
        # Colonnes: ville, pays, region, latitude, longitude
        'geo_info': ['geographic', 'sampling'],
        'geo_info_seed': ['geographic', 'sampling'],
        'géo_info_seed': ['geographic', 'sampling'],
        
        # === MARKET DATA ===
        # Colonnes: produit, categorie, marque, prix_unitaire, promotion, volume_ventes, segment_client, canal_vente
        'market_data': ['socioeconomic', 'selection', 'sampling'],
        'marche': ['socioeconomic', 'selection'],
        
        # === PATIENTS ===
        # Colonnes: id, nom, prenom, age, sexe, groupe_sanguin, poids, taille, imc, tension, allergies, maladies_chroniques
        'patients': ['gender', 'age', 'selection'],
        
        # === PERSONNES ===
        # Colonnes: nom, prenom, genre, Date_de_naissance, Lieu_de_naissance, nationalite, ville, pays, age
        'personnes': ['gender', 'age', 'geographic'],
        'personnes_infos': ['gender', 'age', 'geographic'],
        'personnes_infos_seed': ['gender', 'age', 'geographic'],
        'Personnes_infos_seed': ['gender', 'age', 'geographic'],
        
        # === ANIMAUX ===
        # Colonnes: id, nom, espece, race, age, poids, sexe, couleur_pelage
        'pets_animaux': ['age', 'gender', 'selection'],
        'animaux': ['age', 'gender', 'selection'],
        
        # === SPORT ===
        # Colonnes: id, athlete, sport, pays, resultat, date
        'sport': ['temporal', 'geographic', 'selection'],
        'sport_data': ['temporal', 'geographic', 'selection'],
        
        # === ÉTUDIANTS ===
        # Colonnes: id, nom, prenom, genre, age, pays, ville, type_etablissement, etablissement, niveau, email, moyenne, absence, diplome
        'students_education': ['gender', 'age', 'geographic'],
        'etudiants': ['gender', 'age', 'geographic'],
        
        # === TELECOM ===
        # Colonnes: id, nom_personne, operateur_telephonique, forfait_abonnement
        'telecom': ['selection', 'sampling'],
        'telecom_data': ['selection', 'sampling'],
        
        # === VÉHICULES ===
        # Colonnes: id, type_vehicule, marque_voiture, modele, annee_fabrication, prix, kilometrage
        'vehicules': ['temporal', 'socioeconomic', 'selection'],
        'vehicules_transport': ['temporal', 'socioeconomic', 'selection'],
        'transport': ['temporal', 'selection'],
    }
    
    # ✅ INTERDICTIONS STRICTES (basées sur absence de colonnes)
    FORBIDDEN_RULES = {
        # Pas de colonnes genre/âge
        'agriculture': ['gender', 'age', 'socioeconomic'],
        'agri_data': ['gender', 'age', 'socioeconomic'],
        'telecom': ['gender', 'age', 'socioeconomic', 'geographic', 'temporal'],
        'telecom_data': ['gender', 'age', 'socioeconomic', 'geographic', 'temporal'],
  
  'biens_complets': ['gender', 'age', 'geographic', 'temporal'],
  'biens_immobiliers': ['gender', 'age', 'geographic', 'temporal'],
  'immobilier': ['gender', 'age', 'geographic', 'temporal'],
  
  'chimie': ['gender', 'age', 'geographic', 'socioeconomic', 'temporal'],
  'chimie_data': ['gender', 'age', 'geographic', 'socioeconomic', 'temporal'],
  'Chimie_data': ['gender', 'age', 'geographic', 'socioeconomic', 'temporal'],
  
  'energie': ['gender', 'age'],
  'energie_mondiale': ['gender', 'age'],
  'centrales_energie': ['gender', 'age'],
  
  'finance': ['gender', 'age', 'temporal'],
  'finance_data': ['gender', 'age', 'temporal'],
  'transactions': ['gender', 'age', 'temporal'],
  
  'geo_info': ['gender', 'age', 'socioeconomic', 'temporal'],
  'geo_info_seed': ['gender', 'age', 'socioeconomic', 'temporal'],
  'géo_info_seed': ['gender', 'age', 'socioeconomic', 'temporal'],
  
  'market_data': ['gender', 'age', 'geographic', 'temporal'],
  'marche': ['gender', 'age', 'geographic', 'temporal'],
  
  'sport': ['gender', 'age'],
  'sport_data': ['gender', 'age'],
  
  'telecom': ['gender', 'age', 'geographic', 'socioeconomic', 'temporal'],
  'telecom_data': ['gender', 'age', 'geographic', 'socioeconomic', 'temporal'],
  
  'vehicules': ['gender', 'age', 'geographic'],
  'vehicules_transport': ['gender', 'age', 'geographic'],
  'transport': ['gender', 'age', 'geographic'],
    }
    
    forbidden_biases = []
    for cat_pattern, forbidden in FORBIDDEN_RULES.items():
        cat_pattern_norm = cat_pattern.lower().replace('_', '').replace('-', '')
        category_norm = category.lower().strip().replace('_', '').replace('-', '')
        
        # Vérification plus stricte de correspondance
        if (cat_pattern_norm == category_norm or 
            cat_pattern_norm in category_norm or 
            category_norm in cat_pattern_norm):
            forbidden_biases = forbidden
            print(f"   🚫 BLOCAGE STRICTE : {forbidden_biases}")
            break
    
    # Si on a des interdictions, on les applique immédiatement
    if forbidden_biases:
        available_biases = [b for b in available_biases 
                          if b['type'] not in forbidden_biases]
        
    # Normaliser catégorie
    category_norm = category.lower().strip().replace('_', '').replace('-', '')
    
    # ÉTAPE 1 : Obtenir biais disponibles
    available_types = [b['type'] for b in available_biases if b.get('available', False)]
    
    if not available_types:
        return {'type': None, 'reason': 'Aucun biais applicable'}
    
    print(f"\n🎯 SÉLECTION BIAIS pour '{category}'")
    print(f"   📋 Biais détectés: {available_types}")
    
    # ÉTAPE 2 : Appliquer règles d'EXCLUSION
    forbidden_biases = []
    for cat_pattern, forbidden in FORBIDDEN_RULES.items():
        cat_pattern_norm = cat_pattern.lower().replace('_', '').replace('-', '')
        if cat_pattern_norm in category_norm or category_norm in cat_pattern_norm:
            forbidden_biases = forbidden
            print(f"   🚫 BLOCAGE : {forbidden_biases}")
            break
    
    # FILTRER les biais interdits
    available_types_filtered = [b for b in available_types if b not in forbidden_biases]
    
    if not available_types_filtered:
        return {
            'type': None, 
            'reason': f'Tous les biais sont interdits pour {category}'
        }
    
    print(f"   ✅ Biais autorisés: {available_types_filtered}")
    
    # ÉTAPE 3 : Appliquer règles de PRIORITÉ
    priority_biases = None
    for cat_pattern, biases in CATEGORY_BIAS_RULES.items():
        cat_pattern_norm = cat_pattern.lower().replace('_', '').replace('-', '')
        if cat_pattern_norm in category_norm or category_norm in cat_pattern_norm:
            priority_biases = biases
            print(f"   🎯 Priorités: {biases}")
            break
    
    # ÉTAPE 4 : Heuristiques de fallback
    if not priority_biases:
        if any(kw in category_norm for kw in ['patient', 'etudiant', 'student', 'personne']):
            priority_biases = ['gender', 'age', 'selection']
        elif any(kw in category_norm for kw in ['animal', 'pet']):
            priority_biases = ['age', 'gender', 'selection']
        elif any(kw in category_norm for kw in ['vehicule', 'transport']):
            priority_biases = ['temporal', 'socioeconomic', 'selection']
        elif any(kw in category_norm for kw in ['finance', 'transaction']):
            priority_biases = ['socioeconomic', 'selection']
        else:
            priority_biases = ['selection', 'sampling']
    
    # ÉTAPE 5 : Sélectionner premier biais disponible
    for bias_type in priority_biases:
        if bias_type in available_types_filtered:
            bias_obj = next(b for b in available_biases if b['type'] == bias_type)
            print(f"   ✅ SÉLECTIONNÉ: {bias_type}")
            return {
                'type': bias_type,
                'name': bias_obj['name'],
                'reason': f"Biais '{bias_obj['name']}' sélectionné",
                'description': bias_obj['description']
            }
    
    # ÉTAPE 6 : Fallback
    if available_types_filtered:
        first = next(b for b in available_biases if b['type'] == available_types_filtered[0])
        return {
            'type': first['type'],
            'name': first['name'],
            'reason': 'Biais par défaut',
            'description': first['description']
        }
    
    return {'type': None, 'reason': 'Aucun biais disponible'}


def validate_bias_compatibility(category: str, bias_type: str) -> dict:
    """Validation stricte de compatibilité"""
    
    HARD_INCOMPATIBILITIES = {
        'agriculture': ['gender', 'age'],
        'biens_complets': ['gender', 'age', 'geographic', 'temporal'],
        'chimie': ['gender', 'age', 'geographic', 'socioeconomic', 'temporal'],
        'energie': ['gender', 'age'],
        'finance': ['gender', 'age', 'temporal'],
        'geo_info_seed': ['gender', 'age', 'socioeconomic', 'temporal'],
        'market_data': ['gender', 'age', 'geographic', 'temporal'],
        'sport': ['gender', 'age'],
        'telecom': ['gender', 'age', 'geographic', 'socioeconomic', 'temporal'],
        'vehicules': ['gender', 'age', 'geographic'],
    }
    
    category_norm = category.lower().strip().replace('_', '').replace('-', '')
    
    for cat_pattern, invalid_biases in HARD_INCOMPATIBILITIES.items():
        cat_pattern_norm = cat_pattern.lower().replace('_', '').replace('-', '')
        if cat_pattern_norm in category_norm or category_norm in cat_pattern_norm:
            if bias_type in invalid_biases:
                return {
                    'compatible': False,
                    'reason': f"❌ INCOMPATIBLE : '{bias_type}' impossible pour '{category}'"
                }
    
    return {'compatible': True, 'reason': f"✅ Compatible"}


# ==================== ENDPOINTS ====================

@app.route('/health', methods=['GET', 'OPTIONS'])
def health_check():
    if request.method == 'OPTIONS':
        return '', 204
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "llm_available": llm_handler is not None
    })


@app.route('/categories', methods=['GET', 'OPTIONS'])
def get_categories():
    if request.method == 'OPTIONS':
        return '', 204
    
    try:
        categories = generator.get_available_categories()
        return jsonify({
            "success": True,
            "categories": categories,
            "count": len(categories)
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/biases/<category>', methods=['GET', 'OPTIONS'])
def get_biases_for_category(category):
    """OPTIMISÉ : Utilise le cache"""
    if request.method == 'OPTIONS':
        return '', 204
    
    try:
        print(f"📥 Demande biais pour: {category}")
        start = time.time()
        
        biases = get_cached_biases(category)
        
        print(f"   ✅ Réponse en {time.time() - start:.2f}s")
        
        return jsonify({
            "success": True,
            "category": category,
            "available_biases": biases
        })
    except Exception as e:
        print(f"❌ Erreur get_biases: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/generate', methods=['POST', 'OPTIONS'])
def generate_dataset():
    """Génération avec sélection intelligente"""
    if request.method == 'OPTIONS':
        return '', 204
        
    try:
        data = request.get_json()
        print(f"\n{'='*80}")
        print(f"📥 NOUVELLE GÉNÉRATION")
        print(f"{'='*80}")
        
        if 'category' not in data:
            return jsonify({"success": False, "error": "Paramètre 'category' requis"}), 400
        
        category = data['category']
        n_samples = data.get('n_samples', 1000)
        bias_type = data.get('bias_type')
        bias_intensity = data.get('bias_intensity', 0.5)
        bias_params = data.get('bias_params', {})
        
        total_start = time.time()
        
        # Détecter biais disponibles
        print(f"🔍 Détection biais pour: {category}")
        detect_start = time.time()
        
        try:
            available_biases = get_cached_biases(category)
        except Exception as e:
            print(f"⚠️ Erreur détection: {e}")
            available_biases = []
        
        print(f"   ⏱️ Détection: {time.time() - detect_start:.2f}s")
        
        # Sélection intelligente
        if not bias_type and available_biases:
            smart_selection = select_best_bias(category, available_biases)
            
            if smart_selection['type']:
                bias_type = smart_selection['type']
                print(f"🎯 {smart_selection['reason']}")
            else:
                print(f"ℹ️ {smart_selection['reason']}")
        
        # Validation
        if bias_type:
            validation = validate_bias_compatibility(category, bias_type)
            if not validation['compatible']:
                print(validation['reason'])
                print("🔄 Recherche biais compatible...")
                smart_selection = select_best_bias(category, available_biases)
                if smart_selection['type']:
                    bias_type = smart_selection['type']
                    print(f"✅ Nouveau: {bias_type}")
                else:
                    bias_type = None
                    print("⚠️ Génération neutre")
        
        print(f"\n🎯 CONFIG FINALE:")
        print(f"   • Catégorie: {category}")
        print(f"   • Échantillons: {n_samples}")
        print(f"   • Biais: {bias_type or 'AUCUN'}")
        print(f"   • Intensité: {bias_intensity}")
        
        # Génération
        print(f"\n📊 GÉNÉRATION DES DONNÉES...")
        gen_start = time.time()
        
        result = generator.generate(
            category=category,
            n_samples=n_samples,
            bias_type=bias_type,
            bias_intensity=bias_intensity,
            bias_params=bias_params
        )
        
        gen_time = time.time() - gen_start
        total_time = time.time() - total_start
        
        print(f"\n⏱️ TEMPS:")
        print(f"   • Génération: {gen_time:.2f}s")
        print(f"   • Total: {total_time:.2f}s")
        print(f"{'='*80}\n")
        
        if result.get('success'):
            if 'smart_selection' in locals():
                result['bias_selection_info'] = smart_selection
            
            result['generation_time'] = round(gen_time, 2)
            result['total_time'] = round(total_time, 2)
            
            return jsonify(result), 200
        else:
            print(f"❌ Erreur: {result.get('error')}")
            return jsonify(result), 400
            
    except Exception as e:
        print(f"❌ Exception: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/download/<filename>', methods=['GET', 'OPTIONS'])
def download_file(filename):
    if request.method == 'OPTIONS':
        return '', 204
    
    try:
        filename = filename.replace('output/', '').replace('output\\', '')
        file_path = os.path.join(generator.output_dir, filename)
        
        if not os.path.exists(file_path):
            return jsonify({"success": False, "error": "Fichier introuvable"}), 404
        
        return send_file(file_path, as_attachment=True, download_name=filename)
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/parse-prompt', methods=['POST', 'OPTIONS'])
def parse_prompt():
    if request.method == 'OPTIONS':
        return '', 204
        
    try:
        data = request.get_json()
        prompt = data.get('prompt', '').strip()
        
        if not prompt:
            return jsonify({"success": False, "error": "Prompt vide"}), 400
        
        categories = generator.get_available_categories()
        
        if llm_handler:
            try:
                parsed = llm_handler.parse_prompt(prompt, categories)
            except Exception as e:
                parsed = _parse_user_prompt(prompt, categories)
        else:
            parsed = _parse_user_prompt(prompt, categories)
        
        return jsonify({
            "success": True,
            "parsed": parsed,
            "original_prompt": prompt
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


def _parse_user_prompt(prompt: str, categories: list) -> dict:
    """Parse basique"""
    import re
    
    result = {
        "category": None,
        "n_samples": 1000,
        "bias_type": None,
        "bias_intensity": 0.5
    }
    
    prompt_lower = prompt.lower()
    
    for cat in categories:
        if cat.lower() in prompt_lower:
            result["category"] = cat
            break
    
    numbers = re.findall(r'\b(\d+)\b', prompt)
    if numbers:
        result["n_samples"] = int(numbers[0])
    
    bias_keywords = {
        "genre": "gender", "gender": "gender",
        "âge": "age", "age": "age",
        "géographique": "geographic", "geographic": "geographic",
        "socio": "socioeconomic", "économique": "socioeconomic",
        "échantillonnage": "sampling", "sampling": "sampling",
        "sélection": "selection", "selection": "selection",
        "temporel": "temporal", "temporal": "temporal"
    }
    
    for keyword, bias_type in bias_keywords.items():
        if keyword in prompt_lower:
            result["bias_type"] = bias_type
            break
    
    return result


@app.route('/stats', methods=['GET', 'OPTIONS'])
def get_statistics():
    if request.method == 'OPTIONS':
        return '', 204
    
    try:
        stats = generator.model_manager.get_statistics()
        
        output_files = []
        if os.path.exists(generator.output_dir):
            output_files = [f for f in os.listdir(generator.output_dir) 
                          if f.endswith('.csv') or f.endswith('.json') or f.endswith('.png')]
        
        stats["generated_files"] = len(output_files)
        stats["output_directory"] = generator.output_dir
        
        return jsonify({"success": True, "statistics": stats})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


def preload_popular_models():
    """Précharge les modèles populaires"""
    print("\n🔄 Préchargement des modèles populaires...")
    
    popular = ['students_education', 'patients', 'vehicules_transport', 
               'finance_data', 'agri_data']
    
    for cat in popular:
        try:
            generator.model_manager.load_model(cat)
            get_cached_biases(cat)
            print(f"   ✅ {cat}")
        except Exception as e:
            print(f"   ⚠️ {cat} non disponible")
    
    print("✅ Préchargement terminé\n")


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('DEBUG', 'True').lower() == 'true'
    
    print(f"\n{'='*80}")
    print(f"🚀 API FLASK - Version CORRIGÉE")
    print(f"{'='*80}")
    print(f"📡 Serveur: http://localhost:{port}")
    print(f"🐛 Debug: {debug}")
    print(f"🤖 LLM: {llm_provider}")
    print(f"📂 Modèles: {os.getenv('MODELS_DIR', 'models')}")
    print(f"📁 Output: {os.getenv('OUTPUT_DIR', 'output')}")
    print(f"{'='*80}\n")
    
    preload_popular_models()
    
    app.run(host='0.0.0.0', port=port, debug=debug, use_reloader=False)