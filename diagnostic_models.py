"""
Script de Diagnostic pour Analyser vos Modèles CTGAN
Identifie automatiquement les colonnes disponibles et les biais applicables
"""

import os
import torch
from ctgan import CTGAN
import pandas as pd
from smart_bias_injector import SmartBiasInjector

# Configuration PyTorch 2.6
import torch.serialization
from ctgan.synthesizers.ctgan import CTGAN as CTGANClass
from ctgan.data_transformer import DataTransformer, SpanInfo
from ctgan.data_sampler import DataSampler

torch.serialization.add_safe_globals([
    CTGANClass, DataTransformer, DataSampler, SpanInfo
])

MODELS_DIR = "models"

def diagnose_model(model_path):
    """Analyse complète d'un modèle"""
    
    filename = os.path.basename(model_path)
    print("\n" + "="*80)
    print(f"📊 ANALYSE: {filename}")
    print("="*80)
    
    try:
        # 1. Charger le modèle
        print("🔄 Chargement du modèle...")
        
        try:
            model = CTGAN.load(model_path)
            print("✅ Modèle chargé (méthode normale)")
        except:
            original_load = torch.load
            torch.load = lambda *args, **kwargs: original_load(*args, **{**kwargs, 'weights_only': False})
            model = CTGAN.load(model_path)
            torch.load = original_load
            print("✅ Modèle chargé (mode compatibilité)")
        
        # 2. Générer un échantillon
        print("🔄 Génération d'un échantillon de test...")
        df = model.sample(100)
        
        print(f"\n📋 COLONNES DÉTECTÉES ({len(df.columns)}):")
        print("-" * 80)
        
        for i, col in enumerate(df.columns, 1):
            dtype = df[col].dtype
            unique_vals = df[col].nunique()
            sample_vals = df[col].head(3).tolist()
            
            print(f"{i:2d}. {col:30s} │ Type: {str(dtype):10s} │ Valeurs uniques: {unique_vals:4d}")
            print(f"    Échantillon: {sample_vals}")
        
        # 3. Analyser avec SmartBiasInjector
        print("\n🔍 ANALYSE DES BIAIS APPLICABLES:")
        print("-" * 80)
        
        injector = SmartBiasInjector()
        available_biases = injector.get_available_biases(df)
        
        if not available_biases:
            print("⚠️  Aucun biais automatiquement détecté")
            print("\n💡 Colonnes candidates pour biais:")
            
            # Identifier colonnes catégorielles
            categorical_cols = df.select_dtypes(include=['object', 'category']).columns
            for col in categorical_cols:
                unique_count = df[col].nunique()
                if 2 <= unique_count <= 20:  # Bon candidat
                    print(f"   ✓ {col} ({unique_count} catégories) : {df[col].unique()[:5].tolist()}")
        else:
            print(f"✅ {len(available_biases)} biais détectés automatiquement:")
            
            for bias_type in available_biases:
                detection = injector.detect_columns(df, bias_type)
                prot_attr = detection['protected_attribute']
                target_col = detection['target_column']
                
                print(f"\n   🎯 {bias_type.upper()}")
                print(f"      Colonne protégée: {prot_attr}")
                print(f"      Colonne cible: {target_col}")
                
                # Tester l'injection
                try:
                    df_test, config = injector.inject_bias(
                        df.copy(), 
                        bias_type=bias_type, 
                        intensity=1.0
                    )
                    print(f"      ✅ Test d'injection réussi")
                    
                    # Afficher les groupes
                    groups = df[prot_attr].unique()
                    print(f"      Groupes: {groups[:5].tolist()}")
                    
                except Exception as e:
                    print(f"      ❌ Erreur: {str(e)[:60]}")
        
        # 4. Statistiques générales
        print("\n📊 STATISTIQUES:")
        print("-" * 80)
        print(f"Lignes générées: {len(df)}")
        print(f"Colonnes: {len(df.columns)}")
        print(f"Colonnes numériques: {len(df.select_dtypes(include=['number']).columns)}")
        print(f"Colonnes catégorielles: {len(df.select_dtypes(include=['object', 'category']).columns)}")
        
        # 5. Recommandations
        print("\n💡 RECOMMANDATIONS:")
        print("-" * 80)
        
        if available_biases:
            print(f"✅ Ce modèle supporte les biais: {', '.join(available_biases)}")
            print(f"   Exemple de prompt: 'Génère 5000 {filename.split('_')[0]} avec biais {available_biases[0]}'")
        else:
            print("⚠️  Configuration manuelle nécessaire")
            print("   1. Identifiez une colonne catégorielle (2-20 catégories)")
            print("   2. Identifiez une colonne numérique cible")
            print("   3. Ajoutez-les dans smart_bias_injector.py")
        
        return True
        
    except Exception as e:
        print(f"❌ ERREUR: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Analyse tous les modèles du dossier"""
    
    print("\n" + "="*80)
    print("🔬 DIAGNOSTIC DES MODÈLES CTGAN")
    print("="*80)
    
    if not os.path.exists(MODELS_DIR):
        print(f"❌ Dossier '{MODELS_DIR}' non trouvé")
        return
    
    model_files = [f for f in os.listdir(MODELS_DIR) if f.endswith('.pkl')]
    
    if not model_files:
        print(f"❌ Aucun fichier .pkl trouvé dans '{MODELS_DIR}'")
        return
    
    print(f"\n📁 {len(model_files)} modèles trouvés\n")
    
    results = {}
    
    for model_file in model_files:
        model_path = os.path.join(MODELS_DIR, model_file)
        success = diagnose_model(model_path)
        results[model_file] = success
    
    # Résumé final
    print("\n" + "="*80)
    print("📊 RÉSUMÉ")
    print("="*80)
    
    for model_file, success in results.items():
        status = "✅" if success else "❌"
        print(f"{status} {model_file}")
    
    successful = sum(results.values())
    print(f"\n{successful}/{len(results)} modèles analysés avec succès")
    
    if successful < len(results):
        print("\n💡 Pour les modèles en erreur:")
        print("   - Vérifiez qu'ils sont compatibles CTGAN")
        print("   - Testez le chargement manuel avec torch.load")


if __name__ == '__main__':
    main()