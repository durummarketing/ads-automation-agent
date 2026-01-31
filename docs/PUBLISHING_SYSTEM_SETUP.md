# 🚀 GUIDE DE SETUP - Système de Publication avec Validation Client

## 📋 Vue d'Ensemble

Ce guide vous permet de **configurer complètement** le système de publication automatique avec validation client en **30-45 minutes**.

---

## ✅ Prérequis

- [ ] Compte Airtable avec base configurée
- [ ] Workspace Slack avec droits admin
- [ ] Compte Meta Business Manager
- [ ] Python 3.10+ installé
- [ ] Repository Git local (ads-automation-agent)

---

## 🗂️ ÉTAPE 1: Configuration Airtable (15 min)

### 1.1 Tables à Créer/Modifier

#### Table: **ads** (Modifier si existe, créer si inexiste)

**Colonnes à ajouter**:

```
Nom                    | Type              | Options
-----------------------|-------------------|---------------------------
status                 | Single Select     | Brouillon, Prêt pour Validation, En Validation, Approuvé, Commentaire Client, Publié, Actif, Pause, Archivé, Erreur Publication
publication_mode       | Single Select     | Auto, Manuel, Test
validation_channel     | Text              | (Auto-rempli par bot)
validated_by           | Text              | (Auto-rempli)
validated_at           | DateTime          | (Auto-rempli)
client_comment         | Long Text         | 
meta_ad_id             | Text              | (Auto-rempli après publication)
published_at           | DateTime          | (Auto-rempli)
published_by           | Text              | (Auto-rempli)
meta_status            | Text              | ACTIVE, PAUSED, DRAFT
```

**Colonnes existantes requises**:
- ad_id, ad_name, client_key, campaign_name, adset_name
- copy_hook, copy_body, copy_cta
- asset_url, asset_type, budget_daily

#### Table: **tasks** (NOUVELLE)

```
Nom              | Type              | Options
-----------------|-------------------|---------------------------
task_id          | Auto Number       | 
task_type        | Single Select     | Client Feedback - Ad, Bug, Feature, etc.
title            | Text              | 
description      | Long Text         | 
related_ad       | Link to ads       | 
related_client   | Link to clients   | 
assigned_to      | Single Select     | Équipe Création, Alex, Autre
priority         | Single Select     | Low, Normal, High, Urgent
status           | Single Select     | To Do, In Progress, Done, Cancelled
created_at       | Created Time      | 
due_date         | Date              | 
completed_at     | DateTime          | 
```

#### Table: **validation_logs** (NOUVELLE)

```
Nom                 | Type              | Description
--------------------|-------------------|---------------------------
log_id              | Auto Number       | 
ad_id               | Link to ads       | 
client_key          | Text              | 
sent_at             | DateTime          | 
action              | Single Select     | Sent, Approved, Commented, Rejected, Timeout
validated_by        | Text              | 
validated_at        | DateTime          | 
comment             | Long Text         | 
slack_message_ts    | Text              | Timestamp message Slack
```

#### Table: **clients** (Modifier)

**Colonnes à ajouter**:

```
Nom                       | Type    | Exemple
--------------------------|---------|---------------------------
slack_validation_channel  | Text    | client-avego-validation
slack_channel_id          | Text    | C04ABC123XYZ
```

### 1.2 Copier Base Template

Si vous partez de zéro, contactez-moi pour une base Airtable template pré-configurée.

---

## 💬 ÉTAPE 2: Configuration Slack (10 min)

### 2.1 Créer les Canaux

Pour **chaque client**, créer un canal de validation:

```
#client-avego-validation
#client-nomduclient-validation
```

**Configuration du canal**:
1. Topic: "Validation des nouvelles publicités pour [CLIENT]"
2. Inviter: Le client + votre équipe
3. Épingler message: Instructions pour le client

**Message Instructions (à épingler)**:

```
📢 Validation de Publicités

Vous recevrez ici les nouvelles publicités à valider avant publication.

Pour chaque ad:
✅ Approuver → Publication immédiate sur Meta
💬 Commentaire → Modifications par notre équipe
❌ Rejeter → Ad archivée

Questions? Demandez à l'équipe! 🚀
```

### 2.2 Récupérer les Channel IDs

Pour **chaque canal**:

1. Clic droit sur le canal → "Afficher les détails du canal"
2. Tout en bas: copier l'ID (format: C04ABC123XYZ)
3. Ajouter dans Airtable table **clients**, colonne `slack_channel_id`

### 2.3 Créer Slack App (Si pas déjà fait)

1. Aller sur https://api.slack.com/apps
2. "Create New App" → From scratch
3. Nom: "Ads Publishing Bot"
4. Workspace: Votre workspace DURUM

**Permissions (OAuth Scopes)**:
- `chat:write` - Envoyer messages
- `chat:write.public` - Envoyer dans canaux publics
- `im:write` - Envoyer DM
- `users:read` - Lire infos utilisateurs
- `channels:read` - Lire canaux

**Interactivity**:
1. Enable Interactivity: ON
2. Request URL: `https://VOTRE_DOMAINE/slack/interactions`
   - ⚠️ Vous aurez besoin d'un serveur public (ngrok pour test)

**Install App**:
1. Install to Workspace
2. Copier **Bot User OAuth Token** (commence par xoxb-)
3. Ajouter dans `.env`: `SLACK_BOT_TOKEN=xoxb-...`

### 2.4 Inviter le Bot dans les Canaux

Pour chaque canal de validation:
```
/invite @Ads Publishing Bot
```

---

## 🔧 ÉTAPE 3: Configuration .env (5 min)

Ajouter dans votre fichier `.env`:

```env
# === PUBLISHING SYSTEM ===

# Airtable
AIRTABLE_API_KEY=pat_xxxxxxxxxxxxx
AIRTABLE_BASE_ID=appxxxxxxxxxxxxx

# Slack
SLACK_BOT_TOKEN=xoxb-xxxxxxxxxxxxx
SLACK_SIGNING_SECRET=xxxxxxxxxxxxx

# Meta
META_ACCESS_TOKEN=EAAxxxxxxxxxxxxx
META_API_VERSION=v21.0

# Publishing Config
PUBLISHING_CYCLE_SECONDS=60           # Fréquence check (60s = 1 min)
VALIDATION_TIMEOUT_HOURS=48           # Timeout sans réponse client
PUBLISH_ENABLED=true                  # Activer publication réelle
DRY_RUN=false                         # false = publication réelle

# Canaux Slack
SLACK_CHANNEL_TEAM=team-durum
SLACK_CHANNEL_ALERTS=alerts-urgent
```

---

## 🚀 ÉTAPE 4: Installation du Code (5 min)

### 4.1 Ajouter les Nouveaux Fichiers

Copier dans votre projet `ads-automation-agent/`:

```bash
# Nouveau module
mkdir -p publishing/
cp publishing_workflow.py publishing/workflow.py
cp PUBLISHING_SYSTEM_DESIGN.md docs/
cp PUBLISHING_SYSTEM_SETUP.md docs/
```

### 4.2 Installer Dépendances Additionnelles

Vérifier que `requirements.txt` contient:

```txt
slack-sdk>=3.23.0
slack-bolt>=1.18.0
```

Si manquant:
```bash
pip install slack-sdk slack-bolt
```

---

## ⚙️ ÉTAPE 5: Démarrer le Système (2 min)

### Option A: Lancer en Mode Test

```bash
# Activer venv
source .venv/bin/activate

# Test
python -m publishing.workflow
```

**Que voir**:
```
📋 Publishing Workflow initialisé
   Cycle: 60s
   Timeout validation: 48h

🚀 Démarrage du Publishing Workflow...

[14:23:15] ⏳ En attente... (prochain cycle dans 60s)
```

### Option B: Intégrer dans main.py

Modifier `main.py`:

```python
from publishing.workflow import PublishingWorkflow

def main():
    # ... code existant
    
    # Démarrer publishing workflow
    if os.getenv('PUBLISH_ENABLED', 'false').lower() == 'true':
        print("🚀 Démarrage Publishing Workflow...")
        
        workflow = PublishingWorkflow()
        
        # Lancer dans thread séparé
        import threading
        thread = threading.Thread(target=workflow.start, daemon=True)
        thread.start()
    
    # ... reste du code
```

---

## 🧪 ÉTAPE 6: Test Complet (10 min)

### 6.1 Créer une Ad de Test

Dans Airtable, table **ads**:

1. Nouvelle ligne
2. Remplir tous les champs requis:
   - ad_name: "Ads T1 - V99" (test)
   - client_key: [Votre client test]
   - campaign_name: "[TEST] Campaign"
   - adset_name: "STACK_H:25/65+ _QC _FEED+ _Test"
   - copy_hook: "Ceci est un test de validation"
   - copy_body: "Ce message apparaîtra dans Slack..."
   - copy_cta: "Learn More"
   - publication_mode: **"Test"** (important!)
   - budget_daily: 50

3. **status**: Changer de "Brouillon" → **"Prêt pour Validation"**

### 6.2 Vérifier le Cycle

Dans les **60 secondes**, le bot devrait:

1. ✅ Détecter la nouvelle ad
2. ✅ Envoyer message dans Slack (canal client)
3. ✅ Changer status → "En Validation"

**Dans Slack**, vous devriez voir:

```
📢 Nouvelle Publicité à Valider - [CLIENT]

Campaign: [TEST] Campaign
AdSet: STACK_H:25/65+ _QC _FEED+ _Test

🎨 CRÉATIVE
HOOK: Ceci est un test de validation
BODY: Ce message apparaîtra dans Slack...
CTA: Learn More

🔵 Mode: Test
💰 Budget: $50/jour

[✅ Approuver] [💬 Commentaire] [❌ Rejeter]
```

### 6.3 Tester Approbation

1. Cliquer **"✅ Approuver"**
2. Vérifier dans Airtable:
   - status → "Approuvé"
   - validated_by: rempli
   - validated_at: rempli

3. Au prochain cycle (60s), bot devrait:
   - Publier sur Meta (mode DRAFT car "Test")
   - status → "Publié"
   - meta_ad_id: rempli

### 6.4 Tester Commentaire

1. Créer nouvelle ad test
2. status: "Prêt pour Validation"
3. Attendre message Slack
4. Cliquer **"💬 Commentaire"**
5. Remplir modal:
   - Commentaire: "Changer le hook SVP"
   - Priorité: Urgent
6. Vérifier:
   - Ad status → "Commentaire Client"
   - Tâche créée dans table **tasks**
   - Message dans #team-durum

---

## 📊 ÉTAPE 7: Monitoring (Continu)

### Logs à Surveiller

```bash
# Logs en temps réel
tail -f storage/agent.out.log

# Erreurs
tail -f storage/agent.err.log
```

### Dashboards

**Airtable Views Recommandées**:

1. **"En Validation"** - Filtre: status = "En Validation"
2. **"Approuvées"** - Filtre: status = "Approuvé"
3. **"Publiées Aujourd'hui"** - Filtre: published_at = today
4. **"Erreurs"** - Filtre: status = "Erreur Publication"

**Slack Canaux**:
- `#team-durum` - Notifications internes
- `#alerts-urgent` - Erreurs critiques

---

## ⚠️ Troubleshooting

### Problème: Bot ne détecte pas les ads

**Causes possibles**:
1. status != "Prêt pour Validation" (vérifier orthographe exacte)
2. Champs requis manquants (hook, body, CTA, etc.)
3. Bot pas en marche

**Solution**:
```bash
# Vérifier bot actif
ps aux | grep publishing

# Relancer
python -m publishing.workflow
```

### Problème: Message Slack pas envoyé

**Causes possibles**:
1. slack_channel_id manquant ou invalide
2. Bot pas invité dans le canal
3. Token Slack invalide

**Solution**:
1. Vérifier channel ID dans Airtable
2. `/invite @Ads Publishing Bot` dans le canal
3. Régénérer token si nécessaire

### Problème: Publication Meta échoue

**Causes possibles**:
1. Token Meta expiré
2. IDs campaign/adset invalides
3. Asset manquant (hash ou video_id)

**Solution**:
```bash
# Vérifier token Meta
curl -i -X GET "https://graph.facebook.com/v21.0/me?access_token=VOTRE_TOKEN"

# Vérifier logs
grep "Erreur publication Meta" storage/agent.err.log
```

---

## 🎯 Workflow Opérationnel

### Création d'Ads (Quotidien)

**Votre équipe**:
1. Créer ads dans Airtable (status: "Brouillon")
2. Travailler sur copy, assets
3. Quand prêt: status → "Prêt pour Validation"
4. Sélectionner **publication_mode**:
   - "Auto" = Actif immédiatement après validation
   - "Manuel" = Publié OFF, activation manuelle
   - "Test" = Draft (test structure)

**Le Bot**:
1. Détecte (cycle 60s)
2. Valide structure
3. Envoie Slack
4. Attend réponse client

**Le Client**:
1. Reçoit notification
2. Clique ✅ Approuver OU 💬 Commentaire
3. Si commentaire: équipe notifiée, tâche créée

**Publication**:
1. Si approuvé: Publication au prochain cycle
2. Update Airtable avec meta_ad_id
3. Confirmation Slack

### Corrections Suite Commentaire

**Votre équipe**:
1. Voit tâche dans Airtable
2. Notification dans #team-durum
3. Corrige l'ad
4. Change status: "Commentaire Client" → "Prêt pour Validation"
5. → Re-envoi automatique pour validation

---

## ✅ Checklist Finale

Setup Airtable:
- [ ] Table **ads** avec nouvelles colonnes
- [ ] Table **tasks** créée
- [ ] Table **validation_logs** créée
- [ ] Table **clients** avec slack_channel_id

Setup Slack:
- [ ] Canaux #client-XXX-validation créés
- [ ] Bot invité dans tous les canaux
- [ ] Channel IDs dans Airtable

Setup Code:
- [ ] Fichiers copiés
- [ ] .env configuré
- [ ] Dépendances installées
- [ ] Test réussi

Production:
- [ ] Bot qui tourne en continu
- [ ] Logs monitorés
- [ ] Équipe formée au workflow

---

## 🚀 Prêt!

Le système est maintenant **opérationnel** et prêt à gérer vos publications automatiquement avec validation client! 🎉

**Support**: alex@durum-marketing.com
