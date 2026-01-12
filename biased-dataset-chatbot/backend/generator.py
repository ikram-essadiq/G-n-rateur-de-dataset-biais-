"""
🎯 ORCHESTRATEUR PRINCIPAL - VERSION AMÉLIORÉE
Génère les graphiques détaillés pour chaque type de biais
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import os
import json
from typing import Dict, Optional, List
from scipy import stats
import math

from bias_engine import BiasEngine
from model_manager import ModelManager


def clean_nan_from_dict(d):
    """Remplace tous les NaN par None (sérialisable en JSON)"""
    if isinstance(d, dict):
        return {k: clean_nan_from_dict(v) for k, v in d.items()}
    elif isinstance(d, list):
        return [clean_nan_from_dict(v) for v in d]
    elif isinstance(d, float) and math.isnan(d):
        return None
    else:
        return d


class BiasAnalyzer:
    """Analyse et visualise les biais avec graphiques détaillés"""
    
    def analyze_bias(self, original_df: pd.DataFrame, 
                    biased_df: pd.DataFrame,
                    bias_report: dict) -> dict:
        """Compare dataset original vs biaisé"""
        analysis = {
            "size_comparison": {
                "original": len(original_df),
                "biased": len(biased_df),
                "change_pct": ((len(biased_df) - len(original_df)) / len(original_df)) * 100 if len(original_df) > 0 else 0
            },
            "distribution_changes": {},
            "statistical_tests": {}
        }
        
        # Comparer distributions numériques
        numeric_cols = original_df.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            if col in biased_df.columns:
                try:
                    # Test KS
                    ks_stat, ks_pval = stats.ks_2samp(
                        original_df[col].dropna(), 
                        biased_df[col].dropna()
                    )
                    
                    orig_mean = float(original_df[col].mean()) if not pd.isna(original_df[col].mean()) else 0.0
                    bias_mean = float(biased_df[col].mean()) if not pd.isna(biased_df[col].mean()) else 0.0
                    orig_std = float(original_df[col].std()) if not pd.isna(original_df[col].std()) else 0.0
                    bias_std = float(biased_df[col].std()) if not pd.isna(biased_df[col].std()) else 0.0
                    
                    analysis["distribution_changes"][col] = {
                        "original_mean": orig_mean,
                        "biased_mean": bias_mean,
                        "original_std": orig_std,
                        "biased_std": bias_std,
                        "mean_change_pct": float(
                            ((bias_mean - orig_mean) / (orig_mean + 1e-10)) * 100
                        ) if orig_mean != 0 else 0.0,
                        "ks_statistic": float(ks_stat),
                        "ks_pvalue": float(ks_pval)
                    }
                except Exception as e:
                    print(f"⚠️ Erreur analyse colonne {col}: {e}")
        
        return analysis
    
    def visualize_bias(self, original_df: pd.DataFrame,
                      biased_df: pd.DataFrame,
                      bias_type: str,
                      bias_report: dict,
                      output_file: str = "bias_visualization.png") -> str:
        """
        Génère des visualisations ADAPTÉES au type de biais
        """
        
        try:
            # Configuration style
            plt.style.use('seaborn-v0_8-darkgrid')
            sns.set_palette("husl")
            
            if bias_type == 'gender':
                return self._visualize_gender_bias(original_df, biased_df, bias_report, output_file)
            elif bias_type == 'age':
                return self._visualize_age_bias(original_df, biased_df, bias_report, output_file)
            elif bias_type == 'geographic':
                return self._visualize_geographic_bias(original_df, biased_df, bias_report, output_file)
            elif bias_type == 'socioeconomic':
                return self._visualize_socioeconomic_bias(original_df, biased_df, bias_report, output_file)
            elif bias_type == 'temporal':
                return self._visualize_temporal_bias(original_df, biased_df, bias_report, output_file)
            else:
                return self._visualize_generic_bias(original_df, biased_df, bias_type, output_file)
                
        except Exception as e:
            print(f"⚠️ Erreur visualisation: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def _visualize_gender_bias(self, orig_df, bias_df, report, output_file):
        """Graphiques spécifiques au biais de genre"""
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('📊 Analyse du Biais de Genre', fontsize=20, fontweight='bold', y=0.98)
        
        details = report.get('details', {})
        gender_col = details.get('gender_column')
        target_col = details.get('target_column')
        
        # 1. Distribution des genres
        ax = axes[0, 0]
        if gender_col and gender_col in orig_df.columns:
            orig_counts = orig_df[gender_col].value_counts()
            bias_counts = bias_df[gender_col].value_counts()
            
            x = np.arange(len(orig_counts))
            width = 0.35
            ax.bar(x - width/2, orig_counts.values, width, label='Original', color='#3498db', alpha=0.8)
            ax.bar(x + width/2, bias_counts.values, width, label='Biaisé', color='#e74c3c', alpha=0.8)
            ax.set_xlabel('Genre', fontsize=12, fontweight='bold')
            ax.set_ylabel('Nombre', fontsize=12, fontweight='bold')
            ax.set_title('Répartition des Genres', fontsize=14, fontweight='bold')
            ax.set_xticks(x)
            ax.set_xticklabels(orig_counts.index, rotation=45)
            ax.legend()
            ax.grid(axis='y', alpha=0.3)
        
        # 2. Comparaison des moyennes par genre
        ax = axes[0, 1]
        if target_col and target_col in orig_df.columns and gender_col:
            orig_means = orig_df.groupby(gender_col)[target_col].mean()
            bias_means = bias_df.groupby(gender_col)[target_col].mean()
            
            x = np.arange(len(orig_means))
            width = 0.35
            ax.bar(x - width/2, orig_means.values, width, label='Original', color='#3498db', alpha=0.8)
            ax.bar(x + width/2, bias_means.values, width, label='Biaisé', color='#e74c3c', alpha=0.8)
            ax.set_xlabel('Genre', fontsize=12, fontweight='bold')
            ax.set_ylabel(f'Moyenne {target_col}', fontsize=12, fontweight='bold')
            ax.set_title(f'Impact du Biais sur {target_col}', fontsize=14, fontweight='bold')
            ax.set_xticks(x)
            ax.set_xticklabels(orig_means.index, rotation=45)
            ax.legend()
            ax.grid(axis='y', alpha=0.3)
        
        # 3. Boxplot comparatif
        ax = axes[1, 0]
        if target_col and gender_col:
            data_to_plot = []
            labels = []
            for gender in orig_df[gender_col].unique():
                data_to_plot.append(orig_df[orig_df[gender_col] == gender][target_col].dropna())
                labels.append(f'{gender} (Orig)')
                data_to_plot.append(bias_df[bias_df[gender_col] == gender][target_col].dropna())
                labels.append(f'{gender} (Biais)')
            
            bp = ax.boxplot(data_to_plot, labels=labels, patch_artist=True)
            for i, box in enumerate(bp['boxes']):
                box.set_facecolor('#3498db' if i % 2 == 0 else '#e74c3c')
            ax.set_ylabel(target_col, fontsize=12, fontweight='bold')
            ax.set_title('Distribution par Genre', fontsize=14, fontweight='bold')
            ax.tick_params(axis='x', rotation=45)
            ax.grid(axis='y', alpha=0.3)
        
        # 4. Écart en %
        ax = axes[1, 1]
        if 'gap_percentage' in details:
            gap = details['gap_percentage']
            favored = details.get('favored_gender', 'Genre favorisé')
            
            ax.barh(['Écart de Genre'], [gap], color='#e74c3c' if gap > 0 else '#3498db', height=0.5)
            ax.set_xlabel('Écart en %', fontsize=12, fontweight='bold')
            ax.set_title(f'Écart Salarial - Genre favorisé: {favored}', fontsize=14, fontweight='bold')
            ax.axvline(0, color='black', linestyle='--', alpha=0.5)
            ax.grid(axis='x', alpha=0.3)
            ax.text(gap, 0, f'{gap:.1f}%', ha='left' if gap > 0 else 'right', va='center', fontweight='bold')
        
        plt.tight_layout()
        os.makedirs(os.path.dirname(output_file) if os.path.dirname(output_file) else '.', exist_ok=True)
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.close(fig)
        
        return output_file
    
    def _visualize_age_bias(self, orig_df, bias_df, report, output_file):
        """Graphiques pour biais d'âge"""
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('📊 Analyse du Biais d\'Âge', fontsize=20, fontweight='bold', y=0.98)
        
        details = report.get('details', {})
        age_col = details.get('age_column')
        
        # 1. Distribution des âges
        ax = axes[0, 0]
        if age_col and age_col in orig_df.columns:
            ax.hist(orig_df[age_col].dropna(), bins=30, alpha=0.6, label='Original', color='#3498db', edgecolor='black')
            ax.hist(bias_df[age_col].dropna(), bins=30, alpha=0.6, label='Biaisé', color='#e74c3c', edgecolor='black')
            ax.set_xlabel('Âge', fontsize=12, fontweight='bold')
            ax.set_ylabel('Fréquence', fontsize=12, fontweight='bold')
            ax.set_title('Distribution des Âges', fontsize=14, fontweight='bold')
            ax.legend()
            ax.grid(axis='y', alpha=0.3)
        
        # 2. Pyramide des âges
        ax = axes[0, 1]
        if age_col:
            age_ranges = [(0, 30), (30, 50), (50, 100)]
            orig_counts = [((orig_df[age_col] >= r[0]) & (orig_df[age_col] < r[1])).sum() for r in age_ranges]
            bias_counts = [((bias_df[age_col] >= r[0]) & (bias_df[age_col] < r[1])).sum() for r in age_ranges]
            
            x = np.arange(len(age_ranges))
            width = 0.35
            ax.barh(x - width/2, orig_counts, width, label='Original', color='#3498db', alpha=0.8)
            ax.barh(x + width/2, bias_counts, width, label='Biaisé', color='#e74c3c', alpha=0.8)
            ax.set_yticks(x)
            ax.set_yticklabels([f'{r[0]}-{r[1]}' for r in age_ranges])
            ax.set_xlabel('Nombre', fontsize=12, fontweight='bold')
            ax.set_title('Tranches d\'Âge', fontsize=14, fontweight='bold')
            ax.legend()
            ax.grid(axis='x', alpha=0.3)
        
        # 3. Boxplot
        ax = axes[1, 0]
        if age_col:
            bp = ax.boxplot([orig_df[age_col].dropna(), bias_df[age_col].dropna()], 
                           labels=['Original', 'Biaisé'], patch_artist=True)
            bp['boxes'][0].set_facecolor('#3498db')
            bp['boxes'][1].set_facecolor('#e74c3c')
            ax.set_ylabel('Âge', fontsize=12, fontweight='bold')
            ax.set_title('Distribution Comparative', fontsize=14, fontweight='bold')
            ax.grid(axis='y', alpha=0.3)
        
        # 4. Statistiques
        ax = axes[1, 1]
        if 'removed_count' in details:
            removed = details['removed_count']
            excluded_range = details.get('excluded_range', (0, 100))
            
            stats_text = f"""
            Tranche exclue: {excluded_range[0]}-{excluded_range[1]} ans
            
            Lignes supprimées: {removed}
            
            Taille originale: {len(orig_df)}
            Taille finale: {len(bias_df)}
            
            Réduction: {(removed/len(orig_df)*100):.1f}%
            """
            ax.text(0.1, 0.5, stats_text, fontsize=14, verticalalignment='center', 
                   bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
            ax.axis('off')
        
        plt.tight_layout()
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.close(fig)
        
        return output_file
    
    def _visualize_geographic_bias(self, orig_df, bias_df, report, output_file):
        """Graphiques pour biais géographique"""
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('📊 Analyse du Biais Géographique', fontsize=20, fontweight='bold', y=0.98)
        
        details = report.get('details', {})
        region_col = details.get('region_column')
        
        # 1. Top régions - Original
        ax = axes[0, 0]
        if region_col and region_col in orig_df.columns:
            top_orig = orig_df[region_col].value_counts().head(10)
            ax.barh(range(len(top_orig)), top_orig.values, color='#3498db', alpha=0.8)
            ax.set_yticks(range(len(top_orig)))
            ax.set_yticklabels(top_orig.index)
            ax.set_xlabel('Nombre', fontsize=12, fontweight='bold')
            ax.set_title('Top 10 Régions (Original)', fontsize=14, fontweight='bold')
            ax.grid(axis='x', alpha=0.3)
        
        # 2. Top régions - Biaisé
        ax = axes[0, 1]
        if region_col:
            top_bias = bias_df[region_col].value_counts().head(10)
            ax.barh(range(len(top_bias)), top_bias.values, color='#e74c3c', alpha=0.8)
            ax.set_yticks(range(len(top_bias)))
            ax.set_yticklabels(top_bias.index)
            ax.set_xlabel('Nombre', fontsize=12, fontweight='bold')
            ax.set_title('Top 10 Régions (Biaisé)', fontsize=14, fontweight='bold')
            ax.grid(axis='x', alpha=0.3)
        
        # 3. Comparaison directe
        ax = axes[1, 0]
        if region_col:
            all_regions = set(orig_df[region_col].unique()) | set(bias_df[region_col].unique())
            regions_to_plot = list(all_regions)[:10]
            
            orig_counts = [orig_df[orig_df[region_col] == r].shape[0] for r in regions_to_plot]
            bias_counts = [bias_df[bias_df[region_col] == r].shape[0] for r in regions_to_plot]
            
            x = np.arange(len(regions_to_plot))
            width = 0.35
            ax.bar(x - width/2, orig_counts, width, label='Original', color='#3498db', alpha=0.8)
            ax.bar(x + width/2, bias_counts, width, label='Biaisé', color='#e74c3c', alpha=0.8)
            ax.set_xticks(x)
            ax.set_xticklabels(regions_to_plot, rotation=45, ha='right')
            ax.set_ylabel('Nombre', fontsize=12, fontweight='bold')
            ax.set_title('Comparaison par Région', fontsize=14, fontweight='bold')
            ax.legend()
            ax.grid(axis='y', alpha=0.3)
        
        # 4. Statistiques
        ax = axes[1, 1]
        if 'overrepresented' in details:
            overrep = details['overrepresented']
            duplicated = details.get('duplicated_count', 0)
            
            stats_text = f"""
            Région surreprésentée:
            {overrep}
            
            Lignes dupliquées: {duplicated}
            
            Taille originale: {len(orig_df)}
            Taille finale: {len(bias_df)}
            
            Augmentation: {((len(bias_df)-len(orig_df))/len(orig_df)*100):.1f}%
            """
            ax.text(0.1, 0.5, stats_text, fontsize=14, verticalalignment='center',
                   bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.5))
            ax.axis('off')
        
        plt.tight_layout()
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.close(fig)
        
        return output_file
    
    def _visualize_socioeconomic_bias(self, orig_df, bias_df, report, output_file):
        """Graphiques pour biais socio-économique"""
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('📊 Analyse du Biais Socio-économique', fontsize=20, fontweight='bold', y=0.98)
        
        details = report.get('details', {})
        income_col = details.get('income_column')
        
        # 1. Distribution des revenus/prix
        ax = axes[0, 0]
        if income_col and income_col in orig_df.columns:
            ax.hist(orig_df[income_col].dropna(), bins=50, alpha=0.6, label='Original', color='#3498db')
            ax.hist(bias_df[income_col].dropna(), bins=50, alpha=0.6, label='Biaisé', color='#e74c3c')
            
            if 'threshold' in details:
                ax.axvline(details['threshold'], color='red', linestyle='--', linewidth=2, label='Seuil')
            
            ax.set_xlabel(income_col, fontsize=12, fontweight='bold')
            ax.set_ylabel('Fréquence', fontsize=12, fontweight='bold')
            ax.set_title('Distribution des Valeurs', fontsize=14, fontweight='bold')
            ax.legend()
            ax.grid(axis='y', alpha=0.3)
        
        # 2. Boxplot
        ax = axes[0, 1]
        if income_col:
            bp = ax.boxplot([orig_df[income_col].dropna(), bias_df[income_col].dropna()],
                           labels=['Original', 'Biaisé'], patch_artist=True)
            bp['boxes'][0].set_facecolor('#3498db')
            bp['boxes'][1].set_facecolor('#e74c3c')
            
            if 'threshold' in details:
                ax.axhline(details['threshold'], color='red', linestyle='--', linewidth=2, label='Seuil')
            
            ax.set_ylabel(income_col, fontsize=12, fontweight='bold')
            ax.set_title('Distribution Comparative', fontsize=14, fontweight='bold')
            ax.legend()
            ax.grid(axis='y', alpha=0.3)
        
        # 3. Tranches de valeurs
        ax = axes[1, 0]
        if income_col:
            orig_q = orig_df[income_col].quantile([0, 0.25, 0.5, 0.75, 1.0])
            ranges = [(orig_q.iloc[i], orig_q.iloc[i+1]) for i in range(4)]
            
            orig_counts = [((orig_df[income_col] >= r[0]) & (orig_df[income_col] < r[1])).sum() for r in ranges]
            bias_counts = [((bias_df[income_col] >= r[0]) & (bias_df[income_col] < r[1])).sum() for r in ranges]
            
            x = np.arange(len(ranges))
            width = 0.35
            ax.bar(x - width/2, orig_counts, width, label='Original', color='#3498db', alpha=0.8)
            ax.bar(x + width/2, bias_counts, width, label='Biaisé', color='#e74c3c', alpha=0.8)
            ax.set_xticks(x)
            ax.set_xticklabels(['Q1', 'Q2', 'Q3', 'Q4'])
            ax.set_ylabel('Nombre', fontsize=12, fontweight='bold')
            ax.set_title('Répartition par Quartile', fontsize=14, fontweight='bold')
            ax.legend()
            ax.grid(axis='y', alpha=0.3)
        
        # 4. Statistiques
        ax = axes[1, 1]
        if 'removed_count' in details:
            removed = details['removed_count']
            threshold = details.get('threshold', 0)
            
            stats_text = f"""
            Seuil appliqué: {threshold:.2f}
            
            Lignes supprimées: {removed}
            Lignes conservées: {details.get('remaining_count', len(bias_df))}
            
            Taille originale: {len(orig_df)}
            Taille finale: {len(bias_df)}
            
            Réduction: {(removed/len(orig_df)*100):.1f}%
            """
            ax.text(0.1, 0.5, stats_text, fontsize=14, verticalalignment='center',
                   bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.5))
            ax.axis('off')
        
        plt.tight_layout()
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.close(fig)
        
        return output_file
    
    def _visualize_temporal_bias(self, orig_df, bias_df, report, output_file):
        """Graphiques pour biais temporel"""
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('📊 Analyse du Biais Temporel', fontsize=20, fontweight='bold', y=0.98)
        
        details = report.get('details', {})
        date_col = details.get('date_column')
        
        # 1. Timeline
        ax = axes[0, 0]
        if date_col and date_col in orig_df.columns:
            try:
                orig_dates = pd.to_datetime(orig_df[date_col], errors='coerce').dropna()
                bias_dates = pd.to_datetime(bias_df[date_col], errors='coerce').dropna()
                
                ax.hist(orig_dates, bins=50, alpha=0.6, label='Original', color='#3498db')
                ax.hist(bias_dates, bins=50, alpha=0.6, label='Biaisé', color='#e74c3c')
                ax.set_xlabel('Date', fontsize=12, fontweight='bold')
                ax.set_ylabel('Fréquence', fontsize=12, fontweight='bold')
                ax.set_title('Distribution Temporelle', fontsize=14, fontweight='bold')
                ax.legend()
                ax.grid(axis='y', alpha=0.3)
            except:
                pass
        
        # 2. Cumulative
        ax = axes[0, 1]
        if date_col:
            try:
                orig_dates_sorted = orig_dates.sort_values()
                bias_dates_sorted = bias_dates.sort_values()
                
                ax.plot(orig_dates_sorted.values, np.arange(len(orig_dates_sorted)), 
                       label='Original', color='#3498db', linewidth=2)
                ax.plot(bias_dates_sorted.values, np.arange(len(bias_dates_sorted)), 
                       label='Biaisé', color='#e74c3c', linewidth=2)
                ax.set_xlabel('Date', fontsize=12, fontweight='bold')
                ax.set_ylabel('Nombre Cumulé', fontsize=12, fontweight='bold')
                ax.set_title('Distribution Cumulative', fontsize=14, fontweight='bold')
                ax.legend()
                ax.grid(alpha=0.3)
            except:
                pass
        
        # 3. Par période
        ax = axes[1, 0]
        if 'recent_count' in details and 'old_count' in details:
            recent = details['recent_count']
            old = details['old_count']
            
            x = ['Anciennes', 'Récentes']
            orig_vals = [len(orig_df) - recent, recent]  # Approximation
            bias_vals = [old, recent]
            
            x_pos = np.arange(len(x))
            width = 0.35
            ax.bar(x_pos - width/2, orig_vals, width, label='Original', color='#3498db', alpha=0.8)
            ax.bar(x_pos + width/2, bias_vals, width, label='Biaisé', color='#e74c3c', alpha=0.8)
            ax.set_xticks(x_pos)
            ax.set_xticklabels(x)
            ax.set_ylabel('Nombre', fontsize=12, fontweight='bold')
            ax.set_title('Répartition Temporelle', fontsize=14, fontweight='bold')
            ax.legend()
            ax.grid(axis='y', alpha=0.3)
        
        # 4. Statistiques
        ax = axes[1, 1]
        if 'recent_count' in details:
            recent = details['recent_count']
            old = details['old_count']
            
            stats_text = f"""
            Données récentes: {recent}
            Données anciennes: {old}
            
            Taille originale: {len(orig_df)}
            Taille finale: {len(bias_df)}
            
            % récentes: {(recent/len(bias_df)*100):.1f}%
            """
            ax.text(0.1, 0.5, stats_text, fontsize=14, verticalalignment='center',
                   bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.5))
            ax.axis('off')
        
        plt.tight_layout()
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.close(fig)
        
        return output_file
    
    def _visualize_generic_bias(self, orig_df, bias_df, bias_type, output_file):
        """Graphiques génériques pour autres biais"""
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle(f'Analyse de Biais : {bias_type.upper()}', 
                    fontsize=16, fontweight='bold')
        
        # 1. Comparaison des tailles
        ax = axes[0, 0]
        sizes = [len(orig_df), len(bias_df)]
        colors = ['#3498db', '#e74c3c']
        ax.bar(['Original', 'Biaisé'], sizes, color=colors)
        ax.set_ylabel('Nombre de lignes', fontsize=12)
        ax.set_title('Taille du Dataset', fontsize=14, fontweight='bold')
        for i, v in enumerate(sizes):
            ax.text(i, v + max(sizes)*0.02, str(v), ha='center', fontweight='bold')
        ax.grid(axis='y', alpha=0.3)
        
        # 2. Distribution d'une variable clé
        ax = axes[0, 1]
        numeric_cols = orig_df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            col = numeric_cols[0]
            ax.hist(orig_df[col].dropna(), bins=30, alpha=0.6, 
                   label='Original', color='#3498db', edgecolor='black')
            ax.hist(bias_df[col].dropna(), bins=30, alpha=0.6, 
                   label='Biaisé', color='#e74c3c', edgecolor='black')
            ax.set_xlabel(col, fontsize=12)
            ax.set_ylabel('Fréquence', fontsize=12)
            ax.set_title(f'Distribution: {col}', fontsize=14, fontweight='bold')
            ax.legend(fontsize=10)
            ax.grid(axis='y', alpha=0.3)
        
        # 3. Comparaison des moyennes
        ax = axes[1, 0]
        if len(numeric_cols) > 0:
            cols_to_show = numeric_cols[:5]
            means_orig = [orig_df[col].mean() for col in cols_to_show]
            means_bias = [bias_df[col].mean() for col in cols_to_show]
            x = np.arange(len(cols_to_show))
            width = 0.35
            ax.bar(x - width/2, means_orig, width, label='Original', 
                  color='#3498db', edgecolor='black')
            ax.bar(x + width/2, means_bias, width, label='Biaisé', 
                  color='#e74c3c', edgecolor='black')
            ax.set_xticks(x)
            ax.set_xticklabels(cols_to_show, rotation=45, ha='right', fontsize=10)
            ax.set_ylabel('Moyenne', fontsize=12)
            ax.set_title('Comparaison des Moyennes', fontsize=14, fontweight='bold')
            ax.legend(fontsize=10)
            ax.grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        os.makedirs(os.path.dirname(output_file) if os.path.dirname(output_file) else '.', exist_ok=True)
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.close(fig)
        
        return output_file


class BiasedDatasetGenerator:
    """Orchestrateur principal avec graphiques améliorés"""
    
    def __init__(self, models_dir: str = "models", output_dir: str = "output"):
        self.model_manager = ModelManager(models_dir)
        self.bias_engine = BiasEngine()
        self.bias_analyzer = BiasAnalyzer()
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def get_available_categories(self) -> List[str]:
        return self.model_manager.list_categories()
    
    def get_available_biases_for_category(self, category: str, n_samples: int = 100) -> List[Dict]:
        try:
            model = self.model_manager.load_model(category)
            sample_df = model.sample(n_samples)
            biases = self.bias_engine.get_available_biases(sample_df)
            return biases
        except Exception as e:
            print(f"⚠️ Erreur détection biais: {e}")
            return []
    
    def generate(self, 
                category: str,
                n_samples: int = 1000,
                bias_type: Optional[str] = None,
                bias_intensity: float = 0.5,
                bias_params: Optional[dict] = None) -> Dict:
        """
        Génère un dataset biaisé complet SANS NaN
        """
        print(f"\n{'='*80}")
        print(f"🎯 GÉNÉRATION DE DATASET BIAISÉ")
        print(f"{'='*80}\n")
        print(f"📁 Catégorie     : {category}")
        print(f"📊 Échantillons  : {n_samples}")
        print(f"⚠️  Biais         : {bias_type or 'AUCUN'}")
        print(f"💪 Intensité     : {bias_intensity}\n")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        try:
            # 1. Charger le modèle
            model = self.model_manager.load_model(category)
            
            # 2. Générer données NEUTRES
            print(f"🎲 Génération de {n_samples} échantillons neutres...")
            original_dataset = model.sample(n_samples)
            
            # ✅ NETTOYAGE CRITIQUE DES NaN
            print(f"🧹 Nettoyage des données...")
            nan_counts = original_dataset.isna().sum()
            if nan_counts.sum() > 0:
                print(f"⚠️  NaN détectés avant nettoyage:")
                for col, count in nan_counts[nan_counts > 0].items():
                    print(f"   - {col}: {count} NaN ({count/len(original_dataset)*100:.1f}%)")
            
            # Remplacer les NaN
            for col in original_dataset.columns:
                if original_dataset[col].isna().sum() > 0:
                    if pd.api.types.is_numeric_dtype(original_dataset[col]):
                        median_val = original_dataset[col].median()
                        if pd.isna(median_val):
                            original_dataset[col].fillna(0, inplace=True)
                        else:
                            original_dataset[col].fillna(median_val, inplace=True)
                        print(f"   ✅ {col}: NaN remplacés par {median_val if not pd.isna(median_val) else 0}")
                    else:
                        mode_val = original_dataset[col].mode()
                        if len(mode_val) > 0:
                            original_dataset[col].fillna(mode_val[0], inplace=True)
                            print(f"   ✅ {col}: NaN remplacés par '{mode_val[0]}'")
                        else:
                            original_dataset[col].fillna("Unknown", inplace=True)
                            print(f"   ✅ {col}: NaN remplacés par 'Unknown'")
            
            print(f"✅ {len(original_dataset)} échantillons générés et nettoyés!\n")
            print(f"📊 Aperçu des données:\n{original_dataset.head(3)}\n")
            
            # 3. Appliquer le biais
            if bias_type:
                print(f"⚠️  Application du biais '{bias_type}'...")
                params = bias_params or {}
                biased_dataset, bias_report = self.bias_engine.apply_bias(
                    original_dataset,
                    bias_type,
                    bias_intensity,
                    **params
                )
                
                if "error" in bias_report:
                    print(f"❌ Erreur: {bias_report['error']}")
                    return {
                        "success": False,
                        "error": bias_report['error']
                    }
                
                print(f"✅ Biais appliqué!\n")
                
                # 4. Analyser le biais
                print("📊 Analyse du biais...")
                analysis = self.bias_analyzer.analyze_bias(
                    original_dataset,
                    biased_dataset,
                    bias_report
                )
                
                # 5. Visualiser avec graphiques adaptés
                print("📈 Génération des visualisations...")
                viz_filename = f"bias_{category}_{bias_type}_{timestamp}.png"
                viz_path = os.path.join(self.output_dir, viz_filename)
                self.bias_analyzer.visualize_bias(
                    original_dataset,
                    biased_dataset,
                    bias_type,
                    bias_report,
                    viz_path
                )
                
            else:
                biased_dataset = original_dataset
                bias_report = {"message": "Aucun biais appliqué", "type": "none"}
                analysis = {}
                viz_path = None
            
            # 6. Sauvegarder les datasets
            output_csv = os.path.join(self.output_dir, f"{category}_biased_{timestamp}.csv")
            biased_dataset.to_csv(output_csv, index=False)
            print(f"💾 Dataset sauvegardé: {output_csv}")
            
            original_csv = os.path.join(self.output_dir, f"{category}_original_{timestamp}.csv")
            original_dataset.to_csv(original_csv, index=False)
            print(f"💾 Dataset original: {original_csv}")
            
            # 7. Sauvegarder le rapport JSON (SANS NaN)
            report_json = os.path.join(self.output_dir, f"{category}_report_{timestamp}.json")
            
            full_report = {
                "generation_info": {
                    "category": category,
                    "n_samples": n_samples,
                    "generated_at": datetime.now().isoformat(),
                    "bias_type": bias_type or "none",
                    "bias_intensity": bias_intensity
                },
                "bias_report": clean_nan_from_dict(bias_report),
                "analysis": clean_nan_from_dict(analysis),
                "files": {
                    "biased_dataset": output_csv,
                    "original_dataset": original_csv,
                    "visualization": viz_path,
                    "report": report_json
                }
            }
            
            with open(report_json, 'w', encoding='utf-8') as f:
                json.dump(full_report, f, indent=2, ensure_ascii=False, default=str)
            print(f"💾 Rapport sauvegardé: {report_json}")
            
            print(f"\n{'='*80}")
            print("✨ GÉNÉRATION TERMINÉE AVEC SUCCÈS!")
            print(f"{'='*80}\n")
            
            return {
                "success": True,
                "biased_dataset_path": output_csv,
                "original_dataset_path": original_csv,
                "visualization_path": viz_path,
                "report_path": report_json,
                "bias_report": clean_nan_from_dict(bias_report),
                "analysis": clean_nan_from_dict(analysis),
                "preview": biased_dataset.head(10).to_dict('records')
            }
            
        except Exception as e:
            print(f"\n❌ ERREUR: {e}")
            import traceback
            traceback.print_exc()
            return {
                "success": False,
                "error": str(e)
            }