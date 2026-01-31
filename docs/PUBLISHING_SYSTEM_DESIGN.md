# 🚀 SYSTÈME DE PUBLICATION AVEC VALIDATION CLIENT

## 🎯 Architecture Complète

### Workflow Global

```
Airtable (Source de Vérité)
    ↓
Agent (Détection nouvelles ads)
    ↓
Validation Client (Slack)
    ↓ [Approuvé]
Meta Ads API (Publication)
    ↓
Airtable (Update status)
```

---

## 📊 STRUCTURE AIRTABLE REQUISE

### Table: **ads**

#### Colonnes Essentielles

| Champ | Type | Options | Description |
|-------|------|---------|-------------|
| **ad_id** | Text (Primary) | Auto-increment | ID unique |
| **ad_name** | Text | Required | Nom selon convention |
| **client_key** | Link to Clients | Required | Client propriétaire |
| **campaign_id** | Link to Campaigns | Required | Campaign parent |
| **adset_id** | Link to AdSets | Required | AdSet parent |
| **asset_id** | Link to Assets | Required | Asset (image/vidéo) |
| **copy_hook** | Long Text | | Hook de l'ad |
| **copy_body** | Long Text | | Corps de texte |
| **copy_cta** | Single Select | Learn More, Sign Up, Apply Now, etc. | Call-to-action |

#### **NOUVEAU: Colonnes Workflow**

| Champ | Type | Options | Description | **CRITIQUE** |
|-------|------|---------|-------------|--------------|
| **status** | Single Select | Brouillon, Prêt pour Validation, En Validation, Approuvé, Commentaire Client, Publié, Actif, Pause, Archivé | État dans le workflow | ⭐ |
| **publication_mode** | Single Select | Auto (publish ON), Manuel (publish OFF), Test (draft) | Mode de publication | ⭐ |
| **validation_channel** | Text | Auto-filled | Canal Slack pour validation | |
| **validated_by** | Text | Auto-filled | Qui a validé (nom client) | |
| **validated_at** | DateTime | Auto-filled | Quand validé | |
| **client_comment** | Long Text | | Commentaire du client si rejet | |
| **meta_ad_id** | Text | Auto-filled | ID Meta après publication | |
| **published_at** | DateTime | Auto-filled | Date de publication | |
| **published_by** | Text | Auto-filled | agent | |
| **meta_status** | Text | Auto-filled | ACTIVE, PAUSED | Status Meta réel |

#### Colonnes Optionnelles (Tracking)

| Champ | Type | Description |
|-------|------|-------------|
| **created_at** | Created Time | Date création dans Airtable |
| **last_modified** | Last Modified | Dernière modification |
| **created_by** | Created By | Qui a créé |
| **priority** | Single Select | Low, Medium, High, Urgent |
| **notes** | Long Text | Notes internes |

---

## 🎨 STATUTS WORKFLOW

### Status disponibles

```python
STATUS_WORKFLOW = {
    # Phase Création (Vous)
    "Brouillon": {
        "description": "Ad en cours de création",
        "action_bot": None,  # Bot ignore
        "color": "gray"
    },
    
    # Phase Validation (Automatique)
    "Prêt pour Validation": {
        "description": "Ad prête, en attente envoi client",
        "action_bot": "detect_and_send_validation",
        "color": "yellow"
    },
    
    "En Validation": {
        "description": "Envoyé au client, attente réponse",
        "action_bot": "wait_for_response",
        "color": "orange"
    },
    
    # Phase Résultats Validation
    "Approuvé": {
        "description": "Client a approuvé, prêt publication",
        "action_bot": "publish_to_meta",
        "color": "green"
    },
    
    "Commentaire Client": {
        "description": "Client a laissé commentaire",
        "action_bot": "create_task_for_team",
        "color": "red"
    },
    
    # Phase Post-Publication
    "Publié": {
        "description": "Publié sur Meta, en attente activation",
        "action_bot": "monitor",
        "color": "blue"
    },
    
    "Actif": {
        "description": "Actif sur Meta (spending)",
        "action_bot": "monitor",
        "color": "green"
    },
    
    "Pause": {
        "description": "Pausé sur Meta",
        "action_bot": "monitor",
        "color": "gray"
    },
    
    "Archivé": {
        "description": "Archivé, hors système",
        "action_bot": None,
        "color": "black"
    }
}
```

---

## 🔄 PUBLICATION MODES

### Modes disponibles

```python
PUBLICATION_MODES = {
    "Auto": {
        "description": "Publier avec status ACTIVE (ON)",
        "meta_status": "ACTIVE",
        "budget_active": True,
        "use_case": "Ads approuvées prêtes à dépenser"
    },
    
    "Manuel": {
        "description": "Publier avec status PAUSED (OFF)",
        "meta_status": "PAUSED",
        "budget_active": False,
        "use_case": "Ads à activer manuellement plus tard"
    },
    
    "Test": {
        "description": "Créer en DRAFT (non publié)",
        "meta_status": "DRAFT",
        "budget_active": False,
        "use_case": "Tester structure sans publier réellement"
    }
}
```

---

## 🎯 WORKFLOW DÉTAILLÉ

### Étape 1: Création dans Airtable (Vous)

```
Vous dans Airtable:
1. Créer nouvelle ligne dans table "ads"
2. Remplir tous les champs requis
3. Sélectionner status: "Brouillon"
4. Travailler sur le copy, assets, etc.

→ Bot IGNORE les ads en "Brouillon"
```

### Étape 2: Prêt pour Validation (Vous)

```
Quand prêt:
1. Vérifier que tout est OK
2. Changer status: "Brouillon" → "Prêt pour Validation"
3. Sélectionner publication_mode:
   - "Auto" si doit être ON après validation
   - "Manuel" si doit rester OFF
   - "Test" si mode draft

→ Bot DÉTECTE cette ad au prochain cycle (1 min)
```

### Étape 3: Détection par le Bot

```python
# Bot cycle (toutes les 1 min)
def detect_new_ads_for_validation():
    """
    Cherche ads avec status = "Prêt pour Validation"
    """
    ads = airtable.get_ads(
        filter_by_formula="{status} = 'Prêt pour Validation'"
    )
    
    for ad in ads:
        # Valider structure
        if validate_ad_structure(ad):
            # Envoyer validation client
            send_client_validation(ad)
            
            # Update status
            airtable.update_ad(ad['id'], {
                'status': 'En Validation',
                'validation_sent_at': datetime.now()
            })
```

### Étape 4: Notification Slack Client

```
Message dans #client-avego-validation:

📢 Nouvelle Publicité à Valider

Client: Avego
Campaign: [BOOTCAMP] TOF _CONV.LEADS _TEST
AdSet: STACK_H:25/65+ _QC _FEED+ _Ads T4

🎨 Créative:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
HOOK:
"97% des traders font cette erreur..."

BODY:
"Découvrez la stratégie que les pros utilisent...
[150 mots]
✅ Formation complète
✅ Support 24/7
✅ Garantie 30 jours"

CTA: Télécharger Maintenant
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📸 Asset: [Lien vers preview image/vidéo]

🎯 Publication prévue: ACTIVE (dépense immédiate)
💰 Budget: $150/jour

[✅ Approuver] [💬 Laisser Commentaire] [❌ Rejeter]
```

### Étape 5a: Client Approuve

```
Client clique "✅ Approuver"

Bot reçoit callback:
1. Update Airtable:
   - status: "En Validation" → "Approuvé"
   - validated_by: "Marc Tremblay"
   - validated_at: 2025-01-31 14:23:00

2. Publication immédiate sur Meta

3. Update Airtable après publication:
   - status: "Approuvé" → "Publié"
   - meta_ad_id: "120206848382020123"
   - meta_status: "ACTIVE" (ou "PAUSED" selon mode)
   - published_at: 2025-01-31 14:23:15

4. Notification Slack:
   "✅ Ad approuvée et publiée sur Meta (ID: 120206848382020123)"
```

### Étape 5b: Client Laisse Commentaire

```
Client clique "💬 Laisser Commentaire"

Slack affiche modal:
┌─────────────────────────────────────┐
│ 💬 Commentaire sur l'Ad             │
├─────────────────────────────────────┤
│                                     │
│ [Textbox multi-ligne]               │
│ Ex: "Changer le hook pour parler    │
│      de résultats concrets"         │
│                                     │
│                                     │
│ Priorité: [●] Normale  [ ] Urgente │
│                                     │
│ [Annuler]            [Envoyer] ✓   │
└─────────────────────────────────────┘

Client envoie commentaire:

Bot reçoit:
1. Update Airtable ads:
   - status: "Commentaire Client"
   - client_comment: "Changer le hook pour..."
   - priority: "Urgente" (si sélectionné)

2. Créer tâche dans Airtable table "tasks":
   - task_type: "Client Feedback - Ad"
   - related_ad: [lien vers ad]
   - description: Commentaire du client
   - assigned_to: "Équipe Création"
   - priority: "High"
   - due_date: Aujourd'hui + 1 jour
   - status: "To Do"

3. Notification Slack #team-durum:
   "🚨 URGENT - Commentaire client sur Ad (Avego)
   
   Ad: [BOOTCAMP] TOF... / Ads T4 - V1
   Commentaire: 'Changer le hook pour...'
   
   ✅ Tâche créée dans Airtable
   📋 Assigned to: Équipe Création
   ⏰ Due: 2025-02-01"

4. Notification Slack client (confirmation):
   "✅ Votre commentaire a été enregistré.
   Notre équipe travaille dessus et vous reviendra sous 24h."
```

### Étape 6: Après Corrections (Si commentaire)

```
Vous dans Airtable:
1. Corriger l'ad selon commentaire client
2. Marquer tâche comme "Done"
3. Changer status ad: "Commentaire Client" → "Prêt pour Validation"

→ Bot RE-envoie pour validation (nouveau cycle)
```

---

## 🔧 TABLES AIRTABLE SUPPLÉMENTAIRES

### Table: **tasks** (NOUVELLE)

Pour tracking des tâches générées par commentaires clients.

| Champ | Type | Description |
|-------|------|-------------|
| task_id | Auto Number | ID unique |
| task_type | Single Select | Client Feedback - Ad, Bug, Feature Request, etc. |
| title | Text | Titre court |
| description | Long Text | Description complète |
| related_ad | Link to ads | Ad concernée (si applicable) |
| related_client | Link to clients | Client concerné |
| assigned_to | Single Select | Équipe Création, Alex, etc. |
| priority | Single Select | Low, Normal, High, Urgent |
| status | Single Select | To Do, In Progress, Done, Cancelled |
| created_at | Created Time | Auto |
| due_date | Date | Échéance |
| completed_at | DateTime | Quand complété |

---

### Table: **validation_logs** (NOUVELLE)

Historique de toutes les validations.

| Champ | Type | Description |
|-------|------|-------------|
| log_id | Auto Number | ID unique |
| ad_id | Link to ads | Ad concernée |
| client_key | Link to clients | Client |
| sent_at | DateTime | Quand envoyé pour validation |
| action | Single Select | Approved, Commented, Rejected, Timeout |
| validated_by | Text | Nom de la personne |
| validated_at | DateTime | Quand répondu |
| comment | Long Text | Commentaire si applicable |
| slack_message_ts | Text | Timestamp message Slack (pour édition) |

---

## 💬 CONFIGURATION SLACK

### Canaux Requis

```
Structure Slack:

#client-avego-validation      → Validation ads Avego
#client-client2-validation    → Validation ads Client2
#client-client3-validation    → Validation ads Client3

#team-durum                   → Notifications internes
#alerts-urgent                → Alertes urgentes
```

### Mapping Client → Canal

Dans Airtable table **clients**, ajouter:

| Champ | Type | Exemple |
|-------|------|---------|
| **slack_validation_channel** | Text | client-avego-validation |
| **slack_channel_id** | Text | C04ABC123XYZ |

---

## 🤖 CODE SYSTÈME

### Module: `publishing/validation_workflow.py`

```python
"""
Système de validation client et publication automatique
"""

import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from dataclasses import dataclass

from airtable import AirtableClient
from slack import SlackClient
from meta import MetaPublisher


@dataclass
class AdForValidation:
    """Ad prête pour validation client"""
    ad_id: str
    client_key: str
    ad_name: str
    campaign_name: str
    adset_name: str
    
    hook: str
    body: str
    cta: str
    asset_url: str
    
    publication_mode: str  # Auto, Manuel, Test
    budget_daily: float
    
    validation_channel: str
    

class ValidationWorkflow:
    """
    Gère le workflow complet de validation client
    """
    
    def __init__(
        self,
        airtable_client: AirtableClient,
        slack_client: SlackClient,
        meta_publisher: MetaPublisher
    ):
        self.airtable = airtable_client
        self.slack = slack_client
        self.meta = meta_publisher
    
    def run_validation_cycle(self):
        """
        Cycle principal - Exécuté toutes les 1 minute
        """
        # 1. Détecter ads "Prêt pour Validation"
        new_ads = self._detect_new_ads_for_validation()
        
        for ad in new_ads:
            self._send_client_validation(ad)
        
        # 2. Publier ads "Approuvé"
        approved_ads = self._get_approved_ads()
        
        for ad in approved_ads:
            self._publish_ad(ad)
        
        # 3. Traiter commentaires clients
        commented_ads = self._get_commented_ads()
        
        for ad in commented_ads:
            self._process_client_comment(ad)
    
    def _detect_new_ads_for_validation(self) -> List[AdForValidation]:
        """
        Détecte nouvelles ads prêtes pour validation
        """
        # Chercher dans Airtable
        records = self.airtable.get_ads(
            filter_by_formula="{status} = 'Prêt pour Validation'"
        )
        
        ads = []
        
        for record in records:
            # Valider structure
            if not self._validate_ad_structure(record):
                # Invalide → Mettre commentaire dans Airtable
                self.airtable.update_ad(record['id'], {
                    'status': 'Brouillon',
                    'notes': f"⚠️ Structure invalide - Vérifier convention nommage"
                })
                continue
            
            # Récupérer infos client
            client = self.airtable.get_client(record['fields']['client_key'])
            
            ad = AdForValidation(
                ad_id=record['id'],
                client_key=record['fields']['client_key'],
                ad_name=record['fields']['ad_name'],
                campaign_name=record['fields']['campaign_name'],
                adset_name=record['fields']['adset_name'],
                hook=record['fields'].get('copy_hook', ''),
                body=record['fields'].get('copy_body', ''),
                cta=record['fields'].get('copy_cta', 'Learn More'),
                asset_url=record['fields'].get('asset_url', ''),
                publication_mode=record['fields'].get('publication_mode', 'Manuel'),
                budget_daily=record['fields'].get('budget_daily', 100),
                validation_channel=client['slack_validation_channel']
            )
            
            ads.append(ad)
        
        return ads
    
    def _send_client_validation(self, ad: AdForValidation):
        """
        Envoie notification Slack pour validation client
        """
        # Déterminer emoji selon mode
        mode_emoji = {
            'Auto': '🟢',
            'Manuel': '🟡',
            'Test': '🔵'
        }
        
        mode_description = {
            'Auto': 'Activée immédiatement (dépense)',
            'Manuel': 'Publiée mais OFF (pas de dépense)',
            'Test': 'Mode Draft (test structure)'
        }
        
        # Construire message
        message_blocks = [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": "📢 Nouvelle Publicité à Valider",
                    "emoji": True
                }
            },
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": f"*Campaign:*\n{ad.campaign_name}"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*AdSet:*\n{ad.adset_name}"
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
                    "text": f"*🎨 CRÉATIVE*\n\n*HOOK:*\n_{ad.hook}_\n\n*BODY:*\n{ad.body}\n\n*CTA:* {ad.cta}"
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
                        "text": f"{mode_emoji[ad.publication_mode]} *Mode:* {ad.publication_mode}"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"💰 *Budget:* ${ad.budget_daily}/jour"
                    }
                ]
            },
            {
                "type": "context",
                "elements": [
                    {
                        "type": "mrkdwn",
                        "text": f"ℹ️ {mode_description[ad.publication_mode]}"
                    }
                ]
            }
        ]
        
        # Si asset (image/vidéo), ajouter preview
        if ad.asset_url:
            message_blocks.insert(4, {
                "type": "image",
                "image_url": ad.asset_url,
                "alt_text": "Asset preview"
            })
        
        # Boutons d'action
        message_blocks.append({
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
                    "value": f"approve_{ad.ad_id}",
                    "action_id": "approve_ad"
                },
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "💬 Commentaire",
                        "emoji": True
                    },
                    "value": f"comment_{ad.ad_id}",
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
                    "value": f"reject_{ad.ad_id}",
                    "action_id": "reject_ad"
                }
            ]
        })
        
        # Envoyer message
        response = self.slack.send_message(
            channel=ad.validation_channel,
            blocks=message_blocks
        )
        
        # Logger dans Airtable
        self.airtable.create_validation_log({
            'ad_id': ad.ad_id,
            'client_key': ad.client_key,
            'sent_at': datetime.now().isoformat(),
            'slack_message_ts': response['ts']
        })
        
        # Update status ad
        self.airtable.update_ad(ad.ad_id, {
            'status': 'En Validation',
            'validation_sent_at': datetime.now().isoformat()
        })
    
    def handle_slack_interaction(self, payload: Dict):
        """
        Gère les interactions Slack (boutons cliqués)
        """
        action = payload['actions'][0]
        action_id = action['action_id']
        value = action['value']
        user = payload['user']['name']
        
        # Extraire ad_id
        ad_id = value.split('_')[1]
        
        if action_id == 'approve_ad':
            self._handle_approval(ad_id, user, payload)
        
        elif action_id == 'comment_ad':
            self._handle_comment_request(ad_id, user, payload)
        
        elif action_id == 'reject_ad':
            self._handle_rejection(ad_id, user, payload)
    
    def _handle_approval(self, ad_id: str, user: str, payload: Dict):
        """
        Gère l'approbation d'une ad
        """
        # Update Airtable
        self.airtable.update_ad(ad_id, {
            'status': 'Approuvé',
            'validated_by': user,
            'validated_at': datetime.now().isoformat()
        })
        
        # Update validation log
        self.airtable.update_validation_log_by_ad(ad_id, {
            'action': 'Approved',
            'validated_by': user,
            'validated_at': datetime.now().isoformat()
        })
        
        # Update message Slack (ajouter confirmation)
        self.slack.update_message(
            channel=payload['channel']['id'],
            ts=payload['message']['ts'],
            text=f"✅ *APPROUVÉ* par {user} le {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        )
        
        # Publication sera faite au prochain cycle (automatique)
    
    def _handle_comment_request(self, ad_id: str, user: str, payload: Dict):
        """
        Ouvre modal pour commentaire client
        """
        # Ouvrir modal Slack
        self.slack.open_modal(
            trigger_id=payload['trigger_id'],
            view={
                "type": "modal",
                "callback_id": f"comment_modal_{ad_id}",
                "title": {
                    "type": "plain_text",
                    "text": "💬 Commentaire"
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
                        "element": {
                            "type": "plain_text_input",
                            "action_id": "comment",
                            "multiline": True,
                            "placeholder": {
                                "type": "plain_text",
                                "text": "Décrivez les modifications souhaitées..."
                            }
                        },
                        "label": {
                            "type": "plain_text",
                            "text": "Votre commentaire"
                        }
                    },
                    {
                        "type": "input",
                        "block_id": "priority",
                        "element": {
                            "type": "radio_buttons",
                            "action_id": "priority_select",
                            "options": [
                                {
                                    "text": {
                                        "type": "plain_text",
                                        "text": "Normale"
                                    },
                                    "value": "normal"
                                },
                                {
                                    "type": "plain_text",
                                    "text": "Urgente"
                                    },
                                    "value": "urgent"
                                }
                            ],
                            "initial_option": {
                                "text": {
                                    "type": "plain_text",
                                    "text": "Normale"
                                },
                                "value": "normal"
                            }
                        },
                        "label": {
                            "type": "plain_text",
                            "text": "Priorité"
                        }
                    }
                ]
            }
        )
    
    def handle_modal_submission(self, payload: Dict):
        """
        Gère la soumission du modal de commentaire
        """
        callback_id = payload['view']['callback_id']
        ad_id = callback_id.split('_')[-1]
        
        values = payload['view']['state']['values']
        comment_text = values['comment_text']['comment']['value']
        priority = values['priority']['priority_select']['selected_option']['value']
        user = payload['user']['name']
        
        # Update ad dans Airtable
        self.airtable.update_ad(ad_id, {
            'status': 'Commentaire Client',
            'client_comment': comment_text,
            'validated_by': user,
            'validated_at': datetime.now().isoformat()
        })
        
        # Créer tâche
        task_id = self.airtable.create_task({
            'task_type': 'Client Feedback - Ad',
            'title': f"Modifications Ad - {ad_id}",
            'description': comment_text,
            'related_ad': ad_id,
            'assigned_to': 'Équipe Création',
            'priority': 'High' if priority == 'urgent' else 'Normal',
            'status': 'To Do',
            'due_date': (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
        })
        
        # Notifier équipe
        self.slack.send_message(
            channel='team-durum',
            text=f"🚨 {'URGENT - ' if priority == 'urgent' else ''}Commentaire client sur Ad\n\n"
                 f"*Ad:* {ad_id}\n"
                 f"*Client:* {user}\n"
                 f"*Commentaire:* {comment_text}\n\n"
                 f"✅ Tâche créée: #{task_id}"
        )
        
        # Confirmer au client
        self.slack.send_message(
            channel=payload['user']['id'],  # DM
            text="✅ Votre commentaire a été enregistré. Notre équipe y travaille et vous reviendra sous 24h."
        )
    
    def _publish_ad(self, ad_record: Dict):
        """
        Publie une ad approuvée sur Meta
        """
        ad_id = ad_record['id']
        fields = ad_record['fields']
        
        try:
            # Publier sur Meta
            meta_result = self.meta.publish_ad(
                campaign_id=fields['campaign_meta_id'],
                adset_id=fields['adset_meta_id'],
                creative={
                    'name': fields['ad_name'],
                    'object_story_spec': {
                        'page_id': fields['page_id'],
                        'link_data': {
                            'message': f"{fields['copy_hook']}\n\n{fields['copy_body']}",
                            'link': fields['landing_url'],
                            'call_to_action': {
                                'type': fields['copy_cta'].upper().replace(' ', '_')
                            },
                            'image_hash': fields.get('asset_hash') or fields.get('video_id')
                        }
                    }
                },
                status='ACTIVE' if fields['publication_mode'] == 'Auto' else 'PAUSED'
            )
            
            # Update Airtable avec succès
            self.airtable.update_ad(ad_id, {
                'status': 'Publié',
                'meta_ad_id': meta_result['id'],
                'meta_status': meta_result['status'],
                'published_at': datetime.now().isoformat(),
                'published_by': 'agent'
            })
            
            # Notifier
            self.slack.send_message(
                channel=fields['validation_channel'],
                text=f"✅ Ad publiée avec succès sur Meta\n"
                     f"Meta Ad ID: {meta_result['id']}\n"
                     f"Status: {meta_result['status']}"
            )
            
        except Exception as e:
            # Erreur publication
            self.airtable.update_ad(ad_id, {
                'status': 'Erreur Publication',
                'notes': f"⚠️ Erreur: {str(e)}"
            })
            
            # Alerter équipe
            self.slack.send_message(
                channel='alerts-urgent',
                text=f"🚨 Erreur publication Ad {ad_id}\n"
                     f"Error: {str(e)}"
            )
```

Voulez-vous que je continue avec:
1. Le reste du code (handlers Slack, intégration Meta)
2. Guide de setup complet
3. Scripts de test

Dites-moi! 🚀
