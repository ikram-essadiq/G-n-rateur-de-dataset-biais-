"""
🤖 HANDLER LLM - VERSION ULTRA-RAPIDE
Fallback instantané + LLM optionnel
"""

import json
import re
from typing import Dict, Optional, List
import requests
import time


class LLMHandler:
    """Parser intelligent avec fallback instantané"""
    
    def __init__(self, provider: str = "ollama", model: str = None, api_key: str = None):
        self.provider = provider.lower()
        self.api_key = api_key
        self.model = model or "llama3.2:3b"
        
        if self.provider == "ollama":
            self.api_url = "http://localhost:11434/api/generate"
            self.chat_url = "http://localhost:11434/api/chat"
        else:
            raise ValueError(f"Provider {provider} non supporté")
        
        # ✅ DÉSACTIVER LE LLM PAR DÉFAUT (Fallback instantané)
        self.ollama_available = False
        print(f"✅ Mode fallback activé (parsing instantané)")
        
        # ❌ COMMENTÉ - Désactiver la vérification lente
        # self.ollama_available = self._check_ollama_health()
        # if self.ollama_available:
        #     self._warmup_model()
    
    def parse_prompt(self, prompt: str, available_categories: List[str]) -> Dict:
        """
        Point d'entrée principal - Détection intelligente en 2 passes
        """
        
        prompt_lower = prompt.lower().strip()
        
        # ✅ PASSE 1 : Chercher d'abord une catégorie dans le texte
        detected_category = self._quick_category_detection(prompt_lower)
        
        # Si catégorie détectée → C'est une demande de génération
        if detected_category:
            print(f"🔍 Parsing génération : '{prompt}'")
            return self._fallback_parse(prompt, available_categories)
        
        # ✅ PASSE 2 : Sinon, vérifier si c'est conversationnel pur
        conversational_keywords = [
            'bonjour', 'salut', 'hello', 'hi', 'hey', 'coucou', 'bonsoir',
            'qui es-tu', 'tu es qui', 'c\'est quoi', 'qu\'est-ce que',
            'aide', 'help', 'comment', 'quoi faire',
            'merci', 'thanks', 'au revoir', 'bye'
        ]
        
        # Vérifier si UNIQUEMENT conversationnel (pas de mots de génération)
        is_pure_conversational = any(kw in prompt_lower for kw in conversational_keywords)
        has_generation_intent = any(word in prompt_lower for word in 
                                   ['genere', 'génère', 'generate', 'cree', 'crée', 'create',
                                    'dataset', 'data', 'donnees', 'données', 'base'])
        
        if is_pure_conversational and not has_generation_intent:
            print(f"💬 Message conversationnel : '{prompt}'")
            bot_response = self._fallback_conversation(prompt)
            return {
                "category": None,
                "n_samples": 1000,
                "bias_type": None,
                "bias_intensity": 0.5,
                "is_conversational": True,
                "bot_response": bot_response
            }
        
        # ✅ PASSE 3 : Par défaut, essayer de parser comme génération
        print(f"🔍 Parsing génération : '{prompt}'")
        return self._fallback_parse(prompt, available_categories)
    
    def _quick_category_detection(self, prompt_lower: str) -> bool:
        """
        Détection rapide de catégorie dans le texte
        Retourne True si au moins une catégorie est mentionnée
        """
        category_keywords = [
            'etudiant', 'student', 'eleve', 'ecole', 'education', 'educ',  # ✅ AJOUTÉ education
            'patient', 'medical', 'sante', 'hopital',
            'vehicule', 'voiture', 'transport', 'auto',
            'agriculture', 'ferme', 'agricul', 'agri', 'champs',  # ❌ RETIRÉ 'culture'
            'finance', 'banque', 'transaction',
            'immobilier', 'maison', 'logement',
            'animal', 'pet', 'chien', 'chat',
            'sport', 'athlete',
            'energie', 'electrique', 'centrale',
            'chimie', 'chimi', 'molecule', 'chemical',
            'telecom', 'telephone', 'mobile',
            'marche', 'market', 'bourse',
            'geo', 'geographie', 'ville', 'region',
            'personne', 'people', 'individu'
        ]
        
        return any(keyword in prompt_lower for keyword in category_keywords)
    
    def _fallback_conversation(self, prompt: str) -> str:
        """Réponses instantanées sans LLM - Plus intelligentes"""
        prompt_lower = prompt.lower().strip()
        
        # Réponses spécifiques
        responses = {
            ('bonjour', 'salut', 'hello', 'hi', 'hey', 'coucou'): 
                "👋 Bonjour ! Décrivez-moi ce que vous voulez générer.\n\n💡 Exemples :\n• '500 étudiants'\n• 'Générer dataset chimie'\n• '1000 véhicules avec biais de genre'",
            
            ('qui es-tu', 'tu es qui', 'c\'est quoi', 'qu\'est-ce que', 'qui tu es', 'qui est tu'): 
                "🤖 Je suis un assistant intelligent pour générer des datasets synthétiques.\n\n✨ Je comprends :\n• Les fautes d'orthographe\n• Les synonymes (ferme → agriculture)\n• Différentes formulations\n\n📋 14+ catégories disponibles : patients, étudiants, véhicules, finance, agriculture, chimie, sport, immobilier...",
            
            ('aide', 'help', 'comment', 'quoi faire', 'comment faire'): 
                "💡 Décrivez simplement ce que vous voulez !\n\n📝 Formulations acceptées :\n• 'Génère 500 étudiants'\n• 'Dataset de chimie'\n• '1000 patients avec biais d'âge'\n• 'Créer données agriculture'\n\n🎯 Je détecte automatiquement la catégorie et corrige les fautes !",
            
            ('merci', 'thanks', 'thx', 'thank'): 
                "😊 De rien ! Autre chose ?",
            
            ('au revoir', 'bye', 'ciao', 'adieu', 'à bientôt'): 
                "👋 Au revoir !"
        }
        
        for keywords, response in responses.items():
            if any(kw in prompt_lower for kw in keywords):
                return response
        
        # Réponse par défaut avec suggestion
        return "🤔 Je n'ai pas compris.\n\n💡 Essayez :\n• 'Génère 1000 patients'\n• 'Dataset chimie 500'\n• 'Créer données agriculture'\n\nJe comprends même avec des fautes : 'agrcultur' → agriculture ✅"
    
    def _fallback_parse(self, prompt: str, available_categories: List[str]) -> Dict:
        """
        🎯 PARSER INTELLIGENT INSTANTANÉ
        Corrige fautes + Comprend synonymes
        """
        prompt_lower = prompt.lower().strip()
        
        result = {
            "category": None,
            "n_samples": 1000,
            "bias_type": None,
            "bias_intensity": 0.5,
            "is_conversational": False
        }
        
        # ✅ MAPPINGS ULTRA-COMPLETS (avec fautes courantes)
        mappings = {
            # Étudiants (toutes variantes)
            'etudiant': 'students_education', 'etudian': 'students_education',
            'student': 'students_education', 'studant': 'students_education',
            'eleve': 'students_education', 'elev': 'students_education',
            'ecole': 'students_education', 'universite': 'students_education',
            'etude': 'students_education', 'etudient': 'students_education',
            'education': 'students_education', 'educ': 'students_education',  # ✅ AJOUTÉ
            
            # Patients (toutes variantes)
            'patient': 'patients', 'patien': 'patients', 'patiant': 'patients',
            'medical': 'patients', 'medecine': 'patients', 'medecin': 'patients',
            'sante': 'patients', 'santé': 'patients', 'hopital': 'patients',
            'hôpital': 'patients', 'maladie': 'patients',
            
            # Véhicules (toutes variantes)
            'vehicule': 'vehicules_transport', 'vehicul': 'vehicules_transport',
            'voiture': 'vehicules_transport', 'voitur': 'vehicules_transport',
            'transport': 'vehicules_transport', 'auto': 'vehicules_transport',
            'car': 'vehicules_transport', 'camion': 'vehicules_transport',
            'vehic': 'vehicules_transport', 'vehcule': 'vehicules_transport',
            
            # Agriculture (toutes variantes + synonymes)
            'agriculture': 'agri_data', 'agricul': 'agri_data', 'agri': 'agri_data',
            'agric': 'agri_data', 'agrcultur': 'agri_data', 'agricluture': 'agri_data',
            'ferme': 'agri_data', 'farm': 'agri_data', 'agriculteur': 'agri_data',
            'champs': 'agri_data', 'champ': 'agri_data',
            'exploitation': 'agri_data', 'recolte': 'agri_data',
            # ❌ RETIRÉ 'culture' car trop ambigu avec "education"
            
            # Finance (toutes variantes)
            'finance': 'finance_data', 'financ': 'finance_data', 'finan': 'finance_data',
            'banque': 'finance_data', 'bank': 'finance_data', 'banq': 'finance_data',
            'transaction': 'finance_data', 'transac': 'finance_data',
            'argent': 'finance_data', 'credit': 'finance_data', 'pret': 'finance_data',
            'compte': 'finance_data',
            
            # Immobilier (toutes variantes)
            'immobilier': 'biens_complets', 'immobil': 'biens_complets',
            'maison': 'biens_complets', 'logement': 'biens_complets',
            'appartement': 'biens_complets', 'appart': 'biens_complets',
            'bien': 'biens_complets', 'propriete': 'biens_complets',
            'immo': 'biens_complets',
            
            # Animaux (toutes variantes)
            'animal': 'pets_animaux', 'animaux': 'pets_animaux', 'animo': 'pets_animaux',
            'pet': 'pets_animaux', 'chien': 'pets_animaux', 'chat': 'pets_animaux',
            'pets': 'pets_animaux',
            
            # Sport (toutes variantes)
            'sport': 'sport_data', 'athlete': 'sport_data', 'atlete': 'sport_data',
            'sportif': 'sport_data', 'athlet': 'sport_data',
            
            # Énergie (toutes variantes)
            'energie': 'energie_mondiale', 'energy': 'energie_mondiale',
            'electrique': 'energie_mondiale', 'electric': 'energie_mondiale',
            'centrale': 'energie_mondiale', 'energi': 'energie_mondiale',
            
            # Chimie (toutes variantes)
            'chimie': 'Chimie_data', 'chimi': 'Chimie_data', 'chim': 'Chimie_data',
            'molecule': 'Chimie_data', 'chemical': 'Chimie_data',
            'molecul': 'Chimie_data',
            
            # Telecom (toutes variantes)
            'telecom': 'telecom_data', 'telecommunication': 'telecom_data',
            'telephone': 'telecom_data', 'teleph': 'telecom_data',
            'mobile': 'telecom_data', 'tel': 'telecom_data',
            
            # Marché (toutes variantes)
            'marche': 'market_data', 'market': 'market_data',
            'marché': 'market_data', 'bourse': 'market_data',
            'marc': 'market_data',
            
            # Géographie (toutes variantes)
            'geo': 'géo_info_seed', 'geographie': 'géo_info_seed',
            'geographi': 'géo_info_seed', 'geography': 'géo_info_seed',
            'ville': 'géo_info_seed', 'region': 'géo_info_seed',
            'géographie': 'géo_info_seed',
            
            # Personnes (toutes variantes)
            'personne': 'Personnes_infos_seed', 'people': 'Personnes_infos_seed',
            'personn': 'Personnes_infos_seed', 'individu': 'Personnes_infos_seed',
            'gens': 'Personnes_infos_seed'
        }
        
        # ✅ RECHERCHE INTELLIGENTE
        # 1. Recherche exacte
        for keyword, cat in mappings.items():
            if keyword in prompt_lower:
                result["category"] = cat
                print(f"   ✅ Détecté '{keyword}' → {cat}")
                break
        
        # 2. Si pas trouvé, recherche partielle (plus permissive)
        if not result["category"]:
            for keyword, cat in mappings.items():
                if len(keyword) >= 4:  # Mots de 4+ lettres
                    # Correspondance partielle (au moins 70% de similarité)
                    if keyword[:4] in prompt_lower or keyword[-4:] in prompt_lower:
                        result["category"] = cat
                        print(f"   ✅ Correspondance partielle '{keyword}' → {cat}")
                        break
        
        # 3. Recherche dans les catégories disponibles
        if not result["category"]:
            for cat in available_categories:
                cat_clean = cat.lower().replace('_', '').replace('-', '')
                prompt_clean = prompt_lower.replace(' ', '').replace('_', '').replace('-', '')
                
                if cat_clean in prompt_clean or prompt_clean in cat_clean:
                    result["category"] = cat
                    print(f"   ✅ Catégorie directe : {cat}")
                    break
        
        # ✅ EXTRACTION NOMBRE
        numbers = re.findall(r'\b(\d+)\b', prompt)
        if numbers:
            result["n_samples"] = max(100, min(int(numbers[0]), 10000))
            print(f"   ✅ Nombre : {result['n_samples']}")
        
        # ✅ DÉTECTION BIAIS (avec fautes)
        bias_map = {
            ('genre', 'gender', 'sexe', 'genr', 'gendre'): 'gender',
            ('age', 'âge', 'ag'): 'age',
            ('geo', 'geographique', 'géographique', 'region', 'ville', 'geographic'): 'geographic',
            ('socio', 'economique', 'économique', 'revenu', 'prix', 'socioeconomic', 'eco'): 'socioeconomic',
            ('echantillon', 'échantillon', 'sampling', 'sample', 'echant'): 'sampling',
            ('selection', 'sélection', 'select', 'selec'): 'selection',
            ('temporel', 'temporal', 'temps', 'date', 'temp'): 'temporal'
        }
        
        for keywords, bias_type in bias_map.items():
            if any(kw in prompt_lower for kw in keywords):
                result["bias_type"] = bias_type
                print(f"   ✅ Biais : {bias_type}")
                break
        
        return result


def get_llm_handler(provider: str = "ollama") -> LLMHandler:
    """Retourne handler avec fallback instantané"""
    return LLMHandler(provider=provider)