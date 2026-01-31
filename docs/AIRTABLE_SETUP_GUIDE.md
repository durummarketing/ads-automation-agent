# 📋 AIRTABLE - Setup Complet

## 🚀 Étapes Rapides

1. Aller à https://airtable.com
2. Se connecter (ou créer un compte)
3. Créer une nouvelle base : "DURUM AI Agent"
4. Créer 8 tables (voir plus bas)
5. Obtenir l'API Key + Base ID

---

## 📊 8 TABLES À CRÉER

### TABLE 1: `clients`

```
Colonnes:
- client_key (Text) [PRIMARY]
- client_name (Text)
- industry (Single Select) → coaching, ecom, saas, finance, health, education
- vertical (Text)
- slack_validation_channel (Text)
- slack_channel_id (Text)
- main_offer (Text)
- ticket_price (Currency)
- roi_target (Number with decimals) → default 3.0
- monthly_budget_max (Currency)
- created_at (Created Time)
- updated_at (Last modified time)
```

**Données d'exemple:**
```
client_key: avego
client_name: Avego
industry: coaching
vertical: day trading
slack_validation_channel: client-avego-validation
main_offer: Bootcamp Day Trading Pro
ticket_price: 2997
roi_target: 3.0
monthly_budget_max: 100000
```

---

### TABLE 2: `products`

```
Colonnes:
- product_id (Autonumber) [PRIMARY]
- client_key (Text) → Link to clients
- product_name (Text)
- product_type (Single Select) → coaching_program, course, software, physical_product, service
- price (Currency)
- payment_options (Text)
- status (Single Select) → active, paused, deprecated
- created_at (Created Time)
```

---

### TABLE 3: `funnels`

```
Colonnes:
- funnel_id (Autonumber) [PRIMARY]
- client_key (Text) → Link to clients
- funnel_name (Text)
- funnel_type (Single Select) → webinar, vsl, application, book-call, ecom, hybrid
- stages (Text)
- conversion_benchmarks (Long text) [JSON format]
- created_at (Created Time)
```

**Exemple conversion_benchmarks:**
```json
{
  "ad_to_landing": 15,
  "landing_to_webinar": 45,
  "webinar_to_application": 30,
  "application_to_call": 80,
  "call_to_close": 35
}
```

---

### TABLE 4: `ads_library`

```
Colonnes:
- ad_id (Autonumber) [PRIMARY]
- client_key (Text) → Link to clients
- ad_name (Text)
- angle (Single Select) → fear, desire, logic, social_proof, urgency, education
- hook (Long text)
- body (Long text)
- cta (Text)
- status (Single Select) → active, paused, archived
- performance_tier (Single Select) → winner, performer, testing, loser
- created_at (Created Time)
```

---

### TABLE 5: `suggestions`

⚠️ **IMPORTANT:** Archive automatiquement après 30 jours vers Supabase

```
Colonnes:
- suggestion_id (Autonumber) [PRIMARY]
- client_key (Text) → Link to clients
- type (Single Select) → scale, pause, refresh, test_angle, campaign_diagnostic
- priority (Single Select) → critical, high, medium, low
- action (Long text)
- reason (Long text)
- expected_impact (Long text)
- confidence (Number) → 0-100
- entity_type (Single Select) → ad, adset, campaign, funnel, sales
- entity_id (Text)
- status (Single Select) → pending, approved, refused, backlog, executed
- decided_by (Text)
- decided_at (Date)
- slack_message_ts (Text)
- created_at (Created Time)
- expires_at (Date) → created_at + 48 jours
```

---

### TABLE 6: `decisions`

⚠️ **IMPORTANT:** Archive automatiquement après 90 jours vers Supabase

```
Colonnes:
- decision_id (Autonumber) [PRIMARY]
- suggestion_id (Number) → Link to suggestions
- client_key (Formula) → Lookup from suggestion
- decision (Single Select) → approved, refused, backlog
- decided_by (Text)
- decided_at (Date)
- notes (Long text)
- created_at (Created Time)
```

---

### TABLE 7: `validation_queue`

```
Colonnes:
- queue_id (Autonumber) [PRIMARY]
- client_key (Text) → Link to clients
- item_type (Single Select) → ad_creative, campaign_change, budget_increase
- item_name (Text)
- content (Long text) [JSON format]
- validation_stage (Single Select) → client_review, team_review, approved, rejected
- status (Single Select) → pending, approved, rejected, expired
- submitted_at (Created Time)
- client_validated_at (Date)
- team_validated_at (Date)
- slack_thread_ts (Text)
```

---

### TABLE 8: `winning_patterns`

```
Colonnes:
- pattern_id (Autonumber) [PRIMARY]
- pattern_name (Text)
- pattern_type (Single Select) → hook, body, cta, funnel_step, email_sequence
- industry (Single Select) → coaching, ecom, saas, ALL
- description (Long text)
- why_works (Long text)
- times_tested (Number)
- success_rate (Percent)
- avg_ctr_lift (Percent)
- template (Long text)
- status (Single Select) → active, deprecated, testing
- created_at (Created Time)
```

---

## 🔑 OBTENIR LES CREDENTIALS

### 1. API Key

1. Aller à https://airtable.com/account/tokens
2. Cliquer **"Create new token"**
3. Donner un nom: "DURUM AI Agent"
4. Scopes requis:
   - `data.records:read` ✅
   - `data.records:write` ✅
   - `data.bases:read` ✅
5. Cliquer **"Create token"**
6. Copier le token → `AIRTABLE_API_KEY` dans `.env`

### 2. Base ID

1. Aller à ta base: https://airtable.com/workspace/...
2. Dans l'URL: `https://airtable.com/appXXXXXXXXXXXXXX/...`
3. Copier l'ID qui commence par `app` → `AIRTABLE_BASE_ID`

---

## ✅ CHECKLIST SETUP

```
[ ] Base créée: "DURUM AI Agent"
[ ] Table 1: clients
[ ] Table 2: products
[ ] Table 3: funnels
[ ] Table 4: ads_library
[ ] Table 5: suggestions
[ ] Table 6: decisions
[ ] Table 7: validation_queue
[ ] Table 8: winning_patterns
[ ] API Token créé
[ ] Base ID obtenu
[ ] .env rempli: AIRTABLE_API_KEY + AIRTABLE_BASE_ID
[ ] Test connexion OK
```

---

## 🧪 TEST CONNEXION

Une fois que tu as créé toutes les tables et obtenu les credentials:

```bash
cd ads-automation-agent

# Éditer .env
nano .env
# Remplir: AIRTABLE_API_KEY et AIRTABLE_BASE_ID

# Tester
python3 -c "
from pyairtable import Api
api = Api('YOUR_API_KEY')
bases = api.bases()
print(f'✅ Connected! {len(bases)} bases found')
"
```

---

## 💡 TIPS

### Formules Utiles

**Auto-increment suggestion_id:**
- Airtable auto-incrémente automatiquement (Autonumber)

**Calculer expires_at:**
Formule: `DATEADD({created_at}, 48, 'days')`

### Permissions

- Partager la base avec ton équipe
- Créer des vues publiques pour le monitoring
- Restreindre l'accès API par workspace

### Performance

- Limiter les lignes à ~10,000 par table (archive régulièrement)
- Utiliser les filtres pour réduire les sync
- Grouper par client_key pour des requêtes rapides

---

## 🔗 LIENS UTILES

- Airtable Dashboard: https://airtable.com
- API Docs: https://developers.airtable.com/reference
- Token Management: https://airtable.com/account/tokens
- Field Types: https://support.airtable.com/hc/en-us/articles/203622977

---

**✅ Une fois les 8 tables créées et l'API Key configurée, tu peux commencer les tests!**
