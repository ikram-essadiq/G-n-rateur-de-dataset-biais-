import os
import json
import argparse
import pandas as pd
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

try:
    from ctgan import CTGAN
    from sdv.metadata import SingleTableMetadata
    from scipy import stats
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import accuracy_score, classification_report
except ImportError:
    print("❌ ERREUR: Bibliothèques non installées")
    print("📦 Installez avec: pip install ctgan sdv scipy scikit-learn")
    exit(1)

# ====================
# MÉTRIQUES D'ÉVALUATION
# ====================

def evaluate_distribution_similarity(real_data, synthetic_data):
    """
    Compare les distributions statistiques entre données réelles et synthétiques
    """
    print("\n" + "="*80)
    print("📊 ÉVALUATION DE LA SIMILARITÉ DES DISTRIBUTIONS")
    print("="*80 + "\n")
    
    metrics = {}
    
    # Pour chaque colonne numérique
    numeric_cols = real_data.select_dtypes(include=[np.number]).columns
    
    for col in numeric_cols:
        if col in synthetic_data.columns:
            real_vals = real_data[col].dropna()
            synth_vals = synthetic_data[col].dropna()
            
            # Test de Kolmogorov-Smirnov
            ks_stat, ks_pval = stats.ks_2samp(real_vals, synth_vals)
            
            # Différence de moyenne et écart-type
            mean_diff = abs(real_vals.mean() - synth_vals.mean())
            std_diff = abs(real_vals.std() - synth_vals.std())
            
            metrics[col] = {
                "ks_statistic": round(ks_stat, 4),
                "ks_pvalue": round(ks_pval, 4),
                "mean_difference": round(mean_diff, 4),
                "std_difference": round(std_diff, 4),
                "similarity_score": round(1 - ks_stat, 4)  # Plus proche de 1 = plus similaire
            }
            
            print(f"📈 {col}:")
            print(f"   • Similarité : {metrics[col]['similarity_score']:.3f} (0-1, 1=parfait)")
            print(f"   • KS Test    : stat={ks_stat:.4f}, p-value={ks_pval:.4f}")
            print(f"   • Δ Moyenne  : {mean_diff:.4f}")
            print(f"   • Δ Écart-type: {std_diff:.4f}")
            print()
    
    # Score global de similarité
    if metrics:
        avg_similarity = np.mean([m['similarity_score'] for m in metrics.values()])
        print(f"🎯 SCORE GLOBAL DE SIMILARITÉ: {avg_similarity:.3f} / 1.00")
        
        if avg_similarity > 0.90:
            print("   ✅ Excellent! Distributions très similaires")
        elif avg_similarity > 0.75:
            print("   ✓ Bon! Distributions acceptables")
        elif avg_similarity > 0.60:
            print("   ⚠️ Moyen. Considérez plus d'epochs d'entraînement")
        else:
            print("   ❌ Faible. Le modèle nécessite plus d'entraînement")
    
    return metrics

def evaluate_categorical_similarity(real_data, synthetic_data):
    """
    Compare les distributions catégorielles
    """
    print("\n" + "="*80)
    print("📊 ÉVALUATION DES COLONNES CATÉGORIELLES")
    print("="*80 + "\n")
    
    categorical_cols = real_data.select_dtypes(include=['object']).columns
    metrics = {}
    
    for col in categorical_cols:
        if col in synthetic_data.columns:
            real_dist = real_data[col].value_counts(normalize=True)
            synth_dist = synthetic_data[col].value_counts(normalize=True)
            
            # Total Variation Distance
            all_categories = set(real_dist.index) | set(synth_dist.index)
            tvd = 0
            for cat in all_categories:
                real_prob = real_dist.get(cat, 0)
                synth_prob = synth_dist.get(cat, 0)
                tvd += abs(real_prob - synth_prob)
            tvd = tvd / 2
            
            similarity = 1 - tvd
            metrics[col] = {
                "tvd": round(tvd, 4),
                "similarity": round(similarity, 4)
            }
            
            print(f"📊 {col}:")
            print(f"   • Similarité : {similarity:.3f}")
            print(f"   • TVD        : {tvd:.4f}")
            
            # Afficher les distributions
            print(f"   • Distribution réelle vs synthétique:")
            comparison = pd.DataFrame({
                'Réel %': real_dist * 100,
                'Synthétique %': synth_dist * 100
            }).fillna(0)
            print(comparison.head().to_string(float_format='%.1f'))
            print()
    
    if metrics:
        avg_similarity = np.mean([m['similarity'] for m in metrics.values()])
        print(f"🎯 SIMILARITÉ CATÉGORIELLE MOYENNE: {avg_similarity:.3f} / 1.00")
    
    return metrics

def machine_learning_efficacy_test(real_data, synthetic_data, target_column=None):
    """
    Test TSTR (Train on Synthetic, Test on Real)
    Mesure si un modèle entraîné sur données synthétiques performe sur données réelles
    """
    print("\n" + "="*80)
    print("🤖 TEST D'EFFICACITÉ ML (TSTR - Train Synthetic, Test Real)")
    print("="*80 + "\n")
    
    # Trouver automatiquement une colonne cible catégorielle
    if target_column is None:
        categorical_cols = real_data.select_dtypes(include=['object']).columns
        if len(categorical_cols) == 0:
            print("⚠️ Aucune colonne catégorielle trouvée pour le test ML")
            return None
        target_column = categorical_cols[0]
    
    if target_column not in real_data.columns or target_column not in synthetic_data.columns:
        print(f"⚠️ Colonne cible '{target_column}' non trouvée")
        return None
    
    print(f"🎯 Colonne cible pour classification: {target_column}\n")
    
    try:
        # Préparer les données
        X_real = real_data.drop(columns=[target_column]).select_dtypes(include=[np.number])
        y_real = real_data[target_column]
        
        X_synthetic = synthetic_data.drop(columns=[target_column]).select_dtypes(include=[np.number])
        y_synthetic = synthetic_data[target_column]
        
        # Aligner les colonnes
        common_cols = list(set(X_real.columns) & set(X_synthetic.columns))
        X_real = X_real[common_cols]
        X_synthetic = X_synthetic[common_cols]
        
        if len(common_cols) == 0:
            print("⚠️ Aucune colonne numérique commune trouvée")
            return None
        
        # Split données réelles
        X_real_train, X_real_test, y_real_train, y_real_test = train_test_split(
            X_real, y_real, test_size=0.3, random_state=42
        )
        
        # Modèle 1: Entraîné sur RÉELLES, testé sur RÉELLES (baseline)
        print("📌 Modèle 1: Train RÉEL → Test RÉEL (baseline)")
        clf_real = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
        clf_real.fit(X_real_train, y_real_train)
        y_pred_real = clf_real.predict(X_real_test)
        acc_real = accuracy_score(y_real_test, y_pred_real)
        print(f"   ✓ Accuracy: {acc_real:.4f}\n")
        
        # Modèle 2: Entraîné sur SYNTHÉTIQUES, testé sur RÉELLES (TSTR)
        print("📌 Modèle 2: Train SYNTHÉTIQUE → Test RÉEL (TSTR)")
        clf_synthetic = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
        clf_synthetic.fit(X_synthetic, y_synthetic)
        y_pred_synthetic = clf_synthetic.predict(X_real_test)
        acc_synthetic = accuracy_score(y_real_test, y_pred_synthetic)
        print(f"   ✓ Accuracy: {acc_synthetic:.4f}\n")
        
        # Ratio d'efficacité
        efficacy_ratio = acc_synthetic / acc_real if acc_real > 0 else 0
        
        print("="*80)
        print(f"📊 RÉSULTATS COMPARATIFS:")
        print(f"   • Baseline (Réel→Réel)      : {acc_real:.4f}")
        print(f"   • TSTR (Synthétique→Réel)   : {acc_synthetic:.4f}")
        print(f"   • Ratio d'efficacité        : {efficacy_ratio:.4f}")
        print()
        
        if efficacy_ratio > 0.95:
            print("   ✅ Excellent! Les données synthétiques sont très utiles")
        elif efficacy_ratio > 0.85:
            print("   ✓ Bon! Les données synthétiques sont exploitables")
        elif efficacy_ratio > 0.70:
            print("   ⚠️ Moyen. Les données synthétiques perdent de l'information")
        else:
            print("   ❌ Faible. Les données synthétiques ne capturent pas bien les patterns")
        
        # Rapport de classification détaillé
        print("\n📋 Rapport de classification (TSTR):")
        print(classification_report(y_real_test, y_pred_synthetic, zero_division=0))
        
        return {
            "baseline_accuracy": acc_real,
            "tstr_accuracy": acc_synthetic,
            "efficacy_ratio": efficacy_ratio,
            "target_column": target_column
        }
        
    except Exception as e:
        print(f"⚠️ Erreur lors du test ML: {e}")
        return None

def calculate_privacy_metrics(real_data, synthetic_data):
    """
    Évalue si les données synthétiques ne copient pas exactement les données réelles
    """
    print("\n" + "="*80)
    print("🔒 ÉVALUATION DE LA CONFIDENTIALITÉ")
    print("="*80 + "\n")
    
    # Distance entre lignes réelles et synthétiques
    numeric_cols = real_data.select_dtypes(include=[np.number]).columns
    
    if len(numeric_cols) == 0:
        print("⚠️ Aucune colonne numérique pour évaluer la confidentialité")
        return None
    
    real_normalized = real_data[numeric_cols].fillna(0)
    synth_normalized = synthetic_data[numeric_cols].fillna(0)
    
    # Normaliser
    from sklearn.preprocessing import StandardScaler
    scaler = StandardScaler()
    real_scaled = scaler.fit_transform(real_normalized)
    synth_scaled = scaler.transform(synth_normalized)
    
    # Calculer distance minimale entre chaque ligne synthétique et toutes les réelles
    min_distances = []
    sample_size = min(100, len(synth_scaled))  # Limiter pour performance
    
    for i in range(sample_size):
        distances = np.sqrt(np.sum((real_scaled - synth_scaled[i])**2, axis=1))
        min_distances.append(distances.min())
    
    avg_min_distance = np.mean(min_distances)
    
    print(f"📏 Distance minimale moyenne: {avg_min_distance:.4f}")
    
    if avg_min_distance > 2.0:
        print("   ✅ Excellent! Peu de risque de copie exacte")
    elif avg_min_distance > 1.0:
        print("   ✓ Bon! Distance raisonnable")
    elif avg_min_distance > 0.5:
        print("   ⚠️ Attention! Certaines lignes sont très proches des réelles")
    else:
        print("   ❌ Risque! Possible copie de lignes réelles")
    
    return {
        "avg_min_distance": avg_min_distance,
        "risk_level": "low" if avg_min_distance > 2.0 else "medium" if avg_min_distance > 1.0 else "high"
    }

def comprehensive_evaluation(real_data, synthetic_data, target_column=None):
    """
    Évaluation complète des données synthétiques
    """
    print("\n" + "🎯"*40)
    print("🎯" + " "*15 + "ÉVALUATION COMPLÈTE DES DONNÉES SYNTHÉTIQUES" + " "*15 + "🎯")
    print("🎯"*40 + "\n")
    
    all_metrics = {}
    
    # 1. Similarité des distributions numériques
    dist_metrics = evaluate_distribution_similarity(real_data, synthetic_data)
    all_metrics['distribution_similarity'] = dist_metrics
    
    # 2. Similarité catégorielle
    cat_metrics = evaluate_categorical_similarity(real_data, synthetic_data)
    all_metrics['categorical_similarity'] = cat_metrics
    
    # 3. Test d'efficacité ML
    ml_metrics = machine_learning_efficacy_test(real_data, synthetic_data, target_column)
    all_metrics['ml_efficacy'] = ml_metrics
    
    # 4. Métriques de confidentialité
    privacy_metrics = calculate_privacy_metrics(real_data, synthetic_data)
    all_metrics['privacy'] = privacy_metrics
    
    # Score global
    print("\n" + "="*80)
    print("🏆 SCORE GLOBAL DE QUALITÉ")
    print("="*80)
    
    scores = []
    
    if dist_metrics:
        dist_score = np.mean([m['similarity_score'] for m in dist_metrics.values()])
        scores.append(dist_score)
        print(f"   📊 Similarité Distribution : {dist_score:.3f}")
    
    if cat_metrics:
        cat_score = np.mean([m['similarity'] for m in cat_metrics.values()])
        scores.append(cat_score)
        print(f"   📊 Similarité Catégorielle: {cat_score:.3f}")
    
    if ml_metrics and ml_metrics['efficacy_ratio'] > 0:
        scores.append(ml_metrics['efficacy_ratio'])
        print(f"   🤖 Efficacité ML (TSTR)   : {ml_metrics['efficacy_ratio']:.3f}")
    
    if scores:
        overall_score = np.mean(scores)
        print(f"\n   🎯 SCORE GLOBAL: {overall_score:.3f} / 1.00")
        
        if overall_score > 0.90:
            grade = "A+ (Excellent)"
        elif overall_score > 0.80:
            grade = "A (Très Bon)"
        elif overall_score > 0.70:
            grade = "B (Bon)"
        elif overall_score > 0.60:
            grade = "C (Acceptable)"
        else:
            grade = "D (Insuffisant)"
        
        print(f"   📝 NOTE: {grade}")
    
    print("="*80 + "\n")
    
    return all_metrics

# ====================
# FONCTIONS UTILITAIRES (code existant)
# ====================

def detect_column_types(df):
    """Détecte automatiquement les types de colonnes"""
    discrete_columns = []
    continuous_columns = []
    
    for col in df.columns:
        if 'id' in col.lower() or 'uuid' in col.lower():
            discrete_columns.append(col)
            continue
        
        if df[col].dtype == 'object' or df[col].nunique() < 10:
            discrete_columns.append(col)
        else:
            continuous_columns.append(col)
    
    return discrete_columns, continuous_columns

def create_metadata(df, discrete_columns):
    """Crée les métadonnées pour SDV"""
    metadata = SingleTableMetadata()
    metadata.detect_from_dataframe(df)
    
    for col in discrete_columns:
        if col in df.columns:
            metadata.update_column(col, sdtype='categorical')
    
    return metadata

def validate_dataset(df):
    """Valide que le dataset est prêt pour l'entraînement"""
    print("\n✓ Validation du dataset...")
    
    issues = []
    
    if len(df) < 100:
        issues.append(f"  ⚠️ Dataset trop petit: {len(df)} lignes (minimum recommandé: 500)")
    
    missing = df.isnull().sum()
    if missing.sum() > 0:
        issues.append(f"  ⚠️ Valeurs manquantes détectées: {missing[missing > 0].to_dict()}")
    
    for col in df.columns:
        if df[col].nunique() == 1:
            issues.append(f"  ⚠️ Colonne constante: {col}")
    
    if issues:
        print("\n  Avertissements:")
        for issue in issues:
            print(f"   {issue}")
        print("\n✓ Le modèle peut être entraîné mais la qualité pourrait être affectée.\n")
    else:
        print("✓ Dataset valide!\n")
    
    return len(issues) == 0

def print_training_info(df, discrete_cols, continuous_cols, epochs):
    """Affiche les informations d'entraînement"""
    print("="*80)
    print("⚙️ INFORMATIONS D'ENTRAÎNEMENT")
    print("="*80)
    print(f"📊 Lignes            : {len(df)}")
    print(f"📊 Colonnes          : {len(df.columns)}")
    print(f"🔤 Colonnes discrètes: {len(discrete_cols)} → {discrete_cols}")
    print(f"🔢 Colonnes continues: {len(continuous_cols)} → {continuous_cols}")
    print(f"🔄 Epochs            : {epochs}")
    print(f"💾 Taille mémoire    : {df.memory_usage(deep=True).sum() / 1024:.2f} KB")
    print("="*80 + "\n")

# ====================
# ENTRAÎNEMENT CTGAN
# ====================

def train_ctgan(csv_file, output_name=None, epochs=300, batch_size=500, 
                discrete_columns=None, auto_detect=True, save_model=True):
    """Entraîne un modèle CTGAN sur un dataset"""
    
    print("\n" + "="*80)
    print("🚀 ENTRAÎNEMENT CTGAN")
    print("="*80 + "\n")
    
    print(f"📂 Chargement du dataset: {csv_file}")
    try:
        df = pd.read_csv(csv_file)
        print(f"✓ Dataset chargé: {len(df)} lignes, {len(df.columns)} colonnes\n")
    except Exception as e:
        print(f"❌ Erreur lors du chargement: {e}")
        return None
    
    print("👁️ Aperçu du dataset:")
    print(df.head(3))
    print()
    
    validate_dataset(df)
    
    if discrete_columns is None and auto_detect:
        discrete_cols, continuous_cols = detect_column_types(df)
    elif discrete_columns:
        discrete_cols = discrete_columns
        continuous_cols = [col for col in df.columns if col not in discrete_cols]
    else:
        discrete_cols = []
        continuous_cols = list(df.columns)
    
    print_training_info(df, discrete_cols, continuous_cols, epochs)
    
    print("⚙️ Initialisation du modèle CTGAN...")
    model = CTGAN(
        epochs=epochs,
        batch_size=batch_size,
        verbose=True,
        cuda=False
    )
    
    print(f"\n🚀 Début de l'entraînement ({epochs} epochs)...")
    print("⏳ Cela peut prendre plusieurs minutes...\n")
    
    start_time = datetime.now()
    
    try:
        model.fit(df, discrete_columns=discrete_cols)
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        print(f"\n✅ Entraînement terminé en {duration:.2f} secondes ({duration/60:.2f} minutes)")
        
    except Exception as e:
        print(f"\n❌ Erreur lors de l'entraînement: {e}")
        import traceback
        traceback.print_exc()
        return None
    
    if save_model:
        if output_name is None:
            output_name = os.path.splitext(os.path.basename(csv_file))[0] + "_ctgan"
        
        model_path = f"{output_name}.pkl"
        print(f"\n💾 Sauvegarde du modèle: {model_path}")
        try:
            model.save(model_path)
            print(f"✅ Modèle sauvegardé avec succès!")
            
            metadata = {
                "training_file": csv_file,
                "n_samples": len(df),
                "n_columns": len(df.columns),
                "columns": list(df.columns),
                "discrete_columns": discrete_cols,
                "continuous_columns": continuous_cols,
                "epochs": epochs,
                "batch_size": batch_size,
                "training_duration": duration,
                "trained_at": datetime.now().isoformat()
            }
            
            metadata_path = f"{output_name}_metadata.json"
            with open(metadata_path, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2, ensure_ascii=False)
            print(f"✅ Métadonnées sauvegardées: {metadata_path}")
            
        except Exception as e:
            print(f"❌ Erreur lors de la sauvegarde: {e}")
    
    return model, df  # Retourner aussi les données réelles

# ====================
# GÉNÉRATION DE SAMPLES
# ====================

def generate_samples(model, n_samples=1000, output_file=None, real_data=None, evaluate=True, target_col=None):
    """Génère des échantillons synthétiques avec le modèle entraîné"""
    
    print(f"\n{'='*80}")
    print(f"🎲 GÉNÉRATION DE {n_samples} ÉCHANTILLONS SYNTHÉTIQUES")
    print("="*80 + "\n")
    
    try:
        synthetic_data = model.sample(n_samples)
        print(f"✅ {n_samples} échantillons générés!\n")
        
        print("👁️ Aperçu des données synthétiques:")
        print(synthetic_data.head(5))
        print()
        
        if output_file:
            synthetic_data.to_csv(output_file, index=False)
            print(f"\n💾 Données synthétiques sauvegardées: {output_file}")
        
        # Évaluation si demandé
        if evaluate and real_data is not None:
            metrics = comprehensive_evaluation(real_data, synthetic_data, target_col)
            
            # Sauvegarder les métriques
            if output_file:
                metrics_file = output_file.replace('.csv', '_metrics.json')
                with open(metrics_file, 'w', encoding='utf-8') as f:
                    json.dump(metrics, f, indent=2, ensure_ascii=False, default=str)
                print(f"\n💾 Métriques sauvegardées: {metrics_file}")
        
        return synthetic_data
        
    except Exception as e:
        print(f"❌ Erreur lors de la génération: {e}")
        return None

# ====================
# CLI
# ====================

def main():
    parser = argparse.ArgumentParser(
        description="🚀 Entraînement CTGAN avec évaluation complète",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
EXEMPLES:

🔹 ENTRAÎNEMENT BASIQUE:
  python train_ctgan.py --input data.csv --epochs 300

🔹 AVEC GÉNÉRATION ET ÉVALUATION:
  python train_ctgan.py --input data.csv --generate 1000 --evaluate

🔹 SPÉCIFIER COLONNE CIBLE POUR TEST ML:
  python train_ctgan.py --input data.csv --generate 1000 --evaluate --target-col type_energie

MÉTRIQUES CALCULÉES:
  📊 Similarité des distributions (KS Test)
  📊 Similarité catégorielle (TVD)
  🤖 Efficacité ML (TSTR - Train Synthetic, Test Real)
  🔒 Confidentialité (distance minimale)
  🎯 Score global de qualité
        """
    )
    
    parser.add_argument("--input", "-i", required=True, help="Fichier CSV d'entrée")
    parser.add_argument("--epochs", "-e", type=int, default=300, help="Nombre d'epochs")
    parser.add_argument("--batch-size", "-b", type=int, default=500, help="Taille des batchs")
    parser.add_argument("--output-model", "-om", default=None, help="Nom du modèle")
    parser.add_argument("--discrete", "-d", default=None, help="Colonnes discrètes (séparées par virgule)")
    parser.add_argument("--generate", "-g", type=int, default=0, help="Générer N échantillons")
    parser.add_argument("--output", "-o", default=None, help="Fichier CSV de sortie")
    parser.add_argument("--evaluate", action="store_true", help="Évaluer la qualité des données synthétiques")
    parser.add_argument("--target-col", default=None, help="Colonne cible pour test ML")
    parser.add_argument("--no-save", action="store_true", help="Ne pas sauvegarder le modèle")
    parser.add_argument("--no-auto-detect", action="store_true", help="Désactiver détection auto")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.input):
        print(f"❌ Fichier introuvable: {args.input}")
        return
    
    discrete_cols = None
    if args.discrete:
        discrete_cols = [col.strip() for col in args.discrete.split(',')]
    
    result = train_ctgan(
        csv_file=args.input,
        output_name=args.output_model,
        epochs=args.epochs,
        batch_size=args.batch_size,
        discrete_columns=discrete_cols,
        auto_detect=not args.no_auto_detect,
        save_model=not args.no_save
    )
    
    if result is None:
        print("\n❌ L'entraînement a échoué.")
        return
    
    model, real_data = result
    
    if args.generate > 0:
        output_file = args.output
        if output_file is None:
            base_name = os.path.splitext(args.input)[0]
            output_file = f"{base_name}_synthetic_{args.generate}.csv"
        
        generate_samples(
            model, 
            n_samples=args.generate, 
            output_file=output_file,
            real_data=real_data if args.evaluate else None,
            evaluate=args.evaluate,
            target_col=args.target_col
        )
    
    print("\n" + "="*80)
    print("✨ PROCESSUS TERMINÉ AVEC SUCCÈS!")
    print("="*80 + "\n")

if __name__ == "__main__":
    main()