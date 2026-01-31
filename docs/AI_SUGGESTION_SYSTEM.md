# 🧠 SYSTÈME D'INTELLIGENCE & SUGGESTIONS AUTOMATIQUES

## 📋 Vue d'Ensemble

Système d'IA qui:
- ✅ Analyse TOUS les niveaux du funnel (Ads → Sales)
- ✅ Connaît chaque client par cœur (historique complet)
- ✅ Suggère actions avec hypothèse + raison
- ✅ Apprend des autres clients (sans mélanger)
- ✅ Demande approbation manuelle TOUJOURS
- ✅ Évite surcharge de notifications

---

## 🏗️ Architecture Globale

```
┌──────────────────────────────────────────────────────────────┐
│ CLIENT KNOWLEDGE BASE (Par Client)                          │
├──────────────────────────────────────────────────────────────┤
│ • Historique complet (3+ ans)                                │
│ • Tous les tests passés (angles, hooks, offers)              │
│ • Performance historique (winning patterns)                  │
│ • Context: Produits, Offres, Pages, Funnel                  │
│ • Préférences & Guidelines spécifiques                       │
└──────────────────────────────────────────────────────────────┘
                          ↓
┌──────────────────────────────────────────────────────────────┐
│ CROSS-CLIENT INTELLIGENCE (Learnings Globaux)               │
├──────────────────────────────────────────────────────────────┤
│ • Patterns qui marchent (par industrie)                      │
│ • Angles testés (succès/échecs)                             │
│ • Benchmarks de marché                                       │
│ • Tendances émergentes                                       │
│ ⚠️ JAMAIS mélanger données clients directement              │
└──────────────────────────────────────────────────────────────┘
                          ↓
┌──────────────────────────────────────────────────────────────┐
│ ANALYSIS ENGINE (Analyse Multi-Niveaux)                     │
├──────────────────────────────────────────────────────────────┤
│ Niveau 1: Ads (Creative fatigue, CTR, Engagement)           │
│ Niveau 2: AdSets (CPL, Application Rate, Audience)          │
│ Niveau 3: Campaigns (CPA, ROI, Scaling potential)           │
│ Niveau 4: Funnel (Email, SMS, Booking rate)                 │
│ Niveau 5: Sales (Close rate, Objections, Rep perf)          │
│ Niveau 6: Global (LTV, Churn, Product-market fit)           │
└──────────────────────────────────────────────────────────────┘
                          ↓
┌──────────────────────────────────────────────────────────────┐
│ SUGGESTION ENGINE (Génération Suggestions)                  │
├──────────────────────────────────────────────────────────────┤
│ Type A: Optimisation (Scale, Pause, Budget)                 │
│ Type B: Tests Créatifs (Nouveaux angles, hooks)             │
│ Type C: Funnel (Email sequence, Booking flow)               │
│ Type D: Sales (Rep training, Script updates)                │
│                                                               │
│ Chaque suggestion contient TOUJOURS:                         │
│ 1. Action proposée (quoi faire)                             │
│ 2. Raison (pourquoi le faire)                               │
│ 3. Hypothèse (ce qu'on attend comme résultat)               │
│ 4. Données supportant (chiffres réels)                      │
│ 5. Niveau de confiance (0-100%)                             │
└──────────────────────────────────────────────────────────────┘
                          ↓
┌──────────────────────────────────────────────────────────────┐
│ NOTIFICATION SYSTEM (Slack avec Approbation)                │
├──────────────────────────────────────────────────────────────┤
│ • Suggestions envoyées dans Slack                            │
│ • 3 Boutons: ✅ Approuver | ⏸️ Backlog | ❌ Refuser         │
│ • Tracking décisions (apprendre préférences)                 │
│ • Limitation intelligente (max X notifs/jour)                │
└──────────────────────────────────────────────────────────────┘
                          ↓
┌──────────────────────────────────────────────────────────────┐
│ EXECUTION ENGINE (Si approuvé)                              │
├──────────────────────────────────────────────────────────────┤
│ • Execute l'action via Meta API / GHL API                   │
│ • Log dans Airtable (historique décisions)                  │
│ • Monitor résultats (valider hypothèse)                     │
│ • Feedback loop → Améliorer suggestions futures             │
└──────────────────────────────────────────────────────────────┘
```

---

## 📊 CLIENT KNOWLEDGE BASE

### Table Airtable: **client_knowledge** (NOUVELLE)

Contient TOUT ce qu'on sait sur chaque client.

```
Champ                    | Type           | Description
-------------------------|----------------|----------------------------------
client_key               | Text (Primary) | Clé unique client
industry                 | Text           | coaching, ecom, saas, etc.
products                 | Long Text      | JSON liste produits/offres
target_audience          | Long Text      | JSON persona détaillée
funnel_type              | Text           | webinar, vsl, application, etc.
pages                    | Long Text      | JSON URLs pages importantes
brand_voice              | Long Text      | Tone, style, do's & don'ts
guidelines               | Long Text      | Règles spécifiques client
winning_patterns         | Long Text      | JSON patterns qui marchent
tested_angles            | Long Text      | JSON angles testés (historique)
preferences              | Long Text      | JSON préférences décisions
updated_at               | DateTime       | Dernière mise à jour
```

**Exemple JSON `tested_angles`**:

```json
{
  "angles": [
    {
      "angle": "fear_of_missing_out",
      "tested_date": "2023-05-15",
      "result": "success",
      "metrics": {
        "ctr": 3.2,
        "cpa": 145,
        "roi": 2.8
      },
      "notes": "Hook 'Ne ratez pas cette opportunité' a très bien performé"
    },
    {
      "angle": "scarcity_deadline",
      "tested_date": "2023-08-20",
      "result": "failed",
      "metrics": {
        "ctr": 1.8,
        "cpa": 280,
        "roi": 1.2
      },
      "notes": "Deadline artificielle pas crédible pour cette audience"
    }
  ]
}
```

---

### Table Airtable: **global_learnings** (NOUVELLE)

Learnings cross-clients (anonymisés).

```
Champ                    | Type           | Description
-------------------------|----------------|----------------------------------
learning_id              | Auto Number    | ID unique
industry                 | Text           | coaching, ecom, etc.
learning_type            | Select         | angle, hook_type, funnel_step, etc.
pattern                  | Text           | Nom du pattern
success_rate             | Number         | % de succès quand testé
sample_size              | Number         | Combien de fois testé
best_use_case            | Long Text      | Quand utiliser
avoid_when               | Long Text      | Quand éviter
notes                    | Long Text      | Détails
created_at               | Created Time   | Quand découvert
```

**Exemple**:

```
learning_type: "hook_type"
pattern: "question_provocante"
success_rate: 73
sample_size: 42
best_use_case: "Audience froide, produits complexes nécessitant éducation"
avoid_when: "Audiences chaudes qui connaissent déjà le produit"
notes: "Questions qui challengent croyances limitantes performent +40% vs statements"
```

---

## 🔍 ANALYSIS ENGINE - Multi-Niveaux

### Fréquence d'Analyse

```python
ANALYSIS_FREQUENCY = {
    # Niveau Ads (Créatives)
    "creative_performance": {
        "frequency": "3x/jour",  # 8h, 14h, 20h
        "trigger": "hourly_check",
        "threshold": "significant_change"  # Éviter bruit
    },
    
    # Niveau AdSets
    "adset_performance": {
        "frequency": "2x/jour",  # 10h, 18h
        "trigger": "daily_metrics",
        "min_spend": 50  # Minimum $50 dépensé avant analyse
    },
    
    # Niveau Campaign
    "campaign_performance": {
        "frequency": "1x/jour",  # 9h
        "trigger": "daily_rollup",
        "min_spend": 200
    },
    
    # Niveau Funnel
    "funnel_analysis": {
        "frequency": "2x/semaine",  # Lundi, Jeudi
        "trigger": "weekly_rollup",
        "min_events": 30  # Minimum 30 événements
    },
    
    # Niveau Sales
    "sales_analysis": {
        "frequency": "1x/semaine",  # Vendredi
        "trigger": "weekly_sales_data",
        "min_calls": 10  # Minimum 10 appels
    },
    
    # Niveau Global (Stratégie)
    "strategic_analysis": {
        "frequency": "1x/mois",  # Premier du mois
        "trigger": "monthly_review",
        "comprehensive": True
    }
}
```

---

### Niveau 1: Analyse Ads (Creative)

**Déclencheurs de Suggestions**:

```python
def analyze_creative_performance(ad_data, client_context, benchmarks):
    """
    Analyse performance créative et génère suggestions
    """
    suggestions = []
    
    # 1. Fatigue Detection
    if ad_data['fatigue_index'] > 70:
        suggestions.append({
            'type': 'creative_refresh',
            'priority': 'high',
            'action': f"Rafraîchir ad {ad_data['ad_name']}",
            'reason': f"Fatigue index {ad_data['fatigue_index']}/100 - Performance dégradée de 35% sur 7 jours",
            'hypothesis': "Nouveau hook similaire restaurera CTR à 2.8% (vs 1.8% actuel)",
            'confidence': 85,
            'data': {
                'current_ctr': 1.8,
                'benchmark_ctr': 2.5,
                'fatigue_index': ad_data['fatigue_index'],
                'performance_drop': -35
            }
        })
    
    # 2. Winner Detection
    if (ad_data['ctr'] > benchmarks['ctr']['p90'] and 
        ad_data['cpa'] < benchmarks['cpa']['p25']):
        
        suggestions.append({
            'type': 'creative_scale',
            'priority': 'high',
            'action': f"Créer 3 variations de ad {ad_data['ad_name']}",
            'reason': f"CTR {ad_data['ctr']}% (top 10%) + CPA ${ad_data['cpa']} (top 25%) = Winning creative",
            'hypothesis': "Variations avec hooks similaires généreront 40-60% volume additionnel tout en maintenant CPA",
            'confidence': 78,
            'data': {
                'current_ctr': ad_data['ctr'],
                'benchmark_p90': benchmarks['ctr']['p90'],
                'current_cpa': ad_data['cpa'],
                'benchmark_p25': benchmarks['cpa']['p25']
            },
            'suggested_variations': [
                {
                    'type': 'hook_variation',
                    'original_hook': ad_data['hook'],
                    'suggested_hooks': [
                        "97% des [audience] ignorent cette erreur fatale...",
                        "Cette erreur coûte $X/an aux [audience]...",
                        "Saviez-vous que 97% des [audience]..."
                    ]
                }
            ]
        })
    
    # 3. Angle Gap Detection (cross-client intelligence)
    tested_angles = get_client_tested_angles(client_context['client_key'])
    global_winning_angles = get_global_winning_angles(client_context['industry'])
    
    untested_winners = [
        angle for angle in global_winning_angles 
        if angle not in tested_angles and is_aligned_with_client(angle, client_context)
    ]
    
    if untested_winners:
        for angle in untested_winners[:3]:  # Top 3 seulement
            suggestions.append({
                'type': 'new_angle_test',
                'priority': 'medium',
                'action': f"Tester angle '{angle['name']}'",
                'reason': f"Angle non testé avec {angle['success_rate']}% succès chez pairs ({angle['sample_size']} tests)",
                'hypothesis': f"Aligné avec votre offre '{client_context['main_offer']}' - Potentiel +25% leads",
                'confidence': 65,
                'data': {
                    'angle_name': angle['name'],
                    'success_rate': angle['success_rate'],
                    'industry_match': True,
                    'offer_alignment': 'high'
                },
                'suggested_copy': {
                    'hook': angle['example_hooks'][0],
                    'body_structure': angle['body_template'],
                    'cta': angle['recommended_cta']
                }
            })
    
    return suggestions
```

---

### Niveau 2: Analyse AdSets

**Déclencheurs de Suggestions**:

```python
def analyze_adset_performance(adset_data, client_context, benchmarks):
    """
    Analyse adsets et suggère scaling/optimisation
    """
    suggestions = []
    
    # 1. Scale Opportunity
    if (adset_data['cpl'] < benchmarks['cpl']['p25'] and
        adset_data['application_rate'] > benchmarks['application_rate']['p75'] and
        adset_data['spend_7d'] > 500):  # Validation volume
        
        # Calculer scaling potential
        current_budget = adset_data['budget_daily']
        suggested_budget = current_budget * 1.5  # +50%
        
        expected_leads = adset_data['leads_7d'] / 7 * 1.5  # Estimer impact
        
        suggestions.append({
            'type': 'adset_scale',
            'priority': 'high',
            'action': f"Augmenter budget AdSet {adset_data['adset_name']} de ${current_budget} → ${suggested_budget}/jour (+50%)",
            'reason': f"Performance exceptionnelle: CPL ${adset_data['cpl']} (top 25%) + App rate {adset_data['application_rate']}% (top 25%)",
            'hypothesis': f"Génèrera ~{expected_leads:.0f} leads/jour (vs {adset_data['leads_7d']/7:.0f} actuels) tout en maintenant CPL sous ${adset_data['cpl']*1.15:.0f}",
            'confidence': 82,
            'data': {
                'current_budget': current_budget,
                'suggested_budget': suggested_budget,
                'current_cpl': adset_data['cpl'],
                'benchmark_cpl_p25': benchmarks['cpl']['p25'],
                'current_app_rate': adset_data['application_rate'],
                'spend_last_7d': adset_data['spend_7d'],
                'leads_last_7d': adset_data['leads_7d']
            },
            'risk_level': 'low',
            'rollback_plan': f"Si CPL > ${adset_data['cpl']*1.2:.0f} après 48h, revenir à ${current_budget}"
        })
    
    # 2. Underperformer Detection
    if (adset_data['spend_7d'] > 300 and  # Assez de données
        adset_data['cpl'] > benchmarks['cpl']['p75'] and
        adset_data['ctr'] < benchmarks['ctr']['p25']):
        
        suggestions.append({
            'type': 'adset_pause',
            'priority': 'medium',
            'action': f"Pauser AdSet {adset_data['adset_name']}",
            'reason': f"Sous-performance: CPL ${adset_data['cpl']} (bottom 25%) + CTR {adset_data['ctr']}% (bottom 25%) après ${adset_data['spend_7d']} dépensés",
            'hypothesis': "Réallocation budget vers adsets performants augmentera ROI global de 15-20%",
            'confidence': 75,
            'data': {
                'current_cpl': adset_data['cpl'],
                'benchmark_cpl_p75': benchmarks['cpl']['p75'],
                'current_ctr': adset_data['ctr'],
                'spend_7d': adset_data['spend_7d'],
                'wasted_budget_estimate': (adset_data['cpl'] - benchmarks['cpl']['p50']) * adset_data['leads_7d']
            },
            'alternative_action': f"Ou tester nouveau hook dans cet adset avant de pauser"
        })
    
    # 3. Audience Saturation
    if adset_data['frequency'] > 2.5:
        suggestions.append({
            'type': 'audience_refresh',
            'priority': 'medium',
            'action': f"Dupliquer AdSet {adset_data['adset_name']} avec nouvelle audience",
            'reason': f"Fréquence {adset_data['frequency']} (saturation) - Performance plateau",
            'hypothesis': "Nouvelle audience similaire (ex: expand age range) maintiendra performance 4-6 semaines additionnelles",
            'confidence': 70,
            'data': {
                'current_frequency': adset_data['frequency'],
                'audience_size': adset_data['audience_size'],
                'days_running': adset_data['days_running']
            },
            'suggested_audiences': [
                "Élargir age range: 25-55 → 25-65",
                "Lookalike 1% → 2-3%",
                "Intérêts adjacents: [suggest 3 interests]"
            ]
        })
    
    return suggestions
```

---

### Niveau 3: Analyse Campaign

```python
def analyze_campaign_performance(campaign_data, client_context, benchmarks):
    """
    Analyse campagnes et stratégie globale
    """
    suggestions = []
    
    # 1. ROI Decline Detection
    roi_trend = calculate_trend(campaign_data['roi_history_30d'])
    
    if roi_trend['direction'] == 'declining' and roi_trend['magnitude'] > 15:
        # Diagnostic approfondi
        bottleneck = identify_bottleneck(campaign_data, client_context)
        
        suggestions.append({
            'type': 'campaign_diagnostic',
            'priority': 'critical',
            'action': f"Analyser bottleneck '{bottleneck['level']}' dans campagne {campaign_data['campaign_name']}",
            'reason': f"ROI en baisse de {roi_trend['magnitude']}% sur 30 jours (de {roi_trend['start_value']}x → {roi_trend['end_value']}x)",
            'hypothesis': f"Bottleneck identifié: {bottleneck['level']} - Correction restaurera ROI à {roi_trend['start_value']*0.9:.1f}x",
            'confidence': 88,
            'data': {
                'roi_decline_pct': roi_trend['magnitude'],
                'roi_30d_ago': roi_trend['start_value'],
                'roi_current': roi_trend['end_value'],
                'bottleneck_level': bottleneck['level'],
                'bottleneck_metric': bottleneck['metric'],
                'bottleneck_value': bottleneck['current_value'],
                'bottleneck_benchmark': bottleneck['benchmark']
            },
            'diagnostic': bottleneck['analysis'],
            'recommended_actions': bottleneck['fixes']
        })
    
    return suggestions
```

---

### Niveau 4: Analyse Funnel

```python
def analyze_funnel_performance(funnel_data, client_context, benchmarks):
    """
    Analyse email sequences, booking flow, etc.
    """
    suggestions = []
    
    # 1. Email Sequence Optimization
    if funnel_data['email_open_rate'] < benchmarks['email_open_rate']['p25']:
        suggestions.append({
            'type': 'email_optimization',
            'priority': 'medium',
            'action': "Optimiser subject lines email sequence",
            'reason': f"Open rate {funnel_data['email_open_rate']}% (bottom 25%) - Leads perdus dans inbox",
            'hypothesis': "Nouveaux subject lines testés augmenteront open rate à ~{benchmarks['email_open_rate']['p50']}% (+35% leads activés)",
            'confidence': 72,
            'data': {
                'current_open_rate': funnel_data['email_open_rate'],
                'benchmark_p25': benchmarks['email_open_rate']['p25'],
                'benchmark_p50': benchmarks['email_open_rate']['p50'],
                'emails_sent_30d': funnel_data['emails_sent_30d'],
                'lost_opens_estimate': funnel_data['emails_sent_30d'] * (benchmarks['email_open_rate']['p50'] - funnel_data['email_open_rate']) / 100
            },
            'suggested_tests': [
                {
                    'type': 'curiosity_gap',
                    'example': "Ce qu'on ne vous dit PAS sur [sujet]..."
                },
                {
                    'type': 'personalization',
                    'example': "[Nom], votre plan personnalisé est prêt"
                }
            ]
        })
    
    # 2. Booking Flow Friction
    if funnel_data['booking_completion_rate'] < 60:  # Industry standard ~75%
        suggestions.append({
            'type': 'funnel_friction',
            'priority': 'high',
            'action': "Simplifier booking flow (réduire friction)",
            'reason': f"Taux complétion booking {funnel_data['booking_completion_rate']}% - {100-funnel_data['booking_completion_rate']}% abandonnent",
            'hypothesis': "Réduire étapes booking de 4 → 2 augmentera complétion à ~75% (+25% bookings)",
            'confidence': 80,
            'data': {
                'current_completion_rate': funnel_data['booking_completion_rate'],
                'industry_benchmark': 75,
                'booking_starts_30d': funnel_data['booking_starts_30d'],
                'bookings_completed_30d': funnel_data['bookings_completed_30d'],
                'lost_bookings': funnel_data['booking_starts_30d'] * (0.75 - funnel_data['booking_completion_rate']/100)
            },
            'friction_points': [
                "Étape 1: 15% drop-off (formulaire trop long)",
                "Étape 3: 12% drop-off (calendrier peu intuitif)"
            ],
            'recommended_changes': [
                "Combiner étapes 1-2 en une seule page",
                "Ajouter disponibilités suggérées (vs calendrier complet)"
            ]
        })
    
    return suggestions
```

---

### Niveau 5: Analyse Sales

```python
def analyze_sales_performance(sales_data, client_context, benchmarks):
    """
    Analyse calls, objections, rep performance
    """
    suggestions = []
    
    # 1. Close Rate Issues
    if sales_data['close_rate'] < benchmarks['close_rate']['p25']:
        # Analyser par rep
        rep_performance = analyze_rep_breakdown(sales_data)
        
        if rep_performance['variance'] > 20:  # Grosse variance entre reps
            top_rep = rep_performance['top_rep']
            bottom_reps = rep_performance['bottom_reps']
            
            suggestions.append({
                'type': 'sales_training',
                'priority': 'high',
                'action': f"Formation closers - Adopter techniques de {top_rep['name']}",
                'reason': f"Close rate {sales_data['close_rate']}% (bottom 25%) - Variance {rep_performance['variance']}% entre reps",
                'hypothesis': f"Aligner bottom performers sur {top_rep['name']} augmentera close rate global à ~{benchmarks['close_rate']['p50']}%",
                'confidence': 83,
                'data': {
                    'current_close_rate': sales_data['close_rate'],
                    'top_rep_close_rate': top_rep['close_rate'],
                    'bottom_reps_avg': rep_performance['bottom_avg'],
                    'variance': rep_performance['variance'],
                    'potential_additional_sales': calculate_potential_sales(sales_data, benchmarks['close_rate']['p50'])
                },
                'analysis': {
                    'top_rep_strengths': top_rep['strengths'],  # Ex: "Excellent handling objection prix", "Storytelling fort"
                    'bottom_reps_gaps': rep_performance['common_gaps'],  # Ex: "Perdent sur objection timing"
                    'recommended_training': [
                        "Session shadowing avec {top_rep['name']}",
                        "Roleplay objections prix",
                        "Script update: ajouter story section"
                    ]
                }
            })
        
        # Analyser objections
        top_objections = get_top_objections(sales_data)
        
        if top_objections[0]['frequency'] > 30:  # >30% calls lost sur cette objection
            suggestions.append({
                'type': 'objection_handling',
                'priority': 'high',
                'action': f"Créer framework pour objection '{top_objections[0]['objection']}'",
                'reason': f"{top_objections[0]['frequency']}% des deals perdus sur cette objection",
                'hypothesis': "Framework testé réduira cette objection à <15% et augmentera close rate de 8-10 points",
                'confidence': 78,
                'data': {
                    'objection': top_objections[0]['objection'],
                    'frequency': top_objections[0]['frequency'],
                    'lost_deals_30d': top_objections[0]['count'],
                    'revenue_lost': top_objections[0]['count'] * client_context['avg_deal_value']
                },
                'suggested_framework': {
                    'step1': "Valider l'objection",
                    'step2': "Reframe via story client similaire",
                    'step3': "Present ROI calculation",
                    'step4': "Close avec urgency"
                }
            })
    
    return suggestions
```

---

## 💡 SUGGESTION ENGINE - Génération Intelligente

### Priorités & Filtrage

```python
class SuggestionEngine:
    """
    Génère suggestions intelligentes avec filtrage anti-spam
    """
    
    # Limites quotidiennes par type
    MAX_SUGGESTIONS_PER_DAY = {
        'creative_refresh': 3,
        'creative_scale': 2,
        'new_angle_test': 2,
        'adset_scale': 2,
        'adset_pause': 3,
        'campaign_diagnostic': 1,
        'email_optimization': 1,
        'sales_training': 1
    }
    
    # Seuils de confiance minimaux
    MIN_CONFIDENCE = {
        'high_priority': 75,    # Suggestions haute priorité
        'medium_priority': 65,  # Moyenne priorité
        'low_priority': 55      # Basse priorité
    }
    
    def generate_suggestions(self, client_key: str, analysis_results: Dict) -> List[Dict]:
        """
        Génère suggestions filtrées et priorisées
        """
        all_suggestions = []
        
        # Collecter suggestions de tous les niveaux
        all_suggestions.extend(analysis_results['creative_suggestions'])
        all_suggestions.extend(analysis_results['adset_suggestions'])
        all_suggestions.extend(analysis_results['campaign_suggestions'])
        all_suggestions.extend(analysis_results['funnel_suggestions'])
        all_suggestions.extend(analysis_results['sales_suggestions'])
        
        # Filtrer par confiance
        filtered = [
            s for s in all_suggestions 
            if s['confidence'] >= self.MIN_CONFIDENCE[s['priority']]
        ]
        
        # Vérifier limites quotidiennes
        today_suggestions = self._get_today_suggestions(client_key)
        
        final_suggestions = []
        
        for suggestion in filtered:
            # Check si limite atteinte pour ce type
            type_count_today = len([
                s for s in today_suggestions 
                if s['type'] == suggestion['type']
            ])
            
            if type_count_today < self.MAX_SUGGESTIONS_PER_DAY.get(suggestion['type'], 5):
                final_suggestions.append(suggestion)
        
        # Trier par priorité + confiance
        final_suggestions.sort(
            key=lambda x: (
                {'critical': 4, 'high': 3, 'medium': 2, 'low': 1}[x['priority']],
                x['confidence']
            ),
            reverse=True
        )
        
        # Limiter total (max 10 suggestions/jour toutes catégories)
        return final_suggestions[:10]
```

---

## 📬 NOTIFICATION SYSTEM - Slack Interactif

### Message Type: Suggestion

```python
def send_suggestion_to_slack(suggestion: Dict, client_key: str):
    """
    Envoie suggestion dans Slack avec boutons approbation
    """
    # Construire message riche
    blocks = [
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": f"💡 {get_priority_emoji(suggestion['priority'])} Suggestion - {client_key}",
                "emoji": True
            }
        },
        {
            "type": "section",
            "fields": [
                {
                    "type": "mrkdwn",
                    "text": f"*Type:* {format_type(suggestion['type'])}"
                },
                {
                    "type": "mrkdwn",
                    "text": f"*Confiance:* {suggestion['confidence']}%"
                }
            ]
        },
        {
            "type": "divider"
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"*🎯 ACTION PROPOSÉE*\n{suggestion['action']}"
            }
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"*📊 RAISON*\n{suggestion['reason']}"
            }
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"*🔮 HYPOTHÈSE*\n{suggestion['hypothesis']}"
            }
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"*📈 DONNÉES*\n{format_data(suggestion['data'])}"
            }
        }
    ]
    
    # Boutons d'action
    blocks.append({
        "type": "actions",
        "elements": [
            {
                "type": "button",
                "text": {
                    "type": "plain_text",
                    "text": "✅ Approuver & Exécuter",
                    "emoji": True
                },
                "style": "primary",
                "value": json.dumps({
                    'suggestion_id': suggestion['id'],
                    'action': 'approve'
                }),
                "action_id": "approve_suggestion"
            },
            {
                "type": "button",
                "text": {
                    "type": "plain_text",
                    "text": "⏸️ Backlog (Y revenir)",
                    "emoji": True
                },
                "value": json.dumps({
                    'suggestion_id': suggestion['id'],
                    'action': 'backlog'
                }),
                "action_id": "backlog_suggestion"
            },
            {
                "type": "button",
                "text": {
                    "type": "plain_text",
                    "text": "❌ Refuser",
                    "emoji": True
                },
                "style": "danger",
                "value": json.dumps({
                    'suggestion_id': suggestion['id'],
                    'action': 'refuse'
                }),
                "action_id": "refuse_suggestion"
            }
        ]
    })
    
    # Envoyer
    slack.send_message(
        channel='#ai-suggestions',  # Canal dédié
        blocks=blocks
    )
```

**CONTINUER?** Je peux créer:
1. Code complet du système
2. Tables Airtable détaillées
3. Examples de suggestions réelles
4. Système d'apprentissage (feedback loop)

Dites-moi! 🚀
