# 📋 SPÉCIFICATIONS SYSTÈME FINALES - DURUM AI Agent

## 🎯 PRIORISATION FEATURES (Confirmée)

### PHASE 1 - MVP (Semaine 1-2) - MUST-HAVE

**A. Benchmarks Dynamiques** (Score: 10-6-10)
```
MUST-HAVE Phase 1:
✅ Benchmarks 5 niveaux (CRITIQUE - Score 10)
⏸️ 30+ métriques (NICE-TO-HAVE - Score 6) → Start avec 10-15 essentielles
✅ Calcul automatique quotidien (CRITIQUE - Score 10)

Phase 1 Focus:
- Métriques critiques: ROI, CPL, CPB, Close Rate, CTR, CPA
- 3 niveaux prioritaires: Global, Industry, Client History
- Calcul quotidien 9h AM
```

**C. Publishing Double Validation** (Score: 10-10-10-7)
```
MUST-HAVE Phase 1:
✅ Workflow Airtable → Client → Vous → Meta (Score 10)
✅ Notifications Slack interactives (Score 10)
✅ Rappels automatiques 24h (Score 10)
⏸️ 3 modes publication (Score 7) → Start avec Auto/Manuel, Test = Phase 2

Phase 1 Focus:
- Client validation dans #client-X-validation
- Votre validation finale dans #durum-validation-finale
- Rappels 24h si pas de réponse
- Publication Meta avec safeguards budget
```

**E. Analyse Multi-Niveaux** (Score: 10-6-10-10)
```
MUST-HAVE Phase 1:
✅ Ads → AdSets → Campaigns (Score 10)
⏸️ Funnel Email/Booking (Score 6) → Phase 2
✅ Sales (Score 10)
✅ Identification bottlenecks (Score 10)

Phase 1 Focus:
- Bottom-up analysis (ROI → Ads)
- Bottleneck detection avec données réelles
- Integration GHL pour sales data
```

**F. Suggestions Automatiques** (Score: 9-10-7-10)
```
MUST-HAVE Phase 1:
✅ Scale/Pause recommandations (Score 9)
✅ Tests créatifs suggérés (Score 10)
⏸️ Optimisations funnel (Score 7) → Phase 2
✅ Approbation manuelle obligatoire (Score 10)

Phase 1 Focus:
- Max 10-20 suggestions/jour
- Confiance minimum 90%
- TOUJOURS 2-3 raisons data-driven
- Slack notifications groupées
```

### PHASE 2 - Intelligence (Semaine 3-4)

**B. Analyse Créative Avancée** (Score: 10-8-6-10)
```
✅ Décomposition hooks/body/CTA/asset (Score 10)
✅ Scores performance (Score 8)
⏸️ Détection fatigue (Score 6) → Nice-to-have
✅ Suggestions nouveaux angles (Score 10)
```

**D. Système Apprentissage IA** (Score: 9-7-10-10)
```
✅ Pattern detection décisions (Score 9)
⏸️ Hypothesis tracking (Score 7) → Simple version Phase 1
✅ Amélioration continue (Score 10)
✅ Client knowledge base (Score 10)
```

---

## 📊 DONNÉES & CONTEXTE

### État Actuel

**Growth OS (Google Sheets)**:
- LOG_MASTER: 390 lignes (depuis 10 jan 2026)
- SPEND_MASTER: Depuis 10 jan 2026
- 02_metrics_period: ❌ NON EXISTANT → À créer via AppScript
- Clients configurés: 0 → À créer

**Airtable**:
- Tables ads/campaigns: ❌ NON → À créer from scratch
- Historique: ❌ NON
- Clients: 6
- Ads historiques: 0 → Import manuel/auto à décider

**Meta Ads**:
- API: ✅ Configuré
- Comptes: 6
- Historique: ✅ Depuis création comptes (plusieurs années)

**GHL**:
- Utilisé: ✅ OUI
- API: ✅ Disponible
- Données email/SMS: ✅ IMPORTANTES

### Décision Critique: Import Historique

**Option A**: Import automatique Meta → Airtable
- Récupérer 6-12 mois historique via Meta API
- Populate tables ads/campaigns/adsets
- Enrich avec performance data
- **Avantage**: IA commence avec contexte
- **Temps**: 2-3 jours dev

**Option B**: Start fresh + Import manuel critique
- Créer tables vides
- Vous importez manuellement top 10 winners passés
- Système apprend au fur et à mesure
- **Avantage**: Plus rapide démarrage
- **Temps**: 1 jour dev

**Recommandation**: Option A (import auto)
- IA beaucoup plus précise dès Jour 1
- Worth 2 jours extra dev

---

## 🔄 WORKFLOWS ACTUELS → AUTOMATISÉS

### Workflow 1: Création Nouvelles Ads

**ACTUEL**:
```
1. Vous décidez besoin nouvelles ads
2. Partner crée copy dans Google Doc
3. Assets envoyés via Gmail
4. Review client dans Slack #validation
5. Approbation manuelle
6. Publication manuelle Meta
7. Suivi performance manuel (Meta + Sheets + partout)
```

**FUTUR (Automatisé)**:
```
1. IA détecte besoin refresh (fatigue detection)
   → Suggestion: "Créer 3 variations Hook X"
   → Slack notification #durum-suggestions

2. Vous approuvez suggestion
   → Status: "Approved - En création"

3. Partner crée copy dans Airtable directement
   → Table: ads_drafts
   → Status: "Draft - Prêt validation"

4. Assets uploadés Airtable (ou lien)
   → Validation structure automatique

5. IA envoie validation client Slack #client-X-validation
   → Preview complet ad
   → Boutons: ✅ Approuver / 💬 Commentaire

6. Client approuve
   → Status: "Approuvé Client"
   → Notification #durum-validation-finale

7. Vous validation finale
   → Status: "Approuvé Final"
   → Publication automatique Meta (1 min)

8. Suivi performance automatique
   → Dashboard Looker Studio
   → Alertes Slack si anomalies
   → Suggestions optimization automatiques
```

**Économie temps**: 3-4h/semaine → 30min/semaine

---

### Workflow 2: Décision Scaling

**ACTUEL**:
```
1. Vous regardez Meta manually
2. Identifiez adset qui performe (bon bookings, CPB, ROI)
3. Décidez scaler (ROI >3-5x)
4. Vérifiez capacité vendeurs avec client
5. Scale manuellement Meta
6. Daily check performance
```

**FUTUR (Assisté IA)**:
```
1. IA analyse quotidienne (9h AM)
   → Détecte: AdSet "STACK_H:25/45 _QC" 
   → ROI: 4.2x (benchmark: 2.8x)
   → CPB: $95 (benchmark: $120)
   → Bookings: 18/semaine (stable)

2. IA génère suggestion
   → "Scale AdSet +50% ($150 → $225/jour)"
   → Raison 1: ROI 4.2x (top 15% benchmark)
   → Raison 2: CPB -21% vs benchmark (très efficient)
   → Raison 3: Volume stable 3 semaines (pas fluke)
   → Confiance: 92%

3. Notification Slack #durum-suggestions
   → Vous voyez: données + graphes
   → Check capacité vendeurs (manuel pour l'instant)

4. Vous approuvez
   → IA scale automatiquement Meta
   → Safeguard: Max budget journalier +50% (pas plus)
   → Safeguard: Alerte si CPA >+25% dans 48h

5. Monitoring automatique
   → Daily check performance
   → Alerte si metrics dégradent
   → Suggestion rollback si nécessaire

6. Vous recevez rapport 48h après scaling
   → Performance vs prédictions IA
   → Validation hypothèse
   → IA apprend de l'outcome
```

**Économie temps**: 2h/jour → 15min/jour

---

## 🔒 CONTRAINTES & SAFEGUARDS

### Budget Safeguards (CRITIQUE)

```python
SAFEGUARDS_BUDGET = {
    # Limites par client
    'monthly_max_per_client': 100000,  # $100k/mois max
    
    # Limites par test/campagne
    'test_budget_max': 10000,  # 2x prix produit ($5k produit = $10k test max)
    
    # Scaling safeguards
    'max_scale_increment': 0.5,  # +50% max d'un coup
    'scale_cooldown_hours': 48,  # Attendre 48h entre scales
    
    # Budget blow-up protection
    'daily_overspend_alert': 1.2,  # Alerte si +20% budget prévu
    'daily_overspend_pause': 1.5,  # PAUSE AUTO si +50% budget
    'hourly_check_overspend': True,  # Check chaque heure
    
    # Meta API safeguards
    'lifetime_budget_cap': True,  # TOUJOURS lifetime budget cap
    'bid_cap': True,  # Bid cap activé
    'cost_cap': True,  # Cost cap si disponible
}

# Scénario B Protection
def check_budget_blowup():
    """
    Vérifie budget blow-up CHAQUE HEURE
    """
    for adset in active_adsets:
        expected_spend = adset.budget_daily / 24 * hours_since_start
        actual_spend = get_meta_spend(adset.id)
        
        if actual_spend > expected_spend * 1.5:
            # PAUSE IMMÉDIAT
            pause_adset(adset.id)
            
            # ALERTE URGENTE
            slack.send_urgent_alert(
                channel='alerts-urgent',
                message=f"🚨 BUDGET BLOW-UP DETECTED\n"
                        f"AdSet: {adset.name}\n"
                        f"Expected: ${expected_spend}\n"
                        f"Actual: ${actual_spend}\n"
                        f"→ PAUSED AUTOMATICALLY"
            )
```

### Accuracy Safeguards (IA Suggestions)

```python
SUGGESTION_VALIDATION = {
    # Confiance minimum
    'min_confidence': 90,  # 90% minimum (vous avez demandé)
    
    # Raisons data-driven
    'min_reasons': 2,  # Minimum 2 raisons
    'max_reasons': 4,  # Maximum 4 (éviter overload)
    
    # Validation logique
    'check_conflicts': True,  # Détecte suggestions conflictuelles
    'check_sanity': True,     # Sanity check (ex: pas scale ad en perte)
}

# Scénario C Protection
def validate_suggestion(suggestion):
    """
    Valide suggestion avant envoyer
    """
    # Check 1: Confidence
    if suggestion.confidence < 90:
        return False, "Confiance trop faible (<90%)"
    
    # Check 2: Raisons data-driven
    if len(suggestion.reasons) < 2:
        return False, "Pas assez de raisons"
    
    for reason in suggestion.reasons:
        if not has_data_support(reason):
            return False, f"Raison '{reason}' pas data-driven"
    
    # Check 3: Sanity check
    if suggestion.type == 'scale':
        if suggestion.current_roi < 1.0:
            return False, "ROI négatif - absurde de scaler"
        
        if suggestion.current_cpa > suggestion.benchmark_cpa * 2:
            return False, "CPA 2x benchmark - absurde de scaler"
    
    # Check 4: Conflits
    active_suggestions = get_active_suggestions(suggestion.client_key)
    conflicts = detect_conflicts(suggestion, active_suggestions)
    
    if conflicts:
        return False, f"Conflit: {conflicts}"
    
    return True, "Valid"

# Gestion incertitude
def handle_uncertainty(confidence):
    """
    Si confiance <90%, expliquer pourquoi
    """
    if confidence < 90:
        return {
            'suggest': False,
            'message': f"Je ne suggère pas (confiance {confidence}%). "
                      f"Raisons: [données insuffisantes / pattern pas clair / trop de variance]"
        }
```

### Data Quality Safeguards

```python
DATA_VALIDATION = {
    # Détection doublons
    'check_duplicates': True,
    'duplicate_threshold': 0.95,  # 95% similarité = doublon
    
    # Validation fraîcheur
    'max_data_age_hours': 24,  # Données >24h = alerte
    
    # Validation complétude
    'min_data_completeness': 0.9,  # 90% champs remplis minimum
}

# Scénario D Protection
def validate_data_quality(data_source):
    """
    Valide qualité données avant analyse
    """
    issues = []
    
    # Check duplicates
    duplicates = detect_duplicates(data_source)
    if duplicates:
        issues.append({
            'severity': 'CRITICAL',
            'issue': f"{len(duplicates)} doublons détectés",
            'source': data_source.name,
            'action': 'PAUSE_ANALYSIS'
        })
    
    # Check freshness
    last_update = get_last_update(data_source)
    age_hours = (datetime.now() - last_update).hours
    
    if age_hours > 24:
        issues.append({
            'severity': 'WARNING',
            'issue': f"Données vieilles de {age_hours}h",
            'source': data_source.name,
            'action': 'ALERT_TEAM'
        })
    
    # Check completeness
    completeness = calculate_completeness(data_source)
    if completeness < 0.9:
        issues.append({
            'severity': 'HIGH',
            'issue': f"Données incomplètes ({completeness*100}%)",
            'source': data_source.name,
            'action': 'ALERT_TEAM'
        })
    
    if issues:
        # Alerter immédiatement
        for issue in issues:
            slack.send_alert(
                channel='alerts-urgent' if issue['severity'] == 'CRITICAL' else 'team-durum',
                message=f"⚠️ Data Quality Issue\n{json.dumps(issue, indent=2)}"
            )
        
        if any(i['severity'] == 'CRITICAL' for i in issues):
            # PAUSE analyses
            return False
    
    return True
```

### Conflict Resolution (Scénario E)

```python
def resolve_suggestion_conflicts(suggestions):
    """
    Résout conflits entre suggestions
    Logique: Vue d'ensemble > Optimisations locales
    """
    conflicts = []
    
    # Exemple: Scale AdSet vs Pause Campaign parent
    for s1 in suggestions:
        for s2 in suggestions:
            if s1.id == s2.id:
                continue
            
            # Conflit: Scale AdSet + Pause Campaign parent
            if (s1.type == 'adset_scale' and 
                s2.type == 'campaign_pause' and
                s1.adset.campaign_id == s2.campaign_id):
                
                conflicts.append({
                    'suggestion1': s1,
                    'suggestion2': s2,
                    'type': 'scale_vs_pause_parent'
                })
    
    # Résolution
    for conflict in conflicts:
        s1 = conflict['suggestion1']  # Scale adset
        s2 = conflict['suggestion2']  # Pause campaign
        
        # Analyser vue d'ensemble
        campaign = get_campaign(s2.campaign_id)
        all_adsets = get_campaign_adsets(campaign.id)
        
        winner_adsets = [a for a in all_adsets if a.roi > 3.0]
        loser_adsets = [a for a in all_adsets if a.roi < 1.5]
        
        if len(winner_adsets) == 1 and len(loser_adsets) >= 3:
            # 1 winner, 3+ losers → Scénario spécial
            resolution = {
                'action': 'restructure_campaign',
                'steps': [
                    f"Pause {len(loser_adsets)} adsets sous-performants",
                    f"Garder winner AdSet {s1.adset.name}",
                    f"Continuer campaign avec winner seulement",
                    f"OU créer nouvelle campaign dédiée au winner"
                ],
                'reasoning': "1 mega-winner trouvé, isoler pour scaler proprement"
            }
            
            # Créer nouvelle suggestion composite
            return create_composite_suggestion(
                type='campaign_restructure',
                action=resolution['action'],
                steps=resolution['steps'],
                confidence=min(s1.confidence, s2.confidence) - 10,  # Réduire conf car plus complexe
                reasoning=resolution['reasoning']
            )
        else:
            # Pas de winner clair → Pause campaign correct
            return s2  # Garder suggestion pause campaign
```

---

## 📱 COMMUNICATION & NOTIFICATIONS

### Style & Ton

**Ton**: Décontracté mais smart + Direct data-driven

**Exemples**:

**❌ Mauvais** (trop corporate):
```
"Notre algorithme a détecté une opportunité d'optimisation 
budgétaire sur l'ensemble publicitaire STACK_H:25/45 en 
fonction des métriques de performance observées."
```

**✅ Bon** (votre style):
```
"💡 Opportunité Scale - STACK_H:25/45

ROI: 4.2x (top 15%)
CPB: $95 (-21% vs benchmark)
Volume: 18 bookings/sem (stable 3 sem)

→ Scale +50% ($150 → $225/jour)

Confiance: 92%
[Approuver] [Backlog] [Refuser]"
```

### Fréquence Notifications

```python
NOTIFICATION_SETTINGS = {
    # Max par jour
    'max_suggestions_per_day': 20,
    'max_priority_high': 10,
    'max_priority_medium': 15,
    
    # Grouping
    'group_by_hour': True,  # Grouper par heure
    'digest_time': '09:00',  # Digest quotidien 9h
    
    # Fenêtre horaire
    'notification_window_start': '09:00',
    'notification_window_end': '14:00',
    'after_hours_action': 'backlog',  # Après 14h → backlog lendemain
    
    # AI Credits optimization
    'batch_analysis': True,  # Analyser en batch vs real-time
    'analysis_frequency': 'daily',  # 1x/jour vs hourly
    'use_cache_aggressively': True,  # Cache résultats 24h
}
```

**Scénario 10h00 AM (en meeting)**:
- Suggestion arrive
- Va dans backlog Slack (thread)
- Vous regardez plus tard
- Système ne spam pas

### Format Notifications

**Morning Digest (9h AM)**:
```
🌅 Daily Digest - 31 Jan 2025

📊 Hier Performance:
• Spend: $4,250 (6 clients)
• Leads: 47 (-8% vs avg)
• Bookings: 12 (+15% 🔥)
• Sales: 3 (ROI: 3.8x)

💡 Suggestions Prioritaires (3):
1. [HIGH] Scale AdSet Avego STACK_H:25/45
2. [HIGH] Refresh Hooks Campagne Client2
3. [MED] Test nouveau angle Client3

📋 En Attente Validation (2):
• Client Avego: 1 ad (24h)
• Vous: 1 suggestion (backlog hier)

[Voir Détails] [Dashboard]
```

**Suggestion Individual (Temps réel)**:
```
💡 Suggestion #4521 - Scale Opportunity

Client: Avego
AdSet: STACK_H:25/45 _QC _FEED+

📊 Performance (7 jours):
ROI: 4.2x (vs 2.8x benchmark) ✅
CPB: $95 (vs $120 benchmark) ✅
Volume: 18 bookings/sem (stable) ✅

🎯 Action Proposée:
Scale budget +50%
$150/jour → $225/jour

💰 Impact Attendu:
+~9 leads/semaine
CPB maintenu <$105
ROI attendu: 3.6-4.0x

📈 Raisons:
1. Top 15% performers (benchmark)
2. Stable 3 semaines (pas fluke)
3. Capacité vendeurs OK (vérifié)

Confiance: 92%

[✅ Approuver] [⏸️ Backlog] [❌ Refuser]
```

---

## 🕐 PARCOURS JOURNÉE TYPE

### 9:00 AM - Démarrage Système

```
Système démarre automatiquement:
1. Pull dernières données (LOG_MASTER, SPEND_MASTER, Meta API)
2. Valide qualité données (duplicates, freshness)
3. Calcule benchmarks (si pas à jour)
4. Analyse performance veille/semaine/mois
```

### 9:15 AM - Analyse Complétée

**Slack #durum-daily-digest**:
```
🌅 Daily Digest Ready

📊 Hier (30 Jan):
[Graphique performance]
Spend: $4,250
ROI: 3.8x (↑ vs 3.5x avg)
Leads: 47 (↓ 8%)
Bookings: 12 (↑ 15%)

💡 3 Suggestions Prioritaires
📋 2 Items En Attente

[Voir Rapport Complet]
```

**Fichier Google Drive automatique**:
```
/DURUM/Reports/Daily/2025-01-31_Daily_Report.pdf

Contient:
- Performance tous clients
- Suggestions générées
- Alertes & anomalies
- Données détaillées
```

### 9:20 AM - Vous Ouvrez Notification

**Dans Slack, vous voyez**:
```
Thread avec 3 suggestions:

💡 #1 [HIGH] Scale AdSet Avego
[Preview complet avec data]
[Boutons action]

💡 #2 [HIGH] Refresh Hooks Client2
[Preview complet avec data]
[Boutons action]

💡 #3 [MED] Test Angle Client3
[Preview complet avec data]
[Boutons action]
```

### 9:25 AM - Vous Approuvez Suggestion #1

**Vous cliquez "✅ Approuver"**:

1. Message Slack update:
```
💡 #1 [APPROVED] Scale AdSet Avego
✅ Approuvé par Alex - 09:25
🔄 Exécution en cours...
```

2. Airtable update:
```
Table: suggestions
Record #4521:
  status: "Approved" → "Executing"
  approved_by: "Alex"
  approved_at: "2025-01-31 09:25:00"
```

3. Action Meta API:
```
Scale AdSet ID: 23849384938
Budget: $150 → $225
Status: ACTIVE
```

### 9:30 AM - Action Exécutée

**Slack confirmation**:
```
✅ Suggestion #4521 - Exécutée

AdSet Avego STACK_H:25/45
Budget scaled: $150 → $225/jour

🔍 Monitoring actif:
• Check 24h: Performance stable?
• Alert si CPA >+25%
• Rapport 48h

[Voir Meta] [Dashboard]
```

**Airtable update**:
```
Table: suggestions
Record #4521:
  status: "Executing" → "Executed"
  executed_at: "2025-01-31 09:30:15"
  meta_change_id: "act_123..."
  
Table: hypothesis_tracking (NEW):
  hypothesis: "Scale +50% → +9 leads/sem, CPB <$105, ROI 3.6-4.0x"
  measurement_start: "2025-01-31"
  measurement_end: "2025-02-07" (7 jours)
```

### 10:00 AM - Nouvelle Suggestion (Vous en Meeting)

**Système détecte**: Besoin refresh hooks Client2

**Action système**:
```
1. Génère suggestion #4522
2. Calcule confiance: 91%
3. Valide (confiance >90%, 3 raisons data-driven)
4. Envoie Slack #durum-suggestions
5. Ajoute table suggestions (status: "Pending")
```

**Vous**: En meeting, pas de problème
- Notification reste dans Slack
- Vous verrez plus tard
- Pas de spam/urgence

### 5:00 PM - Fin Journée

**Dashboard Looker Studio**:
```
DURUM - Sales & Pipeline Dashboard

📊 Aujourd'hui:
Calls: 12
Sales: 3 (25% close rate)
Revenue: $14,970
Pipeline: $87,400

👥 Reps Performance:
[Graphique par rep]
Rep 1: 2 sales (30% close)
Rep 2: 1 sale (20% close)
Rep 3: 0 sales (0% - besoin training?)

📋 Pipeline État:
Applications: 47
Booked: 12
Showed: 9
Closed: 3

🚨 Alertes:
• Rep 3: 0% close rate (5 calls) → Training?
• Objection "prix" 60% calls → Script update?

[Suggestions IA] [Détails]
```

**Slack Summary #durum-daily-summary** (Auto 17h):
```
🌆 End of Day Summary

Aujourd'hui vous avez:
✅ Approuvé 1 suggestion (scale)
⏸️ Backlog 2 suggestions
📊 3 nouvelles suggestions générées

Performance Ads:
$4,180 dépensé
48 leads (+2 vs hier)
ROI: 3.9x (↑)

Sales:
3 closes ($14,970)
Pipeline: $87,400

À Demain! 🚀
```

---

## 🗂️ TABLES AIRTABLE - STRUCTURE FINALE

### Tables Critiques Phase 1

**1. clients** (Existante - À enrichir)
```
AJOUTER colonnes:
- industry
- main_offer
- ticket_price
- target_audience (JSON)
- slack_validation_channel
- slack_channel_id
- roi_target_min (default: 3.0)
- monthly_budget_max
```

**2. suggestions** (NOUVELLE)
```
suggestion_id, client_key, type, priority,
action_proposed, reason, hypothesis, confidence_score,
data_supporting (JSON), current_metrics (JSON),
expected_impact (JSON),
status, decided_by, decided_at,
executed_at, execution_status,
created_at, expires_at
```

**3. decisions** (NOUVELLE)
```
decision_id, suggestion_id, client_key,
decision (approved/refused/backlog),
decided_by, decided_at,
reason_approved, reason_refused,
modifications
```

**4. hypothesis_tracking** (NOUVELLE - Simplified Phase 1)
```
hypothesis_id, suggestion_id, client_key,
hypothesis_text, predicted_metrics (JSON),
executed_at, measurement_end_date,
actual_metrics (JSON), outcome,
variance (JSON)
```

**5. client_knowledge** (NOUVELLE)
```
client_key, industry, products (JSON),
target_audience (JSON), funnel_type,
winning_patterns (JSON), tested_angles (JSON),
preferences (JSON), updated_at
```

### Tables Phase 2

- global_learnings
- validation_logs
- decision_patterns
- feedback_loops
- etc.

---

## ⚡ OPTIMISATION AI CREDITS

**Votre contrainte**: "Le moins de crédits IA possible"

### Stratégie

```python
AI_OPTIMIZATION = {
    # Batch vs Real-time
    'analysis_mode': 'batch_daily',  # 1x/jour vs hourly
    'analysis_time': '09:00',        # 9h AM
    
    # Caching agressif
    'cache_benchmarks': 24,  # Cache 24h
    'cache_patterns': 168,   # Cache 7 jours
    'cache_suggestions': 1,  # Cache 1h (suggestions changent)
    
    # Éviter appels inutiles
    'min_data_change_pct': 5,  # Re-analyze seulement si >5% changement
    'skip_weekends': False,     # Analyser weekends? (à décider)
    
    # Utiliser models plus légers quand possible
    'simple_tasks_model': 'haiku',    # Haiku pour tasks simples
    'complex_tasks_model': 'sonnet',  # Sonnet pour analyse complexe
}

# Estimation crédits
# Avec batch daily + caching agressif:
# ~10-20 appels API/jour (vs 100+ si real-time)
# = ~$2-5/jour en crédits (Anthropic)
```

---

## ✅ RÉSUMÉ DÉCISIONS FINALES

### Must-Have Phase 1 (2 semaines)

1. ✅ Benchmarks dynamiques (3 niveaux: global, industry, client)
2. ✅ Publishing double validation (Client → Vous → Meta)
3. ✅ Analyse multi-niveaux (Ads → Campaigns → Sales)
4. ✅ Suggestions automatiques (10-20/jour max, confiance >90%)
5. ✅ Safeguards budget (blow-up protection critique)
6. ✅ Data quality validation (anti-corruption)
7. ✅ Slack notifications (digest 9h + real-time groupé)
8. ✅ Dashboard sales/pipeline (Looker Studio)

### Nice-to-Have Phase 2

1. ⏸️ Analyse créative avancée (fatigue, scores détaillés)
2. ⏸️ Système apprentissage complet (patterns, amélioration continue)
3. ⏸️ 3ème mode publication (Test/Draft)
4. ⏸️ Optimisations funnel (email sequences, etc.)

### Contraintes Critiques

- ❌ JAMAIS mélanger données clients dans communications
- ✅ TOUJOURS validation manuelle (pas d'actions auto sans approval)
- ✅ TOUJOURS 2-3 raisons data-driven par suggestion
- ✅ Confiance minimum 90%
- ✅ Budget safeguards (pause auto si overspend >50%)
- ✅ Notifications fenêtre 9h-14h (après = backlog)
- ✅ Max 10-20 suggestions/jour
- ✅ Optimiser crédits IA (batch daily, caching)

### Import Historique

**Décision**: Import automatique Meta → Airtable
- 6-12 mois historique
- Enrichir avec performance data
- IA démarre avec contexte
- +2-3 jours dev mais worth it

---

## 🚀 PRÊT POUR SPECS TECHNIQUES

Avec ces décisions, je peux maintenant créer:

1. **Architecture Technique Détaillée**
   - Diagrammes séquence
   - Specs API complètes
   - Structure données finalisée

2. **User Stories Détaillées**
   - 10-15 scénarios complets
   - Critères acceptation
   - Tests validation

3. **Roadmap Développement**
   - Semaine par semaine
   - Milestones clairs
   - Dépendances identifiées

**Prêt pour ça?** Ou questions sur les décisions ci-dessus?
