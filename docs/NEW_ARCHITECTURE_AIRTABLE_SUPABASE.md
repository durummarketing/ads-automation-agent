# 🏗️ ARCHITECTURE FINALE - Airtable + Supabase

## 🎯 NOUVELLE ARCHITECTURE VALIDÉE

**Décision**: Séparer données business (Airtable) des données système (Supabase)

**Pourquoi?**
- ✅ Performance optimale
- ✅ Coûts réduits ($20-45/mois vs $200+)
- ✅ Scalabilité infinie
- ✅ Chaque outil pour son usage optimal

---

## 📊 RÉPARTITION DONNÉES

### AIRTABLE (8 Tables) - Business Layer

**Usage**: Interface humaine, données consultées/modifiées quotidiennement

```
┌─────────────────────────────────────────────────────┐
│ AIRTABLE = Ce que VOUS voyez et manipulez          │
├─────────────────────────────────────────────────────┤
│ 1. clients             → Infos clients business    │
│ 2. products            → Catalogue produits        │
│ 3. funnels             → Structure funnels         │
│ 4. ads_library         → Bibliothèque créatives    │
│ 5. suggestions         → Suggestions actives (30j) │
│ 6. decisions           → Décisions récentes (90j)  │
│ 7. validation_queue    → Workflow validation ads   │
│ 8. winning_patterns    → Patterns confirmés        │
└─────────────────────────────────────────────────────┘

Limite lignes: ~10,000 max (reste léger et rapide)
Coût: $0-20/mois (Plan Free ou Plus)
```

### SUPABASE (12 Tables) - System Layer

**Usage**: Backend système, logs, analytics, ML

```
┌─────────────────────────────────────────────────────┐
│ SUPABASE = Ce que le SYSTÈME génère et analyse     │
├─────────────────────────────────────────────────────┤
│ ANALYTICS & PERFORMANCE                             │
│ 1. execution_logs           → Logs Meta API        │
│ 2. performance_metrics      → Métriques daily      │
│ 3. spend_history            → Dépenses tracking    │
│ 4. creative_performance     → Analyse créatives    │
│                                                     │
│ ML & LEARNING                                       │
│ 5. hypothesis_tracking      → Validation IA        │
│ 6. decision_patterns        → Patterns décisions   │
│ 7. feedback_loops           → Amélioration IA      │
│ 8. tested_angles            → Historique tests     │
│                                                     │
│ ARCHIVES                                            │
│ 9. suggestions_archive      → Suggestions 30j+     │
│ 10. decisions_archive       → Décisions 90j+       │
│                                                     │
│ SYSTEM                                              │
│ 11. system_logs             → Logs application     │
│ 12. api_calls_log           → Tracking APIs        │
└─────────────────────────────────────────────────────┘

Limite lignes: Illimité (millions OK)
Coût: $0-25/mois (Free tier généreux)
```

---

## 🔄 FLUX DE DONNÉES

### Workflow Suggestion Quotidienne

```
┌─────────────────────────────────────────────────────┐
│ 1. ANALYSE (9h AM)                                  │
└─────────────────────────────────────────────────────┘
                    ↓
    ┌───────────────────────────────────┐
    │ SUPABASE READ:                    │
    │ • performance_metrics (7 jours)   │
    │ • decision_patterns (historique)  │
    │ • hypothesis_tracking (learning)  │
    └───────────────────────────────────┘
                    ↓
    ┌───────────────────────────────────┐
    │ IA GÉNÈRE SUGGESTIONS             │
    │ • Analyse données                 │
    │ • Calcule confiance               │
    │ • Applique patterns appris        │
    └───────────────────────────────────┘
                    ↓
    ┌───────────────────────────────────┐
    │ AIRTABLE WRITE:                   │
    │ • INSERT suggestion (visible)     │
    └───────────────────────────────────┘
                    ↓
    ┌───────────────────────────────────┐
    │ SUPABASE LOG:                     │
    │ • INSERT system_logs              │
    │ • INSERT suggestion metadata      │
    └───────────────────────────────────┘
                    ↓
    ┌───────────────────────────────────┐
    │ SLACK NOTIFICATION                │
    └───────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│ 2. APPROBATION (Vous)                               │
└─────────────────────────────────────────────────────┘
                    ↓
    ┌───────────────────────────────────┐
    │ AIRTABLE UPDATE:                  │
    │ • suggestion.status = approved    │
    │ • INSERT decision                 │
    └───────────────────────────────────┘
                    ↓
    ┌───────────────────────────────────┐
    │ SUPABASE WRITE:                   │
    │ • LOG decision (full context)     │
    │ • UPDATE decision_patterns        │
    └───────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│ 3. EXÉCUTION                                        │
└─────────────────────────────────────────────────────┘
                    ↓
    ┌───────────────────────────────────┐
    │ META API CALL                     │
    │ • Scale budget / Pause ad / etc.  │
    └───────────────────────────────────┘
                    ↓
    ┌───────────────────────────────────┐
    │ SUPABASE WRITE:                   │
    │ • INSERT execution_logs (full)    │
    │ • INSERT hypothesis_tracking      │
    └───────────────────────────────────┘
                    ↓
    ┌───────────────────────────────────┐
    │ AIRTABLE UPDATE:                  │
    │ • suggestion.status = executed    │
    └───────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│ 4. MONITORING (24h)                                 │
└─────────────────────────────────────────────────────┘
                    ↓
    ┌───────────────────────────────────┐
    │ SUPABASE QUERY:                   │
    │ • performance_metrics (new data)  │
    │ • Compare vs hypothesis           │
    └───────────────────────────────────┘
                    ↓
    ┌───────────────────────────────────┐
    │ SUPABASE UPDATE:                  │
    │ • hypothesis_tracking (validated) │
    │ • feedback_loops (learning)       │
    └───────────────────────────────────┘
```

---

## 📋 SCHÉMAS DÉTAILLÉS

### AIRTABLE - 8 Tables

#### 1. clients

```javascript
{
  // Identité
  client_key: "avego",              // Primary (text)
  client_name: "Avego",             // Text
  industry: "coaching",              // Single Select
  vertical: "day trading",           // Text
  
  // Contact & Slack
  slack_validation_channel: "client-avego-validation",  // Text
  slack_channel_id: "C04ABC123XYZ",                     // Text
  
  // Business
  main_offer: "Bootcamp Day Trading Pro",  // Text
  ticket_price: 2997,                      // Currency
  roi_target: 3.0,                         // Number
  monthly_budget_max: 100000,              // Currency
  
  // Metadata
  created_at: "2025-01-15T10:00:00Z",  // Created Time
  updated_at: "2025-01-31T14:30:00Z"   // Last Modified
}
```

**Colonnes**:
- client_key (Text - Primary)
- client_name (Text)
- industry (Single Select: coaching, ecom, saas, finance, health, education)
- vertical (Text)
- slack_validation_channel (Text)
- slack_channel_id (Text)
- main_offer (Text)
- ticket_price (Currency)
- roi_target (Number - Decimal, default: 3.0)
- monthly_budget_max (Currency)
- created_at (Created Time)
- updated_at (Last Modified)

---

#### 2. products

```javascript
{
  product_id: 1,                    // Auto Number (Primary)
  client_key: "avego",              // Link to clients
  product_name: "Bootcamp Pro",     // Text
  product_type: "coaching_program", // Single Select
  price: 2997,                      // Currency
  payment_options: "1x $2997 ou 3x $999",  // Text
  status: "active",                 // Single Select
  created_at: "2025-01-15T10:00:00Z"
}
```

**Colonnes**:
- product_id (Auto Number - Primary)
- client_key (Link to clients)
- product_name (Text)
- product_type (Single Select: coaching_program, course, software, physical_product, service)
- price (Currency)
- payment_options (Text)
- status (Single Select: active, paused, deprecated)
- created_at (Created Time)

---

#### 3. funnels

```javascript
{
  funnel_id: 1,                         // Auto Number (Primary)
  client_key: "avego",                  // Link to clients
  funnel_name: "Main Webinar Funnel",   // Text
  funnel_type: "webinar",               // Single Select
  stages: "Ad → Landing → Webinar → Application → Call → Close",  // Text
  conversion_benchmarks: {              // Long Text (JSON)
    "ad_to_landing": 15,
    "landing_to_webinar": 45,
    "webinar_to_application": 30,
    "application_to_call": 80,
    "call_to_close": 35
  },
  created_at: "2025-01-15T10:00:00Z"
}
```

**Colonnes**:
- funnel_id (Auto Number - Primary)
- client_key (Link to clients)
- funnel_name (Text)
- funnel_type (Single Select: webinar, vsl, application, book-call, ecom, hybrid)
- stages (Text)
- conversion_benchmarks (Long Text - JSON format)
- created_at (Created Time)

---

#### 4. ads_library

```javascript
{
  ad_id: 1,                         // Auto Number (Primary)
  client_key: "avego",              // Link to clients
  ad_name: "Fear Hook - Market Crash",  // Text
  angle: "fear_of_missing_out",     // Single Select
  hook: "97% des traders font cette erreur...",  // Long Text
  status: "active",                 // Single Select
  performance_tier: "winner",       // Single Select
  created_at: "2025-01-20T10:00:00Z"
}
```

**Colonnes**:
- ad_id (Auto Number - Primary)
- client_key (Link to clients)
- ad_name (Text)
- angle (Single Select: fear, desire, logic, social_proof, urgency, education)
- hook (Long Text)
- body (Long Text)
- cta (Text)
- status (Single Select: active, paused, archived)
- performance_tier (Single Select: winner, performer, testing, loser)
- created_at (Created Time)

---

#### 5. suggestions

**⚠️ IMPORTANT**: Garde seulement **30 derniers jours**. Archive automatique vers Supabase après.

```javascript
{
  suggestion_id: 4521,                  // Auto Number (Primary)
  client_key: "avego",                  // Link to clients
  type: "scale",                        // Single Select
  priority: "high",                     // Single Select
  
  // Content
  action: "Scale AdSet STACK_H:25/45 +50%",  // Long Text
  reason: "ROI 4.2x (top 15%), stable 3 sem",  // Long Text
  expected_impact: "+9 leads/sem, ROI 3.6-4.0x",  // Long Text
  confidence: 92,                       // Number (0-100)
  
  // Meta
  entity_type: "adset",                 // Single Select
  entity_id: "23849384938",             // Text (Meta ID)
  
  // Status
  status: "pending",                    // Single Select
  decided_by: null,                     // Text
  decided_at: null,                     // DateTime
  
  // Slack
  slack_message_ts: "1706789123.456789",  // Text
  
  // Timestamps
  created_at: "2025-01-31T09:15:00Z",   // Created Time
  expires_at: "2025-02-02T09:15:00Z"    // DateTime (+48h)
}
```

**Colonnes**:
- suggestion_id (Auto Number - Primary)
- client_key (Link to clients)
- type (Single Select: scale, pause, refresh, test_angle, campaign_diagnostic)
- priority (Single Select: critical, high, medium, low)
- action (Long Text)
- reason (Long Text)
- expected_impact (Long Text)
- confidence (Number - Integer, 0-100)
- entity_type (Single Select: ad, adset, campaign, funnel, sales)
- entity_id (Text)
- status (Single Select: pending, approved, refused, backlog, executed)
- decided_by (Text)
- decided_at (DateTime)
- slack_message_ts (Text)
- created_at (Created Time)
- expires_at (DateTime)

---

#### 6. decisions

**⚠️ IMPORTANT**: Garde seulement **90 derniers jours**. Archive après.

```javascript
{
  decision_id: 1247,                    // Auto Number (Primary)
  suggestion_id: 4521,                  // Link to suggestions
  client_key: "avego",                  // Link to clients (via formula)
  
  decision: "approved",                 // Single Select
  decided_by: "Alex",                   // Text
  decided_at: "2025-01-31T09:25:00Z",  // DateTime
  
  notes: "Good data, scaling makes sense",  // Long Text
  
  created_at: "2025-01-31T09:25:00Z"   // Created Time
}
```

**Colonnes**:
- decision_id (Auto Number - Primary)
- suggestion_id (Link to suggestions)
- client_key (Formula - Lookup from suggestion)
- decision (Single Select: approved, refused, backlog)
- decided_by (Text)
- decided_at (DateTime)
- notes (Long Text)
- created_at (Created Time)

---

#### 7. validation_queue

```javascript
{
  queue_id: 892,                        // Auto Number (Primary)
  client_key: "avego",                  // Link to clients
  
  item_type: "ad_creative",             // Single Select
  item_name: "New Hook Test - Market Crash",  // Text
  content: {                            // Long Text (JSON)
    "hook": "Le marché va crasher...",
    "body": "Voici comment...",
    "cta": "Réserver appel"
  },
  
  validation_stage: "client_review",    // Single Select
  status: "pending",                    // Single Select
  
  submitted_at: "2025-01-31T10:00:00Z",  // Created Time
  client_validated_at: null,             // DateTime
  team_validated_at: null,               // DateTime
  
  slack_thread_ts: "1706789456.123456"   // Text
}
```

**Colonnes**:
- queue_id (Auto Number - Primary)
- client_key (Link to clients)
- item_type (Single Select: ad_creative, campaign_change, budget_increase)
- item_name (Text)
- content (Long Text - JSON)
- validation_stage (Single Select: client_review, team_review, approved, rejected)
- status (Single Select: pending, approved, rejected, expired)
- submitted_at (Created Time)
- client_validated_at (DateTime)
- team_validated_at (DateTime)
- slack_thread_ts (Text)

---

#### 8. winning_patterns

```javascript
{
  pattern_id: 42,                       // Auto Number (Primary)
  pattern_name: "Question Provocante",  // Text
  pattern_type: "hook",                 // Single Select
  industry: "coaching",                 // Single Select
  
  description: "Hook qui challenge croyance limitante",  // Long Text
  why_works: "Arrête scroll + curiosity gap",  // Long Text
  
  times_tested: 47,                     // Number
  success_rate: 73,                     // Percent
  avg_ctr_lift: 42,                     // Percent
  
  template: "[Croyance commune]? Voici pourquoi c'est faux...",  // Long Text
  status: "active",                     // Single Select
  
  created_at: "2024-08-15T10:00:00Z"
}
```

**Colonnes**:
- pattern_id (Auto Number - Primary)
- pattern_name (Text)
- pattern_type (Single Select: hook, body, cta, funnel_step, email_sequence)
- industry (Single Select: coaching, ecom, saas, ALL)
- description (Long Text)
- why_works (Long Text)
- times_tested (Number)
- success_rate (Percent)
- avg_ctr_lift (Percent)
- template (Long Text)
- status (Single Select: active, deprecated, testing)
- created_at (Created Time)

---

### SUPABASE - 12 Tables (PostgreSQL)

#### SQL Schema Complete

```sql
-- ============================================
-- 1. EXECUTION_LOGS
-- ============================================
CREATE TABLE execution_logs (
  id BIGSERIAL PRIMARY KEY,
  suggestion_id INTEGER NOT NULL,
  client_key VARCHAR(50) NOT NULL,
  
  action_type VARCHAR(50) NOT NULL,  -- scale_budget, pause_ad, etc.
  entity_type VARCHAR(20) NOT NULL,  -- ad, adset, campaign
  entity_id VARCHAR(100) NOT NULL,    -- Meta ID
  
  executed_at TIMESTAMPTZ DEFAULT NOW(),
  executed_by VARCHAR(50) DEFAULT 'system',
  
  before_state JSONB,  -- État avant action
  after_state JSONB,   -- État après action
  api_response JSONB,  -- Réponse Meta API
  
  success BOOLEAN DEFAULT TRUE,
  error_message TEXT,
  
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_execution_logs_client ON execution_logs(client_key);
CREATE INDEX idx_execution_logs_date ON execution_logs(executed_at);
CREATE INDEX idx_execution_logs_entity ON execution_logs(entity_type, entity_id);

-- ============================================
-- 2. PERFORMANCE_METRICS
-- ============================================
CREATE TABLE performance_metrics (
  id BIGSERIAL PRIMARY KEY,
  client_key VARCHAR(50) NOT NULL,
  date DATE NOT NULL,
  
  entity_type VARCHAR(20) NOT NULL,  -- ad, adset, campaign
  entity_id VARCHAR(100) NOT NULL,
  entity_name VARCHAR(255),
  
  -- Core Metrics
  spend DECIMAL(10,2) DEFAULT 0,
  impressions INTEGER DEFAULT 0,
  clicks INTEGER DEFAULT 0,
  ctr DECIMAL(5,2) DEFAULT 0,
  cpc DECIMAL(10,2) DEFAULT 0,
  
  -- Conversion Metrics
  leads INTEGER DEFAULT 0,
  cpl DECIMAL(10,2) DEFAULT 0,
  applications INTEGER DEFAULT 0,
  bookings INTEGER DEFAULT 0,
  cpb DECIMAL(10,2) DEFAULT 0,
  
  -- Sales Metrics
  sales INTEGER DEFAULT 0,
  revenue DECIMAL(10,2) DEFAULT 0,
  cpa DECIMAL(10,2) DEFAULT 0,
  roi DECIMAL(5,2) DEFAULT 0,
  
  -- Engagement
  frequency DECIMAL(5,2) DEFAULT 0,
  reach INTEGER DEFAULT 0,
  
  created_at TIMESTAMPTZ DEFAULT NOW(),
  
  UNIQUE(client_key, date, entity_type, entity_id)
);

CREATE INDEX idx_perf_client_date ON performance_metrics(client_key, date DESC);
CREATE INDEX idx_perf_entity ON performance_metrics(entity_type, entity_id);
CREATE INDEX idx_perf_roi ON performance_metrics(roi DESC);

-- ============================================
-- 3. SPEND_HISTORY
-- ============================================
CREATE TABLE spend_history (
  id BIGSERIAL PRIMARY KEY,
  client_key VARCHAR(50) NOT NULL,
  timestamp TIMESTAMPTZ DEFAULT NOW(),
  
  entity_type VARCHAR(20) NOT NULL,
  entity_id VARCHAR(100) NOT NULL,
  
  spend_total DECIMAL(10,2) DEFAULT 0,
  spend_hourly DECIMAL(10,2) DEFAULT 0,
  budget_daily DECIMAL(10,2) DEFAULT 0,
  
  overspend_detected BOOLEAN DEFAULT FALSE,
  overspend_percent DECIMAL(5,2),
  
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_spend_client_time ON spend_history(client_key, timestamp DESC);
CREATE INDEX idx_spend_overspend ON spend_history(overspend_detected) WHERE overspend_detected = TRUE;

-- ============================================
-- 4. CREATIVE_PERFORMANCE
-- ============================================
CREATE TABLE creative_performance (
  id BIGSERIAL PRIMARY KEY,
  client_key VARCHAR(50) NOT NULL,
  ad_id VARCHAR(100) NOT NULL,
  date DATE NOT NULL,
  
  -- Creative Elements
  hook TEXT,
  angle VARCHAR(50),
  asset_type VARCHAR(20),  -- image, video, carousel
  
  -- Performance
  impressions INTEGER DEFAULT 0,
  ctr DECIMAL(5,2) DEFAULT 0,
  hook_rate DECIMAL(5,2),  -- 3-sec video views / impressions
  engagement_rate DECIMAL(5,2),
  
  -- Results
  leads INTEGER DEFAULT 0,
  cpl DECIMAL(10,2),
  roi DECIMAL(5,2),
  
  -- Fatigue Detection
  days_active INTEGER DEFAULT 0,
  fatigue_index DECIMAL(5,2) DEFAULT 0,  -- 0-100
  
  created_at TIMESTAMPTZ DEFAULT NOW(),
  
  UNIQUE(client_key, ad_id, date)
);

CREATE INDEX idx_creative_client_date ON creative_performance(client_key, date DESC);
CREATE INDEX idx_creative_fatigue ON creative_performance(fatigue_index DESC);

-- ============================================
-- 5. HYPOTHESIS_TRACKING
-- ============================================
CREATE TABLE hypothesis_tracking (
  id BIGSERIAL PRIMARY KEY,
  suggestion_id INTEGER NOT NULL,
  client_key VARCHAR(50) NOT NULL,
  
  hypothesis_text TEXT NOT NULL,
  predicted_metrics JSONB NOT NULL,  -- {leads: 18, cpl: 28, roi: 3.6}
  confidence_score INTEGER NOT NULL CHECK (confidence_score >= 0 AND confidence_score <= 100),
  
  executed_at TIMESTAMPTZ,
  measurement_period_days INTEGER DEFAULT 7,
  measurement_end_date DATE,
  
  actual_metrics JSONB,  -- Résultats réels
  variance JSONB,        -- Écarts vs prédictions
  
  outcome VARCHAR(20),   -- validated, invalidated, partial, inconclusive
  why_accurate TEXT,
  why_inaccurate TEXT,
  confounding_factors TEXT,
  
  model_adjustment_needed BOOLEAN DEFAULT FALSE,
  adjustment_notes TEXT,
  applied_to_model BOOLEAN DEFAULT FALSE,
  
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_hypothesis_client ON hypothesis_tracking(client_key);
CREATE INDEX idx_hypothesis_outcome ON hypothesis_tracking(outcome);
CREATE INDEX idx_hypothesis_confidence ON hypothesis_tracking(confidence_score DESC);

-- ============================================
-- 6. DECISION_PATTERNS
-- ============================================
CREATE TABLE decision_patterns (
  id BIGSERIAL PRIMARY KEY,
  pattern_name VARCHAR(255) NOT NULL,
  pattern_type VARCHAR(50) NOT NULL,  -- approval_preference, refusal_reason, etc.
  
  description TEXT,
  detected_from_decisions INTEGER DEFAULT 0,
  confidence DECIMAL(5,2) DEFAULT 0,  -- 0-100
  significance VARCHAR(20) DEFAULT 'low',  -- high, medium, low
  
  condition TEXT,  -- "suggestion_type = 'scale' AND increase > 75%"
  typical_decision VARCHAR(20),  -- approved, refused, backlog
  typical_reason TEXT,
  
  how_ai_uses_it TEXT,
  impact_on_suggestions TEXT,
  
  first_detected DATE,
  last_validated DATE,
  status VARCHAR(20) DEFAULT 'active',
  
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_patterns_status ON decision_patterns(status) WHERE status = 'active';
CREATE INDEX idx_patterns_confidence ON decision_patterns(confidence DESC);

-- ============================================
-- 7. FEEDBACK_LOOPS
-- ============================================
CREATE TABLE feedback_loops (
  id BIGSERIAL PRIMARY KEY,
  loop_type VARCHAR(50) NOT NULL,  -- accuracy_improvement, bias_correction, etc.
  triggered_by_hypothesis_id BIGINT REFERENCES hypothesis_tracking(id),
  
  issue_description TEXT NOT NULL,
  frequency_of_issue INTEGER DEFAULT 1,
  impact_severity VARCHAR(20) DEFAULT 'low',
  
  adjustment_type VARCHAR(50),  -- algorithm_tweak, threshold_change, etc.
  adjustment_description TEXT,
  before_vs_after JSONB,
  
  test_period_start DATE,
  test_period_end DATE,
  improvement_measured DECIMAL(5,2),  -- Percentage
  
  status VARCHAR(20) DEFAULT 'testing',  -- testing, validated, rolled_back
  applied_to_production BOOLEAN DEFAULT FALSE,
  
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_feedback_status ON feedback_loops(status);
CREATE INDEX idx_feedback_severity ON feedback_loops(impact_severity);

-- ============================================
-- 8. TESTED_ANGLES
-- ============================================
CREATE TABLE tested_angles (
  id BIGSERIAL PRIMARY KEY,
  client_key VARCHAR(50) NOT NULL,
  
  angle_name VARCHAR(100) NOT NULL,
  angle_category VARCHAR(50),  -- fear, desire, logic, etc.
  angle_description TEXT,
  
  tested_date DATE NOT NULL,
  campaign_id VARCHAR(100),
  ads_count INTEGER DEFAULT 0,
  total_spend DECIMAL(10,2) DEFAULT 0,
  duration_days INTEGER DEFAULT 0,
  
  result_status VARCHAR(20),  -- success, failed, inconclusive, ongoing
  
  -- Performance
  ctr DECIMAL(5,2),
  cpa DECIMAL(10,2),
  cpl DECIMAL(10,2),
  conversion_rate DECIMAL(5,2),
  roi DECIMAL(5,2),
  leads_generated INTEGER DEFAULT 0,
  sales_generated INTEGER DEFAULT 0,
  
  -- Analysis
  why_succeeded TEXT,
  why_failed TEXT,
  key_learnings TEXT,
  would_retest BOOLEAN DEFAULT FALSE,
  
  example_hooks JSONB,
  best_performing_ad VARCHAR(100),
  
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_angles_client ON tested_angles(client_key);
CREATE INDEX idx_angles_result ON tested_angles(result_status);
CREATE INDEX idx_angles_roi ON tested_angles(roi DESC);

-- ============================================
-- 9. SUGGESTIONS_ARCHIVE
-- ============================================
CREATE TABLE suggestions_archive (
  id BIGSERIAL PRIMARY KEY,
  airtable_suggestion_id INTEGER NOT NULL,  -- Référence Airtable original
  client_key VARCHAR(50) NOT NULL,
  
  type VARCHAR(50),
  priority VARCHAR(20),
  action TEXT,
  reason TEXT,
  expected_impact TEXT,
  confidence INTEGER,
  
  entity_type VARCHAR(20),
  entity_id VARCHAR(100),
  
  status VARCHAR(20),
  decided_by VARCHAR(50),
  decided_at TIMESTAMPTZ,
  
  created_at TIMESTAMPTZ,
  archived_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_archive_sug_client ON suggestions_archive(client_key);
CREATE INDEX idx_archive_sug_created ON suggestions_archive(created_at DESC);

-- ============================================
-- 10. DECISIONS_ARCHIVE
-- ============================================
CREATE TABLE decisions_archive (
  id BIGSERIAL PRIMARY KEY,
  airtable_decision_id INTEGER NOT NULL,
  suggestion_id INTEGER NOT NULL,
  client_key VARCHAR(50) NOT NULL,
  
  decision VARCHAR(20),
  decided_by VARCHAR(50),
  decided_at TIMESTAMPTZ,
  notes TEXT,
  
  created_at TIMESTAMPTZ,
  archived_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_archive_dec_client ON decisions_archive(client_key);
CREATE INDEX idx_archive_dec_created ON decisions_archive(created_at DESC);

-- ============================================
-- 11. SYSTEM_LOGS
-- ============================================
CREATE TABLE system_logs (
  id BIGSERIAL PRIMARY KEY,
  timestamp TIMESTAMPTZ DEFAULT NOW(),
  level VARCHAR(20) NOT NULL,  -- INFO, WARNING, ERROR, CRITICAL
  module VARCHAR(100),
  
  message TEXT NOT NULL,
  context JSONB,
  
  exception_type VARCHAR(100),
  exception_message TEXT,
  stack_trace TEXT,
  
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_logs_timestamp ON system_logs(timestamp DESC);
CREATE INDEX idx_logs_level ON system_logs(level);
CREATE INDEX idx_logs_module ON system_logs(module);

-- ============================================
-- 12. API_CALLS_LOG
-- ============================================
CREATE TABLE api_calls_log (
  id BIGSERIAL PRIMARY KEY,
  timestamp TIMESTAMPTZ DEFAULT NOW(),
  
  api_name VARCHAR(50) NOT NULL,  -- meta, slack, airtable, anthropic
  endpoint VARCHAR(255),
  method VARCHAR(10),  -- GET, POST, PUT, DELETE
  
  request_payload JSONB,
  response_payload JSONB,
  status_code INTEGER,
  
  duration_ms INTEGER,
  success BOOLEAN DEFAULT TRUE,
  error_message TEXT,
  
  cost_estimate DECIMAL(10,4),  -- Coût estimé de l'appel
  
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_api_timestamp ON api_calls_log(timestamp DESC);
CREATE INDEX idx_api_name ON api_calls_log(api_name);
CREATE INDEX idx_api_success ON api_calls_log(success);
```

---

## 📦 SETUP INSTRUCTIONS

### Airtable Setup (2h)

1. Créer base Airtable "DURUM AI Agent"
2. Créer 8 tables avec colonnes exactes ci-dessus
3. Remplir table `clients` avec vos 6 clients
4. Obtenir Base ID et API Key

### Supabase Setup (30 min)

1. Créer compte sur supabase.com
2. Créer nouveau projet
3. Copier SQL schema complet ci-dessus
4. Exécuter dans SQL Editor Supabase
5. Obtenir connection string et API keys

---

## 🔄 SYNC AUTOMATIQUE

### Archive Scheduler (Daily Cron)

```python
# Chaque nuit à 2h AM
async def archive_old_data():
    """Archive suggestions et decisions anciennes vers Supabase"""
    
    # 1. Archive suggestions >30 jours
    old_suggestions = airtable.get_suggestions(
        filter="created_at < '30 days ago'"
    )
    
    for suggestion in old_suggestions:
        # Insert to Supabase
        supabase.table('suggestions_archive').insert({
            'airtable_suggestion_id': suggestion['id'],
            'client_key': suggestion['client_key'],
            'type': suggestion['type'],
            # ... all fields
        }).execute()
        
        # Delete from Airtable
        airtable.delete_suggestion(suggestion['id'])
    
    # 2. Archive decisions >90 jours
    old_decisions = airtable.get_decisions(
        filter="created_at < '90 days ago'"
    )
    
    for decision in old_decisions:
        supabase.table('decisions_archive').insert({
            'airtable_decision_id': decision['id'],
            # ... all fields
        }).execute()
        
        airtable.delete_decision(decision['id'])
```

---

## 💰 COÛTS ESTIMÉS

### Airtable
- Free: 1,200 lignes (possible si archive agressif)
- Plus: $20/mois (50k lignes - recommandé)

Avec 8 tables et archive automatique: **$0-20/mois**

### Supabase
- Free: 500 MB database (suffisant 6-12 mois)
- Pro: $25/mois (8 GB - si croissance forte)

Estimation: **$0-25/mois**

**Total Système: $20-45/mois** (vs $200+ tout Airtable)

---

## ✅ PROCHAINES ÉTAPES

1. Je vais maintenant créer:
   - Python database clients (Airtable + Supabase)
   - Code système complet avec dual-database
   - Scripts migration
   - Guide setup détaillé

2. Documents à mettre à jour:
   - SETUP_GUIDE_COMPLET.md
   - Tous les fichiers Python
   - Scripts configuration

Confirmez que cette architecture vous convient et je génère tout le code! 🚀
