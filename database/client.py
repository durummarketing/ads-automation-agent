"""
Database Layer - Airtable + Supabase Dual Architecture
Gère toutes les interactions avec les deux bases de données
"""

import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
import json

# Airtable
from pyairtable import Api as AirtableApi
from pyairtable.formulas import match

# Supabase
from supabase import create_client, Client

# Environment
from dotenv import load_dotenv
load_dotenv()


@dataclass
class Suggestion:
    """Suggestion data model"""
    client_key: str
    type: str
    priority: str
    action: str
    reason: str
    expected_impact: str
    confidence: int
    entity_type: str
    entity_id: str
    status: str = "pending"
    decided_by: Optional[str] = None
    decided_at: Optional[datetime] = None
    slack_message_ts: Optional[str] = None
    suggestion_id: Optional[int] = None
    created_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None


class DatabaseClient:
    """
    Unified database client handling both Airtable and Supabase
    
    AIRTABLE (Business Layer):
    - clients, products, funnels, ads_library
    - suggestions (active only, 30 days)
    - decisions (recent only, 90 days)
    - validation_queue, winning_patterns
    
    SUPABASE (System Layer):
    - execution_logs, performance_metrics, spend_history
    - hypothesis_tracking, decision_patterns, feedback_loops
    - tested_angles, archives, system_logs, api_calls_log
    """
    
    def __init__(self):
        # Airtable Setup
        self.airtable_api = AirtableApi(os.getenv('AIRTABLE_API_KEY'))
        self.base_id = os.getenv('AIRTABLE_BASE_ID')
        
        # Airtable Tables
        self.clients_table = self.airtable_api.table(self.base_id, 'clients')
        self.products_table = self.airtable_api.table(self.base_id, 'products')
        self.funnels_table = self.airtable_api.table(self.base_id, 'funnels')
        self.ads_library_table = self.airtable_api.table(self.base_id, 'ads_library')
        self.suggestions_table = self.airtable_api.table(self.base_id, 'suggestions')
        self.decisions_table = self.airtable_api.table(self.base_id, 'decisions')
        self.validation_queue_table = self.airtable_api.table(self.base_id, 'validation_queue')
        self.winning_patterns_table = self.airtable_api.table(self.base_id, 'winning_patterns')
        
        # Supabase Setup
        supabase_url = os.getenv('SUPABASE_URL')
        supabase_key = os.getenv('SUPABASE_KEY')
        self.supabase: Client = create_client(supabase_url, supabase_key)
    
    
    # ============================================
    # CLIENTS (Airtable)
    # ============================================
    
    def get_all_clients(self) -> List[Dict]:
        """Get all active clients from Airtable"""
        return self.clients_table.all()
    
    def get_client(self, client_key: str) -> Optional[Dict]:
        """Get specific client by key"""
        results = self.clients_table.all(formula=match({"client_key": client_key}))
        return results[0] if results else None
    
    
    # ============================================
    # SUGGESTIONS (Airtable - Active Only)
    # ============================================
    
    def create_suggestion(self, suggestion: Suggestion) -> Dict:
        """
        Create suggestion in Airtable (visible to user)
        Also log to Supabase for system tracking
        """
        # Calculate expiration (48h from now)
        expires_at = datetime.now() + timedelta(hours=48)
        
        # Prepare Airtable data
        airtable_data = {
            'client_key': [self._get_client_record_id(suggestion.client_key)],
            'type': suggestion.type,
            'priority': suggestion.priority,
            'action': suggestion.action,
            'reason': suggestion.reason,
            'expected_impact': suggestion.expected_impact,
            'confidence': suggestion.confidence,
            'entity_type': suggestion.entity_type,
            'entity_id': suggestion.entity_id,
            'status': suggestion.status,
            'expires_at': expires_at.isoformat()
        }
        
        # Insert to Airtable
        airtable_record = self.suggestions_table.create(airtable_data)
        suggestion_id = airtable_record['id']
        
        # Log to Supabase for full tracking
        self.supabase.table('system_logs').insert({
            'level': 'INFO',
            'module': 'suggestions',
            'message': f'Suggestion created: {suggestion_id}',
            'context': {
                'airtable_id': suggestion_id,
                'client_key': suggestion.client_key,
                'type': suggestion.type,
                'confidence': suggestion.confidence
            }
        }).execute()
        
        return airtable_record
    
    def get_pending_suggestions(self, client_key: Optional[str] = None) -> List[Dict]:
        """Get all pending suggestions (optionally filtered by client)"""
        formula = "status = 'pending'"
        if client_key:
            formula = f"AND({formula}, client_key = '{client_key}')"
        
        return self.suggestions_table.all(formula=formula)
    
    def update_suggestion_status(
        self, 
        suggestion_id: str, 
        status: str,
        decided_by: Optional[str] = None
    ) -> Dict:
        """Update suggestion status after decision"""
        update_data = {
            'status': status,
            'decided_at': datetime.now().isoformat()
        }
        if decided_by:
            update_data['decided_by'] = decided_by
        
        return self.suggestions_table.update(suggestion_id, update_data)
    
    
    # ============================================
    # DECISIONS (Airtable - Recent Only)
    # ============================================
    
    def create_decision(
        self,
        suggestion_id: str,
        decision: str,
        decided_by: str,
        notes: Optional[str] = None
    ) -> Dict:
        """
        Record decision in Airtable
        Also log full context to Supabase
        """
        # Airtable record
        airtable_data = {
            'suggestion_id': [suggestion_id],
            'decision': decision,
            'decided_by': decided_by,
            'decided_at': datetime.now().isoformat(),
            'notes': notes or ''
        }
        
        airtable_record = self.decisions_table.create(airtable_data)
        
        # Full log to Supabase
        suggestion = self.suggestions_table.get(suggestion_id)
        
        self.supabase.table('system_logs').insert({
            'level': 'INFO',
            'module': 'decisions',
            'message': f'Decision recorded: {decision}',
            'context': {
                'airtable_decision_id': airtable_record['id'],
                'suggestion_id': suggestion_id,
                'decision': decision,
                'decided_by': decided_by,
                'suggestion_data': suggestion['fields']
            }
        }).execute()
        
        return airtable_record
    
    
    # ============================================
    # PERFORMANCE METRICS (Supabase Only)
    # ============================================
    
    def insert_performance_metrics(
        self,
        client_key: str,
        date: str,
        entity_type: str,
        entity_id: str,
        metrics: Dict[str, Any]
    ) -> None:
        """Insert daily performance metrics to Supabase"""
        data = {
            'client_key': client_key,
            'date': date,
            'entity_type': entity_type,
            'entity_id': entity_id,
            'entity_name': metrics.get('entity_name'),
            'spend': metrics.get('spend', 0),
            'impressions': metrics.get('impressions', 0),
            'clicks': metrics.get('clicks', 0),
            'ctr': metrics.get('ctr', 0),
            'cpc': metrics.get('cpc', 0),
            'leads': metrics.get('leads', 0),
            'cpl': metrics.get('cpl', 0),
            'applications': metrics.get('applications', 0),
            'bookings': metrics.get('bookings', 0),
            'cpb': metrics.get('cpb', 0),
            'sales': metrics.get('sales', 0),
            'revenue': metrics.get('revenue', 0),
            'cpa': metrics.get('cpa', 0),
            'roi': metrics.get('roi', 0),
            'frequency': metrics.get('frequency', 0),
            'reach': metrics.get('reach', 0)
        }
        
        # Upsert (insert or update if exists)
        self.supabase.table('performance_metrics').upsert(
            data,
            on_conflict='client_key,date,entity_type,entity_id'
        ).execute()
    
    def get_performance_metrics(
        self,
        client_key: str,
        entity_type: str,
        entity_id: str,
        days: int = 7
    ) -> List[Dict]:
        """Get performance metrics for last N days"""
        start_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
        
        result = self.supabase.table('performance_metrics')\
            .select('*')\
            .eq('client_key', client_key)\
            .eq('entity_type', entity_type)\
            .eq('entity_id', entity_id)\
            .gte('date', start_date)\
            .order('date', desc=True)\
            .execute()
        
        return result.data
    
    def calculate_benchmarks(
        self,
        client_key: str,
        metric_name: str,
        level: str = 'client'
    ) -> Dict[str, float]:
        """
        Calculate benchmarks (percentiles) for a metric
        
        Levels:
        - global: All clients
        - industry: Same industry clients
        - client: This client historical
        """
        # Build query based on level
        query = self.supabase.table('performance_metrics').select(metric_name)
        
        if level == 'client':
            query = query.eq('client_key', client_key)
        elif level == 'industry':
            # Get client industry first
            client = self.get_client(client_key)
            if client:
                industry = client['fields'].get('industry')
                # Query clients in same industry
                query = query.in_('client_key', self._get_clients_by_industry(industry))
        
        # Execute query
        result = query.execute()
        values = [r[metric_name] for r in result.data if r.get(metric_name)]
        
        if not values:
            return {'p25': 0, 'p50': 0, 'p75': 0, 'p90': 0}
        
        # Calculate percentiles
        import numpy as np
        return {
            'p25': float(np.percentile(values, 25)),
            'p50': float(np.percentile(values, 50)),
            'p75': float(np.percentile(values, 75)),
            'p90': float(np.percentile(values, 90))
        }
    
    
    # ============================================
    # EXECUTION LOGS (Supabase Only)
    # ============================================
    
    def log_execution(
        self,
        suggestion_id: int,
        client_key: str,
        action_type: str,
        entity_type: str,
        entity_id: str,
        before_state: Dict,
        after_state: Dict,
        api_response: Dict,
        success: bool = True,
        error_message: Optional[str] = None
    ) -> None:
        """Log action execution to Supabase"""
        self.supabase.table('execution_logs').insert({
            'suggestion_id': suggestion_id,
            'client_key': client_key,
            'action_type': action_type,
            'entity_type': entity_type,
            'entity_id': entity_id,
            'before_state': before_state,
            'after_state': after_state,
            'api_response': api_response,
            'success': success,
            'error_message': error_message
        }).execute()
    
    
    # ============================================
    # HYPOTHESIS TRACKING (Supabase Only)
    # ============================================
    
    def create_hypothesis(
        self,
        suggestion_id: int,
        client_key: str,
        hypothesis_text: str,
        predicted_metrics: Dict,
        confidence_score: int
    ) -> None:
        """Create hypothesis for prediction tracking"""
        measurement_end_date = (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')
        
        self.supabase.table('hypothesis_tracking').insert({
            'suggestion_id': suggestion_id,
            'client_key': client_key,
            'hypothesis_text': hypothesis_text,
            'predicted_metrics': predicted_metrics,
            'confidence_score': confidence_score,
            'executed_at': datetime.now().isoformat(),
            'measurement_period_days': 7,
            'measurement_end_date': measurement_end_date
        }).execute()
    
    def validate_hypothesis(
        self,
        hypothesis_id: int,
        actual_metrics: Dict,
        outcome: str,
        analysis: Dict
    ) -> None:
        """Update hypothesis with actual results"""
        # Calculate variance
        hypothesis = self.supabase.table('hypothesis_tracking')\
            .select('predicted_metrics')\
            .eq('id', hypothesis_id)\
            .single()\
            .execute()
        
        predicted = hypothesis.data['predicted_metrics']
        variance = {}
        for key in predicted.keys():
            if key in actual_metrics:
                variance[key] = ((actual_metrics[key] - predicted[key]) / predicted[key] * 100)
        
        # Update
        self.supabase.table('hypothesis_tracking').update({
            'actual_metrics': actual_metrics,
            'variance': variance,
            'outcome': outcome,
            'why_accurate': analysis.get('why_accurate'),
            'why_inaccurate': analysis.get('why_inaccurate'),
            'confounding_factors': analysis.get('confounding_factors')
        }).eq('id', hypothesis_id).execute()
    
    
    # ============================================
    # ARCHIVING (Airtable → Supabase)
    # ============================================
    
    def archive_old_suggestions(self, days_old: int = 30) -> int:
        """Archive suggestions older than X days to Supabase"""
        cutoff_date = (datetime.now() - timedelta(days=days_old)).isoformat()
        
        # Get old suggestions from Airtable
        formula = f"created_at < '{cutoff_date}'"
        old_suggestions = self.suggestions_table.all(formula=formula)
        
        archived_count = 0
        for suggestion in old_suggestions:
            fields = suggestion['fields']
            
            # Insert to Supabase archive
            self.supabase.table('suggestions_archive').insert({
                'airtable_suggestion_id': suggestion['id'],
                'client_key': fields.get('client_key'),
                'type': fields.get('type'),
                'priority': fields.get('priority'),
                'action': fields.get('action'),
                'reason': fields.get('reason'),
                'expected_impact': fields.get('expected_impact'),
                'confidence': fields.get('confidence'),
                'entity_type': fields.get('entity_type'),
                'entity_id': fields.get('entity_id'),
                'status': fields.get('status'),
                'decided_by': fields.get('decided_by'),
                'decided_at': fields.get('decided_at'),
                'created_at': suggestion.get('createdTime')
            }).execute()
            
            # Delete from Airtable
            self.suggestions_table.delete(suggestion['id'])
            archived_count += 1
        
        return archived_count
    
    def archive_old_decisions(self, days_old: int = 90) -> int:
        """Archive decisions older than X days to Supabase"""
        cutoff_date = (datetime.now() - timedelta(days=days_old)).isoformat()
        
        formula = f"created_at < '{cutoff_date}'"
        old_decisions = self.decisions_table.all(formula=formula)
        
        archived_count = 0
        for decision in old_decisions:
            fields = decision['fields']
            
            self.supabase.table('decisions_archive').insert({
                'airtable_decision_id': decision['id'],
                'suggestion_id': fields.get('suggestion_id'),
                'client_key': fields.get('client_key'),
                'decision': fields.get('decision'),
                'decided_by': fields.get('decided_by'),
                'decided_at': fields.get('decided_at'),
                'notes': fields.get('notes'),
                'created_at': decision.get('createdTime')
            }).execute()
            
            self.decisions_table.delete(decision['id'])
            archived_count += 1
        
        return archived_count
    
    
    # ============================================
    # HELPER METHODS
    # ============================================
    
    def _get_client_record_id(self, client_key: str) -> str:
        """Get Airtable record ID for a client_key"""
        client = self.get_client(client_key)
        return client['id'] if client else None
    
    def _get_clients_by_industry(self, industry: str) -> List[str]:
        """Get all client_keys in a specific industry"""
        clients = self.clients_table.all(formula=match({"industry": industry}))
        return [c['fields']['client_key'] for c in clients]


# Singleton instance
db = DatabaseClient()
