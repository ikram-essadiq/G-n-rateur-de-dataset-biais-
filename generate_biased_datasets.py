

import argparse
import os
import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
from ctgan import CTGAN
from universal_bias_injector import UniversalBiasInjector

# Configuration visuelle
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

def create_comparison_visualizations(df_original, df_biased, bias_config, output_dir):
    """
    Crée des visualisations comparatives entre original et biaisé
    """
    
    protected_attr = bias_config.get('protected_attribute')
    target_col = bias_config.get('target_column')
    
    if not protected_attr or not target_col:
        print("  Impossible de créer les visualisations (colonnes manquantes)")
        return
    
    # Créer une figure avec 3 sous-graphiques
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    fig.suptitle(f'Comparaison : {bias_config["description"]}', 
                 fontsize=16, fontweight='bold')
    
    # 1. Distributions comparées
    ax1 = axes[0]
    groups = df_original[protected_attr].unique()
    
    x = range(len(groups))
    width = 0.35
    
    means_original = [df_original[df_original[protected_attr] == g][target_col].mean() 
                     for g in groups]
    means_biased = [df_biased[df_biased[protected_attr] == g][target_col].mean() 
                   for g in groups]
    
    ax1.bar([i - width/2 for i in x], means_original, width, label='Original', alpha=0.8)
    ax1.bar([i + width/2 for i in x], means_biased, width, label='Biaisé', alpha=0.8)
    
    ax1.set_xlabel(protected_attr.upper(), fontweight='bold')
    ax1.set_ylabel(f'{target_col.upper()} (moyenne)', fontweight='bold')
    ax1.set_title('Moyennes par groupe')
    ax1.set_xticks(x)
    ax1.set_xticklabels(groups)
    ax1.legend()
    ax1.grid(axis='y', alpha=0.3)
    
    # 2. Box plots comparés
    ax2 = axes[1]
    
    df_original['dataset'] = 'Original'
    df_biased['dataset'] = 'Biaisé'
    df_combined = pd.concat([df_original, df_biased])
    
    sns.boxplot(data=df_combined, x=protected_attr, y=target_col, 
               hue='dataset', ax=ax2, palette=['skyblue', 'salmon'])
    ax2.set_title('Distribution détaillée')
    ax2.set_xlabel(protected_attr.upper(), fontweight='bold')
    ax2.set_ylabel(f'{target_col.upper()}', fontweight='bold')
    ax2.legend(title='Dataset')
    
    # 3. Écart absolu
    ax3 = axes[2]
    
    differences = [means_biased[i] - means_original[i] for i in range(len(groups))]
    colors = ['green' if d > 0 else 'red' for d in differences]
    
    ax3.barh(groups, differences, color=colors, alpha=0.7)
    ax3.axvline(x=0, color='black', linestyle='--', linewidth=1)
    ax3.set_xlabel(f'Différence ({target_col})', fontweight='bold')
    ax3.set_ylabel(protected_attr.upper(), fontweight='bold')
    ax3.set_title('Écart causé par le biais')
    ax3.grid(axis='x', alpha=0.3)
    
    # Sauvegarder
    plt.tight_layout()
    viz_path = os.path.join(output_dir, 'bias_comparison.png')
    plt.savefig(viz_path, dpi=300, bbox_inches='tight')
    print(f"📊 Visualisation sauvegardée : {viz_path}")
    
    plt.close()
    
    # Nettoyer les colonnes temporaires
    df_original.drop('dataset', axis=1, inplace=True)
    df_biased.drop('dataset', axis=1, inplace=True)

def create_statistics_report(df_original, df_biased, bias_config, output_dir):
    """
    Crée un rapport statistique détaillé
    """
    
    protected_attr = bias_config.get('protected_attribute')
    target_col = bias_config.get('target_column')
    
    if not protected_attr or not target_col:
        return
    
    print("\n" + "="*80)
    print("📈 RAPPORT STATISTIQUE")
    print("="*80 + "\n")
    
    # Statistiques par groupe
    print(f"📊 {target_col.upper()} par {protected_attr.upper()}")
    print("-" * 80)
    
    stats_original = df_original.groupby(protected_attr)[target_col].describe()
    stats_biased = df_biased.groupby(protected_attr)[target_col].describe()
    
    print("\nORIGINAL :")
    print(stats_original[['mean', 'std', 'min', 'max']].round(2))
    
    print("\nBIAISÉ :")
    print(stats_biased[['mean', 'std', 'min', 'max']].round(2))
    
    # Calcul des métriques de fairness
    print("\n" + "-" * 80)
    print("🎯 MÉTRIQUES DE FAIRNESS")
    print("-" * 80)
    
    groups = df_original[protected_attr].unique()
    if len(groups) == 2:
        # Disparate Impact (pour 2 groupes)
        mean_g1_orig = df_original[df_original[protected_attr] == groups[0]][target_col].mean()
        mean_g2_orig = df_original[df_original[protected_attr] == groups[1]][target_col].mean()
        
        mean_g1_bias = df_biased[df_biased[protected_attr] == groups[0]][target_col].mean()
        mean_g2_bias = df_biased[df_biased[protected_attr] == groups[1]][target_col].mean()
        
        di_original = min(mean_g1_orig, mean_g2_orig) / max(mean_g1_orig, mean_g2_orig)
        di_biased = min(mean_g1_bias, mean_g2_bias) / max(mean_g1_bias, mean_g2_bias)
        
        print(f"\nDisparate Impact :")
        print(f"  Original : {di_original:.3f}")
        print(f"  Biaisé   : {di_biased:.3f}")
        print(f"  Change   : {abs(di_biased - di_original):.3f}")
        
        if di_biased < 0.8:
            print(f"  ⚠️  ALERTE : DI < 0.8 (règle des 80%)")
    
    # Statistical Parity Difference
    mean_overall_orig = df_original[target_col].mean()
    mean_overall_bias = df_biased[target_col].mean()
    
    print(f"\nMoyenne globale :")
    print(f"  Original : {mean_overall_orig:.2f}")
    print(f"  Biaisé   : {mean_overall_bias:.2f}")
    print(f"  Change   : {abs(mean_overall_bias - mean_overall_orig):.2f}")
    
    print()

def generate_single_with_visualization(
    model_path,
    output_dir,
    n_samples=10000,
    bias_type="gender",
    intensity=1.0,
    target_column=None
):
    """
    Génère 1 dataset biaisé avec visualisations
    """
    
    print("\n" + "="*80)
    print("🎯 GÉNÉRATEUR SIMPLE AVEC VISUALISATION")
    print("="*80 + "\n")
    
    # Créer dossier de sortie
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. CHARGER LE MODÈLE
    print(f"📥 Chargement du modèle : {model_path}")
    try:
        # Fix PyTorch 2.6 weights_only issue - Ajouter TOUTES les classes CTGAN
        import torch
        import torch.serialization
        from ctgan.synthesizers.ctgan import CTGAN as CTGANClass
        from ctgan.data_transformer import DataTransformer
        from ctgan.data_sampler import DataSampler
        
        # Autoriser toutes les classes CTGAN nécessaires
        torch.serialization.add_safe_globals([
            CTGANClass,
            DataTransformer,
            DataSampler
        ])
        
        model = CTGAN.load(model_path)
        print("✅ Modèle chargé\n")
    except Exception as e:
        print(f"❌ Erreur de chargement : {e}")
        print("\n💡 Solution alternative : Charger avec weights_only=False")
        
        # Tentative alternative avec weights_only=False
        try:
            import torch
            # Monkey patch temporaire
            original_load = torch.load
            torch.load = lambda *args, **kwargs: original_load(*args, **{**kwargs, 'weights_only': False})
            
            model = CTGAN.load(model_path)
            torch.load = original_load  # Restaurer
            
            print("✅ Modèle chargé (mode compatibilité)\n")
        except Exception as e2:
            print(f"❌ Échec définitif : {e2}")
            return
    
    # 2. GÉNÉRER DONNÉES ORIGINALES
    print(f"🔄 Génération de {n_samples:,} échantillons...")
    df_original = model.sample(n_samples)
    print(f"✅ Généré : {len(df_original):,} lignes\n")
    
    print("👀 Aperçu :")
    print(df_original.head(3))
    print()
    
    # 3. INJECTER LE BIAIS
    print(f"💉 Injection du biais : {bias_type.upper()}")
    print(f"   Intensité : {intensity}\n")
    
    injector = UniversalBiasInjector()
    
    # Détecter les biais applicables
    applicable = injector.detect_applicable_biases(df_original)
    
    if bias_type not in applicable:
        print(f"❌ Biais '{bias_type}' non applicable")
        print(f"   Biais disponibles : {list(applicable.keys())}")
        return
    
    try:
        df_biased, config = injector.inject_bias(
            df_original.copy(),
            bias_type=bias_type,
            target_column=target_column,
            intensity=intensity
        )
        
        print(f"✅ {config['description']}")
        print(f"   Attribut protégé : {config['protected_attribute']}")
        print(f"   Colonne cible    : {config['target_column']}")
        print(f"   Facteur          : {config.get('factor', 'N/A')}\n")
        
    except Exception as e:
        print(f"❌ Erreur lors de l'injection : {e}")
        return
    
    # 4. SAUVEGARDER LES DONNÉES
    print("💾 Sauvegarde des fichiers...")
    
    # Original
    original_path = os.path.join(output_dir, f"original_{n_samples}.csv")
    df_original.to_csv(original_path, index=False)
    print(f"   • {original_path}")
    
    # Biaisé
    biased_path = os.path.join(output_dir, f"biased_{bias_type}_{n_samples}.csv")
    df_biased.to_csv(biased_path, index=False)
    print(f"   • {biased_path}")
    
    # Rapport JSON
    report_path = os.path.join(output_dir, "bias_report.json")
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False, default=str)
    print(f"   • {report_path}\n")
    
    # 5. CRÉER LES VISUALISATIONS
    print("📊 Création des visualisations...")
    create_comparison_visualizations(df_original, df_biased, config, output_dir)
    
    # 6. RAPPORT STATISTIQUE
    create_statistics_report(df_original, df_biased, config, output_dir)
    
    # 7. RÉSUMÉ
    print("="*80)
    print("✨ GÉNÉRATION TERMINÉE")
    print("="*80)
    print(f"\n📁 Fichiers créés dans : {output_dir}/")
    print(f"   • original_{n_samples}.csv")
    print(f"   • biased_{bias_type}_{n_samples}.csv")
    print(f"   • bias_report.json")
    print(f"   • bias_comparison.png")
    print()

def main():
    parser = argparse.ArgumentParser(
        description="🎯 Générateur simple avec visualisation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
📖 EXEMPLES :

  1️⃣  Biais de genre (par défaut) :
     python generate_single_with_visual.py -m models/Personnes_infos_seed_ctgan.pkl -o outputs/test/

  2️⃣  Biais de nationalité fort :
     python generate_single_with_visual.py -m models/Personnes_infos_seed_ctgan.pkl -o outputs/nationality/ -t nationality -i 1.5

  3️⃣  100k échantillons avec biais d'âge :
     python generate_single_with_visual.py -m models/Personnes_infos_seed_ctgan.pkl -o outputs/age/ -t age -n 100000
     
📊 RÉSULTAT :
   - 2 fichiers CSV (original + biaisé)
   - 1 rapport JSON détaillé
   - 1 image PNG avec 3 graphiques comparatifs
        """
    )
    
    parser.add_argument("--model", "-m", required=True, 
                       help="Chemin vers le modèle CTGAN")
    parser.add_argument("--output", "-o", required=True, 
                       help="Dossier de sortie")
    parser.add_argument("--samples", "-n", type=int, default=10000, 
                       help="Nombre d'échantillons (défaut: 10000)")
    parser.add_argument("--type", "-t", default="gender",
                       choices=["gender", "age", "nationality", "location"],
                       help="Type de biais (défaut: gender)")
    parser.add_argument("--intensity", "-i", type=float, default=1.0,
                       help="Intensité (0.5=faible, 1.0=normal, 2.0=fort)")
    parser.add_argument("--target", default=None,
                       help="Colonne cible (auto si non spécifié)")
    
    args = parser.parse_args()
    
    generate_single_with_visualization(
        model_path=args.model,
        output_dir=args.output,
        n_samples=args.samples,
        bias_type=args.type,
        intensity=args.intensity,
        target_column=args.target
    )

if __name__ == "__main__":
    main()