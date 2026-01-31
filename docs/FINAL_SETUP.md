# 🚀 DURUM AI Agent - Setup Ultime

## ✅ Qu'on a déjà fait

| ✅ | Tâche |
|:---:|-------|
| ✅ | **GitHub** - Repo créé + code pushé |
| ✅ | **.env.example** - Template de configuration |
| 🔄 | **Airtable** - À créer (8 tables) |
| 🔄 | **Supabase** - À créer (12 tables) |
| ⏳ | **Configuration .env** - À remplir |
| ⏳ | **Déploiement** - À faire |

---

## 🎯 Prochaines étapes

### 1️⃣ AIRTABLE (5 min)

**Créer la base Airtable avec ces 8 tables :**

```
1. clients
2. products
3. funnels
4. ads_library
5. suggestions (garde 30 derniers jours)
6. decisions (garde 90 derniers jours)
7. validation_queue
8. winning_patterns
```

**Colonnes pour chaque table :** Voir `NEW_ARCHITECTURE_AIRTABLE_SUPABASE.md`

**URL :** https://airtable.com/create

---

### 2️⃣ SUPABASE (10 min)

**Option A : Via SQL Editor (si tu as accès)**
1. Aller à https://app.supabase.com
2. Sélectionner le projet `ads-automation-agent`
3. Aller à SQL Editor
4. Copier-coller le SQL complet de `NEW_ARCHITECTURE_AIRTABLE_SUPABASE.md`
5. Exécuter

**Option B : Via Supabase CLI**
```bash
cd ads-automation-agent
export SUPABASE_URL=https://xxx.supabase.co
export SUPABASE_KEY=eyxxx
export SUPABASE_DB_PASSWORD=xxxxx

# Exécuter les migrations
supabase db push
```

**Schéma SQL :** Voir section SQL dans `NEW_ARCHITECTURE_AIRTABLE_SUPABASE.md`

---

### 3️⃣ OBTENIR LES CREDENTIALS

#### Airtable
1. https://airtable.com/account/tokens
2. Créer un token personnalisé (scope: data.records:read/write, data.bases:read)
3. Copier le token → `AIRTABLE_API_KEY` dans `.env`
4. Aller dans ta base → Copier l'ID → `AIRTABLE_BASE_ID`

#### Supabase
1. https://app.supabase.com → Projet → Settings → API
2. Copier `Project URL` → `SUPABASE_URL`
3. Copier `anon key` → `SUPABASE_KEY`
4. Database password → `SUPABASE_DB_PASSWORD`

#### Meta Ads
1. https://business.facebook.com → Outils → Pixel & Events → Conversions API
2. Générer un token → `META_ACCESS_TOKEN`
3. Copier l'ID → `META_BUSINESS_ACCOUNT_ID`

#### Slack
1. https://api.slack.com/apps → Créer une app
2. Invite le bot dans ton workspace
3. Copier `Bot Token` → `SLACK_BOT_TOKEN`
4. Copier `Signing Secret` → `SLACK_SIGNING_SECRET`

#### Anthropic
1. https://console.anthropic.com → API Keys
2. Créer une clé → `ANTHROPIC_API_KEY`

---

### 4️⃣ FICHIER .env

```bash
# Copier .env.example vers .env
cp .env.example .env

# Remplir les valeurs
nano .env  # ou ton éditeur
```

**Assurez-vous que ces valeurs sont remplies :**
```
✅ AIRTABLE_API_KEY
✅ AIRTABLE_BASE_ID
✅ SUPABASE_URL
✅ SUPABASE_KEY
✅ META_ACCESS_TOKEN
✅ SLACK_BOT_TOKEN
✅ ANTHROPIC_API_KEY
```

---

### 5️⃣ TEST DE CONNEXION

```bash
# Tester les connections
python3 -c "
from database.client import AirtableClient, SupabaseClient
air = AirtableClient()
supa = SupabaseClient()
print('✅ Airtable connected')
print('✅ Supabase connected')
"
```

---

### 6️⃣ LANCER LE SYSTÈME

```bash
# Environnement virtuel
python3 -m venv .venv
source .venv/bin/activate

# Installer dépendances
pip install -r requirements.txt

# Premier lancement (test)
python3 main.py

# Ou en cron automatique (9h chaque jour)
crontab -e
# Ajouter: 0 9 * * * cd ~/ads-automation-agent && source .venv/bin/activate && python3 main.py
```

---

### 7️⃣ DEPLOY EN LIGNE (Optional)

**Vercel** (recommandé pour Node apps)
**Railway** (Python apps)
**Render** (Python/Node/PostgreSQL)

```bash
# Exemple Railway
railway link
railway variables
railway deploy
```

---

## 📊 CHECKLIST FINALE

```
[ ] GitHub repo créé + code pushé
[ ] Airtable base créée + 8 tables
[ ] Supabase project setup + 12 tables
[ ] .env rempli avec credentials
[ ] Test de connexion OK
[ ] Cron job configuré
[ ] (Optional) Déploiement en ligne
```

---

## 🆘 TROUBLESHOOTING

**Airtable connection error:**
```python
# Vérifier la clé API
curl -H "Authorization: Bearer YOUR_KEY" https://api.airtable.com/v0/meta/bases
```

**Supabase connection error:**
```python
# Vérifier l'URL et la clé
import requests
resp = requests.get("https://YOUR_URL/rest/v1/", headers={"Authorization": "Bearer YOUR_KEY"})
print(resp.status_code)
```

**Script pas d'exécution:**
```bash
# Vérifier Python
python3 --version

# Vérifier les dépendances
pip list | grep -E "airtable|supabase|anthropic"
```

---

## 📞 SUPPORT

- Documentation complète: `docs/INDEX_COMPLET.md`
- Architecture DB: `docs/NEW_ARCHITECTURE_AIRTABLE_SUPABASE.md`
- Setup guide: `docs/SETUP_GUIDE_COMPLET.md`

---

**🎯 Suivre ce guide et tu auras un système 100% opérationnel en moins d'1h!**
