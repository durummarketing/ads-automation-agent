"""
Publishing Workflow System - Publication automatique avec validation client
Gère le cycle complet: Airtable → Validation Client → Meta Publication
"""

import os
import time
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum

# Imports internes
from airtable.client import AirtableClient
from slack.notifier import SlackNotifier  
from meta.publisher import MetaPublisher
from utils.log_sanitizer import sanitize_log


class AdStatus(Enum):
    """Statuts possibles pour une ad"""
    BROUILLON = "Brouillon"
    PRET_VALIDATION = "Prêt pour Validation"
    EN_VALIDATION_CLIENT = "En Validation Client"
    APPROUVE_CLIENT = "Approuvé Client"
    EN_VALIDATION_FINALE = "En Validation Finale (Vous)"
    APPROUVE_FINAL = "Approuvé Final"
    COMMENTAIRE_CLIENT = "Commentaire Client"
    PUBLIE = "Publié"
    ACTIF = "Actif"
    PAUSE = "Pause"
    ARCHIVE = "Archivé"
    ERREUR = "Erreur Publication"


class PublicationMode(Enum):
    """Modes de publication"""
    AUTO = "Auto"      # Publier ON (ACTIVE)
    MANUEL = "Manuel"  # Publier OFF (PAUSED)
    TEST = "Test"      # Draft (non publié)


@dataclass
class ValidationRequest:
    """Requête de validation client"""
    ad_id: str
    client_key: str
    client_name: str
    
    # Structure Meta
    campaign_name: str
    adset_name: str
    ad_name: str
    
    # Creative
    hook: str
    body: str
    cta: str
    asset_type: str  # image, video
    asset_url: str
    
    # Publication
    publication_mode: str
    budget_daily: float
    
    # Slack
    validation_channel: str
    validation_channel_id: str
    
    # Metadata
    created_at: datetime
    sent_for_validation_at: Optional[datetime] = None


@dataclass
class ClientComment:
    """Commentaire client sur une ad"""
    ad_id: str
    client_key: str
    comment_text: str
    priority: str  # normal, urgent
    commented_by: str
    commented_at: datetime


class PublishingWorkflow:
    """
    Système complet de publication avec validation client
    """
    
    def __init__(self):
        self.airtable = AirtableClient()
        self.slack = SlackNotifier()
        self.meta = MetaPublisher()
        
        # Configuration
        self.cycle_interval_seconds = int(os.getenv('PUBLISHING_CYCLE_SECONDS', '60'))
        self.validation_timeout_hours = int(os.getenv('VALIDATION_TIMEOUT_HOURS', '48'))
        
        print(f"📋 Publishing Workflow initialisé")
        print(f"   Cycle: {self.cycle_interval_seconds}s")
        print(f"   Timeout validation: {self.validation_timeout_hours}h")
    
    def start(self):
        """
        Démarre le workflow en boucle continue
        """
        print("\n🚀 Démarrage du Publishing Workflow...\n")
        
        while True:
            try:
                self.run_cycle()
                
                # Pause avant prochain cycle
                time.sleep(self.cycle_interval_seconds)
                
            except KeyboardInterrupt:
                print("\n⚠️  Arrêt demandé par l'utilisateur")
                break
            
            except Exception as e:
                print(f"❌ Erreur dans le cycle: {e}")
                sanitize_log(str(e))
                # Continuer malgré l'erreur
                time.sleep(self.cycle_interval_seconds)
    
    def run_cycle(self):
        """
        Exécute un cycle complet du workflow
        """
        timestamp = datetime.now().strftime('%H:%M:%S')
        
        # 1. Détecter nouvelles ads pour validation CLIENT
        new_ads = self._detect_new_ads_for_validation()
        
        if new_ads:
            print(f"[{timestamp}] 📢 {len(new_ads)} nouvelle(s) ad(s) pour validation CLIENT")
            
            for ad_request in new_ads:
                self._send_client_validation(ad_request)
        
        # 2. Détecter ads approuvées par client → Envoyer validation FINALE (vous)
        client_approved_ads = self._get_client_approved_ads()
        
        if client_approved_ads:
            print(f"[{timestamp}] ✅ {len(client_approved_ads)} ad(s) approuvée(s) par client → Validation finale")
            
            for ad in client_approved_ads:
                self._send_final_validation(ad)
        
        # 3. Publier ads approuvées FINALEMENT (par vous)
        final_approved_ads = self._get_final_approved_ads()
        
        if final_approved_ads:
            print(f"[{timestamp}] 🚀 {len(final_approved_ads)} ad(s) approuvée(s) FINALEMENT → Publication")
            
            for ad in final_approved_ads:
                self._publish_ad_to_meta(ad)
        
        # 4. Traiter commentaires clients
        commented_ads = self._get_ads_with_comments()
        
        if commented_ads:
            print(f"[{timestamp}] 💬 {len(commented_ads)} commentaire(s) client(s) à traiter")
            
            for ad in commented_ads:
                self._process_client_comment(ad)
        
        # 5. Vérifier timeouts validation client (24h sans réponse)
        self._check_client_validation_timeouts()
        
        # 6. Vérifier ads en attente validation finale depuis 24h+
        self._check_final_validation_delays()
        
        # Afficher statut si rien à faire
        if not (new_ads or client_approved_ads or final_approved_ads or commented_ads):
            print(f"[{timestamp}] ⏳ En attente... (prochain cycle dans {self.cycle_interval_seconds}s)")
    
    def _detect_new_ads_for_validation(self) -> List[ValidationRequest]:
        """
        Détecte ads avec status "Prêt pour Validation"
        """
        # Query Airtable
        formula = f"{{status}} = '{AdStatus.PRET_VALIDATION.value}'"
        
        records = self.airtable.get_records(
            table='ads',
            filter_by_formula=formula
        )
        
        validation_requests = []
        
        for record in records:
            try:
                # Valider structure de l'ad
                validation_result = self._validate_ad_structure(record)
                
                if not validation_result['valid']:
                    # Structure invalide → Remettre en brouillon avec note
                    self.airtable.update_record(
                        table='ads',
                        record_id=record['id'],
                        fields={
                            'status': AdStatus.BROUILLON.value,
                            'notes': f"⚠️ Structure invalide: {validation_result['errors']}"
                        }
                    )
                    
                    print(f"   ⚠️  Ad {record['id']} invalide - remise en brouillon")
                    continue
                
                # Récupérer infos client
                client = self.airtable.get_record(
                    table='clients',
                    record_id=record['fields']['client_key'][0]  # Link field
                )
                
                # Créer requête validation
                validation_request = ValidationRequest(
                    ad_id=record['id'],
                    client_key=client['fields']['key'],
                    client_name=client['fields']['Client_Name'],
                    campaign_name=record['fields']['campaign_name'],
                    adset_name=record['fields']['adset_name'],
                    ad_name=record['fields']['ad_name'],
                    hook=record['fields'].get('copy_hook', ''),
                    body=record['fields'].get('copy_body', ''),
                    cta=record['fields'].get('copy_cta', 'Learn More'),
                    asset_type=record['fields'].get('asset_type', 'image'),
                    asset_url=record['fields'].get('asset_url', ''),
                    publication_mode=record['fields'].get('publication_mode', PublicationMode.MANUEL.value),
                    budget_daily=float(record['fields'].get('budget_daily', 100)),
                    validation_channel=client['fields'].get('slack_validation_channel', 'validation'),
                    validation_channel_id=client['fields'].get('slack_channel_id', ''),
                    created_at=datetime.fromisoformat(record['createdTime'])
                )
                
                validation_requests.append(validation_request)
                
            except Exception as e:
                print(f"   ❌ Erreur traitement ad {record['id']}: {e}")
                continue
        
        return validation_requests
    
    def _validate_ad_structure(self, record: Dict) -> Dict[str, Any]:
        """
        Valide qu'une ad respecte la structure et conventions
        """
        errors = []
        fields = record['fields']
        
        # Champs requis
        required_fields = [
            'ad_name', 'client_key', 'campaign_name', 
            'adset_name', 'copy_hook', 'copy_body', 
            'copy_cta', 'publication_mode'
        ]
        
        for field in required_fields:
            if field not in fields or not fields[field]:
                errors.append(f"Champ requis manquant: {field}")
        
        # Validation convention nommage ad
        ad_name = fields.get('ad_name', '')
        
        # Format attendu: "Ads T4 - V1" ou "Ads T4 - I1"
        if not self._validate_ad_naming(ad_name):
            errors.append(f"Nom ad invalide: '{ad_name}' (Format: 'Ads TX - V1')")
        
        # Publication mode valide
        pub_mode = fields.get('publication_mode', '')
        valid_modes = [mode.value for mode in PublicationMode]
        
        if pub_mode not in valid_modes:
            errors.append(f"Mode publication invalide: {pub_mode} (Valides: {valid_modes})")
        
        return {
            'valid': len(errors) == 0,
            'errors': errors
        }
    
    def _validate_ad_naming(self, ad_name: str) -> bool:
        """
        Valide convention nommage ad
        Format: "Ads T{tier} - V{version}" ou "Ads T{tier} - I{version}"
        """
        import re
        pattern = r'^Ads T\d+ - [VI]\d+$'
        return bool(re.match(pattern, ad_name))
    
    def _send_client_validation(self, request: ValidationRequest):
        """
        Envoie notification Slack pour validation client
        """
        print(f"   📤 Envoi validation: {request.ad_name} ({request.client_name})")
        
        # Construire message Slack
        message = self._build_validation_message(request)
        
        try:
            # Envoyer dans canal client
            response = self.slack.send_interactive_message(
                channel=request.validation_channel_id or f"#{request.validation_channel}",
                blocks=message['blocks'],
                text=message['fallback_text']
            )
            
            # Logger validation
            self.airtable.create_record(
                table='validation_logs',
                fields={
                    'ad_id': [request.ad_id],  # Link field
                    'client_key': request.client_key,
                    'sent_at': datetime.now().isoformat(),
                    'slack_message_ts': response['ts'],
                    'action': 'Sent'
                }
            )
            
            # Update status ad
            self.airtable.update_record(
                table='ads',
                record_id=request.ad_id,
                fields={
                    'status': AdStatus.EN_VALIDATION.value,
                    'validation_sent_at': datetime.now().isoformat()
                }
            )
            
            print(f"   ✅ Validation envoyée (message ts: {response['ts']})")
            
        except Exception as e:
            print(f"   ❌ Erreur envoi Slack: {e}")
            
            # Update avec erreur
            self.airtable.update_record(
                table='ads',
                record_id=request.ad_id,
                fields={
                    'status': AdStatus.ERREUR.value,
                    'notes': f"Erreur envoi Slack: {str(e)}"
                }
            )
    
    def _build_validation_message(self, request: ValidationRequest) -> Dict:
        """
        Construit le message Slack de validation
        """
        # Emojis et descriptions selon mode
        mode_config = {
            PublicationMode.AUTO.value: {
                'emoji': '🟢',
                'description': 'Activée immédiatement (dépense)'
            },
            PublicationMode.MANUEL.value: {
                'emoji': '🟡',
                'description': 'Publiée mais OFF (aucune dépense)'
            },
            PublicationMode.TEST.value: {
                'emoji': '🔵',
                'description': 'Mode Draft (test structure seulement)'
            }
        }
        
        mode = mode_config.get(
            request.publication_mode,
            {'emoji': '⚪', 'description': 'Mode inconnu'}
        )
        
        # Construire blocks
        blocks = [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": f"📢 Nouvelle Publicité à Valider - {request.client_name}",
                    "emoji": True
                }
            },
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": f"*Campaign:*\n`{request.campaign_name}`"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*AdSet:*\n`{request.adset_name}`"
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
                    "text": f"*🎨 CRÉATIVE*\n\n"
                            f"*HOOK:*\n_{request.hook}_\n\n"
                            f"*BODY:*\n{request.body[:500]}{'...' if len(request.body) > 500 else ''}\n\n"
                            f"*CTA:* {request.cta}"
                }
            }
        ]
        
        # Ajouter preview asset si disponible
        if request.asset_url:
            blocks.append({
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*📸 Asset ({request.asset_type}):*"
                },
                "accessory": {
                    "type": "image",
                    "image_url": request.asset_url,
                    "alt_text": "Asset preview"
                }
            })
        
        blocks.extend([
            {
                "type": "divider"
            },
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": f"{mode['emoji']} *Mode:* {request.publication_mode}"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"💰 *Budget:* ${request.budget_daily}/jour"
                    }
                ]
            },
            {
                "type": "context",
                "elements": [
                    {
                        "type": "mrkdwn",
                        "text": f"ℹ️ {mode['description']}"
                    }
                ]
            },
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "✅ Approuver",
                            "emoji": True
                        },
                        "style": "primary",
                        "value": json.dumps({
                            'action': 'approve',
                            'ad_id': request.ad_id
                        }),
                        "action_id": "approve_ad"
                    },
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "💬 Commentaire",
                            "emoji": True
                        },
                        "value": json.dumps({
                            'action': 'comment',
                            'ad_id': request.ad_id
                        }),
                        "action_id": "comment_ad"
                    },
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "❌ Rejeter",
                            "emoji": True
                        },
                        "style": "danger",
                        "value": json.dumps({
                            'action': 'reject',
                            'ad_id': request.ad_id
                        }),
                        "action_id": "reject_ad"
                    }
                ]
            }
        ])
        
        return {
            'blocks': blocks,
            'fallback_text': f"Nouvelle ad à valider: {request.ad_name}"
        }
    
    def handle_slack_interaction(self, payload: Dict):
        """
        Point d'entrée pour interactions Slack (appelé par webhook)
        """
        action = payload['actions'][0]
        action_id = action['action_id']
        value_data = json.loads(action['value'])
        user = payload['user']['name']
        
        ad_id = value_data['ad_id']
        action_type = value_data['action']
        
        print(f"\n📥 Interaction Slack: {action_type} par {user} (ad: {ad_id})")
        
        # Actions CLIENT
        if action_type == 'approve':
            self._handle_approval(ad_id, user, payload)
        
        elif action_type == 'comment':
            self._show_comment_modal(ad_id, payload)
        
        elif action_type == 'reject':
            self._handle_rejection(ad_id, user, payload)
        
        # Actions FINALE (DURUM)
        elif action_type == 'approve_final':
            self.handle_final_approval(ad_id, user, payload)
        
        elif action_type == 'reject_final':
            self.handle_final_rejection(ad_id, user, payload)
    
    def _handle_approval(self, ad_id: str, user: str, payload: Dict):
        """
        Traite l'approbation d'une ad par le CLIENT
        Change status → "Approuvé Client" (pas encore publié!)
        """
        try:
            # Update ad dans Airtable
            self.airtable.update_record(
                table='ads',
                record_id=ad_id,
                fields={
                    'status': AdStatus.APPROUVE_CLIENT.value,
                    'validated_by_client': user,
                    'validated_at_client': datetime.now().isoformat()
                }
            )
            
            # Update validation log
            logs = self.airtable.get_records(
                table='validation_logs',
                filter_by_formula=f"{{ad_id}} = '{ad_id}'"
            )
            
            if logs:
                self.airtable.update_record(
                    table='validation_logs',
                    record_id=logs[0]['id'],
                    fields={
                        'action': 'Approved by Client',
                        'validated_by': user,
                        'validated_at': datetime.now().isoformat()
                    }
                )
            
            # Update message Slack
            original_message = payload['message']
            original_message['blocks'].append({
                "type": "context",
                "elements": [{
                    "type": "mrkdwn",
                    "text": f"✅ *APPROUVÉ PAR CLIENT* ({user}) le {datetime.now().strftime('%Y-%m-%d %H:%M')}\n⏳ En attente validation finale équipe..."
                }]
            })
            
            # Remplacer boutons par statut
            for block in original_message['blocks']:
                if block.get('type') == 'actions':
                    original_message['blocks'].remove(block)
                    break
            
            self.slack.update_message(
                channel=payload['channel']['id'],
                ts=payload['message']['ts'],
                blocks=original_message['blocks']
            )
            
            print(f"   ✅ Ad approuvée par CLIENT ({user}) - En attente validation FINALE")
            
            # La validation finale sera envoyée au prochain cycle
            
        except Exception as e:
            print(f"   ❌ Erreur traitement approbation: {e}")
    
    def _show_comment_modal(self, ad_id: str, payload: Dict):
        """
        Affiche modal pour commentaire client
        """
        modal_view = {
            "type": "modal",
            "callback_id": json.dumps({'ad_id': ad_id}),
            "title": {
                "type": "plain_text",
                "text": "💬 Votre Commentaire"
            },
            "submit": {
                "type": "plain_text",
                "text": "Envoyer"
            },
            "close": {
                "type": "plain_text",
                "text": "Annuler"
            },
            "blocks": [
                {
                    "type": "input",
                    "block_id": "comment_text",
                    "label": {
                        "type": "plain_text",
                        "text": "Décrivez les modifications souhaitées"
                    },
                    "element": {
                        "type": "plain_text_input",
                        "action_id": "comment_input",
                        "multiline": True,
                        "placeholder": {
                            "type": "plain_text",
                            "text": "Ex: Changer le hook pour parler de résultats concrets plutôt que de problèmes..."
                        }
                    }
                },
                {
                    "type": "input",
                    "block_id": "priority",
                    "label": {
                        "type": "plain_text",
                        "text": "Priorité"
                    },
                    "element": {
                        "type": "radio_buttons",
                        "action_id": "priority_select",
                        "options": [
                            {
                                "text": {
                                    "type": "plain_text",
                                    "text": "⚪ Normale (24-48h)"
                                },
                                "value": "normal"
                            },
                            {
                                "text": {
                                    "type": "plain_text",
                                    "text": "🔴 Urgente (< 24h)"
                                },
                                "value": "urgent"
                            }
                        ],
                        "initial_option": {
                            "text": {
                                "type": "plain_text",
                                "text": "⚪ Normale (24-48h)"
                            },
                            "value": "normal"
                        }
                    }
                }
            ]
        }
        
        try:
            self.slack.open_modal(
                trigger_id=payload['trigger_id'],
                view=modal_view
            )
        except Exception as e:
            print(f"   ❌ Erreur ouverture modal: {e}")
    
    def handle_modal_submission(self, payload: Dict):
        """
        Traite la soumission du modal de commentaire
        """
        callback_data = json.loads(payload['view']['callback_id'])
        ad_id = callback_data['ad_id']
        
        values = payload['view']['state']['values']
        comment_text = values['comment_text']['comment_input']['value']
        priority = values['priority']['priority_select']['selected_option']['value']
        user = payload['user']['name']
        
        print(f"\n💬 Commentaire reçu de {user} (ad: {ad_id}, priorité: {priority})")
        
        try:
            # Créer objet commentaire
            comment = ClientComment(
                ad_id=ad_id,
                client_key='',  # Sera rempli depuis ad
                comment_text=comment_text,
                priority=priority,
                commented_by=user,
                commented_at=datetime.now()
            )
            
            # Update ad
            self.airtable.update_record(
                table='ads',
                record_id=ad_id,
                fields={
                    'status': AdStatus.COMMENTAIRE_CLIENT.value,
                    'client_comment': comment_text,
                    'validated_by': user,
                    'validated_at': datetime.now().isoformat()
                }
            )
            
            # Créer tâche
            ad_record = self.airtable.get_record('ads', ad_id)
            
            task_id = self.airtable.create_record(
                table='tasks',
                fields={
                    'task_type': 'Client Feedback - Ad',
                    'title': f"Modifications Ad - {ad_record['fields']['ad_name']}",
                    'description': comment_text,
                    'related_ad': [ad_id],
                    'related_client': ad_record['fields']['client_key'],
                    'assigned_to': 'Équipe Création',
                    'priority': 'High' if priority == 'urgent' else 'Normal',
                    'status': 'To Do',
                    'due_date': (datetime.now() + timedelta(days=1 if priority == 'urgent' else 2)).strftime('%Y-%m-%d')
                }
            )
            
            # Notifier équipe DURUM
            priority_emoji = '🚨' if priority == 'urgent' else '📝'
            
            self.slack.send_message(
                channel='team-durum',
                text=f"{priority_emoji} {'URGENT - ' if priority == 'urgent' else ''}Commentaire client sur Ad\n\n"
                     f"*Client:* {user}\n"
                     f"*Ad:* {ad_record['fields']['ad_name']}\n"
                     f"*Commentaire:*\n{comment_text}\n\n"
                     f"✅ Tâche créée dans Airtable (ID: {task_id})\n"
                     f"⏰ Due: {(datetime.now() + timedelta(days=1 if priority == 'urgent' else 2)).strftime('%Y-%m-%d')}"
            )
            
            # Confirmer au client (DM)
            self.slack.send_dm(
                user_id=payload['user']['id'],
                text="✅ Merci! Votre commentaire a été enregistré.\n\n"
                     f"Notre équipe y travaille et vous reviendra {'sous 24h' if priority == 'urgent' else 'sous 48h'}. 🚀"
            )
            
            print(f"   ✅ Commentaire traité, tâche créée (ID: {task_id})")
            
        except Exception as e:
            print(f"   ❌ Erreur traitement commentaire: {e}")
    
    def _handle_rejection(self, ad_id: str, user: str, payload: Dict):
        """
        Traite le rejet d'une ad
        """
        try:
            # Update ad
            self.airtable.update_record(
                table='ads',
                record_id=ad_id,
                fields={
                    'status': AdStatus.ARCHIVE.value,
                    'validated_by': user,
                    'validated_at': datetime.now().isoformat(),
                    'notes': f"❌ Rejetée par {user}"
                }
            )
            
            # Update message
            self.slack.update_message(
                channel=payload['channel']['id'],
                ts=payload['message']['ts'],
                text=f"❌ *REJETÉE* par {user}"
            )
            
            print(f"   ❌ Ad rejetée par {user}")
            
        except Exception as e:
            print(f"   ❌ Erreur traitement rejet: {e}")
    
    def _get_client_approved_ads(self) -> List[Dict]:
        """
        Récupère ads approuvées par CLIENT (en attente validation finale)
        """
        formula = f"{{status}} = '{AdStatus.APPROUVE_CLIENT.value}'"
        
        return self.airtable.get_records(
            table='ads',
            filter_by_formula=formula
        )
    
    def _send_final_validation(self, ad_record: Dict):
        """
        Envoie validation FINALE à l'équipe (vous)
        """
        ad_id = ad_record['id']
        fields = ad_record['fields']
        
        print(f"   📤 Envoi validation FINALE: {fields['ad_name']}")
        
        # Construire message pour votre équipe
        message_blocks = [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": f"🎯 VALIDATION FINALE REQUISE",
                    "emoji": True
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Client:* {fields.get('client_name', 'N/A')}\n"
                            f"*Approuvé par:* {fields.get('validated_by_client', 'Client')} le {fields.get('validated_at_client', 'N/A')}"
                }
            },
            {
                "type": "divider"
            },
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": f"*Campaign:*\n`{fields['campaign_name']}`"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*AdSet:*\n`{fields['adset_name']}`"
                    }
                ]
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*🎨 CRÉATIVE*\n\n"
                            f"*HOOK:*\n_{fields.get('copy_hook', '')}_\n\n"
                            f"*BODY:*\n{fields.get('copy_body', '')[:500]}\n\n"
                            f"*CTA:* {fields.get('copy_cta', 'N/A')}"
                }
            },
            {
                "type": "divider"
            },
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": f"*Mode:* {fields.get('publication_mode', 'N/A')}"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*Budget:* ${fields.get('budget_daily', 0)}/jour"
                    }
                ]
            },
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "✅ Approuver & Publier",
                            "emoji": True
                        },
                        "style": "primary",
                        "value": json.dumps({
                            'action': 'approve_final',
                            'ad_id': ad_id
                        }),
                        "action_id": "approve_final"
                    },
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "❌ Rejeter",
                            "emoji": True
                        },
                        "style": "danger",
                        "value": json.dumps({
                            'action': 'reject_final',
                            'ad_id': ad_id
                        }),
                        "action_id": "reject_final"
                    }
                ]
            }
        ]
        
        try:
            # Envoyer dans canal équipe
            team_channel = os.getenv('SLACK_CHANNEL_TEAM', 'team-durum')
            
            response = self.slack.send_interactive_message(
                channel=f"#{team_channel}",
                blocks=message_blocks,
                text=f"Validation finale requise: {fields['ad_name']}"
            )
            
            # Update status
            self.airtable.update_record(
                table='ads',
                record_id=ad_id,
                fields={
                    'status': AdStatus.EN_VALIDATION_FINALE.value,
                    'final_validation_sent_at': datetime.now().isoformat(),
                    'final_validation_message_ts': response['ts']
                }
            )
            
            print(f"   ✅ Validation finale envoyée (#{team_channel})")
            
        except Exception as e:
            print(f"   ❌ Erreur envoi validation finale: {e}")
    
    def _get_final_approved_ads(self) -> List[Dict]:
        """
        Récupère ads approuvées FINALEMENT (par vous)
        """
        formula = f"{{status}} = '{AdStatus.APPROUVE_FINAL.value}'"
        
        return self.airtable.get_records(
            table='ads',
            filter_by_formula=formula
        )
    
    def handle_final_approval(self, ad_id: str, user: str, payload: Dict):
        """
        Traite approbation FINALE (par vous)
        """
        try:
            # Update ad
            self.airtable.update_record(
                table='ads',
                record_id=ad_id,
                fields={
                    'status': AdStatus.APPROUVE_FINAL.value,
                    'validated_by_final': user,
                    'validated_at_final': datetime.now().isoformat()
                }
            )
            
            # Update message
            self.slack.update_message(
                channel=payload['channel']['id'],
                ts=payload['message']['ts'],
                text=f"✅ *APPROUVÉ FINAL* par {user} - Publication en cours..."
            )
            
            print(f"   ✅ Approbation FINALE par {user} - Prêt pour publication")
            
        except Exception as e:
            print(f"   ❌ Erreur approbation finale: {e}")
    
    def handle_final_rejection(self, ad_id: str, user: str, payload: Dict):
        """
        Traite rejet final (par vous)
        """
        try:
            # Update ad
            self.airtable.update_record(
                table='ads',
                record_id=ad_id,
                fields={
                    'status': AdStatus.ARCHIVE.value,
                    'validated_by_final': user,
                    'validated_at_final': datetime.now().isoformat(),
                    'notes': f"❌ Rejetée en validation finale par {user}"
                }
            )
            
            # Update message
            self.slack.update_message(
                channel=payload['channel']['id'],
                ts=payload['message']['ts'],
                text=f"❌ *REJETÉE* par {user}"
            )
            
            print(f"   ❌ Rejetée en validation finale par {user}")
            
        except Exception as e:
            print(f"   ❌ Erreur rejet final: {e}")
    
    def _check_client_validation_timeouts(self):
        """
        Vérifie validations CLIENT en timeout (24h sans réponse)
        Envoie RAPPEL au client
        """
        # Calculer date limite (24h)
        timeout_date = datetime.now() - timedelta(hours=24)
        
        # Chercher ads en validation client depuis >24h
        formula = f"AND({{status}} = '{AdStatus.EN_VALIDATION_CLIENT.value}', {{validation_sent_at}} < '{timeout_date.isoformat()}')"
        
        timedout_ads = self.airtable.get_records(
            table='ads',
            filter_by_formula=formula
        )
        
        for ad in timedout_ads:
            ad_id = ad['id']
            fields = ad['fields']
            
            print(f"   ⏰ Timeout validation CLIENT (24h): {fields['ad_name']}")
            
            # Vérifier si rappel déjà envoyé
            if fields.get('reminder_sent_at'):
                last_reminder = datetime.fromisoformat(fields['reminder_sent_at'])
                hours_since_reminder = (datetime.now() - last_reminder).total_seconds() / 3600
                
                if hours_since_reminder < 24:
                    # Rappel déjà envoyé il y a moins de 24h, skip
                    continue
            
            # Envoyer RAPPEL au client
            client_channel = fields.get('validation_channel_id') or f"#{fields.get('validation_channel', 'validation')}"
            
            self.slack.send_message(
                channel=client_channel,
                text=f"⏰ *RAPPEL - Validation en Attente*\n\n"
                     f"La publicité suivante attend votre validation depuis plus de 24h:\n\n"
                     f"*Ad:* {fields['ad_name']}\n"
                     f"*Campaign:* {fields['campaign_name']}\n\n"
                     f"Merci de valider dès que possible! 🙏"
            )
            
            # Notifier équipe aussi
            self.slack.send_message(
                channel='team-durum',
                text=f"⏰ Rappel envoyé au client: {fields.get('client_name', 'N/A')}\n"
                     f"Ad en attente validation depuis >24h: {fields['ad_name']}"
            )
            
            # Update timestamp rappel
            self.airtable.update_record(
                table='ads',
                record_id=ad_id,
                fields={
                    'reminder_sent_at': datetime.now().isoformat()
                }
            )
            
            print(f"   ✅ Rappel envoyé au client")
    
    def _check_final_validation_delays(self):
        """
        Vérifie ads en attente validation FINALE depuis 24h+
        Envoie RAPPEL à l'équipe (vous)
        """
        # Date limite (24h)
        delay_date = datetime.now() - timedelta(hours=24)
        
        # Chercher ads en validation finale depuis >24h
        formula = f"AND({{status}} = '{AdStatus.EN_VALIDATION_FINALE.value}', {{final_validation_sent_at}} < '{delay_date.isoformat()}')"
        
        delayed_ads = self.airtable.get_records(
            table='ads',
            filter_by_formula=formula
        )
        
        for ad in delayed_ads:
            fields = ad['fields']
            
            print(f"   ⏰ Délai validation FINALE (24h): {fields['ad_name']}")
            
            # Vérifier si rappel déjà envoyé
            if fields.get('final_reminder_sent_at'):
                last_reminder = datetime.fromisoformat(fields['final_reminder_sent_at'])
                hours_since_reminder = (datetime.now() - last_reminder).total_seconds() / 3600
                
                if hours_since_reminder < 24:
                    continue
            
            # Envoyer RAPPEL équipe
            self.slack.send_message(
                channel='team-durum',
                text=f"⏰🚨 *RAPPEL URGENT - Validation Finale en Attente*\n\n"
                     f"Cette ad attend VOTRE validation depuis plus de 24h:\n\n"
                     f"*Client:* {fields.get('client_name', 'N/A')}\n"
                     f"*Ad:* {fields['ad_name']}\n"
                     f"*Approuvée par client:* {fields.get('validated_by_client', 'N/A')}\n\n"
                     f"⚠️ Le client attend la publication!"
            )
            
            # Update timestamp
            self.airtable.update_record(
                table='ads',
                record_id=ad['id'],
                fields={
                    'final_reminder_sent_at': datetime.now().isoformat()
                }
            )
            
            print(f"   ✅ Rappel validation finale envoyé à l'équipe")
    
    def _publish_ad_to_meta(self, ad_record: Dict):
        """
        Publie une ad approuvée sur Meta
        """
        ad_id = ad_record['id']
        fields = ad_record['fields']
        
        print(f"   🚀 Publication: {fields['ad_name']}")
        
        try:
            # Préparer données pour Meta
            publication_mode = fields.get('publication_mode', PublicationMode.MANUEL.value)
            
            meta_status = {
                PublicationMode.AUTO.value: 'ACTIVE',
                PublicationMode.MANUEL.value: 'PAUSED',
                PublicationMode.TEST.value: 'DRAFT'
            }.get(publication_mode, 'PAUSED')
            
            # Publier
            result = self.meta.create_ad(
                campaign_id=fields['campaign_meta_id'],
                adset_id=fields['adset_meta_id'],
                creative_data={
                    'name': fields['ad_name'],
                    'message': f"{fields['copy_hook']}\n\n{fields['copy_body']}",
                    'link': fields.get('landing_url', ''),
                    'call_to_action_type': fields['copy_cta'].upper().replace(' ', '_'),
                    'image_hash': fields.get('asset_hash'),  # ou video_id
                },
                status=meta_status
            )
            
            # Update Airtable avec succès
            self.airtable.update_record(
                table='ads',
                record_id=ad_id,
                fields={
                    'status': AdStatus.PUBLIE.value,
                    'meta_ad_id': result['id'],
                    'meta_status': meta_status,
                    'published_at': datetime.now().isoformat(),
                    'published_by': 'agent'
                }
            )
            
            # Notifier succès
            channel = fields.get('validation_channel', 'validation')
            
            self.slack.send_message(
                channel=channel,
                text=f"✅ *Ad publiée avec succès sur Meta*\n\n"
                     f"*Nom:* {fields['ad_name']}\n"
                     f"*Meta Ad ID:* `{result['id']}`\n"
                     f"*Status:* {meta_status}\n"
                     f"*Mode:* {publication_mode}"
            )
            
            print(f"   ✅ Publié (Meta ID: {result['id']}, Status: {meta_status})")
            
        except Exception as e:
            print(f"   ❌ Erreur publication Meta: {e}")
            
            # Update avec erreur
            self.airtable.update_record(
                table='ads',
                record_id=ad_id,
                fields={
                    'status': AdStatus.ERREUR.value,
                    'notes': f"❌ Erreur publication: {str(e)}"
                }
            )
            
            # Alerter équipe
            self.slack.send_message(
                channel='alerts-urgent',
                text=f"🚨 *Erreur Publication Ad*\n\n"
                     f"*Ad:* {fields['ad_name']}\n"
                     f"*Erreur:* {str(e)}"
            )
    
    def _get_ads_with_comments(self) -> List[Dict]:
        """
        Récupère ads avec status "Commentaire Client" non traitées
        """
        # Déjà traité dans handle_modal_submission
        # Cette méthode peut servir pour re-check ou notifications
        return []
    
    def _process_client_comment(self, ad_record: Dict):
        """
        Traite un commentaire client (déjà fait dans modal)
        """
        pass  # Géré dans handle_modal_submission
    
    def _check_validation_timeouts(self):
        """
        Vérifie si des validations ont timeout (> X heures sans réponse)
        """
        # Calculer date limite
        timeout_date = datetime.now() - timedelta(hours=self.validation_timeout_hours)
        
        # Chercher ads en validation depuis trop longtemps
        formula = f"AND({{status}} = '{AdStatus.EN_VALIDATION.value}', {{validation_sent_at}} < '{timeout_date.isoformat()}')"
        
        timedout_ads = self.airtable.get_records(
            table='ads',
            filter_by_formula=formula
        )
        
        for ad in timedout_ads:
            print(f"   ⏰ Timeout validation: {ad['fields']['ad_name']}")
            
            # Notifier équipe
            self.slack.send_message(
                channel='team-durum',
                text=f"⏰ *Timeout Validation*\n\n"
                     f"Ad '{ad['fields']['ad_name']}' en attente validation depuis > {self.validation_timeout_hours}h\n"
                     f"Action requise!"
            )
            
            # Optionnel: Remettre en brouillon ou autre status
            # self.airtable.update_record(...)


# Point d'entrée
if __name__ == '__main__':
    workflow = PublishingWorkflow()
    workflow.start()
