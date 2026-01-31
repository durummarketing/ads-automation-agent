"""
Creative Performance Analyzer - Système d'analyse avancée des créatives
Analyse hooks, bodies, CTAs, et assets avec IA
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any, Tuple
from dataclasses import dataclass
from enum import Enum
import re


class CreativeComponent(Enum):
    """Types de composants créatifs"""
    HOOK = "hook"
    BODY = "body"
    CTA = "cta"
    ASSET = "asset"


@dataclass
class ComponentPerformance:
    """Performance d'un composant créatif"""
    component_id: str
    component_type: CreativeComponent
    
    # Métriques brutes
    impressions: int
    clicks: int
    conversions: int
    spend: float
    
    # Métriques calculées
    ctr: float
    conversion_rate: float
    cost_per_conversion: float
    
    # Scores (0-100)
    performance_score: float
    fatigue_index: float
    
    # Comparaisons
    percentile_rank: int  # 0-100
    vs_benchmark: float  # Ratio vs benchmark
    
    # Analyse
    strengths: List[str]
    weaknesses: List[str]
    recommendations: List[str]


class CreativePerformanceAnalyzer:
    """
    Analyseur de performance créative avec intelligence contextuelle
    """
    
    def __init__(self, benchmarks_data: pd.DataFrame):
        """
        Args:
            benchmarks_data: DataFrame avec benchmarks par type de composant
        """
        self.benchmarks = benchmarks_data
        
        # Benchmarks par défaut si pas de données
        self.default_benchmarks = {
            'hook': {'ctr': 2.5, 'engagement': 1.8},
            'body': {'link_click_rate': 3.2, 'read_through': 45},
            'cta': {'ctr': 2.1, 'conversion': 0.12},
            'asset_video': {'hook_rate': 50, 'completion': 25},
            'asset_image': {'ctr': 1.9, 'engagement': 1.7}
        }
    
    def analyze_hook(
        self,
        hook_data: Dict[str, Any],
        context: Dict[str, Any]
    ) -> ComponentPerformance:
        """
        Analyse complète d'un hook
        
        Args:
            hook_data: Données du hook
            context: Contexte (industrie, audience, etc.)
            
        Returns:
            ComponentPerformance avec analyse détaillée
        """
        # Calculer métriques
        ctr = (hook_data['clicks'] / hook_data['impressions']) * 100 if hook_data['impressions'] > 0 else 0
        
        # Récupérer benchmarks appropriés
        benchmark = self._get_benchmark('hook', context)
        
        # Calculer scores
        performance_score = self._calculate_performance_score(
            {'ctr': ctr},
            benchmark,
            weights={'ctr': 1.0}
        )
        
        fatigue_index = self._calculate_fatigue_index(hook_data)
        percentile_rank = self._calculate_percentile(ctr, benchmark['ctr'])
        
        # Analyse sémantique du hook
        semantic_analysis = self._analyze_hook_semantics(hook_data['text'])
        
        # Identifier forces et faiblesses
        strengths, weaknesses = self._identify_hook_strengths_weaknesses(
            hook_data,
            benchmark,
            semantic_analysis
        )
        
        # Générer recommandations
        recommendations = self._generate_hook_recommendations(
            hook_data,
            semantic_analysis,
            weaknesses,
            context
        )
        
        return ComponentPerformance(
            component_id=hook_data['hook_id'],
            component_type=CreativeComponent.HOOK,
            impressions=hook_data['impressions'],
            clicks=hook_data['clicks'],
            conversions=hook_data.get('conversions', 0),
            spend=hook_data.get('spend', 0),
            ctr=ctr,
            conversion_rate=0,  # Calculé différemment pour hook
            cost_per_conversion=0,
            performance_score=performance_score,
            fatigue_index=fatigue_index,
            percentile_rank=percentile_rank,
            vs_benchmark=ctr / benchmark['ctr'] if benchmark['ctr'] > 0 else 1.0,
            strengths=strengths,
            weaknesses=weaknesses,
            recommendations=recommendations
        )
    
    def _analyze_hook_semantics(self, hook_text: str) -> Dict[str, Any]:
        """
        Analyse sémantique avancée du hook
        """
        analysis = {
            'length': len(hook_text),
            'word_count': len(hook_text.split()),
            'has_question': '?' in hook_text,
            'has_numbers': bool(re.search(r'\d+', hook_text)),
            'has_emoji': self._contains_emoji(hook_text),
            'emotion': self._detect_emotion(hook_text),
            'power_words': self._count_power_words(hook_text),
            'reading_level': self._calculate_reading_level(hook_text)
        }
        
        # Identifier le type de hook
        analysis['hook_type'] = self._classify_hook_type(hook_text)
        
        return analysis
    
    def _classify_hook_type(self, text: str) -> str:
        """
        Classifie le type de hook automatiquement
        """
        text_lower = text.lower()
        
        # Question
        if '?' in text:
            return 'question'
        
        # Statistique (contient chiffres)
        if re.search(r'\d+[%xK$]', text):
            return 'statistic'
        
        # Challenge/Défi
        challenge_words = ['prouve', 'défie', 'ose', 'capable']
        if any(word in text_lower for word in challenge_words):
            return 'challenge'
        
        # Story
        story_words = ['il y a', 'quand', 'jour où', 'fois que']
        if any(phrase in text_lower for phrase in story_words):
            return 'story'
        
        # Par défaut: statement
        return 'statement'
    
    def _detect_emotion(self, text: str) -> str:
        """
        Détecte l'émotion dominante du hook
        """
        emotion_keywords = {
            'fear': ['erreur', 'danger', 'perte', 'manquer', 'risque', 'attention'],
            'curiosity': ['secret', 'découvre', 'révèle', 'caché', 'méthode'],
            'desire': ['rêve', 'liberté', 'succès', 'richesse', 'gagne'],
            'urgency': ['maintenant', 'urgent', 'dernier', 'fin', 'expire'],
            'trust': ['garanti', 'prouvé', 'certifié', 'vérifi'],
        }
        
        text_lower = text.lower()
        
        # Compter occurrences par émotion
        emotion_scores = {}
        for emotion, keywords in emotion_keywords.items():
            score = sum(1 for kw in keywords if kw in text_lower)
            if score > 0:
                emotion_scores[emotion] = score
        
        # Retourner émotion dominante
        if emotion_scores:
            return max(emotion_scores, key=emotion_scores.get)
        
        return 'neutral'
    
    def _count_power_words(self, text: str) -> int:
        """
        Compte les power words dans le texte
        """
        power_words = [
            'gratuit', 'garanti', 'prouvé', 'simple', 'facile', 'rapide',
            'nouveau', 'exclusif', 'limité', 'secret', 'révélé', 'découvre',
            'instantané', 'immédiat', 'maintenant', 'aujourd\'hui', 'erreur',
            'danger', 'attention', 'important', 'critique'
        ]
        
        text_lower = text.lower()
        return sum(1 for word in power_words if word in text_lower)
    
    def _calculate_reading_level(self, text: str) -> str:
        """
        Calcule le niveau de lecture requis
        """
        words = text.split()
        avg_word_length = sum(len(w) for w in words) / len(words) if words else 0
        
        if avg_word_length < 4:
            return 'very_simple'
        elif avg_word_length < 5.5:
            return 'simple'
        elif avg_word_length < 7:
            return 'medium'
        else:
            return 'complex'
    
    def _contains_emoji(self, text: str) -> bool:
        """
        Vérifie présence d'emojis
        """
        # Pattern simplifié pour emojis Unicode
        emoji_pattern = re.compile(
            "["
            "\U0001F600-\U0001F64F"  # emoticons
            "\U0001F300-\U0001F5FF"  # symbols & pictographs
            "\U0001F680-\U0001F6FF"  # transport & map
            "\U0001F1E0-\U0001F1FF"  # flags
            "]+",
            flags=re.UNICODE
        )
        return bool(emoji_pattern.search(text))
    
    def _identify_hook_strengths_weaknesses(
        self,
        hook_data: Dict[str, Any],
        benchmark: Dict[str, float],
        semantic: Dict[str, Any]
    ) -> Tuple[List[str], List[str]]:
        """
        Identifie forces et faiblesses d'un hook
        """
        strengths = []
        weaknesses = []
        
        ctr = (hook_data['clicks'] / hook_data['impressions']) * 100 if hook_data['impressions'] > 0 else 0
        
        # CTR analysis
        if ctr > benchmark['ctr'] * 1.2:
            strengths.append(f"CTR excellent ({ctr:.2f}% vs {benchmark['ctr']:.2f}% benchmark)")
        elif ctr < benchmark['ctr'] * 0.8:
            weaknesses.append(f"CTR faible ({ctr:.2f}% vs {benchmark['ctr']:.2f}% benchmark)")
        
        # Semantic analysis
        if semantic['has_question']:
            strengths.append("Utilise une question (augmente curiosité)")
        
        if semantic['has_numbers']:
            strengths.append("Contient chiffres spécifiques (crédibilité)")
        
        if semantic['power_words'] >= 2:
            strengths.append(f"Bon usage de power words ({semantic['power_words']})")
        elif semantic['power_words'] == 0:
            weaknesses.append("Aucun power word (manque d'impact)")
        
        if semantic['reading_level'] == 'complex':
            weaknesses.append("Niveau de lecture trop complexe")
        
        if semantic['word_count'] > 15:
            weaknesses.append("Hook trop long (>15 mots)")
        
        return strengths, weaknesses
    
    def _generate_hook_recommendations(
        self,
        hook_data: Dict[str, Any],
        semantic: Dict[str, Any],
        weaknesses: List[str],
        context: Dict[str, Any]
    ) -> List[str]:
        """
        Génère recommandations actionnables pour améliorer le hook
        """
        recommendations = []
        
        # Basé sur les faiblesses
        if any('CTR faible' in w for w in weaknesses):
            recommendations.append({
                'priority': 'high',
                'category': 'performance',
                'action': 'Tester variations de hooks',
                'suggestion': self._suggest_hook_variations(hook_data['text'], semantic)
            })
        
        if any('trop long' in w for w in weaknesses):
            recommendations.append({
                'priority': 'medium',
                'category': 'structure',
                'action': 'Réduire longueur',
                'suggestion': f"Cibler 8-12 mots maximum (actuellement {semantic['word_count']})"
            })
        
        if not semantic['has_question'] and semantic['hook_type'] != 'statistic':
            recommendations.append({
                'priority': 'medium',
                'category': 'format',
                'action': 'Tester format question',
                'suggestion': self._convert_to_question(hook_data['text'])
            })
        
        if semantic['power_words'] == 0:
            recommendations.append({
                'priority': 'high',
                'category': 'copywriting',
                'action': 'Ajouter power words',
                'suggestion': 'Intégrer mots comme: garanti, secret, erreur, découvre'
            })
        
        # Basé sur l'émotion détectée
        if semantic['emotion'] == 'neutral':
            recommendations.append({
                'priority': 'high',
                'category': 'emotion',
                'action': 'Augmenter charge émotionnelle',
                'suggestion': 'Cibler curiosité, peur ou désir plus fortement'
            })
        
        return recommendations
    
    def _suggest_hook_variations(self, original_text: str, semantic: Dict[str, Any]) -> List[str]:
        """
        Suggère des variations du hook
        """
        variations = []
        
        # Variation 1: Ajouter question si pas déjà
        if not semantic['has_question']:
            variations.append(f"{original_text}?")
        
        # Variation 2: Ajouter chiffre si pas déjà
        if not semantic['has_numbers']:
            variations.append(f"97% {original_text.lower()}")
        
        # Variation 3: Format négatif
        variations.append(f"Arrêtez de {original_text.lower()}")
        
        return variations[:3]  # Max 3 suggestions
    
    def _convert_to_question(self, statement: str) -> str:
        """
        Convertit un statement en question
        """
        # Simplification - en production utiliserait NLP
        question_starters = [
            "Saviez-vous que",
            "Et si",
            "Pourquoi",
            "Comment"
        ]
        
        # Prendre un starter aléatoire et combiner
        return f"{question_starters[0]} {statement.lower()}?"
    
    def _get_benchmark(self, component_type: str, context: Dict[str, Any]) -> Dict[str, float]:
        """
        Récupère le benchmark approprié selon le contexte
        """
        # En production, interrogerait la DB de benchmarks
        # Pour l'instant, retourner défaut
        return self.default_benchmarks.get(component_type, {})
    
    def _calculate_performance_score(
        self,
        metrics: Dict[str, float],
        benchmark: Dict[str, float],
        weights: Dict[str, float]
    ) -> float:
        """
        Calcule score composite de performance (0-100)
        """
        score = 0
        
        for metric, weight in weights.items():
            if metric in metrics and metric in benchmark:
                ratio = metrics[metric] / benchmark[metric] if benchmark[metric] > 0 else 1.0
                
                # Normaliser (médiane = 50, top 10% = 100)
                if ratio >= 1.5:  # Top 10%
                    normalized = 100
                elif ratio >= 1.2:  # Top 25%
                    normalized = 75 + ((ratio - 1.2) / 0.3) * 25
                elif ratio >= 1.0:  # Au-dessus médiane
                    normalized = 50 + ((ratio - 1.0) / 0.2) * 25
                elif ratio >= 0.8:  # Légèrement sous médiane
                    normalized = 25 + ((ratio - 0.8) / 0.2) * 25
                else:  # Sous-performance
                    normalized = max(0, (ratio / 0.8) * 25)
                
                score += normalized * weight
        
        return round(score, 1)
    
    def _calculate_fatigue_index(self, component_data: Dict[str, Any]) -> float:
        """
        Calcule l'index de fatigue (0-100)
        100 = complètement fatigué
        """
        fatigue = 0
        
        # Facteur 1: Déclin de performance
        if 'ctr_initial' in component_data and 'ctr_current' in component_data:
            ctr_decline = (component_data['ctr_initial'] - component_data['ctr_current']) / component_data['ctr_initial']
            fatigue += min(ctr_decline * 100, 40)  # Max 40 points
        
        # Facteur 2: Durée d'utilisation
        days_active = component_data.get('days_active', 0)
        fatigue += min(days_active / 30 * 30, 30)  # Max 30 points
        
        # Facteur 3: Fréquence
        frequency = component_data.get('frequency', 1.0)
        if frequency > 2.0:
            fatigue += min((frequency - 2.0) * 15, 30)  # Max 30 points
        
        return round(min(fatigue, 100), 1)
    
    def _calculate_percentile(self, value: float, benchmark: float) -> int:
        """
        Calcule rang percentile approximatif
        """
        ratio = value / benchmark if benchmark > 0 else 1.0
        
        if ratio >= 1.5:
            return 95
        elif ratio >= 1.2:
            return 80
        elif ratio >= 1.0:
            return 50
        elif ratio >= 0.8:
            return 25
        else:
            return 10


# Fonctions utilitaires pour analyse de combinaisons

def analyze_combination_synergy(
    hook_performance: ComponentPerformance,
    body_performance: ComponentPerformance,
    cta_performance: ComponentPerformance,
    asset_performance: ComponentPerformance,
    combo_actual_performance: Dict[str, float]
) -> Dict[str, Any]:
    """
    Analyse la synergie entre composants
    
    Détermine si la combinaison performe mieux/moins bien
    que la somme de ses parties
    """
    # Performance attendue (moyenne des composants)
    expected_ctr = np.mean([
        hook_performance.ctr,
        asset_performance.ctr
    ])
    
    expected_conversion = cta_performance.conversion_rate
    
    # Performance réelle de la combo
    actual_ctr = combo_actual_performance['ctr']
    actual_conversion = combo_actual_performance['conversion_rate']
    
    # Calculer synergie
    ctr_synergy = (actual_ctr / expected_ctr) * 100 if expected_ctr > 0 else 100
    conversion_synergy = (actual_conversion / expected_conversion) * 100 if expected_conversion > 0 else 100
    
    overall_synergy = (ctr_synergy + conversion_synergy) / 2
    
    # Interpréter
    if overall_synergy >= 120:
        verdict = {
            'grade': 'A+',
            'status': 'Excellente synergie',
            'recommendation': '🌟 Combinaison gagnante! Scaler.',
            'action': 'scale'
        }
    elif overall_synergy >= 105:
        verdict = {
            'grade': 'B+',
            'status': 'Bonne synergie',
            'recommendation': '✅ Combo solide. Continuer.',
            'action': 'maintain'
        }
    elif overall_synergy >= 95:
        verdict = {
            'grade': 'C',
            'status': 'Synergie neutre',
            'recommendation': 'ℹ️ Tester variations.',
            'action': 'test'
        }
    else:
        verdict = {
            'grade': 'D',
            'status': 'Synergie négative',
            'recommendation': '⚠️ Composants ne matchent pas. Recombiner.',
            'action': 'recombine'
        }
    
    return {
        'synergy_score': overall_synergy,
        'ctr_synergy': ctr_synergy,
        'conversion_synergy': conversion_synergy,
        'verdict': verdict,
        
        # Détails
        'expected_performance': {
            'ctr': expected_ctr,
            'conversion_rate': expected_conversion
        },
        'actual_performance': {
            'ctr': actual_ctr,
            'conversion_rate': actual_conversion
        },
        
        # Analyse détaillée
        'component_compatibility': analyze_component_compatibility(
            hook_performance,
            body_performance,
            cta_performance,
            asset_performance
        )
    }


def analyze_component_compatibility(
    hook: ComponentPerformance,
    body: ComponentPerformance,
    cta: ComponentPerformance,
    asset: ComponentPerformance
) -> Dict[str, str]:
    """
    Analyse si les composants sont compatibles entre eux
    """
    compatibility = {}
    
    # Hook-Asset compatibility
    # (ex: hook curiosité + asset testimonial = bon match)
    compatibility['hook_asset'] = 'good'  # À implémenter logique
    
    # Body-CTA compatibility
    # (ex: body long + CTA high-friction = mauvais match pour cold traffic)
    compatibility['body_cta'] = 'good'
    
    # Overall message consistency
    compatibility['message_consistency'] = 'high'
    
    return compatibility


# Export pour utilisation
__all__ = [
    'CreativePerformanceAnalyzer',
    'ComponentPerformance',
    'CreativeComponent',
    'analyze_combination_synergy',
    'analyze_component_compatibility'
]
