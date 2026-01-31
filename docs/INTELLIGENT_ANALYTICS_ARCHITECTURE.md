# 🧠 SYSTÈME D'ANALYSE INTELLIGENT - Architecture Complète

## 🎯 Philosophie du Système

### Principes Fondamentaux

1. **Zéro Seuil Fixe**
   - Tout est relatif aux benchmarks
   - Comparaison multi-niveaux
   - Adaptation continue

2. **Analyse Bottom-Up**
   ```
   ROI (top métrique)
     ↓ Si problème, analyser:
   Closing Rate
     ↓ Si problème, analyser:
   Booking Rate
     ↓ Si problème, analyser:
   CPB
     ↓ Si problème, analyser:
   Application Rate
     ↓ Si problème, analyser:
   CPApp
     ↓ Si problème, analyser:
   Click Rate
     ↓ Si problème, analyser:
   CTR / Relevance / Creative
   ```

3. **Benchmarks Multi-Niveaux**
   - Niveau 1: Historique propre du compte
   - Niveau 2: Moyenne de tous les comptes
   - Niveau 3: Moyenne par industrie
   - Niveau 4: Moyenne par type d'offre
   - Niveau 5: Moyenne par GEO
   - Niveau 6: Percentiles (top 10%, 25%, 50%)

4. **Contexte Complet**
   - Type de client (coaching, ecom, saas, etc.)
   - Type d'offre (high-ticket, low-ticket, subscription)
   - Maturité du compte (nouveau, établi, mature)
   - Saisonnalité
   - Cycle de vente

---

## 📁 STRUCTURE AIRTABLE COMPLÈTE

### BASE: Growth OS Master

#### Table 1: **Clients** (Existante - À Enrichir)

| Champ | Type | Description | Nouveau? |
|-------|------|-------------|----------|
| client_key | Text (Primary) | Identifiant unique | ✅ Existe |
| client_name | Text | Nom affichable | ✅ Existe |
| **industry** | Single Select | coaching, ecom, saas, info, agency, local | 🆕 AJOUTER |
| **offer_type** | Single Select | high-ticket, low-ticket, subscription, one-time | 🆕 AJOUTER |
| **ticket_price** | Number | Prix moyen de l'offre | 🆕 AJOUTER |
| **sales_cycle_days** | Number | Durée moyenne du cycle de vente | 🆕 AJOUTER |
| **target_geo** | Multiple Select | CA, US, FR, UK, etc. | 🆕 AJOUTER |
| **funnel_type** | Single Select | webinar, vsl, application, book-call | 🆕 AJOUTER |
| **maturity_stage** | Single Select | new (<3 mois), established (3-12), mature (12+) | 🆕 AJOUTER |
| meta_id | Text | ID compte Meta | ✅ Existe |
| ghl_id | Text | ID sous-compte GHL | ✅ Existe |
| slack_id | Text | Channel Slack | ✅ Existe |
| **benchmark_group** | Text | Groupement pour comparaisons | 🆕 AJOUTER |
| **active** | Checkbox | Client actif | 🆕 AJOUTER |
| **started_date** | Date | Date de début | 🆕 AJOUTER |

**benchmark_group** = Combinaison pour grouper clients similaires
- Exemple: `coaching_high-ticket_CA`
- Permet benchmarks précis

---

#### Table 2: **Campaigns** (NOUVELLE)

Structure hiérarchique complète de vos campagnes Meta.

| Champ | Type | Description |
|-------|------|-------------|
| campaign_key | Text (Primary) | {client_key}_{campaign_id} |
| client_key | Link to Clients | Client propriétaire |
| campaign_id | Text | ID Meta campaign |
| campaign_name | Text | Nom (format Growth OS) |
| **offer** | Text | Ex: BOOTCAMP, COACHING |
| **funnel_stage** | Single Select | TOF, MOF, BOF |
| **objective** | Single Select | CONV.LEADS, CONV.PURCHASE, TRAFFIC |
| **phase** | Single Select | TEST, SCALE, WINNING |
| status | Single Select | active, paused, completed |
| budget_daily | Number | Budget quotidien |
| **created_date** | Date | Date création |
| **last_active_date** | Date | Dernière activité |
| **lifetime_spend** | Number | Spend total |
| **lifetime_results** | Number | Résultats totaux |
| **notes** | Long Text | Notes internes |

---

#### Table 3: **AdSets** (NOUVELLE)

| Champ | Type | Description |
|-------|------|-------------|
| adset_key | Text (Primary) | {campaign_key}_{adset_id} |
| campaign_key | Link to Campaigns | Campaign parent |
| client_key | Link to Clients | Client (via campaign) |
| adset_id | Text | ID Meta adset |
| adset_name | Text | Nom (format Growth OS) |
| **stack** | Text | Ex: STACK_H:25/65+ |
| **audience_key** | Text | Clé de l'audience |
| **geo** | Multiple Select | CA-QC, US-CA, etc. |
| **placement** | Single Select | FB, IG, ALL, ADVANTAGE+ |
| **targeting_type** | Single Select | broad, interest, lookalike, retargeting |
| **age_min** | Number | Âge minimum |
| **age_max** | Number | Âge maximum |
| **gender** | Single Select | all, male, female |
| budget_daily | Number | Budget quotidien |
| status | Single Select | active, paused |
| **created_date** | Date | Date création |
| **last_active_date** | Date | Dernière activité |

---

#### Table 4: **Ads** (NOUVELLE)

| Champ | Type | Description |
|-------|------|-------------|
| ad_key | Text (Primary) | {adset_key}_{ad_id} |
| adset_key | Link to AdSets | AdSet parent |
| campaign_key | Link to Campaigns | Campaign (via adset) |
| client_key | Link to Clients | Client |
| ad_id | Text | ID Meta ad |
| ad_name | Text | Nom (format Growth OS) |
| **ads_tier** | Text | Ex: T1, T2, T3, T4 |
| **creative_type** | Single Select | video, image, carousel, collection |
| **hook_id** | Link to Hooks | Crochet utilisé |
| **body_id** | Link to Bodies | Corps de texte |
| **cta_id** | Link to CTAs | Call-to-action |
| **asset_id** | Link to Assets | Asset visuel/vidéo |
| status | Single Select | active, paused |
| **created_date** | Date | Date création |
| **last_active_date** | Date | Dernière activité |
| **performance_score** | Number | Score calculé (0-100) |

---

#### Table 5: **Assets** (NOUVELLE - Créatives)

Stockage de tous vos assets créatifs.

| Champ | Type | Description |
|-------|------|-------------|
| asset_id | Text (Primary) | Identifiant unique |
| asset_name | Text | Nom descriptif |
| **asset_type** | Single Select | video, image, carousel |
| **format** | Single Select | square, vertical, horizontal |
| **duration_sec** | Number | Durée (si vidéo) |
| **url** | URL | Lien vers asset |
| **thumbnail_url** | URL | Miniature |
| client_key | Link to Clients | Client propriétaire |
| **tags** | Multiple Select | testimonial, demo, lifestyle, etc. |
| **created_date** | Date | Date création |
| **performance_avg_ctr** | Number | CTR moyen historique |
| **performance_avg_cpc** | Number | CPC moyen historique |
| **times_used** | Number | Nombre d'utilisations |
| **status** | Single Select | active, archived, testing |

---

#### Table 6: **Hooks** (NOUVELLE)

Bibliothèque de tous vos hooks (accroches).

| Champ | Type | Description |
|-------|------|-------------|
| hook_id | Text (Primary) | Ex: H1, H2, H3 |
| hook_text | Long Text | Texte du hook |
| **hook_type** | Single Select | question, statement, statistic, story |
| **emotion** | Single Select | curiosity, fear, desire, urgency |
| client_key | Link to Clients | Client |
| **language** | Single Select | FR, EN |
| **created_date** | Date | Date création |
| **times_used** | Number | Utilisations |
| **avg_ctr** | Number | CTR moyen |
| **status** | Single Select | active, testing, archived |

---

#### Table 7: **Bodies** (NOUVELLE)

Corps de texte des annonces.

| Champ | Type | Description |
|-------|------|-------------|
| body_id | Text (Primary) | Ex: B1, B2, B3 |
| body_text | Long Text | Texte du corps |
| **body_length** | Single Select | short (<100), medium (100-300), long (300+) |
| **angle** | Single Select | benefit, transformation, social-proof, objection |
| client_key | Link to Clients | Client |
| **language** | Single Select | FR, EN |
| **created_date** | Date | Date création |
| **times_used** | Number | Utilisations |
| **status** | Single Select | active, testing, archived |

---

#### Table 8: **CTAs** (NOUVELLE)

Call-to-actions.

| Champ | Type | Description |
|-------|------|-------------|
| cta_id | Text (Primary) | Ex: CTA1, CTA2 |
| cta_text | Text | Texte du CTA |
| **cta_type** | Single Select | learn-more, sign-up, apply, book-call |
| **urgency_level** | Single Select | low, medium, high |
| client_key | Link to Clients | Client |
| **created_date** | Date | Date création |
| **times_used** | Number | Utilisations |
| **avg_conversion_rate** | Number | Taux conversion moyen |
| **status** | Single Select | active, testing, archived |

---

#### Table 9: **Funnels** (NOUVELLE)

Structure complète de vos funnels.

| Champ | Type | Description |
|-------|------|-------------|
| funnel_key | Text (Primary) | Identifiant unique |
| funnel_name | Text | Nom du funnel |
| client_key | Link to Clients | Client propriétaire |
| **funnel_type** | Single Select | webinar, vsl, application, book-call, ecom |
| **steps** | Multiple Select | ad, landing, thank-you, email1, email2, call, close |
| **landing_page_url** | URL | URL page d'atterrissage |
| **thank_you_page_url** | URL | URL page de remerciement |
| **ghl_form_id** | Text | ID du formulaire GHL |
| **ghl_workflow_id** | Text | ID du workflow GHL |
| **email_sequence_ids** | Long Text | IDs emails (JSON array) |
| **created_date** | Date | Date création |
| **status** | Single Select | active, paused, archived |

---

#### Table 10: **Email_Sequences** (NOUVELLE)

Séquences d'emails dans les funnels.

| Champ | Type | Description |
|-------|------|-------------|
| sequence_id | Text (Primary) | Identifiant unique |
| sequence_name | Text | Nom de la séquence |
| funnel_key | Link to Funnels | Funnel parent |
| client_key | Link to Clients | Client |
| **ghl_workflow_id** | Text | ID workflow GHL |
| **num_emails** | Number | Nombre d'emails |
| **emails** | Link to Emails | Emails de la séquence |
| **created_date** | Date | Date création |
| **status** | Single Select | active, paused |

---

#### Table 11: **Emails** (NOUVELLE)

Détails de chaque email.

| Champ | Type | Description |
|-------|------|-------------|
| email_id | Text (Primary) | Identifiant unique |
| email_name | Text | Nom interne |
| sequence_id | Link to Email_Sequences | Séquence parent |
| client_key | Link to Clients | Client |
| **position_in_sequence** | Number | 1, 2, 3, etc. |
| **delay_days** | Number | Jours après événement déclencheur |
| **subject_line** | Text | Objet de l'email |
| **preview_text** | Text | Texte preview |
| **body_html** | Long Text | Corps HTML |
| **ghl_email_id** | Text | ID email dans GHL |
| **created_date** | Date | Date création |
| **avg_open_rate** | Number | Taux ouverture moyen |
| **avg_click_rate** | Number | Taux clic moyen |
| **status** | Single Select | active, testing, archived |

---

#### Table 12: **SMS_Sequences** (NOUVELLE)

Séquences SMS.

| Champ | Type | Description |
|-------|------|-------------|
| sms_sequence_id | Text (Primary) | Identifiant unique |
| sequence_name | Text | Nom |
| funnel_key | Link to Funnels | Funnel parent |
| client_key | Link to Clients | Client |
| **ghl_workflow_id** | Text | ID workflow GHL |
| **num_sms** | Number | Nombre de SMS |
| **created_date** | Date | Date création |
| **status** | Single Select | active, paused |

---

#### Table 13: **SMS_Messages** (NOUVELLE)

Détails de chaque SMS.

| Champ | Type | Description |
|-------|------|-------------|
| sms_id | Text (Primary) | Identifiant unique |
| sms_name | Text | Nom interne |
| sms_sequence_id | Link to SMS_Sequences | Séquence parent |
| client_key | Link to Clients | Client |
| **position_in_sequence** | Number | 1, 2, 3 |
| **delay_minutes** | Number | Minutes après événement |
| **message_text** | Long Text | Texte du SMS |
| **ghl_sms_id** | Text | ID SMS dans GHL |
| **avg_response_rate** | Number | Taux de réponse |
| **status** | Single Select | active, testing |

---

#### Table 14: **Benchmarks** (NOUVELLE - CRITIQUE)

Stocke tous les benchmarks calculés.

| Champ | Type | Description |
|-------|------|-------------|
| benchmark_id | Text (Primary) | Identifiant unique |
| **benchmark_type** | Single Select | global, industry, offer_type, geo, client_history |
| **metric_name** | Text | Ex: cpa, roi_vendu, close_rate |
| **segment** | Text | Ex: coaching, high-ticket, CA |
| **period** | Single Select | 7d, 30d, 90d, all-time |
| **percentile_10** | Number | 10e percentile (top performers) |
| **percentile_25** | Number | 25e percentile |
| **percentile_50** | Number | Médiane |
| **percentile_75** | Number | 75e percentile |
| **percentile_90** | Number | 90e percentile (underperformers) |
| **mean** | Number | Moyenne |
| **std_dev** | Number | Écart-type |
| **sample_size** | Number | Nombre de comptes dans le calcul |
| **calculated_at** | DateTime | Dernière mise à jour |

**Exemples de benchmarks stockés**:
```
benchmark_type: industry
metric_name: cpa
segment: coaching
period: 30d
percentile_50: 145.00  # Médiane CPA pour coaching
mean: 167.00
sample_size: 23  # 23 comptes coaching

benchmark_type: offer_type
metric_name: roi_vendu
segment: high-ticket
period: 30d
percentile_50: 2.8  # Médiane ROI pour high-ticket
```

---

#### Table 15: **Performance_Snapshots** (NOUVELLE)

Snapshots quotidiens de performance pour analyse historique.

| Champ | Type | Description |
|-------|------|-------------|
| snapshot_id | Text (Primary) | {client_key}_{date} |
| client_key | Link to Clients | Client |
| **date** | Date | Date du snapshot |
| **period** | Single Select | daily, weekly, monthly |
| ad_spend | Number | Dépense |
| impressions | Number | Impressions |
| clicks | Number | Clics |
| ctr | Number | CTR |
| cpc | Number | CPC |
| leads | Number | Leads |
| cpl | Number | CPL |
| applications | Number | Applications |
| cpapp | Number | CPApp |
| bookings | Number | Bookings |
| cpb | Number | CPB |
| sales | Number | Ventes |
| cpa | Number | CPA |
| amount_sold | Number | Revenus |
| roi_vendu | Number | ROI |
| **percentile_vs_global** | Number | Position vs tous (0-100) |
| **percentile_vs_industry** | Number | Position vs industrie |
| **z_score** | Number | Écart vs moyenne (σ) |

---

## 📊 GOOGLE SHEETS - Structure Complète

### Sheet 1: LOG_MASTER (Existant - À Enrichir)

Ajouter ces colonnes:

| Colonne | Description | Nouveau? |
|---------|-------------|----------|
| **funnel_key** | Lien vers funnel Airtable | 🆕 |
| **step_in_funnel** | ad, landing, email1, call, close | 🆕 |
| **email_id** | Si événement lié à email | 🆕 |
| **sms_id** | Si événement lié à SMS | 🆕 |
| **page_url** | URL de la page | 🆕 |
| **referrer** | Referrer | 🆕 |
| **device_type** | mobile, desktop, tablet | 🆕 |
| **browser** | Chrome, Safari, etc. | 🆕 |
| **ip_address** | IP (hashé pour privacy) | 🆕 |

---

### Sheet 2: SPEND_MASTER (Existant - À Enrichir)

Ajouter ces colonnes:

| Colonne | Description | Nouveau? |
|---------|-------------|----------|
| **relevance_score** | Score de pertinence Meta (1-10) | 🆕 |
| **quality_ranking** | Classement qualité (above_average, average, below_average) | 🆕 |
| **engagement_rate_ranking** | Classement engagement | 🆕 |
| **conversion_rate_ranking** | Classement conversion | 🆕 |
| **video_avg_watch_time** | Temps visionnage moyen (si vidéo) | 🆕 |
| **video_p25_watched** | % ayant vu 25% | 🆕 |
| **video_p50_watched** | % ayant vu 50% | 🆕 |
| **video_p75_watched** | % ayant vu 75% | 🆕 |
| **video_p100_watched** | % ayant vu 100% | 🆕 |
| **outbound_clicks** | Clics sortants (vers landing) | 🆕 |
| **landing_page_views** | Vues page atterrissage | 🆕 |
| **cost_per_outbound_click** | Coût par clic sortant | 🆕 |

---

### Sheet 3: EMAIL_PERFORMANCE (NOUVELLE)

Performance des emails (data de GHL API).

| Colonne | Description |
|---------|-------------|
| date | Date |
| client_key | Client |
| email_id | ID email Airtable |
| sequence_id | ID séquence |
| funnel_key | Funnel |
| sent_count | Emails envoyés |
| delivered_count | Emails délivrés |
| bounced_count | Bounces |
| opened_count | Ouvertures |
| clicked_count | Clics |
| open_rate | Taux ouverture |
| click_rate | Taux clic |
| click_to_open_rate | CTOR |
| unsubscribed_count | Désabonnements |
| complained_count | Plaintes |

---

### Sheet 4: SMS_PERFORMANCE (NOUVELLE)

Performance des SMS.

| Colonne | Description |
|---------|-------------|
| date | Date |
| client_key | Client |
| sms_id | ID SMS Airtable |
| sequence_id | ID séquence |
| funnel_key | Funnel |
| sent_count | SMS envoyés |
| delivered_count | Délivrés |
| failed_count | Échecs |
| responded_count | Réponses |
| response_rate | Taux réponse |
| opt_out_count | Opt-outs |

---

### Sheet 5: FUNNEL_ANALYTICS (NOUVELLE)

Analyse du parcours complet dans le funnel.

| Colonne | Description |
|---------|-------------|
| date | Date |
| client_key | Client |
| funnel_key | Funnel |
| **ad_impressions** | Impressions |
| **ad_clicks** | Clics sur ad |
| **landing_page_views** | Vues landing page |
| **form_starts** | Débuts formulaire |
| **form_completions** | Formulaires complétés |
| **thank_you_page_views** | Vues page remerciement |
| **email1_sent** | Email 1 envoyé |
| **email1_opened** | Email 1 ouvert |
| **booking_page_views** | Vues page booking |
| **bookings_scheduled** | RDV pris |
| **calls_attended** | Appels tenus |
| **sales_closed** | Ventes closes |
| **conversion_ad_to_landing** | % |
| **conversion_landing_to_lead** | % |
| **conversion_lead_to_booking** | % |
| **conversion_booking_to_sale** | % |
| **overall_conversion_rate** | % global |

---

### Sheet 6: CREATIVE_PERFORMANCE (NOUVELLE)

Performance granulaire par composant créatif.

| Colonne | Description |
|---------|-------------|
| date | Date |
| client_key | Client |
| ad_id | ID ad |
| hook_id | Hook utilisé |
| body_id | Body utilisé |
| cta_id | CTA utilisé |
| asset_id | Asset utilisé |
| spend | Spend |
| impressions | Impressions |
| clicks | Clics |
| ctr | CTR |
| cpc | CPC |
| leads | Leads |
| cpl | CPL |
| **hook_ctr** | CTR attribué au hook |
| **body_engagement** | Engagement attribué au body |
| **cta_conversion_rate** | CR attribué au CTA |
| **asset_view_through_rate** | VTR de l'asset |

---

### Sheet 7: BENCHMARK_CALCULATIONS (NOUVELLE)

Résultats des calculs de benchmarks (mis à jour quotidiennement).

| Colonne | Description |
|---------|-------------|
| calculated_date | Date calcul |
| benchmark_type | global, industry, etc. |
| metric_name | Métrique |
| segment | Segment |
| period | Période |
| p10 | 10e percentile |
| p25 | 25e percentile |
| p50 | Médiane |
| p75 | 75e percentile |
| p90 | 90e percentile |
| mean | Moyenne |
| std_dev | Écart-type |
| sample_size | Taille échantillon |

---

## 🔌 GHL API - Données à Pull

### Endpoints Nécessaires

#### 1. **Contacts API**
```
GET /contacts/{contactId}
```
**Data needed**:
- Contact custom fields
- Tags
- Attribution source
- Lifecycle stage
- Score

#### 2. **Workflows API**
```
GET /workflows/{workflowId}
GET /workflows/{workflowId}/contacts
```
**Data needed**:
- Workflow structure
- Steps in workflow
- Contacts in workflow
- Position de chaque contact

#### 3. **Email Stats API**
```
GET /emails/{emailId}/stats
```
**Data needed**:
- Sent count
- Delivered count
- Opened count
- Clicked count
- Bounced count
- Unsubscribed count

#### 4. **SMS Stats API**
```
GET /conversations/{conversationId}/messages
```
**Data needed**:
- SMS sent
- SMS delivered
- SMS responses
- Opt-outs

#### 5. **Forms API**
```
GET /forms/{formId}/submissions
```
**Data needed**:
- Form submissions
- Completion rate
- Abandonment at which field
- Time to complete

#### 6. **Calendars API**
```
GET /calendars/{calendarId}/appointments
```
**Data needed**:
- Bookings scheduled
- Bookings attended
- No-shows
- Cancellations
- Reschedules

#### 7. **Opportunities (Pipelines) API**
```
GET /opportunities
```
**Data needed**:
- Pipeline stages
- Stage changes
- Time in each stage
- Deal values
- Assigned user

---

## 🧠 LOGIQUE D'ANALYSE INTELLIGENTE

### Étape 1: Construire le Contexte

Pour chaque client analysé:

```python
context = {
    "client": {
        "key": "avego",
        "industry": "coaching",
        "offer_type": "high-ticket",
        "ticket_price": 5000,
        "maturity": "established",  # 6 mois actif
        "benchmark_group": "coaching_high-ticket_CA"
    },
    
    "historical_performance": {
        "last_7d": {...},
        "last_30d": {...},
        "last_90d": {...},
        "best_7d_ever": {...},  # Meilleure semaine historique
        "avg_when_profitable": {...}  # Moyenne quand ROI > 2x
    },
    
    "benchmarks": {
        "global_all_clients": {
            "cpa": {"p10": 80, "p50": 150, "p90": 300},
            "roi": {"p10": 1.2, "p50": 2.5, "p90": 5.0}
        },
        "industry_coaching": {
            "cpa": {"p10": 120, "p50": 200, "p90": 400},
            ...
        },
        "offer_high_ticket": {
            ...
        },
        "exact_segment_coaching_high_ticket": {
            # Le plus précis si assez de données
            ...
        }
    },
    
    "current_period": {
        "spend": 1234,
        "leads": 45,
        "sales": 2,
        "roi": 2.1,
        ...
    }
}
```

### Étape 2: Analyser par Niveaux (Bottom-Up)

```python
def analyze_account(context):
    """
    Analyse intelligente multi-niveaux
    """
    
    # Niveau 1: ROI (Top Metric)
    roi_analysis = analyze_roi(context)
    
    if roi_analysis["status"] == "problem":
        # Descendre au niveau suivant
        
        # Niveau 2: Closing (Est-ce que les bookings closent?)
        closing_analysis = analyze_closing_rate(context)
        
        if closing_analysis["status"] == "problem":
            # Problème = closing
            return {
                "bottleneck": "closing_process",
                "recommendations": [
                    "Analyser qualité des leads bookés",
                    "Former les closers",
                    "Revoir script de vente"
                ]
            }
        
        # Niveau 3: Booking Rate (Est-ce qu'on book assez?)
        booking_analysis = analyze_booking_rate(context)
        
        if booking_analysis["status"] == "problem":
            # Problème = booking
            return {
                "bottleneck": "booking_conversion",
                "recommendations": analyze_booking_funnel(context)
            }
        
        # Niveau 4: CPB (Le coût pour booker est-il élevé?)
        cpb_analysis = analyze_cpb(context)
        
        if cpb_analysis["status"] == "problem":
            # Descendre encore
            
            # Niveau 5: Application Rate
            app_rate_analysis = analyze_application_rate(context)
            
            if app_rate_analysis["status"] == "problem":
                # Problème = application
                return analyze_application_funnel(context)
            
            # Niveau 6: CPApp
            cpapp_analysis = analyze_cpapp(context)
            
            if cpapp_analysis["status"] == "problem":
                # Descendre au niveau créatif
                
                # Niveau 7: CTR & Relevance
                creative_analysis = analyze_creative_performance(context)
                
                return creative_analysis
```

### Étape 3: Comparaisons Multi-Niveaux

```python
def analyze_roi(context):
    """
    Analyse ROI avec benchmarks dynamiques
    """
    current_roi = context["current_period"]["roi"]
    
    # Niveau 1: Vs historique propre
    historical_best = context["historical_performance"]["best_7d_ever"]["roi"]
    historical_avg_profitable = context["historical_performance"]["avg_when_profitable"]["roi"]
    
    if current_roi < historical_avg_profitable * 0.7:  # 30% sous la moyenne profitable
        severity = "high"
    
    # Niveau 2: Vs benchmarks industrie
    industry_p50 = context["benchmarks"]["industry_coaching"]["roi"]["p50"]
    industry_p25 = context["benchmarks"]["industry_coaching"]["roi"]["p25"]
    
    if current_roi < industry_p25:
        # Pire que 75% des comptes similaires
        severity = "critical"
    
    # Niveau 3: Tendance (est-ce que ça empire?)
    last_7d = context["historical_performance"]["last_7d"]["roi"]
    last_30d = context["historical_performance"]["last_30d"]["roi"]
    
    trend = "declining" if current_roi < last_7d < last_30d else "stable"
    
    # Niveau 4: Contexte maturité
    if context["client"]["maturity"] == "new":
        # Plus de tolérance pour nouveau compte
        acceptable_roi = 1.5
    else:
        acceptable_roi = 2.0
    
    return {
        "status": "problem" if current_roi < acceptable_roi else "good",
        "severity": severity,
        "current": current_roi,
        "vs_own_best": f"{(current_roi / historical_best * 100):.0f}%",
        "vs_industry_median": f"{(current_roi / industry_p50 * 100):.0f}%",
        "percentile_position": calculate_percentile(current_roi, benchmarks),
        "trend": trend,
        "recommendation": generate_roi_recommendation(...)
    }
```

---

## 📈 ÉVÉNEMENTS NÉCESSAIRES (Webhooks + API Pulls)

### Webhooks GHL (Temps Réel)

1. **Form Submission** → LOG_MASTER
2. **Appointment Scheduled** → LOG_MASTER
3. **Appointment Attended** → LOG_MASTER
4. **Appointment No-Show** → LOG_MASTER
5. **Appointment Cancelled** → LOG_MASTER
6. **Opportunity Stage Change** → LOG_MASTER
7. **Payment Received** → LOG_MASTER
8. **Contact Tag Added** → LOG_MASTER

### API Pulls Quotidiens

1. **Email Stats** → EMAIL_PERFORMANCE sheet
2. **SMS Stats** → SMS_PERFORMANCE sheet
3. **Workflow Progress** → FUNNEL_ANALYTICS
4. **Form Analytics** → FUNNEL_ANALYTICS
5. **Contact Lifecycle Updates** → Enrichir LOG_MASTER

### API Pulls Hebdomadaires

1. **All Contacts Export** → Backup + ML training
2. **All Opportunities** → Sales cycle analysis
3. **Workflow Structures** → Funnel mapping

---

## 🎯 MÉTRIQUES CALCULÉES (Intelligence)

### Métriques de Base
- ROI vendu
- ROI cash
- CPA
- CPL
- CPApp
- CPB
- Close rate
- Booking rate
- Application rate
- CTR
- CPC
- Relevance score

### Métriques Avancées (Nouvelles)
- **Funnel Velocity**: Temps moyen lead → sale
- **Stage Conversion Rates**: Conversion entre chaque étape
- **Creative Fatigue Index**: Score de fatigue (0-100)
- **Audience Saturation**: % reach vs audience size
- **Email Engagement Score**: Composite open + click + response
- **SMS Response Quality**: Analyse sentiment des réponses
- **Rep Performance Index**: Score composite par rep
- **Account Health Score**: Score global (0-100)
- **Percentile Rank**: Position vs tous les comptes (0-100)
- **Z-Score**: Écart en σ vs moyenne
- **Trend Momentum**: Direction et vitesse de changement

---

Voulez-vous que je continue avec:
1. **Le code Python complet** pour cette analyse intelligente?
2. **Les requêtes SQL** pour calculer les benchmarks?
3. **L'implémentation des API GHL** pulls?

Dites-moi par où commencer! 🚀
