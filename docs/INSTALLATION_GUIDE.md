# 📦 GUIDE D'INSTALLATION COMPLET - PAS À PAS

## 🎯 POUR QUI?

Ce guide est fait pour quelqu'un qui:
- ❌ N'a JAMAIS utilisé GitHub
- ❌ N'a JAMAIS utilisé le Terminal
- ❌ N'a JAMAIS programmé
- ✅ Veut installer le système Growth OS en toute sécurité

**Durée totale estimée: 2-3 heures** (la première fois)

---

## ⚠️ AVANT DE COMMENCER

### Ce dont vous avez besoin:

1. **Un Mac** (ce guide est pour macOS)
   - macOS 12+ (Monterey ou plus récent)
   - 8GB RAM minimum
   - 10GB espace disque libre

2. **Accès à ces services**:
   - ✅ Airtable (compte payant recommandé)
   - ✅ Meta Business Manager (accès admin)
   - ✅ Google Sheets
   - ✅ Slack (workspace)
   - ✅ Anthropic (pour Claude AI)

3. **2-3 heures de temps**
   - Ne précipitez rien
   - Suivez CHAQUE étape
   - Vérifiez après chaque étape

---

# 📋 PARTIE 1: PRÉPARATION (30 min)

## ÉTAPE 1.1: Créer le dossier du projet

### 🎯 Ce qu'on va faire:
Créer un dossier sur votre Mac où tous les fichiers seront installés.

### 📝 Instructions:

1. **Ouvrir Finder**
   - Cliquer sur l'icône Finder dans le Dock (icône bleue qui sourit)

2. **Aller dans votre dossier utilisateur**
   - Dans la barre latérale gauche
   - Cliquer sur votre nom d'utilisateur (sous "Favoris")

3. **Créer un nouveau dossier**
   - Clic droit dans la fenêtre
   - Sélectionner "Nouveau dossier"
   - Nommer le dossier: `ads-automation-agent`
   - Appuyer sur Enter

✅ **Vérification**: Vous devez voir un dossier nommé `ads-automation-agent` dans votre dossier utilisateur

---

## ÉTAPE 1.2: Télécharger les fichiers du projet

### 🎯 Ce qu'on va faire:
Récupérer tous les fichiers du système depuis le chat.

### 📝 Instructions:

1. **Dans ce chat Claude.ai**
   - En haut, vous voyez des fichiers attachés
   - Cliquer sur le dossier `ads-automation-agent`

2. **Télécharger le dossier**
   - Cliquer sur les 3 points (⋯) à droite
   - Sélectionner "Télécharger"
   - Le fichier ZIP va se télécharger

3. **Décompresser le ZIP**
   - Aller dans "Téléchargements" (dans Finder)
   - Double-cliquer sur `ads-automation-agent.zip`
   - Un dossier `ads-automation-agent` sera créé

4. **Copier les fichiers**
   - Ouvrir le dossier décompressé
   - Sélectionner TOUS les fichiers (Cmd+A)
   - Copier (Cmd+C)
   - Aller dans le dossier créé à l'étape 1.1
   - Coller (Cmd+V)

✅ **Vérification**: Dans votre dossier `ads-automation-agent`, vous devez voir des fichiers comme:
- `main.py`
- `README.md`
- Dossiers: `airtable`, `engine`, `meta`, etc.

---

## ÉTAPE 1.3: Ouvrir le Terminal

### 🎯 Ce qu'on va faire:
Ouvrir l'application Terminal pour taper des commandes.

### 📝 Instructions:

1. **Ouvrir Terminal**
   - Appuyer sur Cmd + Espace (Spotlight)
   - Taper: `Terminal`
   - Appuyer sur Enter

2. **Vous voyez une fenêtre noire (ou blanche)**
   - C'est normal!
   - Il y a un curseur qui clignote
   - C'est là que vous allez taper des commandes

3. **Naviguer vers votre projet**
   - Taper cette commande EXACTEMENT:
   ```bash
   cd ~/ads-automation-agent
   ```
   - Appuyer sur Enter

4. **Vérifier que vous êtes au bon endroit**
   - Taper:
   ```bash
   pwd
   ```
   - Appuyer sur Enter
   - Vous devez voir quelque chose comme: `/Users/votrenom/ads-automation-agent`

✅ **Vérification**: Quand vous tapez `ls` (puis Enter), vous voyez la liste des fichiers du projet

---

## ÉTAPE 1.4: Installer Python (si pas déjà installé)

### 🎯 Ce qu'on va faire:
Vérifier si Python est installé, sinon l'installer.

### 📝 Instructions:

1. **Vérifier si Python 3 est installé**
   - Dans Terminal, taper:
   ```bash
   python3 --version
   ```
   - Appuyer sur Enter

2. **Si vous voyez un numéro de version (ex: Python 3.11.5)**
   - ✅ Parfait! Python est installé
   - Passer à l'étape 1.5

3. **Si vous voyez "command not found"**
   - ❌ Python n'est pas installé
   - Installer Homebrew d'abord:
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```
   - Attendre la fin (5-10 minutes)
   - Puis installer Python:
   ```bash
   brew install python@3.11
   ```
   - Attendre la fin (5 minutes)

4. **Vérifier l'installation**
   - Taper à nouveau:
   ```bash
   python3 --version
   ```
   - Vous devez voir: `Python 3.11.x`

✅ **Vérification**: La commande `python3 --version` affiche un numéro de version

---

## ÉTAPE 1.5: Créer un environnement virtuel

### 🎯 Ce qu'on va faire:
Créer un espace isolé pour les dépendances Python du projet.

### 📝 Instructions:

1. **Créer l'environnement virtuel**
   - Taper:
   ```bash
   python3 -m venv .venv
   ```
   - Appuyer sur Enter
   - Attendre 10-20 secondes

2. **Activer l'environnement**
   - Taper:
   ```bash
   source .venv/bin/activate
   ```
   - Appuyer sur Enter

3. **Vérifier l'activation**
   - Votre ligne de commande doit maintenant commencer par `(.venv)`
   - Exemple: `(.venv) alex@mac ads-automation-agent %`

✅ **Vérification**: Vous voyez `(.venv)` au début de votre ligne de commande

---

## ÉTAPE 1.6: Installer les dépendances Python

### 🎯 Ce qu'on va faire:
Installer toutes les bibliothèques nécessaires au projet.

### 📝 Instructions:

1. **Installer depuis requirements.txt**
   - Taper:
   ```bash
   pip install -r requirements.txt
   ```
   - Appuyer sur Enter
   - **Attendre 2-5 minutes** (beaucoup de texte va défiler - c'est normal!)

2. **Vérifier qu'il n'y a pas d'erreurs**
   - À la fin, vous devez voir: "Successfully installed..."
   - Si erreur, me copier l'erreur exacte

✅ **Vérification**: La commande se termine sans erreur "ERROR"

---

# 🔐 PARTIE 2: CONFIGURATION SÉCURITÉ (45 min)

## ÉTAPE 2.1: Activer FileVault (chiffrement disque)

### 🎯 Ce qu'on va faire:
Chiffrer votre disque Mac pour protéger vos secrets.

### 📝 Instructions:

1. **Ouvrir Préférences Système**
   - Cliquer sur  (pomme) en haut à gauche
   - Sélectionner "Réglages Système" (ou "System Settings")

2. **Aller dans Confidentialité et Sécurité**
   - Dans la barre latérale gauche
   - Cliquer sur "Confidentialité et sécurité"

3. **Activer FileVault**
   - Scroller jusqu'à voir "FileVault"
   - Si "Désactivé", cliquer sur "Activer"
   - Suivre les instructions (créer clé de récupération)
   - **IMPORTANT**: Noter la clé de récupération quelque part de sûr!

⏱️ **Note**: Le chiffrement peut prendre plusieurs heures en arrière-plan. C'est OK, continuez les étapes suivantes.

✅ **Vérification**: FileVault affiche "Activé" (ou "Activation en cours...")

---

## ÉTAPE 2.2: Créer le dossier secrets/

### 🎯 Ce qu'on va faire:
Créer un dossier pour stocker les fichiers de credentials.

### 📝 Instructions:

1. **Dans Terminal, créer le dossier**
   - Taper:
   ```bash
   mkdir secrets
   ```
   - Appuyer sur Enter

2. **Sécuriser les permissions**
   - Taper:
   ```bash
   chmod 700 secrets
   ```
   - Appuyer sur Enter

✅ **Vérification**: Taper `ls -la` et vous voyez `drwx------` à gauche de `secrets`

---

## ÉTAPE 2.3: Copier .env.example vers .env

### 🎯 Ce qu'on va faire:
Créer votre fichier de configuration à partir du template.

### 📝 Instructions:

1. **Copier le fichier**
   - Taper:
   ```bash
   cp .env.example .env
   ```
   - Appuyer sur Enter

2. **Sécuriser les permissions**
   - Taper:
   ```bash
   chmod 600 .env
   ```
   - Appuyer sur Enter

✅ **Vérification**: Le fichier `.env` existe (taper `ls -la .env`)

---

## ÉTAPE 2.4: Lancer le Security Check

### 🎯 Ce qu'on va faire:
Vérifier que la configuration de sécurité est bonne.

### 📝 Instructions:

1. **Lancer le script de sécurité**
   - Taper:
   ```bash
   python3 utils/security_check.py
   ```
   - Appuyer sur Enter

2. **Lire les résultats**
   - ✅ Lignes vertes = OK
   - ⚠️ Lignes jaunes = Avertissements (à corriger si possible)
   - ❌ Lignes rouges = CRITIQUE (à corriger AVANT de continuer)

3. **Si erreurs critiques**
   - Suivre les instructions affichées
   - Relancer le script après correction

✅ **Vérification**: Aucune ligne rouge (❌ CRITIQUE)

---

# 🔑 PARTIE 3: OBTENIR VOS CREDENTIALS (60 min)

Cette partie est **CRITIQUE** - prenez votre temps!

---

## ÉTAPE 3.1: Airtable API Key

### 🎯 Ce qu'on va faire:
Obtenir votre token d'accès Airtable.

### 📝 Instructions:

1. **Aller sur Airtable**
   - Ouvrir navigateur
   - Aller sur: https://airtable.com/create/tokens

2. **Se connecter**
   - Utiliser vos identifiants Airtable

3. **Créer un nouveau token**
   - Cliquer "Create new token"
   - Nom: "Growth OS Agent"
   - Scopes à cocher:
     - ✅ `data.records:read`
     - ✅ `data.records:write`
     - ✅ `schema.bases:read`
   - Access: Sélectionner votre Base Airtable
   - Cliquer "Create token"

4. **Copier le token**
   - Il ressemble à: `pat_abc123xyz789...`
   - **IMPORTANT**: Le copier IMMÉDIATEMENT (il ne sera plus affiché!)

5. **Mettre le token dans .env**
   - Ouvrir .env dans un éditeur de texte:
   ```bash
   open -a TextEdit .env
   ```
   - Trouver la ligne: `AIRTABLE_API_KEY=pat_xxxxxxxx`
   - Remplacer `pat_xxxxxxxx` par votre vrai token
   - Sauvegarder (Cmd+S)
   - Fermer TextEdit

✅ **Vérification**: Dans .env, la ligne AIRTABLE_API_KEY contient `pat_` suivi de caractères

---

## ÉTAPE 3.2: Airtable Base ID

### 🎯 Ce qu'on va faire:
Obtenir l'ID de votre base Airtable.

### 📝 Instructions:

1. **Ouvrir votre base Airtable**
   - Aller sur https://airtable.com
   - Ouvrir la base que vous voulez utiliser

2. **Copier le Base ID depuis l'URL**
   - Regarder l'URL dans le navigateur
   - Elle ressemble à: `https://airtable.com/appXXXXXXXXXXXXXX/...`
   - Le Base ID est la partie `appXXXXXXXXXXXXXX`
   - La copier

3. **Mettre dans .env**
   - Ouvrir .env:
   ```bash
   open -a TextEdit .env
   ```
   - Trouver: `AIRTABLE_BASE_ID=appxxxxxxxx`
   - Remplacer par votre Base ID
   - Sauvegarder

✅ **Vérification**: AIRTABLE_BASE_ID commence par `app`

---

## ÉTAPE 3.3: Meta Access Token

### 🎯 Ce qu'on va faire:
Obtenir un token pour accéder à Meta Ads.

### 📝 Instructions:

1. **Aller sur Meta Business Manager**
   - https://business.facebook.com
   - Se connecter

2. **Créer un System User**
   - Menu hamburger (☰) en haut à gauche
   - Business settings
   - Users → System users
   - Add (Ajouter)
   - Nom: "Growth OS Agent"
   - Role: Admin
   - Create

3. **Générer un token**
   - Cliquer sur le System User créé
   - Generate new token
   - App: Choisir votre app (ou créer une app)
   - Permissions requises:
     - ✅ `ads_management`
     - ✅ `ads_read`
     - ✅ `business_management`
   - Generate token

4. **Copier le token**
   - Il commence par `EAA...`
   - **CRITIQUE**: Le copier immédiatement!

5. **Mettre dans .env**
   - Ouvrir .env
   - Trouver: `META_ACCESS_TOKEN=EAABxxxx`
   - Remplacer par votre token
   - Sauvegarder

✅ **Vérification**: META_ACCESS_TOKEN commence par `EAA`

---

## ÉTAPE 3.4: Slack Webhook URL

### 🎯 Ce qu'on va faire:
Créer un webhook Slack pour recevoir les notifications.

### 📝 Instructions:

1. **Aller sur Slack Apps**
   - https://api.slack.com/apps
   - Se connecter

2. **Créer une app**
   - "Create New App"
   - "From scratch"
   - Nom: "Growth OS Notifications"
   - Workspace: Sélectionner votre workspace
   - Create

3. **Activer Incoming Webhooks**
   - Dans la barre latérale: "Incoming Webhooks"
   - Toggle: Activate Incoming Webhooks → ON
   - Scroll en bas: "Add New Webhook to Workspace"
   - Sélectionner le channel (ex: #marketing-automation)
   - Allow

4. **Copier le Webhook URL**
   - Il ressemble à: `https://hooks.slack.com/services/XXX/YYY/ZZZ`
   - Copier

5. **Mettre dans .env**
   - Ouvrir .env
   - Trouver: `SLACK_WEBHOOK_URL=https://hooks.slack.com/...`
   - Remplacer par votre URL
   - Sauvegarder

✅ **Vérification**: SLACK_WEBHOOK_URL commence par `https://hooks.slack.com`

---

## ÉTAPE 3.5: Google Service Account

### 🎯 Ce qu'on va faire:
Créer un compte de service Google pour accéder aux Sheets.

### 📝 Instructions:

1. **Aller sur Google Cloud Console**
   - https://console.cloud.google.com
   - Se connecter avec votre compte Google

2. **Créer un projet (si vous n'en avez pas)**
   - En haut: Sélectionner projet → "New Project"
   - Nom: "Growth OS"
   - Create

3. **Activer l'API Google Sheets**
   - Menu (☰) → "APIs & Services" → "Library"
   - Chercher: "Google Sheets API"
   - Click dessus → Enable

4. **Créer un Service Account**
   - Menu → "APIs & Services" → "Credentials"
   - "Create Credentials" → "Service Account"
   - Nom: "growth-os-agent"
   - Create and Continue
   - Role: "Editor"
   - Done

5. **Créer une clé JSON**
   - Cliquer sur le Service Account créé
   - Onglet "Keys"
   - "Add Key" → "Create new key"
   - Type: JSON
   - Create
   - **Le fichier JSON se télécharge automatiquement**

6. **Déplacer le fichier JSON**
   - Renommer le fichier téléchargé en: `gsheet_sa.json`
   - Le déplacer dans le dossier `secrets/` de votre projet
   - Via Terminal:
   ```bash
   mv ~/Downloads/growth-os-*.json secrets/gsheet_sa.json
   ```

7. **Mettre le chemin dans .env**
   - Ouvrir .env
   - Trouver: `GOOGLE_SERVICE_ACCOUNT_JSON=/Users/...`
   - Remplacer par le chemin complet:
   ```bash
   pwd
   ```
   - Copier le résultat et ajouter `/secrets/gsheet_sa.json`
   - Exemple: `/Users/alex/ads-automation-agent/secrets/gsheet_sa.json`
   - Sauvegarder

✅ **Vérification**: Le fichier `secrets/gsheet_sa.json` existe

---

## ÉTAPE 3.6: Google Sheets IDs

### 🎯 Ce qu'on va faire:
Créer 2 Google Sheets (LOG et SPEND) et noter leurs IDs.

### 📝 Instructions:

1. **Créer le LOG MASTER Sheet**
   - Aller sur https://sheets.google.com
   - "Blank" (nouvelle feuille)
   - Nommer: "Growth OS - LOG MASTER"
   - Renommer le premier onglet en: `LOG`

2. **Partager avec le Service Account**
   - Cliquer "Share" (en haut à droite)
   - Coller l'email du service account
     - Format: `growth-os-agent@PROJECT-ID.iam.gserviceaccount.com`
     - (Trouvable dans le fichier gsheet_sa.json sous "client_email")
   - Role: Editor
   - Send

3. **Copier le Sheet ID**
   - Regarder l'URL: `https://docs.google.com/spreadsheets/d/SHEET-ID-ICI/edit`
   - Le SHEET-ID est la longue chaîne entre `/d/` et `/edit`
   - Copier

4. **Mettre dans .env**
   - Ouvrir .env
   - Trouver: `LOG_SHEET_ID=1xxxxxxxxx`
   - Remplacer par le SHEET-ID
   - Sauvegarder

5. **Répéter pour SPEND MASTER**
   - Créer une 2ème feuille: "Growth OS - SPEND MASTER"
   - Onglet: `SPEND`
   - Partager avec le même service account
   - Copier le Sheet ID
   - Dans .env: `SPEND_SHEET_ID=...`

✅ **Vérification**: LOG_SHEET_ID et SPEND_SHEET_ID remplis dans .env

---

## ÉTAPE 3.7: Anthropic API Key

### 🎯 Ce qu'on va faire:
Obtenir une clé API pour Claude AI (auto-correction).

### 📝 Instructions:

1. **Aller sur Anthropic Console**
   - https://console.anthropic.com
   - Se connecter (créer compte si nécessaire)

2. **Créer une API Key**
   - Menu: "API Keys"
   - "Create Key"
   - Nom: "Growth OS Self-Healing"
   - Create

3. **Copier la clé**
   - Elle commence par `sk-ant-`
   - **CRITIQUE**: La copier immédiatement!

4. **Mettre dans .env**
   - Ouvrir .env
   - Trouver: `ANTHROPIC_API_KEY=sk-ant-xxxxx`
   - Remplacer
   - Sauvegarder

✅ **Vérification**: ANTHROPIC_API_KEY commence par `sk-ant-`

---

## ÉTAPE 3.8: GitHub Token (Optionnel)

### 🎯 Ce qu'on va faire:
Créer un token GitHub pour les commits automatiques.

### 📝 Instructions:

1. **Aller sur GitHub**
   - https://github.com
   - Se connecter (créer compte si nécessaire)

2. **Créer un token**
   - Settings → Developer settings → Personal access tokens
   - Tokens (classic) → Generate new token
   - Note: "Growth OS Agent"
   - Expiration: 90 days
   - Scopes à cocher:
     - ✅ `repo` (Full control)
   - Generate token

3. **Copier le token**
   - Commence par `ghp_`
   - **Le copier immédiatement!**

4. **Mettre dans .env**
   - Ouvrir .env
   - Trouver: `GITHUB_TOKEN=ghp_xxxxx`
   - Remplacer
   - Sauvegarder

5. **Créer un repository GitHub**
   - Sur GitHub: New repository
   - Nom: `ads-automation-agent`
   - Private
   - Create

6. **Noter le nom du repo dans .env**
   - Format: `votre-username/ads-automation-agent`
   - Dans .env: `GITHUB_REPO=...`

✅ **Vérification**: GITHUB_TOKEN et GITHUB_REPO remplis

---

# ✅ PARTIE 4: VÉRIFICATION FINALE (15 min)

## ÉTAPE 4.1: Re-lancer Security Check

### 📝 Instructions:

```bash
python3 utils/security_check.py
```

**Résultat attendu**:
- ✅ Toutes les vérifications vertes
- ⚠️ Peut-être quelques warnings (OK)
- ❌ AUCUNE erreur critique

---

## ÉTAPE 4.2: Tester la connexion Airtable

### 📝 Instructions:

```bash
python3 -c "
from airtable.client import AirtableClient
client = AirtableClient.from_env()
print('✅ Connexion Airtable OK!')
"
```

**Si erreur**: Vérifier AIRTABLE_API_KEY et AIRTABLE_BASE_ID

---

## ÉTAPE 4.3: Tester la connexion Slack

### 📝 Instructions:

```bash
python3 -c "
from slack.notifier import SlackNotifier
notifier = SlackNotifier.from_env()
notifier.info('🎉 Test connexion Slack!')
print('✅ Vérifiez Slack, vous devriez voir le message')
"
```

**Vérifier**: Votre channel Slack a reçu le message

---

## ÉTAPE 4.4: Test setup complet

### 📝 Instructions:

```bash
python3 test_setup.py
```

**Attendre 1-2 minutes**

**Résultat attendu**:
- ✅ Toutes les connexions testées
- ✅ Aucune erreur

**Si erreur**: Me copier le message d'erreur exact

---

# 🚀 PARTIE 5: PREMIER DÉMARRAGE (TEST)

## ÉTAPE 5.1: Vérifier mode DRY_RUN

### 📝 Instructions:

1. **Ouvrir .env**
   ```bash
   open -a TextEdit .env
   ```

2. **Vérifier ces lignes**:
   ```
   DRY_RUN=true                    ← DOIT être true
   PUBLISH_ENABLED=false           ← DOIT être false
   AUTO_PAUSE_ENABLED=false        ← DOIT être false
   ENABLE_AUTO_HEALING=false       ← DOIT être false (pour l'instant)
   ```

3. **Sauvegarder si vous avez changé quelque chose**

✅ **CRITIQUE**: En mode DRY_RUN, aucune action réelle ne sera prise!

---

## ÉTAPE 5.2: Lancer l'agent (première fois)

### 📝 Instructions:

1. **Lancer l'agent**
   ```bash
   python3 main.py
   ```

2. **Observer les messages**
   - Vous devez voir:
   ```
   🤖 ADS AUTOMATION AGENT - GROWTH OS
   Environment: prod
   Dry Run Mode: ✅ YES (safe)
   ...
   ⏰ Scheduler running
   ```

3. **Laisser tourner 5 minutes**
   - Observer les messages dans Terminal
   - Vérifier Slack (devrait recevoir notifications)

4. **Arrêter l'agent**
   - Appuyer sur Ctrl+C dans Terminal

✅ **Vérification**: 
- Aucune erreur dans Terminal
- Messages reçus dans Slack

---

## ÉTAPE 5.3: Vérifier les logs

### 📝 Instructions:

```bash
# Voir les dernières lignes du log
tail -20 storage/agent.out.log
```

**Vérifier**:
- Pas d'erreurs
- Messages normaux de démarrage/arrêt

---

# 🎉 FÉLICITATIONS!

## Vous avez installé le système avec succès! ✅

### Prochaines étapes:

1. **Lire SECURITY.md** (CRITIQUE!)
   - Comprendre tous les risques
   - Suivre les bonnes pratiques

2. **Configurer Airtable**
   - Créer les 7 tables
   - Suivre config/airtable_schema.md

3. **Tester en DRY_RUN pendant 1 semaine**
   - Observer le comportement
   - Vérifier les logs quotidiennement

4. **Activer progressivement**
   - Voir GROWTH_OS_CHECKLIST.md

---

## ❓ Besoin d'aide?

### Si problème pendant l'installation:

1. **Noter EXACTEMENT**:
   - Quelle étape causait problème
   - Message d'erreur complet
   - Ce que vous avez essayé

2. **Me le copier dans le chat**

3. **Ne pas paniquer!**
   - On va résoudre ensemble
   - C'est normal d'avoir des petits problèmes

---

## 📝 Checklist finale

- [ ] Python 3.11+ installé
- [ ] Environnement virtuel créé et activé
- [ ] Dépendances installées
- [ ] FileVault activé
- [ ] Dossier secrets/ créé avec bonnes permissions
- [ ] Fichier .env créé avec permissions 600
- [ ] Tous les credentials dans .env
- [ ] Security check passe (aucune erreur rouge)
- [ ] Tests de connexion OK
- [ ] Premier démarrage réussi
- [ ] Logs vérifiés
- [ ] SECURITY.md lu

**Si TOUS cochés: PARFAIT! Vous êtes prêt! 🚀**

---

**Version**: 1.0  
**Créé pour**: Utilisateurs débutants  
**Durée**: 2-3 heures  
**Niveau requis**: Aucun
