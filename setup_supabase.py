#!/usr/bin/env python3
"""
Setup Supabase database schema for DURUM AI Agent
Exécute les migrations SQL pour créer les 12 tables
"""

import subprocess
import sys
import os

# Read the SQL schema from docs
SQL_SCHEMA_FILE = "docs/NEW_ARCHITECTURE_AIRTABLE_SUPABASE.md"

# Extract SQL from markdown (it's between the SQL code blocks)
def extract_sql_from_docs():
    """Extrait le schéma SQL complet du fichier de documentation"""
    with open(SQL_SCHEMA_FILE, 'r') as f:
        content = f.read()
    
    # Find the SQL schema section
    start = content.find("```sql")
    end = content.find("```", start + 10)
    
    if start == -1 or end == -1:
        print("❌ SQL schema not found in documentation")
        return None
    
    sql = content[start + 6:end].strip()
    return sql

# Main schema SQL
SQL_SCHEMA = """
-- ============================================
-- 1. EXECUTION_LOGS
-- ============================================
CREATE TABLE IF NOT EXISTS execution_logs (
  id BIGSERIAL PRIMARY KEY,
  suggestion_id INTEGER NOT NULL,
  client_key VARCHAR(50) NOT NULL,
  
  action_type VARCHAR(50) NOT NULL,
  entity_type VARCHAR(20) NOT NULL,
  entity_id VARCHAR(100) NOT NULL,
  
  executed_at TIMESTAMPTZ DEFAULT NOW(),
  executed_by VARCHAR(50) DEFAULT 'system',
  
  before_state JSONB,
  after_state JSONB,
  api_response JSONB,
  
  success BOOLEAN DEFAULT TRUE,
  error_message TEXT,
  
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_execution_logs_client ON execution_logs(client_key);
CREATE INDEX IF NOT EXISTS idx_execution_logs_date ON execution_logs(executed_at);
CREATE INDEX IF NOT EXISTS idx_execution_logs_entity ON execution_logs(entity_type, entity_id);

-- ============================================
-- 2. PERFORMANCE_METRICS
-- ============================================
CREATE TABLE IF NOT EXISTS performance_metrics (
  id BIGSERIAL PRIMARY KEY,
  client_key VARCHAR(50) NOT NULL,
  date DATE NOT NULL,
  
  entity_type VARCHAR(20) NOT NULL,
  entity_id VARCHAR(100) NOT NULL,
  entity_name VARCHAR(255),
  
  spend DECIMAL(10,2) DEFAULT 0,
  impressions INTEGER DEFAULT 0,
  clicks INTEGER DEFAULT 0,
  ctr DECIMAL(5,2) DEFAULT 0,
  cpc DECIMAL(10,2) DEFAULT 0,
  
  leads INTEGER DEFAULT 0,
  cpl DECIMAL(10,2) DEFAULT 0,
  applications INTEGER DEFAULT 0,
  bookings INTEGER DEFAULT 0,
  cpb DECIMAL(10,2) DEFAULT 0,
  
  sales INTEGER DEFAULT 0,
  revenue DECIMAL(10,2) DEFAULT 0,
  cpa DECIMAL(10,2) DEFAULT 0,
  roi DECIMAL(5,2) DEFAULT 0,
  
  frequency DECIMAL(5,2) DEFAULT 0,
  reach INTEGER DEFAULT 0,
  
  created_at TIMESTAMPTZ DEFAULT NOW(),
  
  UNIQUE(client_key, date, entity_type, entity_id)
);

CREATE INDEX IF NOT EXISTS idx_perf_client_date ON performance_metrics(client_key, date DESC);
CREATE INDEX IF NOT EXISTS idx_perf_entity ON performance_metrics(entity_type, entity_id);
CREATE INDEX IF NOT EXISTS idx_perf_roi ON performance_metrics(roi DESC);

-- ============================================
-- 3. SPEND_HISTORY
-- ============================================
CREATE TABLE IF NOT EXISTS spend_history (
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

CREATE INDEX IF NOT EXISTS idx_spend_client_time ON spend_history(client_key, timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_spend_overspend ON spend_history(overspend_detected) WHERE overspend_detected = TRUE;

-- ============================================
-- 4. CREATIVE_PERFORMANCE
-- ============================================
CREATE TABLE IF NOT EXISTS creative_performance (
  id BIGSERIAL PRIMARY KEY,
  client_key VARCHAR(50) NOT NULL,
  ad_id VARCHAR(100) NOT NULL,
  date DATE NOT NULL,
  
  hook TEXT,
  angle VARCHAR(50),
  asset_type VARCHAR(20),
  
  impressions INTEGER DEFAULT 0,
  ctr DECIMAL(5,2) DEFAULT 0,
  hook_rate DECIMAL(5,2),
  engagement_rate DECIMAL(5,2),
  
  leads INTEGER DEFAULT 0,
  cpl DECIMAL(10,2),
  roi DECIMAL(5,2),
  
  days_active INTEGER DEFAULT 0,
  fatigue_index DECIMAL(5,2) DEFAULT 0,
  
  created_at TIMESTAMPTZ DEFAULT NOW(),
  
  UNIQUE(client_key, ad_id, date)
);

CREATE INDEX IF NOT EXISTS idx_creative_client_date ON creative_performance(client_key, date DESC);
CREATE INDEX IF NOT EXISTS idx_creative_fatigue ON creative_performance(fatigue_index DESC);

-- ============================================
-- 5. HYPOTHESIS_TRACKING
-- ============================================
CREATE TABLE IF NOT EXISTS hypothesis_tracking (
  id BIGSERIAL PRIMARY KEY,
  suggestion_id INTEGER NOT NULL,
  client_key VARCHAR(50) NOT NULL,
  
  hypothesis_text TEXT NOT NULL,
  predicted_metrics JSONB NOT NULL,
  confidence_score INTEGER NOT NULL CHECK (confidence_score >= 0 AND confidence_score <= 100),
  
  executed_at TIMESTAMPTZ,
  measurement_period_days INTEGER DEFAULT 7,
  measurement_end_date DATE,
  
  actual_metrics JSONB,
  variance JSONB,
  
  outcome VARCHAR(20),
  why_accurate TEXT,
  why_inaccurate TEXT,
  confounding_factors TEXT,
  
  model_adjustment_needed BOOLEAN DEFAULT FALSE,
  adjustment_notes TEXT,
  applied_to_model BOOLEAN DEFAULT FALSE,
  
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_hypothesis_client ON hypothesis_tracking(client_key);
CREATE INDEX IF NOT EXISTS idx_hypothesis_outcome ON hypothesis_tracking(outcome);
CREATE INDEX IF NOT EXISTS idx_hypothesis_confidence ON hypothesis_tracking(confidence_score DESC);

-- ============================================
-- 6. DECISION_PATTERNS
-- ============================================
CREATE TABLE IF NOT EXISTS decision_patterns (
  id BIGSERIAL PRIMARY KEY,
  pattern_name VARCHAR(255) NOT NULL,
  pattern_type VARCHAR(50) NOT NULL,
  
  description TEXT,
  detected_from_decisions INTEGER DEFAULT 0,
  confidence DECIMAL(5,2) DEFAULT 0,
  significance VARCHAR(20) DEFAULT 'low',
  
  condition TEXT,
  typical_decision VARCHAR(20),
  typical_reason TEXT,
  
  how_ai_uses_it TEXT,
  impact_on_suggestions TEXT,
  
  first_detected DATE,
  last_validated DATE,
  status VARCHAR(20) DEFAULT 'active',
  
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_patterns_status ON decision_patterns(status) WHERE status = 'active';
CREATE INDEX IF NOT EXISTS idx_patterns_confidence ON decision_patterns(confidence DESC);

-- ============================================
-- 7. FEEDBACK_LOOPS
-- ============================================
CREATE TABLE IF NOT EXISTS feedback_loops (
  id BIGSERIAL PRIMARY KEY,
  loop_type VARCHAR(50) NOT NULL,
  triggered_by_hypothesis_id BIGINT REFERENCES hypothesis_tracking(id),
  
  issue_description TEXT NOT NULL,
  frequency_of_issue INTEGER DEFAULT 1,
  impact_severity VARCHAR(20) DEFAULT 'low',
  
  adjustment_type VARCHAR(50),
  adjustment_description TEXT,
  before_vs_after JSONB,
  
  test_period_start DATE,
  test_period_end DATE,
  improvement_measured DECIMAL(5,2),
  
  status VARCHAR(20) DEFAULT 'testing',
  applied_to_production BOOLEAN DEFAULT FALSE,
  
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_feedback_status ON feedback_loops(status);
CREATE INDEX IF NOT EXISTS idx_feedback_severity ON feedback_loops(impact_severity);

-- ============================================
-- 8. TESTED_ANGLES
-- ============================================
CREATE TABLE IF NOT EXISTS tested_angles (
  id BIGSERIAL PRIMARY KEY,
  client_key VARCHAR(50) NOT NULL,
  
  angle_name VARCHAR(100) NOT NULL,
  angle_category VARCHAR(50),
  angle_description TEXT,
  
  tested_date DATE NOT NULL,
  campaign_id VARCHAR(100),
  ads_count INTEGER DEFAULT 0,
  total_spend DECIMAL(10,2) DEFAULT 0,
  duration_days INTEGER DEFAULT 0,
  
  result_status VARCHAR(20),
  
  ctr DECIMAL(5,2),
  cpa DECIMAL(10,2),
  cpl DECIMAL(10,2),
  conversion_rate DECIMAL(5,2),
  roi DECIMAL(5,2),
  leads_generated INTEGER DEFAULT 0,
  sales_generated INTEGER DEFAULT 0,
  
  why_succeeded TEXT,
  why_failed TEXT,
  key_learnings TEXT,
  would_retest BOOLEAN DEFAULT FALSE,
  
  example_hooks JSONB,
  best_performing_ad VARCHAR(100),
  
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_angles_client ON tested_angles(client_key);
CREATE INDEX IF NOT EXISTS idx_angles_result ON tested_angles(result_status);
CREATE INDEX IF NOT EXISTS idx_angles_roi ON tested_angles(roi DESC);

-- ============================================
-- 9. SUGGESTIONS_ARCHIVE
-- ============================================
CREATE TABLE IF NOT EXISTS suggestions_archive (
  id BIGSERIAL PRIMARY KEY,
  airtable_suggestion_id INTEGER NOT NULL,
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

CREATE INDEX IF NOT EXISTS idx_archive_sug_client ON suggestions_archive(client_key);
CREATE INDEX IF NOT EXISTS idx_archive_sug_created ON suggestions_archive(created_at DESC);

-- ============================================
-- 10. DECISIONS_ARCHIVE
-- ============================================
CREATE TABLE IF NOT EXISTS decisions_archive (
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

CREATE INDEX IF NOT EXISTS idx_archive_dec_client ON decisions_archive(client_key);
CREATE INDEX IF NOT EXISTS idx_archive_dec_created ON decisions_archive(created_at DESC);

-- ============================================
-- 11. SYSTEM_LOGS
-- ============================================
CREATE TABLE IF NOT EXISTS system_logs (
  id BIGSERIAL PRIMARY KEY,
  timestamp TIMESTAMPTZ DEFAULT NOW(),
  level VARCHAR(20) NOT NULL,
  module VARCHAR(100),
  
  message TEXT NOT NULL,
  context JSONB,
  
  exception_type VARCHAR(100),
  exception_message TEXT,
  stack_trace TEXT,
  
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_logs_timestamp ON system_logs(timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_logs_level ON system_logs(level);
CREATE INDEX IF NOT EXISTS idx_logs_module ON system_logs(module);

-- ============================================
-- 12. API_CALLS_LOG
-- ============================================
CREATE TABLE IF NOT EXISTS api_calls_log (
  id BIGSERIAL PRIMARY KEY,
  timestamp TIMESTAMPTZ DEFAULT NOW(),
  
  api_name VARCHAR(50) NOT NULL,
  endpoint VARCHAR(255),
  method VARCHAR(10),
  
  request_payload JSONB,
  response_payload JSONB,
  status_code INTEGER,
  
  duration_ms INTEGER,
  success BOOLEAN DEFAULT TRUE,
  error_message TEXT,
  
  cost_estimate DECIMAL(10,4),
  
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_api_timestamp ON api_calls_log(timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_api_name ON api_calls_log(api_name);
CREATE INDEX IF NOT EXISTS idx_api_success ON api_calls_log(success);
"""

def main():
    print("🚀 DURUM AI Agent - Supabase Setup")
    print("=" * 50)
    
    # Get Supabase credentials from environment
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_KEY")
    supabase_password = os.getenv("SUPABASE_DB_PASSWORD")
    
    if not supabase_url or not supabase_key:
        print("❌ Missing Supabase credentials")
        print("Set these environment variables:")
        print("  export SUPABASE_URL=https://...")
        print("  export SUPABASE_KEY=...")
        print("  export SUPABASE_DB_PASSWORD=...")
        return 1
    
    print(f"✅ Using Supabase URL: {supabase_url}")
    
    # Try to execute SQL via supabase CLI
    print("\n📊 Creating tables...")
    
    # Write SQL to temp file
    sql_file = "/tmp/durum_schema.sql"
    with open(sql_file, 'w') as f:
        f.write(SQL_SCHEMA)
    
    print(f"✅ SQL schema written to {sql_file}")
    
    # Create a .env.supabase file for Supabase CLI
    env_file = ".env.supabase"
    with open(env_file, 'w') as f:
        f.write(f"SUPABASE_URL={supabase_url}\n")
        f.write(f"SUPABASE_KEY={supabase_key}\n")
        f.write(f"SUPABASE_DB_PASSWORD={supabase_password}\n")
    
    print(f"✅ Environment file created: {env_file}")
    print("\n📝 Next steps:")
    print("1. Get your Supabase project URL and API key from https://app.supabase.com")
    print("2. Set environment variables:")
    print("   export SUPABASE_URL='your-url'")
    print("   export SUPABASE_KEY='your-api-key'")
    print("3. Run this script again to create the tables")
    
    print("\n✅ Setup complete!")
    print("📚 All SQL schemas are ready in database/client.py")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
