# 🔗 GUIDE D'INTÉGRATION GROWTH OS

## 🎯 Objectif

Connecter l'agent d'automatisation avec **vos Google Sheets Growth OS existants** sans toucher à Make.com.

---

## 📋 Prérequis

✅ Vous avez déjà:
- Growth OS fonctionnel (Make.com)
- Google Sheets avec LOG, SPEND, METRICS
- Service Account Google configuré
- Mac Mini M4 prêt

✅ Temps estimé: **30 minutes**

---

## 🗂️ ÉTAPE 1: Identifier Vos Sheet IDs (10 min)

### 1.1 Liste des Sheets à identifier

Vous avez besoin des Sheet IDs pour:

| Sheet | Description | Variable .env |
|-------|-------------|---------------|
| LOG_MASTER | Événements bruts | GROWTHOS_LOG_SHEET_ID |
| SPEND_MASTER | Dépenses Meta | GROWTHOS_SPEND_SHEET_ID |
| 02_metrics_period | Métriques agrégées | GROWTHOS_METRICS_SHEET_ID |
| 01_clients_master | Config clients | GROWTHOS_CLIENTS_SHEET_ID |
| 01.1_reps_master | Reps commerciaux | GROWTHOS_REPS_SHEET_ID |

### 1.2 Comment trouver un Sheet ID

Pour **chaque** Google Sheet:

1. **Ouvrir le Google Sheet** dans votre navigateur

2. **Regarder l'URL**:
   ```
   https://docs.google.com/spreadsheets/d/1abc123xyz789def/edit#gid=0
   ```

3. **Copier la partie entre `/d/` et `/edit`**:
   ```
   1abc123xyz789def
   ```
   ☝️ C'est le Sheet ID

4. **Noter dans un fichier texte** temporaire:
   ```
   LOG_MASTER: 1abc123xyz789def
   SPEND_MASTER: 1xyz789abc123def
   (etc.)
   ```

### 1.3 Identifier les noms d'onglets

Pour chaque Sheet, noter aussi le **nom exact de l'onglet**:

- Si votre onglet s'appelle "LOG_MASTER" → OK
- Si votre onglet s'appelle "LOG" → Noter "LOG"
- Si votre onglet s'appelle "Events" → Noter "Events"

**IMPORTANT**: Le nom doit être EXACT (majuscules/minuscules comptent)

---

## 📄 ÉTAPE 2: Créer le Nouveau Sheet AGENT_DECISIONS (5 min)

### 2.1 Créer un nouveau Google Sheet

1. Aller sur https://sheets.google.com
2. Créer une nouvelle feuille (vierge)
3. La nommer: **"Growth OS - Agent Decisions"**
4. Renommer le premier onglet en: **"AGENT_DECISIONS"**

### 2.2 Récupérer le Sheet ID

- Copier le Sheet ID de cette nouvelle feuille (méthode ci-dessus)
- Noter: `AGENT_DECISIONS: 1nouveau_sheet_id`

### 2.3 Partager avec le Service Account

**CRITIQUE**: Le Service Account doit avoir accès!

1. Dans le nouveau Sheet, cliquer **"Share"** (Partager)

2. **Trouver l'email du Service Account**:
   - Ouvrir votre fichier `secrets/gsheet_sa.json`
   - Chercher la ligne `"client_email"`
   - Copier l'email (format: `nom@projet.iam.gserviceaccount.com`)

3. **Dans Share → Add people**:
   - Coller l'email du service account
   - Role: **Editor**
   - Décocher "Notify people" (pas besoin)
   - Cliquer "Share"

✅ **Vérification**: L'email du service account apparaît dans "People with access"

---

## ⚙️ ÉTAPE 3: Configurer .env (10 min)

### 3.1 Ouvrir votre fichier .env

Sur votre Mac Mini:

```bash
cd ~/ads-automation-agent
open -a TextEdit .env
```

### 3.2 Ajouter les nouvelles variables

**Copier-coller ces lignes à la fin de .env**:

```env
# ============================================
# GROWTH OS INTEGRATION
# ============================================

# Sheet IDs de votre Growth OS
GROWTHOS_LOG_SHEET_ID=REMPLACER_PAR_VOTRE_ID
GROWTHOS_LOG_TAB=LOG_MASTER

GROWTHOS_SPEND_SHEET_ID=REMPLACER_PAR_VOTRE_ID
GROWTHOS_SPEND_TAB=SPEND_MASTER

GROWTHOS_METRICS_SHEET_ID=REMPLACER_PAR_VOTRE_ID
GROWTHOS_METRICS_TAB=02_metrics_period

GROWTHOS_CLIENTS_SHEET_ID=REMPLACER_PAR_VOTRE_ID
GROWTHOS_CLIENTS_TAB=01_clients_master

GROWTHOS_REPS_SHEET_ID=REMPLACER_PAR_VOTRE_ID
GROWTHOS_REPS_TAB=01.1_reps_master

# Nouveau sheet pour décisions agent
GROWTHOS_DECISIONS_SHEET_ID=REMPLACER_PAR_VOTRE_ID
GROWTHOS_DECISIONS_TAB=AGENT_DECISIONS

# Clients à analyser (séparés par virgules)
GROWTHOS_CLIENTS=avego,client2,client3
```

### 3.3 Remplacer les IDs

Pour **chaque ligne** `REMPLACER_PAR_VOTRE_ID`:

1. Prendre le Sheet ID que vous avez noté à l'étape 1
2. Remplacer `REMPLACER_PAR_VOTRE_ID` par l'ID réel
3. Vérifier le nom de l'onglet (TAB) est correct

**Exemple après remplacement**:

```env
GROWTHOS_LOG_SHEET_ID=1abc123xyz789def
GROWTHOS_LOG_TAB=LOG_MASTER

GROWTHOS_SPEND_SHEET_ID=1xyz789abc123def
GROWTHOS_SPEND_TAB=SPEND_MASTER

# etc.
```

### 3.4 Configurer la liste des clients

Dernière ligne: `GROWTHOS_CLIENTS=avego,client2,client3`

Remplacer par vos client_keys réels (ceux dans `01_clients_master.key`):

```env
GROWTHOS_CLIENTS=avego,tradingacademy,bootcamp
```

**Où trouver les client_keys?**

- Ouvrir votre Google Sheet `01_clients_master`
- Colonne `key` = ce sont vos client_keys
- Les lister séparés par des virgules (sans espaces)

### 3.5 Sauvegarder .env

- Cmd + S pour sauvegarder
- Fermer TextEdit

---

## 🧪 ÉTAPE 4: Tester la Connexion (5 min)

### 4.1 Partager TOUS vos Sheets avec le Service Account

**IMPORTANT**: Chaque Sheet Growth OS doit être partagé!

Pour **chacun** de vos Sheets (LOG, SPEND, METRICS, CLIENTS, REPS):

1. Ouvrir le Sheet
2. Cliquer "Share"
3. Ajouter l'email du service account
4. Role: **Viewer** (lecture seule)
5. Share

✅ **Pourquoi Viewer?** L'agent lit seulement, Make.com continue d'écrire.

### 4.2 Lancer le test de connexion

Dans Terminal:

```bash
cd ~/ads-automation-agent
source .venv/bin/activate
python3 test_growthos_connection.py
```

**Ce script va**:
1. Tester lecture de chaque Sheet
2. Afficher le nombre de lignes
3. Valider que les colonnes attendues existent
4. Tester écriture dans AGENT_DECISIONS

**Résultat attendu**:

```
🔍 Test connexion Growth OS...

✅ LOG_MASTER: 1,234 événements
✅ SPEND_MASTER: 5,678 lignes
✅ 02_metrics_period: 123 périodes
✅ 01_clients_master: 3 clients
✅ 01.1_reps_master: 8 reps
✅ AGENT_DECISIONS: Écriture OK

🎉 Tous les tests passent!
```

**Si erreur**:
- Vérifier Sheet ID correct
- Vérifier nom onglet exact
- Vérifier service account a accès
- Me copier l'erreur complète

---

## 🚀 ÉTAPE 5: Premier Cycle d'Analyse (Test)

### 5.1 Lancer analyse manuelle

```bash
python3 run_growthos_analysis.py
```

**Ce script va**:
1. Lire vos données Growth OS
2. Appliquer les 7 règles de décision
3. Générer recommandations
4. Écrire dans AGENT_DECISIONS
5. (Optionnel) Envoyer alertes Slack

**Sortie attendue**:

```
🔍 Analyse Growth OS...

📊 Client: avego
   - Métriques semaine: ROI 2.5x, CPA $150
   - 2 décisions générées:
     ✅ SCALE +20% (ROI > 2x)
     ⚠️ No-show rate 32%

📊 Client: tradingacademy
   - Métriques semaine: ROI 1.2x, CPA $280
   - 1 décision générée:
     🛑 STOP - CPA trop élevé

✅ Total: 3 décisions écrites dans AGENT_DECISIONS
```

### 5.2 Vérifier le Sheet AGENT_DECISIONS

1. Ouvrir votre Sheet "Growth OS - Agent Decisions"
2. Onglet "AGENT_DECISIONS"
3. Vous devez voir:
   - Headers en ligne 1
   - Vos décisions en lignes 2, 3, 4...

**Colonnes attendues**:

| decision_id | timestamp | client_key | rule_triggered | recommendation |
|-------------|-----------|------------|----------------|----------------|
| abc123 | 2025-01-31... | avego | excellent_performance | 📈 SCALE +20%... |
| def456 | 2025-01-31... | avego | high_no_show_rate | 📞 NO-SHOW... |

✅ **Si vous voyez ça: PARFAIT! L'intégration fonctionne!**

---

## ⏰ ÉTAPE 6: Automatiser l'Analyse (5 min)

### 6.1 Configurer l'intervalle d'analyse

Dans `.env`, ajouter:

```env
# Growth OS Analysis (minutes)
GROWTHOS_ANALYSIS_MINUTES=60
```

Cela lance l'analyse toutes les 60 minutes.

### 6.2 Activer dans main.py

L'analyse Growth OS est **déjà intégrée** dans le scheduler.

Quand vous lancez:

```bash
python3 main.py
```

Le système va:
1. Cycle Publish (toutes les 5 min) - Meta Ads
2. Cycle Analysis (toutes les 60 min) - **Growth OS** ✨
3. Alertes Slack automatiques

---

## 📊 ÉTAPE 7: Comprendre les Règles de Décision

### Les 7 Règles Actives

| # | Règle | Déclencheur | Action |
|---|-------|-------------|--------|
| 1 | **High CPA** | CPA > seuil OU $500 sans vente | 🛑 STOP/RÉDUIRE |
| 2 | **Excellent Performance** | ROI ≥ 3x avec 3+ ventes | 📈 SCALE +20% |
| 3 | **Revenue Leak** | 3+ bookings sans vente (7 jours) | 💸 Audit closing |
| 4 | **Rep Underperformance** | Close rate < team avg -30% | 👤 Coaching |
| 5 | **Creative Fatigue** | CTR baisse de 30%+ | 🎨 Nouvelle créative |
| 6 | **High No-Show Rate** | No-show > 30% | 📞 Améliorer rappels |
| 7 | **Critical Health** | Health score < 50 | 🚨 Audit complet |

### Personnaliser les Seuils

Dans `01_clients_master`, vous pouvez ajouter ces colonnes (optionnel):

```
max_cpa              # Ex: 200 (défaut si absent)
min_roi_scale        # Ex: 3.0 (défaut si absent)
max_weekly_spend     # Ex: 5000 (défaut: 10000)
allow_auto_pause     # true/false (défaut: false)
```

**Sans ces colonnes**: L'agent utilise des valeurs par défaut conservatrices.

---

## 🔔 ÉTAPE 8: Configurer Alertes Slack (Optionnel)

Les décisions peuvent être envoyées automatiquement dans Slack.

### 8.1 Activer notifications

Dans `.env`:

```env
GROWTHOS_SLACK_ENABLED=true
```

### 8.2 Format des alertes

Chaque décision génère un message Slack:

```
🛑 HIGH CPA NO SALES

Client: avego
Période: W - 2025-W05
Condition: Spend $523.50 avec 0 vente

Recommandation:
🛑 STOP - Dépensé $523.50 sans aucune vente. 
Revoir campagnes urgence.

Confiance: HIGH
Timestamp: 2025-01-31 10:23:15
```

---

## ✅ CHECKLIST FINALE

Avant de mettre en production, vérifier:

- [ ] Tous les Sheet IDs configurés dans .env
- [ ] Tous les Sheets partagés avec service account
- [ ] test_growthos_connection.py passe tous les tests
- [ ] run_growthos_analysis.py génère des décisions
- [ ] AGENT_DECISIONS contient des lignes
- [ ] Alertes Slack reçues (si activé)
- [ ] Variables GROWTHOS_CLIENTS contient vos clients

---

## 🎯 Résumé de l'Architecture

```
┌──────────────────────────────────┐
│   MAKE.COM (votre système)       │
│   Continue de tourner 24/7       │
│                                  │
│   - Webhooks GHL                 │
│   - Import Meta Ads              │
│   - Calculs métriques            │
│   - Rapports Slack               │
└──────────────────────────────────┘
            ↓ (écrit dans)
┌──────────────────────────────────┐
│   GOOGLE SHEETS (vos données)    │
│                                  │
│   - LOG_MASTER                   │
│   - SPEND_MASTER                 │
│   - 02_metrics_period            │
│   - 01_clients_master            │
└──────────────────────────────────┘
            ↓ (lu par)
┌──────────────────────────────────┐
│   NOTRE AGENT (Mac Mini M4)      │
│   Analyse toutes les 60 min      │
│                                  │
│   - Lit vos métriques            │
│   - Applique 7 règles            │
│   - Génère recommandations       │
└──────────────────────────────────┘
            ↓ (écrit dans)
┌──────────────────────────────────┐
│   AGENT_DECISIONS (nouveau)      │
│   Historique des décisions       │
└──────────────────────────────────┘
            ↓ (notifie)
┌──────────────────────────────────┐
│   SLACK (alertes)                │
│   Recommandations actionnables   │
└──────────────────────────────────┘
```

**Avantages**:
- ✅ Zéro duplication de données
- ✅ Make.com continue normalement
- ✅ Agent 100% indépendant
- ✅ Pas de conflit
- ✅ Utilise VOS calculs de métriques

---

## 🆘 Dépannage

### Erreur: "Sheet not found"
- Vérifier Sheet ID exact
- Vérifier que le Sheet existe
- Vérifier service account a accès

### Erreur: "Permission denied"
- Sheet pas partagé avec service account
- Partager avec email dans gsheet_sa.json
- Role: Viewer (lecture) ou Editor (AGENT_DECISIONS)

### Pas de décisions générées
- Vérifier que vos Sheets contiennent des données
- Vérifier GROWTHOS_CLIENTS contient vos client_keys exacts
- Lancer en mode debug: `python3 run_growthos_analysis.py --debug`

### Colonnes manquantes
- Vérifier noms de colonnes dans vos Sheets
- Respecter exactement les noms dans la documentation
- Ou adapter le code si vos noms diffèrent

---

## 📞 Support

Si problème pendant le setup:

1. **Copier l'erreur exacte** du Terminal
2. **Noter quelle étape** causait problème
3. **Me partager** dans le chat

Je vous aiderai à résoudre!

---

**Prêt à commencer le setup?** 🚀

Suivez les étapes dans l'ordre et prenez votre temps!
