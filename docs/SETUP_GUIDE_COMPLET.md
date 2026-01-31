# 🚀 GUIDE SETUP COMPLET - DURUM AI Agent
## Pour Mac Mini M4 - Prêt pour Lundi Matin

**Temps total estimé**: 4-6 heures (ce weekend)
**Niveau**: Débutant-Intermédiaire (tout est expliqué pas-à-pas)

---

## 📋 CHECKLIST AVANT DE COMMENCER

Assurez-vous d'avoir:
- [ ] Mac Mini M4 allumé et connecté Internet
- [ ] Accès admin Mac (mot de passe sudo)
- [ ] Compte GitHub (AlexBedardDurum)
- [ ] Accès Airtable (compte avec droits créer bases)
- [ ] Accès Slack Workspace (droits admin)
- [ ] Meta Business Manager (Admin)
- [ ] Anthropic API Key (ou carte crédit pour en créer une)
- [ ] 4-6 heures devant vous (pause café incluse ☕)

---

# PARTIE 1: SETUP ENVIRONNEMENT (1-1.5h)

## ÉTAPE 1: Installer Homebrew (5 min)

**Qu'est-ce que c'est?** Gestionnaire de packages pour Mac (comme App Store mais pour développeurs)

**Comment faire**:

1. Ouvrir **Terminal**:
   - Appuyer `Cmd + Espace`
   - Taper "Terminal"
   - Appuyer `Entrée`

2. Copier-coller cette commande EXACTEMENT:
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

3. Appuyer `Entrée`
   - Terminal demandera votre mot de passe Mac
   - **Tapez-le** (rien n'apparaît quand vous tapez = normal)
   - Appuyer `Entrée`

4. Attendre 2-3 minutes (téléchargement + installation)

5. Quand fini, copier-coller ces 2 commandes:
   ```bash
   echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
   eval "$(/opt/homebrew/bin/brew shellenv)"
   ```

6. **Vérifier** que ça marche:
   ```bash
   brew --version
   ```
   - Devrait afficher: `Homebrew 4.x.x`
   - ✅ Si oui = Succès!
   - ❌ Si erreur = Recommencer étape 2

---

## ÉTAPE 2: Installer Python 3.10+ (5 min)

**Qu'est-ce que c'est?** Langage de programmation du système

**Comment faire**:

1. Dans Terminal, taper:
   ```bash
   brew install python@3.10
   ```

2. Appuyer `Entrée` et attendre 3-5 min

3. **Vérifier** installation:
   ```bash
   python3 --version
   ```
   - Devrait afficher: `Python 3.10.x` ou `3.11.x` ou `3.12.x`
   - ✅ Si 3.10+ = Parfait!

4. Installer pip (gestionnaire packages Python):
   ```bash
   python3 -m ensurepip --upgrade
   ```

---

## ÉTAPE 3: Installer Git (3 min)

**Qu'est-ce que c'est?** Outil pour versionner code (déjà expliqué GitHub)

**Comment faire**:

1. Dans Terminal:
   ```bash
   brew install git
   ```

2. Configurer Git avec vos infos:
   ```bash
   git config --global user.name "Alex Bedard"
   git config --global user.email "alex@durum-marketing.com"
   ```

3. **Vérifier**:
   ```bash
   git --version
   ```
   - Devrait afficher: `git version 2.x.x`
   - ✅ Si oui = Bon!

---

## ÉTAPE 4: Créer Dossier Projet (2 min)

**Où?** Dans votre dossier utilisateur

**Comment faire**:

1. Dans Terminal:
   ```bash
   cd ~
   mkdir ads-automation-agent
   cd ads-automation-agent
   pwd
   ```

2. La commande `pwd` devrait afficher:
   ```
   /Users/alexbedard/ads-automation-agent
   ```
   (ou votre nom utilisateur)

3. ✅ Parfait, vous êtes dans le bon dossier!

---

## ÉTAPE 5: Cloner Code depuis GitHub (5 min)

**Qu'est-ce qu'on fait?** Télécharger tout le code que j'ai préparé

**Comment faire**:

1. Dans Terminal (toujours dans `~/ads-automation-agent`):
   ```bash
   git clone https://github.com/AlexBedardDurum/ads-automation-agent.git .
   ```
   
   **Note**: Le `.` à la fin est important!

2. GitHub demandera authentification:
   - **Username**: `AlexBedardDurum`
   - **Password**: Votre **Personal Access Token** GitHub
   
   **Si vous n'avez pas de token**:
   - Aller sur: https://github.com/settings/tokens
   - Click "Generate new token (classic)"
   - Nom: "Mac Mini - Ads Agent"
   - Cocher: `repo` (full control)
   - Generate token
   - **COPIER LE TOKEN** (vous ne le reverrez plus!)
   - Coller comme password

3. Attendre téléchargement (30 secondes)

4. **Vérifier**:
   ```bash
   ls -la
   ```
   - Vous devriez voir: `README.md`, `main.py`, `docs/`, etc.
   - ✅ Si oui = Code téléchargé!

---

## ÉTAPE 6: Créer Environnement Virtuel Python (5 min)

**Pourquoi?** Isoler les dépendances du projet (bonne pratique)

**Comment faire**:

1. Dans Terminal (dans `~/ads-automation-agent`):
   ```bash
   python3 -m venv .venv
   ```

2. Attendre 1-2 minutes (crée dossier `.venv`)

3. **Activer** l'environnement:
   ```bash
   source .venv/bin/activate
   ```

4. Votre prompt Terminal devrait changer:
   ```
   (.venv) alexbedard@mac-mini ads-automation-agent %
   ```
   - Le `(.venv)` au début = ✅ Environnement actif!

5. **Installer dépendances**:
   ```bash
   pip install -r requirements.txt
   ```
   
6. Attendre 3-5 minutes (installe tous les packages)

7. **Vérifier**:
   ```bash
   pip list
   ```
   - Devrait afficher 30-40 packages installés
   - ✅ Si liste longue = Parfait!

---

## ✅ CHECKPOINT PARTIE 1

**À ce stade, vous devriez avoir**:
- ✅ Homebrew installé
- ✅ Python 3.10+ installé
- ✅ Git installé et configuré
- ✅ Code téléchargé dans `~/ads-automation-agent`
- ✅ Environnement virtuel créé et activé
- ✅ Dépendances Python installées

**Problème?** Revérifiez les étapes ci-dessus avant de continuer.

**Tout bon?** ☕ **Pause café 5 min** puis on continue!

---

# PARTIE 2: CONFIGURATION APIs (1-1.5h)

## ÉTAPE 7: Créer Fichier .env (10 min)

**Qu'est-ce que c'est?** Fichier avec vos clés API secrètes

**Comment faire**:

1. Dans Terminal (toujours `~/ads-automation-agent` avec `.venv` actif):
   ```bash
   cp .env.example .env
   nano .env
   ```

2. L'éditeur `nano` s'ouvre. Vous devez remplir les valeurs:

   **Template à remplir** (je vous guide pour chaque):
   ```env
   # === AIRTABLE ===
   AIRTABLE_API_KEY=pat_VOTRE_CLE_ICI
   AIRTABLE_BASE_ID=app_VOTRE_BASE_ID_ICI
   
   # === META ADS ===
   META_ACCESS_TOKEN=VOTRE_TOKEN_META_ICI
   META_API_VERSION=v21.0
   
   # === SLACK ===
   SLACK_BOT_TOKEN=xoxb-VOTRE_TOKEN_SLACK_ICI
   SLACK_SIGNING_SECRET=VOTRE_SECRET_SLACK_ICI
   
   # === ANTHROPIC (IA) ===
   ANTHROPIC_API_KEY=sk-ant-VOTRE_CLE_ANTHROPIC_ICI
   
   # === GOOGLE SHEETS ===
   GOOGLE_SHEETS_CREDENTIALS_FILE=secrets/google-service-account.json
   GROWTH_OS_SPREADSHEET_ID=VOTRE_SPREADSHEET_ID_ICI
   
   # === SYSTEM ===
   ANALYSIS_HOUR=09
   MAX_SUGGESTIONS_PER_DAY=20
   MIN_CONFIDENCE_SCORE=90
   ```

3. **NE FERMEZ PAS ENCORE** - On va remplir chaque valeur une par une

---

## ÉTAPE 8: Obtenir Airtable API Key (5 min)

**Comment faire**:

1. Aller sur: https://airtable.com/create/tokens

2. Click "Create token"

3. Nom: `DURUM AI Agent`

4. Scopes à cocher:
   - ✅ `data.records:read`
   - ✅ `data.records:write`
   - ✅ `schema.bases:read`

5. Access: Choisir `All current and future bases in all workspaces`

6. Click "Create token"

7. **COPIER LE TOKEN** (commence par `pat...`)

8. Retourner Terminal (nano ouvert)
   - Remplacer `pat_VOTRE_CLE_ICI` par votre vrai token
   - Ex: `AIRTABLE_API_KEY=patAbCdEf123456789...`

**Ne sauvegardez pas encore**, on continue...

---

## ÉTAPE 9: Créer Base Airtable (15 min)

**Comment faire**:

1. Aller sur: https://airtable.com/

2. Click "Create a base"

3. Nom: `DURUM AI Agent - Production`

4. Click sur la base créée

5. Dans l'URL du navigateur, copier l'ID:
   ```
   https://airtable.com/appXXXXXXXXXXXXXX/...
                        ^^^^^^^^^^^^^^^^
                        Copier cette partie
   ```

6. Retourner Terminal (nano)
   - Remplacer `app_VOTRE_BASE_ID_ICI` par l'ID copié
   - Ex: `AIRTABLE_BASE_ID=appAbCdEf12345678`

**IMPORTANT**: On créera les tables plus tard (Étape 13)

---

## ÉTAPE 10: Obtenir Meta Access Token (10 min)

**Comment faire**:

1. Aller sur: https://business.facebook.com/

2. Aller dans **Business Settings** (roue dentée en haut à droite)

3. Menu gauche: **System Users**

4. Click "Add" → Créer nouveau System User:
   - Nom: `DURUM AI Agent`
   - Role: `Admin`

5. Click sur le System User créé

6. Click "Generate New Token"

7. Sélectionner votre compte pub Meta

8. Permissions à cocher:
   - ✅ `ads_management`
   - ✅ `ads_read`
   - ✅ `business_management`

9. Click "Generate Token"

10. **COPIER LE TOKEN** (très long, commence par `EAA...`)

11. Retourner Terminal (nano)
    - Remplacer `VOTRE_TOKEN_META_ICI` par votre token
    - Ex: `META_ACCESS_TOKEN=EAABwz...` (très long)

---

## ÉTAPE 11: Configurer Slack App (20 min)

**Comment faire**:

1. Aller sur: https://api.slack.com/apps

2. Click "Create New App"

3. Choisir "From scratch"

4. Nom: `DURUM AI Agent`
   Workspace: Votre workspace DURUM

5. Dans **OAuth & Permissions**, scroll vers **Scopes**

6. Ajouter ces **Bot Token Scopes**:
   ```
   chat:write
   chat:write.public
   im:write
   users:read
   channels:read
   ```

7. Click "Install to Workspace" (en haut de la page)

8. Autoriser l'app

9. **COPIER le Bot User OAuth Token** (commence par `xoxb-`)

10. Retourner Terminal (nano)
    - Remplacer `xoxb-VOTRE_TOKEN_SLACK_ICI`
    - Ex: `SLACK_BOT_TOKEN=xoxb-123456...`

11. Retourner sur https://api.slack.com/apps

12. Votre app → **Basic Information**

13. Scroll vers **App Credentials**

14. **COPIER Signing Secret**

15. Retourner Terminal (nano)
    - Remplacer `VOTRE_SECRET_SLACK_ICI`
    - Ex: `SLACK_SIGNING_SECRET=abc123def456...`

---

## ÉTAPE 12: Obtenir Anthropic API Key (5 min)

**Comment faire**:

1. Aller sur: https://console.anthropic.com/

2. Si pas de compte:
   - Sign up avec email
   - Vérifier email
   - Ajouter carte crédit (ils chargent $5 minimum)

3. Aller dans **API Keys**

4. Click "Create Key"

5. Nom: `DURUM AI Agent`

6. **COPIER LA CLÉ** (commence par `sk-ant-`)

7. Retourner Terminal (nano)
   - Remplacer `sk-ant-VOTRE_CLE_ANTHROPIC_ICI`
   - Ex: `ANTHROPIC_API_KEY=sk-ant-api03-...`

---

## ÉTAPE 13: Configurer Google Sheets (15 min)

**Comment faire**:

1. Aller sur: https://console.cloud.google.com/

2. Créer nouveau projet:
   - Click "Select a project" (en haut)
   - Click "New Project"
   - Nom: `DURUM AI Agent`
   - Click "Create"

3. Activer Google Sheets API:
   - Menu hamburger → APIs & Services → Library
   - Chercher "Google Sheets API"
   - Click dessus → Click "Enable"

4. Créer Service Account:
   - Menu → APIs & Services → Credentials
   - Click "Create Credentials" → "Service Account"
   - Nom: `durum-ai-agent`
   - Click "Create and Continue"
   - Role: "Editor"
   - Click "Done"

5. Créer clé JSON:
   - Click sur le Service Account créé
   - Onglet "Keys"
   - "Add Key" → "Create new key"
   - Type: JSON
   - Click "Create"
   - **Fichier JSON téléchargé automatiquement**

6. Déplacer le fichier JSON:
   ```bash
   # Dans un nouveau Terminal (Cmd+T pour nouveau tab)
   cd ~/ads-automation-agent
   mkdir -p secrets
   # Glisser-déposer le fichier JSON téléchargé dans Finder
   # vers le dossier secrets/
   # OU copier manuellement:
   mv ~/Downloads/durum-ai-agent-*.json secrets/google-service-account.json
   ```

7. Obtenir Spreadsheet ID de Growth OS:
   - Ouvrir votre Google Sheet Growth OS
   - Dans l'URL:
     ```
     https://docs.google.com/spreadsheets/d/SPREADSHEET_ID_ICI/edit
                                            ^^^^^^^^^^^^^^^^^^^^
                                            Copier cette partie
     ```

8. Retourner Terminal avec nano ouvert
   - Remplacer `VOTRE_SPREADSHEET_ID_ICI`
   - Ex: `GROWTH_OS_SPREADSHEET_ID=1AbC-dEfGhI...`

9. **IMPORTANT**: Partager Growth OS Sheet avec Service Account:
   - Ouvrir le fichier `secrets/google-service-account.json`
   - Copier le email (ex: `durum-ai-agent@xxx.iam.gserviceaccount.com`)
   - Dans Google Sheet Growth OS: Share
   - Coller l'email du Service Account
   - Role: Editor
   - Envoyer

---

## ÉTAPE 14: Sauvegarder .env (2 min)

**Vous avez rempli toutes les valeurs?** Vérifions:

- ✅ AIRTABLE_API_KEY
- ✅ AIRTABLE_BASE_ID
- ✅ META_ACCESS_TOKEN
- ✅ SLACK_BOT_TOKEN
- ✅ SLACK_SIGNING_SECRET
- ✅ ANTHROPIC_API_KEY
- ✅ GROWTH_OS_SPREADSHEET_ID

**Sauvegarder**:
1. Dans nano: `Ctrl + O` (sauvegarder)
2. Appuyer `Entrée` (confirmer nom fichier)
3. `Ctrl + X` (quitter nano)

**Vérifier**:
```bash
cat .env
```
- Devrait afficher vos vraies valeurs (pas les `VOTRE_XXX_ICI`)
- ✅ Si oui = Parfait!

---

## ✅ CHECKPOINT PARTIE 2

**À ce stade, vous devriez avoir**:
- ✅ Fichier `.env` créé avec TOUTES vos clés API
- ✅ Base Airtable créée (vide pour l'instant)
- ✅ Slack App créée et configurée
- ✅ Google Service Account créé et Sheet partagé
- ✅ Anthropic API Key créée

**Problème?** Revérifiez chaque étape API.

**Tout bon?** ☕ **Pause 10 min** puis Partie 3!

---

# PARTIE 3: CRÉATION TABLES AIRTABLE (1h)

## ÉTAPE 15: Créer Tables Essentielles (30 min)

**On va créer 3 tables pour MVP**:
1. `clients`
2. `suggestions`
3. `decisions`

### Table 1: clients

1. Ouvrir votre base Airtable dans navigateur

2. Renommer la table par défaut:
   - Click sur nom "Table 1"
   - Renommer: `clients`

3. Ajouter colonnes (click sur `+` à droite):

   **Colonne 1**: `client_key` (Primary)
   - Type: Single line text
   - **IMPORTANT**: Déjà créée (renommer "Name" → "client_key")

   **Colonne 2**: `client_name`
   - Type: Single line text

   **Colonne 3**: `industry`
   - Type: Single select
   - Options: `coaching`, `ecom`, `saas`, `finance`, `health`, `education`

   **Colonne 4**: `roi_target`
   - Type: Number
   - Format: Decimal (1 decimal place)

   **Colonne 5**: `monthly_budget_max`
   - Type: Currency
   - Symbol: $ USD

   **Colonne 6**: `slack_validation_channel`
   - Type: Single line text

   **Colonne 7**: `slack_channel_id`
   - Type: Single line text

4. **Remplir avec vos 6 clients** (exemples):
   
   | client_key | client_name | industry  | roi_target | monthly_budget_max | slack_validation_channel |
   |------------|-------------|-----------|------------|-------------------|-------------------------|
   | avego      | Avego       | coaching  | 3.0        | $100,000          | client-avego-validation |
   | client2    | Client 2    | coaching  | 3.5        | $50,000           | client-client2-validation |
   
   (Répéter pour vos 6 clients)

### Table 2: suggestions

1. Click "Add or import" → "Create empty table"

2. Nom: `suggestions`

3. Ajouter colonnes:

   **Colonne 1**: `suggestion_id` (Primary - auto number)
   - Renommer "Name" → "suggestion_id"
   - Type: Auto number

   **Colonne 2**: `date`
   - Type: Date
   - Include time: Yes

   **Colonne 3**: `client_key`
   - Type: Link to another record
   - Table: `clients`
   - Field name in clients: `suggestions` (auto)

   **Colonne 4**: `type`
   - Type: Single select
   - Options: `scale`, `pause`, `refresh`, `test_angle`

   **Colonne 5**: `action`
   - Type: Long text

   **Colonne 6**: `reason`
   - Type: Long text

   **Colonne 7**: `confidence`
   - Type: Number
   - Format: Integer

   **Colonne 8**: `status`
   - Type: Single select
   - Options: `pending`, `approved`, `refused`, `executed`

   **Colonne 9**: `approved_by`
   - Type: Single line text

   **Colonne 10**: `approved_at`
   - Type: Date
   - Include time: Yes

4. **Laisser vide** (sera rempli par le système)

### Table 3: decisions

1. Click "Add or import" → "Create empty table"

2. Nom: `decisions`

3. Ajouter colonnes:

   **Colonne 1**: `decision_id` (Primary - auto number)
   - Renommer "Name" → "decision_id"
   - Type: Auto number

   **Colonne 2**: `suggestion_id`
   - Type: Link to another record
   - Table: `suggestions`

   **Colonne 3**: `decision`
   - Type: Single select
   - Options: `approved`, `refused`, `backlog`

   **Colonne 4**: `decided_by`
   - Type: Single line text

   **Colonne 5**: `decided_at`
   - Type: Date
   - Include time: Yes

   **Colonne 6**: `notes`
   - Type: Long text

4. **Laisser vide** (sera rempli par système)

---

## ÉTAPE 16: Créer Canaux Slack (15 min)

**Pour chaque client, créer canal validation**:

1. Dans Slack, click `+` à côté de "Channels"

2. "Create a channel"

3. Nom: `client-avego-validation` (exemple pour Avego)
   - **Respecter format exact**: `client-NOMCLIENT-validation`

4. Description: "Validation publicités Avego"

5. Make private: **NO** (laisser public)

6. Create

7. **Inviter bot**:
   - Dans le canal, taper: `/invite @DURUM AI Agent`
   - Le bot devrait rejoindre

8. **Récupérer Channel ID**:
   - Click sur nom canal (en haut)
   - Scroll tout en bas
   - Copier "Channel ID" (ex: `C04ABC123XYZ`)
   - Aller dans Airtable table `clients`
   - Coller dans colonne `slack_channel_id` pour ce client

9. **Répéter pour les 6 clients**

**Créer aussi**:
- Canal `#durum-suggestions` (vos suggestions quotidiennes)
- Canal `#alerts-urgent` (alertes critiques)

10. Inviter bot dans ces 2 canaux aussi

---

## ÉTAPE 17: Tester Connexions APIs (15 min)

**Vérifier que tout est bien configuré**

1. Dans Terminal (environnement virtuel actif):
   ```bash
   cd ~/ads-automation-agent
   python3 test_setup.py
   ```

2. Le script va tester:
   - ✅ Airtable connection
   - ✅ Meta API connection
   - ✅ Slack connection
   - ✅ Google Sheets connection
   - ✅ Anthropic API connection

3. **Résultats attendus**:
   ```
   Testing Airtable... ✅ Connected
   Testing Meta API... ✅ Connected (6 accounts)
   Testing Slack... ✅ Connected
   Testing Google Sheets... ✅ Connected (Growth OS)
   Testing Anthropic... ✅ Connected
   
   🎉 All systems operational!
   ```

4. **Si erreur**:
   - Vérifier `.env` (clés correctes?)
   - Vérifier permissions APIs
   - Relire étapes configuration

---

## ✅ CHECKPOINT PARTIE 3

**À ce stade, vous devriez avoir**:
- ✅ 3 tables Airtable créées et remplies
- ✅ 6+ canaux Slack créés avec bot invité
- ✅ Channel IDs dans Airtable
- ✅ Toutes connexions APIs testées ✅

**Problème?** Vérifier tables et canaux.

**Tout bon?** ☕ **Pause 10 min** - Presque fini!

---

# PARTIE 4: LANCEMENT SYSTÈME (30 min)

## ÉTAPE 18: Premier Test Manuel (10 min)

**Tester analyse manuelle**

1. Dans Terminal:
   ```bash
   cd ~/ads-automation-agent
   source .venv/bin/activate  # Si pas déjà actif
   python3 main.py --test
   ```

2. Le système va:
   - Analyser vos données Meta + Growth OS
   - Générer 2-3 suggestions test
   - Les afficher dans Terminal

3. **Résultat attendu**:
   ```
   🌅 Daily Analysis - Test Mode
   
   📊 Analyzing 6 clients...
   ✅ Avego: 5 adsets analyzed
   ✅ Client2: 3 adsets analyzed
   ...
   
   💡 Generated 3 suggestions:
   
   1. [HIGH] Scale AdSet Avego STACK_H:25/45
      ROI: 4.2x → Scale +50%
      Confidence: 92%
   
   2. [MED] Pause AdSet Client2 STACK_X
      ROI: 1.8x → Pause
      Confidence: 88%
   
   3. [LOW] Refresh Client3 hooks
      CTR: -35% → Need refresh
      Confidence: 75%
   
   ✅ Test completed successfully!
   ```

4. **Si erreurs**:
   - Vérifier connexions APIs
   - Vérifier données dans Growth OS
   - Check logs: `tail -f storage/agent.err.log`

---

## ÉTAPE 19: Tester Notifications Slack (5 min)

**Envoyer message test**

1. Dans Terminal:
   ```bash
   python3 -c "
   from slack.notifier import SlackNotifier
   slack = SlackNotifier()
   slack.send_message('durum-suggestions', '🧪 Test - Le système fonctionne!')
   "
   ```

2. **Vérifier dans Slack #durum-suggestions**:
   - Vous devriez voir message du bot
   - ✅ Si oui = Slack marche!

---

## ÉTAPE 20: Configurer Exécution Automatique (15 min)

**Lancer le système chaque matin à 9h**

1. Créer script de lancement:
   ```bash
   nano ~/ads-automation-agent/scripts/run_daily.sh
   ```

2. Copier-coller ceci:
   ```bash
   #!/bin/bash
   
   # Activer environnement
   cd ~/ads-automation-agent
   source .venv/bin/activate
   
   # Lancer analyse
   python3 main.py
   
   # Logs
   echo "Completed at $(date)" >> storage/cron.log
   ```

3. Sauvegarder: `Ctrl+O`, `Entrée`, `Ctrl+X`

4. Rendre exécutable:
   ```bash
   chmod +x ~/ads-automation-agent/scripts/run_daily.sh
   ```

5. Configurer cron (exécution automatique):
   ```bash
   crontab -e
   ```

6. Ajouter cette ligne (appuyer `i` pour mode insertion):
   ```
   0 9 * * * ~/ads-automation-agent/scripts/run_daily.sh
   ```
   
   (Signifie: "À 9h00 tous les jours")

7. Sauvegarder: `Esc`, `:wq`, `Entrée`

8. **Vérifier**:
   ```bash
   crontab -l
   ```
   - Devrait afficher votre ligne cron
   - ✅ Si oui = Configuré!

---

## ÉTAPE 21: Test Complet End-to-End (10 min)

**Simuler demain matin**

1. Forcer exécution manuelle:
   ```bash
   ~/ads-automation-agent/scripts/run_daily.sh
   ```

2. **Dans les 2-3 minutes**, vérifier:

   **✅ Dans Slack #durum-suggestions**:
   - Message "🌅 Daily Digest"
   - 2-3 suggestions affichées
   - Boutons [Approuver] [Refuser]

   **✅ Dans Airtable table `suggestions`**:
   - 2-3 nouvelles lignes
   - Status = "pending"
   - Tous champs remplis

   **✅ Dans Terminal**:
   - Logs affichent succès
   - Pas d'erreurs

3. **Tester approbation**:
   - Click bouton "✅ Approuver" dans Slack
   - Vérifier Airtable: status → "approved"
   - Vérifier action exécutée sur Meta

4. **Si tout marche** = 🎉 **SYSTÈME OPÉRATIONNEL!**

---

## ✅ CHECKPOINT FINAL

**Votre système est prêt si**:
- ✅ Test manuel marche (suggestions générées)
- ✅ Notifications Slack arrivent
- ✅ Cron job configuré (9h auto)
- ✅ Test end-to-end réussi
- ✅ Approbations Slack fonctionnent

---

# LUNDI MATIN - Ce Qui Va Se Passer

## 9:00 AM - Automatique

1. Mac Mini exécute `run_daily.sh` (cron)
2. Système analyse vos 6 clients
3. Génère 2-3 suggestions
4. Envoie Slack #durum-suggestions

## 9:15 AM - Vous

1. Ouvrir Slack
2. Voir suggestions
3. Cliquer ✅ Approuver ou ❌ Refuser
4. Système exécute automatiquement

## Reste de la Journée

- Nouvelles suggestions si nécessaire
- Alertes si anomalies
- Vous gardez contrôle total

---

# 🆘 TROUBLESHOOTING

## Problème: Cron ne lance pas

**Solution**:
```bash
# Tester script manuellement
~/ads-automation-agent/scripts/run_daily.sh

# Check logs
tail -f storage/cron.log
```

## Problème: Slack messages n'arrivent pas

**Solution**:
- Vérifier bot invité dans canaux
- Vérifier SLACK_BOT_TOKEN dans `.env`
- Re-tester: `python3 test_setup.py`

## Problème: Erreur Airtable

**Solution**:
- Vérifier AIRTABLE_API_KEY
- Vérifier AIRTABLE_BASE_ID
- Vérifier noms tables (exactement `clients`, `suggestions`, `decisions`)

## Problème: Meta API erreur

**Solution**:
- Vérifier META_ACCESS_TOKEN
- Vérifier token pas expiré
- Régénérer si nécessaire

---

# 📞 BESOIN D'AIDE?

Si problème:

1. **Check logs**:
   ```bash
   tail -f ~/ads-automation-agent/storage/agent.err.log
   ```

2. **Me contacter** avec:
   - Screenshot erreur
   - Contenu logs
   - Étape où vous êtes bloqué

3. **Ressources**:
   - Documentation: `~/ads-automation-agent/docs/`
   - GitHub Issues: Si bug code

---

# ✅ CHECKLIST FINALE

Avant Lundi, vérifier:

- [ ] Toutes étapes Partie 1 complétées
- [ ] Toutes étapes Partie 2 complétées  
- [ ] Toutes étapes Partie 3 complétées
- [ ] Toutes étapes Partie 4 complétées
- [ ] Test end-to-end réussi
- [ ] Cron job configuré
- [ ] Slack fonctionne
- [ ] Airtable rempli
- [ ] Mac Mini restera allumé 24/7

**Tout coché?** 🎉 **VOUS ÊTES PRÊT POUR LUNDI!**

---

# 🚀 BON SETUP!

Temps estimé: 4-6 heures
Résultat: Système opérationnel automatique

**Questions pendant setup?** Notez-les, on ajustera ensemble!

**Bonne chance!** 💪🔥
