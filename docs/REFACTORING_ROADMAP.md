# 🔄 REFONTE COMPLÈTE - Plan d'Exécution

## 📋 RÉSUMÉ

**Décision validée**: Architecture Airtable (8 tables) + Supabase (12 tables)

**Impact**: Refonte complète de TOUS les documents et code créés jusqu'ici

---

## ✅ CE QUI EST FAIT

### 1. Architecture Définie
- ✅ `NEW_ARCHITECTURE_AIRTABLE_SUPABASE.md` - Architecture complète
- ✅ 8 tables Airtable schématisées
- ✅ 12 tables Supabase (SQL complet)
- ✅ Flux de données documenté

### 2. Database Layer Créé
- ✅ `database/client.py` - Client unifié Airtable + Supabase
- ✅ Méthodes CRUD pour toutes opérations
- ✅ Archivage automatique intégré
- ✅ Benchmarks calculation

---

## 📝 FICHIERS À CRÉER/MODIFIER

### GROUPE 1: Configuration (4 fichiers)

#### 1. `.env.example` - MODIFIER
```bash
# AJOUTER variables Supabase:
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_KEY=your_supabase_key_here
SUPABASE_SERVICE_KEY=your_service_key_here
```

#### 2. `requirements.txt` - MODIFIER
```python
# AJOUTER:
supabase==2.3.0
numpy==1.26.3  # Pour calculs benchmarks
```

#### 3. `config/database.py` - CRÉER
```python
"""
Database configuration settings
"""

AIRTABLE_TABLES = {
    'clients': 'clients',
    'products': 'products',
    'funnels': 'funnels',
    'ads_library': 'ads_library',
    'suggestions': 'suggestions',
    'decisions': 'decisions',
    'validation_queue': 'validation_queue',
    'winning_patterns': 'winning_patterns'
}

SUPABASE_TABLES = {
    'execution_logs': 'execution_logs',
    'performance_metrics': 'performance_metrics',
    'spend_history': 'spend_history',
    'creative_performance': 'creative_performance',
    'hypothesis_tracking': 'hypothesis_tracking',
    'decision_patterns': 'decision_patterns',
    'feedback_loops': 'feedback_loops',
    'tested_angles': 'tested_angles',
    'suggestions_archive': 'suggestions_archive',
    'decisions_archive': 'decisions_archive',
    'system_logs': 'system_logs',
    'api_calls_log': 'api_calls_log'
}

# Archiving settings
ARCHIVE_SUGGESTIONS_DAYS = 30
ARCHIVE_DECISIONS_DAYS = 90
```

#### 4. `database/__init__.py` - CRÉER
```python
"""Database package"""
from .client import db, DatabaseClient, Suggestion

__all__ = ['db', 'DatabaseClient', 'Suggestion']
```

---

### GROUPE 2: Core System (5 fichiers)

#### 5. `main.py` - REFACTORER COMPLET
```python
"""
Main entry point - Refactoré pour dual database
"""
import os
import sys
from datetime import datetime
from dotenv import load_dotenv

# Import database layer
from database import db

# Import modules
from analysis.analyzer import DailyAnalyzer
from suggestions.generator import SuggestionGenerator
from execution.executor import ActionExecutor
from slack.notifier import SlackNotifier

load_dotenv()

def main():
    """Run daily analysis cycle"""
    print("🚀 DURUM AI Agent - Starting...")
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        # 1. Get all clients from Airtable
        clients = db.get_all_clients()
        print(f"📊 Analyzing {len(clients)} clients...")
        
        # 2. Run analysis for each client
        analyzer = DailyAnalyzer(db)
        suggestions_generated = []
        
        for client in clients:
            client_key = client['fields']['client_key']
            print(f"\n🔍 Analyzing {client_key}...")
            
            # Analyze and generate suggestions
            suggestions = analyzer.analyze_client(client_key)
            suggestions_generated.extend(suggestions)
        
        # 3. Send notifications
        if suggestions_generated:
            notifier = SlackNotifier()
            notifier.send_daily_digest(suggestions_generated)
            print(f"\n✅ {len(suggestions_generated)} suggestions sent to Slack")
        
        # 4. Archive old data
        print("\n🗄️ Archiving old data...")
        archived_sug = db.archive_old_suggestions(days_old=30)
        archived_dec = db.archive_old_decisions(days_old=90)
        print(f"   Archived {archived_sug} suggestions, {archived_dec} decisions")
        
        print("\n✅ Daily cycle complete!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        # Log to Supabase
        db.supabase.table('system_logs').insert({
            'level': 'ERROR',
            'module': 'main',
            'message': str(e),
            'exception_type': type(e).__name__
        }).execute()
        sys.exit(1)

if __name__ == "__main__":
    main()
```

#### 6. `analysis/analyzer.py` - CRÉER
```python
"""
Daily Analysis Module
Queries Supabase for metrics, generates insights
"""
from datetime import datetime, timedelta
from typing import List, Dict
from database import db, Suggestion

class DailyAnalyzer:
    """Analyzes client performance and generates suggestions"""
    
    def __init__(self, database_client):
        self.db = database_client
    
    def analyze_client(self, client_key: str) -> List[Suggestion]:
        """
        Analyze client and generate suggestions
        
        1. Pull performance metrics from Supabase (7 days)
        2. Calculate benchmarks
        3. Identify opportunities (scale/pause/refresh)
        4. Generate suggestions
        5. Store in Airtable (user-visible)
        6. Log to Supabase (full context)
        """
        suggestions = []
        
        # Get client info
        client = self.db.get_client(client_key)
        if not client:
            return suggestions
        
        roi_target = client['fields'].get('roi_target', 3.0)
        
        # Analyze adsets (example)
        adsets = self._get_active_adsets(client_key)
        
        for adset in adsets:
            # Get performance metrics from Supabase
            metrics = self.db.get_performance_metrics(
                client_key=client_key,
                entity_type='adset',
                entity_id=adset['id'],
                days=7
            )
            
            if not metrics:
                continue
            
            # Calculate current performance
            latest = metrics[0]
            avg_roi = latest.get('roi', 0)
            avg_cpl = latest.get('cpl', 0)
            total_spend = sum(m.get('spend', 0) for m in metrics)
            
            # Get benchmarks from Supabase
            benchmarks = self.db.calculate_benchmarks(
                client_key=client_key,
                metric_name='roi',
                level='client'
            )
            
            # OPPORTUNITY: Scale high performers
            if avg_roi > roi_target and avg_roi > benchmarks['p75']:
                suggestion = Suggestion(
                    client_key=client_key,
                    type='scale',
                    priority='high',
                    action=f"Scale AdSet {adset['name']} +50%",
                    reason=f"ROI {avg_roi:.1f}x (target: {roi_target}x, p75: {benchmarks['p75']:.1f}x)",
                    expected_impact=f"Maintain ROI {avg_roi*0.9:.1f}-{avg_roi:.1f}x while increasing volume",
                    confidence=85,
                    entity_type='adset',
                    entity_id=adset['id']
                )
                suggestions.append(suggestion)
            
            # OPPORTUNITY: Pause underperformers
            elif avg_roi < roi_target * 0.6 and total_spend > 500:
                suggestion = Suggestion(
                    client_key=client_key,
                    type='pause',
                    priority='medium',
                    action=f"Pause AdSet {adset['name']}",
                    reason=f"ROI {avg_roi:.1f}x (target: {roi_target}x), ${total_spend:.0f} spent",
                    expected_impact=f"Save ~${total_spend/7*7:.0f}/week to reallocate",
                    confidence=78,
                    entity_type='adset',
                    entity_id=adset['id']
                )
                suggestions.append(suggestion)
        
        # Create suggestions in Airtable
        for suggestion in suggestions:
            self.db.create_suggestion(suggestion)
        
        return suggestions
    
    def _get_active_adsets(self, client_key: str) -> List[Dict]:
        """
        Get active adsets from Meta API
        (This would integrate with your Meta client)
        """
        # TODO: Implement Meta API integration
        # For now, return mock data
        return [
            {'id': 'adset_123', 'name': 'STACK_H:25/45 _QC'},
            {'id': 'adset_456', 'name': 'STACK_X:35/55 _ON'}
        ]
```

#### 7. `suggestions/generator.py` - CRÉER
```python
"""
Suggestion Generation Module
Uses ML patterns from Supabase to generate smart suggestions
"""

class SuggestionGenerator:
    """Generates AI-powered suggestions based on learned patterns"""
    
    def __init__(self, database_client):
        self.db = database_client
    
    def generate_from_patterns(self, client_key: str, analysis_data: Dict) -> List[Suggestion]:
        """
        Generate suggestions using learned patterns from Supabase
        
        1. Query decision_patterns (what you typically approve/refuse)
        2. Query winning_patterns (what works historically)
        3. Apply patterns to current situation
        4. Generate tailored suggestions
        """
        # Query decision patterns from Supabase
        patterns = self.db.supabase.table('decision_patterns')\
            .select('*')\
            .eq('status', 'active')\
            .gte('confidence', 70)\
            .execute()
        
        # Apply patterns to generate suggestions
        # ... ML logic here
        
        return suggestions
```

#### 8. `execution/executor.py` - CRÉER
```python
"""
Action Execution Module
Executes approved suggestions on Meta Ads
"""

class ActionExecutor:
    """Executes actions on Meta after approval"""
    
    def __init__(self, database_client):
        self.db = database_client
    
    def execute_suggestion(self, suggestion_id: str) -> bool:
        """
        Execute approved suggestion
        
        1. Get suggestion from Airtable
        2. Execute action via Meta API
        3. Log execution to Supabase
        4. Update suggestion status in Airtable
        5. Create hypothesis in Supabase
        """
        # Get suggestion
        suggestion = self.db.suggestions_table.get(suggestion_id)
        fields = suggestion['fields']
        
        # Execute on Meta
        # ... Meta API call
        
        # Log to Supabase
        self.db.log_execution(
            suggestion_id=int(suggestion_id),
            client_key=fields['client_key'],
            action_type=fields['type'],
            entity_type=fields['entity_type'],
            entity_id=fields['entity_id'],
            before_state={'budget': 100},
            after_state={'budget': 150},
            api_response={'success': True},
            success=True
        )
        
        # Update Airtable
        self.db.update_suggestion_status(
            suggestion_id=suggestion_id,
            status='executed'
        )
        
        # Create hypothesis for tracking
        self.db.create_hypothesis(
            suggestion_id=int(suggestion_id),
            client_key=fields['client_key'],
            hypothesis_text=fields['expected_impact'],
            predicted_metrics={'roi': 3.8, 'leads': 25},
            confidence_score=fields['confidence']
        )
        
        return True
```

#### 9. `slack/notifier.py` - CRÉER
```python
"""
Slack Notification Module
Sends suggestions to Slack with approval buttons
"""

class SlackNotifier:
    """Handles all Slack communications"""
    
    def __init__(self):
        from slack_sdk import WebClient
        self.client = WebClient(token=os.getenv('SLACK_BOT_TOKEN'))
    
    def send_daily_digest(self, suggestions: List[Suggestion]):
        """Send morning digest with all suggestions"""
        # Format message
        blocks = self._format_digest(suggestions)
        
        # Send to Slack
        response = self.client.chat_postMessage(
            channel='durum-suggestions',
            blocks=blocks
        )
        
        # Store message_ts in Airtable for each suggestion
        for suggestion in suggestions:
            if suggestion.suggestion_id:
                self.db.suggestions_table.update(
                    suggestion.suggestion_id,
                    {'slack_message_ts': response['ts']}
                )
    
    def _format_digest(self, suggestions: List[Suggestion]) -> List[Dict]:
        """Format suggestions as Slack blocks"""
        # ... Slack Block Kit formatting
        return blocks
```

---

### GROUPE 3: Documentation (6 fichiers)

#### 10. `SETUP_GUIDE_COMPLET.md` - REFACTORER
**Changements**:
- Section Supabase setup (30 min)
- 8 tables Airtable (pas 3, pas 15)
- SQL execution dans Supabase
- Dual database configuration
- Tests connexions Airtable + Supabase

#### 11. `NEW_SYSTEM_ARCHITECTURE.md` - CRÉER
**Contenu**: Architecture finale validée (déjà créé)

#### 12. `AIRTABLE_SETUP_GUIDE.md` - CRÉER
**Contenu**: Guide création 8 tables Airtable étape par étape

#### 13. `SUPABASE_SETUP_GUIDE.md` - CRÉER
**Contenu**: 
- Créer compte Supabase
- Exécuter SQL schema
- Obtenir credentials
- Tester connexion

#### 14. `DATABASE_USAGE_GUIDE.md` - CRÉER
**Contenu**: Comment utiliser database/client.py

#### 15. `MIGRATION_GUIDE.md` - CRÉER
**Contenu**: Migrer de l'ancienne architecture si nécessaire

---

### GROUPE 4: Scripts Utilitaires (4 fichiers)

#### 16. `scripts/setup_supabase.sh` - CRÉER
```bash
#!/bin/bash
# Setup Supabase database with all tables

echo "🚀 Setting up Supabase database..."

# Read SQL file and execute
cat config/supabase_schema.sql | supabase db execute

echo "✅ Supabase setup complete!"
```

#### 17. `scripts/test_connections.py` - CRÉER
```python
"""Test Airtable and Supabase connections"""

from database import db

def test_airtable():
    """Test Airtable connection"""
    clients = db.get_all_clients()
    print(f"✅ Airtable: {len(clients)} clients found")
    return True

def test_supabase():
    """Test Supabase connection"""
    result = db.supabase.table('system_logs').select('id').limit(1).execute()
    print(f"✅ Supabase: Connected")
    return True

if __name__ == "__main__":
    test_airtable()
    test_supabase()
    print("\n🎉 All connections working!")
```

#### 18. `scripts/archive_now.py` - CRÉER
```python
"""Manually trigger archiving"""

from database import db

archived_sug = db.archive_old_suggestions(days_old=30)
archived_dec = db.archive_old_decisions(days_old=90)

print(f"✅ Archived {archived_sug} suggestions, {archived_dec} decisions")
```

#### 19. `config/supabase_schema.sql` - CRÉER
**Contenu**: Le SQL complet des 12 tables (déjà dans NEW_ARCHITECTURE_AIRTABLE_SUPABASE.md)

---

### GROUPE 5: Tests (2 fichiers)

#### 20. `tests/test_database.py` - CRÉER
```python
"""Test database layer"""

import pytest
from database import db, Suggestion

def test_create_suggestion():
    """Test creating suggestion in Airtable + logging to Supabase"""
    suggestion = Suggestion(
        client_key='test_client',
        type='scale',
        priority='high',
        action='Test action',
        reason='Test reason',
        expected_impact='Test impact',
        confidence=85,
        entity_type='adset',
        entity_id='test_123'
    )
    
    result = db.create_suggestion(suggestion)
    assert result is not None
    assert 'id' in result

def test_benchmarks():
    """Test benchmark calculation"""
    benchmarks = db.calculate_benchmarks(
        client_key='avego',
        metric_name='roi',
        level='client'
    )
    
    assert 'p25' in benchmarks
    assert 'p50' in benchmarks
    assert 'p75' in benchmarks
    assert 'p90' in benchmarks
```

#### 21. `tests/test_analysis.py` - CRÉER
```python
"""Test analysis module"""

import pytest
from analysis.analyzer import DailyAnalyzer
from database import db

def test_client_analysis():
    """Test analyzing a client"""
    analyzer = DailyAnalyzer(db)
    suggestions = analyzer.analyze_client('avego')
    
    assert isinstance(suggestions, list)
    # More assertions...
```

---

## 📊 RÉCAPITULATIF REFONTE

### Fichiers à Créer: 18
- Database layer: 2 fichiers
- Core system: 5 fichiers  
- Documentation: 6 fichiers
- Scripts: 4 fichiers
- Tests: 2 fichiers

### Fichiers à Modifier: 3
- .env.example
- requirements.txt
- SETUP_GUIDE_COMPLET.md

### Fichiers Obsolètes: ~8
- Anciens fichiers avec architecture 15 tables Airtable
- À archiver, pas supprimer

---

## ⏱️ TEMPS ESTIMÉ

**Phase 1: Database Layer** (Fait)
- ✅ database/client.py créé
- ✅ Architecture documentée

**Phase 2: Core System** (2-3h)
- main.py refactoré
- analysis/analyzer.py
- execution/executor.py
- suggestions/generator.py
- slack/notifier.py

**Phase 3: Documentation** (2h)
- Guides setup
- Guides usage
- Migration guide

**Phase 4: Scripts & Tests** (1h)
- Scripts setup
- Tests unitaires

**TOTAL: 5-6 heures** de travail pour moi

---

## 🎯 PROCHAINE ÉTAPE

**Vous confirmez?**
- ✅ Architecture Airtable (8) + Supabase (12)
- ✅ Je crée tous les fichiers listés ci-dessus
- ✅ Je mets à jour documentation complète
- ✅ Je teste le tout

**Si OUI**: Je génère tout maintenant (va prendre 30-45 min)

**Si vous voulez ajustements**: Dites-moi quoi changer d'abord

**GO?** 🚀
