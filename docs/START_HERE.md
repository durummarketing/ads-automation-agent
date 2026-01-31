# 🤖 Self-Healing System - Guide Complet

## Objectif

Le système d'auto-correction utilise **Claude AI** pour détecter, analyser et corriger automatiquement les erreurs du code, **sans intervention humaine**.

---

## 🌟 Fonctionnalités

### 1. Détection Automatique d'Erreur
Toute exception Python est interceptée et analysée.

### 2. Notification Slack Immédiate
Dès qu'une erreur survient, vous recevez:
- Type d'erreur
- Message complet
- Contexte (fonction, module, client)
- Traceback

### 3. Analyse par Claude AI
Claude AI analyse l'erreur et détermine:
- ✅ Si elle peut être corrigée automatiquement
- 📊 Catégorie (syntax, import, logic, api, config)
- 🎯 Cause racine
- 📁 Fichier concerné
- 📈 Niveau de confiance

### 4. Génération du Fix
Si l'erreur est réparable, Claude génère:
- Code corrigé complet
- Explication de la correction
- Résumé des changements

### 5. Application Automatique
Le système:
- ✅ Crée un backup du fichier original
- ✅ Applique le fix
- ✅ Vérifie la syntaxe Python
- ✅ Restaure le backup si syntaxe invalide

### 6. Commit & Push GitHub
- ✅ Commit automatique avec message détaillé
- ✅ Push vers votre repository
- ✅ Hash du commit notifié dans Slack

### 7. Notification Complète
Slack reçoit un rapport détaillé:
- ✅ Analyse Claude AI
- ✅ Fichiers modifiés
- ✅ Explication du fix
- ✅ Lien vers le commit GitHub

---

## ⚙️ Configuration

### Variables d'Environnement Requises

```env
# Activer le self-healing
ENABLE_AUTO_HEALING=true

# API Key Anthropic (pour Claude AI)
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxxxxxxxxxx

# GitHub (optionnel mais recommandé)
GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxxx
GITHUB_REPO=votre-username/ads-automation-agent
```

### Obtenir les Credentials

#### 1. Anthropic API Key

1. Aller sur https://console.anthropic.com
2. Créer un compte ou se connecter
3. Aller dans "API Keys"
4. Créer une nouvelle clé
5. Copier dans `.env` → `ANTHROPIC_API_KEY`

**Coût**: ~$0.01 par analyse d'erreur (très faible)

#### 2. GitHub Token (Optionnel)

1. Aller sur https://github.com/settings/tokens
2. Generate new token (classic)
3. Scopes requis:
   - `repo` (Full control of private repositories)
   - `workflow` (Update GitHub Action workflows)
4. Copier dans `.env` → `GITHUB_TOKEN`

#### 3. GitHub Repo

Format: `username/repository-name`

Exemple: `durum-agency/ads-automation-agent`

---

## 📊 Exemple de Flow Complet

### Scénario: ImportError

```python
# Erreur dans engine/decision_engine.py
from non_existent_module import something  # ❌ Module n'existe pas
```

### Étape 1: Détection (0 secondes)

```
🚨 ERREUR DÉTECTÉE - err_20260128_143022

Type: ImportError
Message: No module named 'non_existent_module'

Contexte:
• Fonction: run_publish_cycle
• Module: engine.decision_engine
• Client: avego

Traceback:
  File "engine/decision_engine.py", line 15, in run_publish_cycle
    from non_existent_module import something
ImportError: No module named 'non_existent_module'

⏳ Analyse en cours avec Claude AI...
```

### Étape 2: Analyse Claude (5-10 secondes)

Claude AI répond:
```json
{
  "fixable": true,
  "reason": "Import incorrect - module n'existe pas",
  "error_category": "import",
  "root_cause": "Tentative d'import d'un module non installé ou inexistant",
  "affected_file": "engine/decision_engine.py",
  "confidence": "high"
}
```

Slack:
```
🤖 Claude AI analyse l'erreur err_20260128_143022...
```

### Étape 3: Génération Fix (10-15 secondes)

Claude génère le fix:
```python
# Code corrigé: retirer l'import incorrect
# Au lieu de:
# from non_existent_module import something

# Claude identifie que cet import n'est pas utilisé
# ou propose une alternative valide
```

Slack:
```
🔧 Génération du fix pour err_20260128_143022...
```

### Étape 4: Application (1 seconde)

```
✅ Backup créé: storage/errors/err_20260128_143022_backup_decision_engine.py
✅ Fix appliqué
✅ Syntaxe Python validée
```

Slack:
```
✏️ Application du fix pour err_20260128_143022...
```

### Étape 5: Git Commit (2-3 secondes)

```bash
git add engine/decision_engine.py
git commit -m "🤖 Auto-fix: err_20260128_143022

Error: Tentative d'import d'un module non installé
Category: import
Files: engine/decision_engine.py

Fix: Retrait de l'import non utilisé 'non_existent_module'

Confidence: high"

git push
```

Slack:
```
📤 Push du fix vers GitHub...
```

### Étape 6: Notification Finale

```
✅ AUTO-FIX APPLIQUÉ - err_20260128_143022

Analyse Claude AI:
• Cause: Tentative d'import d'un module non installé ou inexistant
• Catégorie: import
• Confiance: high

Correction appliquée:
• Fichiers modifiés: engine/decision_engine.py
• Retrait de l'import non utilisé qui causait l'erreur

Changements:
Ligne 15: Suppression de 'from non_existent_module import something'
Module non nécessaire pour le fonctionnement

Actions prises:
✅ Code corrigé appliqué
✅ Backup créé: storage/errors/err_20260128_143022_backup_decision_engine.py
✅ Syntaxe Python validée
✅ Push GitHub effectué

Statut: Système opérationnel
L'agent va redémarrer automatiquement avec le fix.
```

**Durée totale**: 20-30 secondes

---

## 🎯 Types d'Erreurs Corrigibles

### ✅ Haute Confiance (auto-fix recommandé)

1. **Syntax Errors**
   - Parenthèses manquantes
   - Indentation incorrecte
   - Virgules manquantes

2. **Import Errors**
   - Modules inexistants
   - Imports circulaires
   - Chemins incorrects

3. **Type Errors**
   - Conversion de types
   - Arguments manquants
   - Retours de fonction

4. **Attribute Errors**
   - Attributs inexistants
   - Typos dans noms

### ⚠️ Moyenne Confiance (validation recommandée)

5. **Logic Errors**
   - Conditions incorrectes
   - Boucles infinies
   - Calculs erronés

6. **API Errors**
   - Rate limiting
   - Credentials invalides
   - Endpoints incorrects

### ❌ Non Corrigibles Automatiquement

7. **Business Logic Complex**
   - Décisions métier
   - Règles client spécifiques
   - Algorithmes complexes

8. **External Dependencies**
   - Services tiers down
   - Network issues
   - Permissions manquantes

---

## 🔒 Sécurité & Validation

### Backups Automatiques

Chaque fix crée un backup:
```
storage/errors/{error_id}_backup_{filename}
```

Vous pouvez restaurer manuellement si besoin.

### Validation Syntaxe

Avant d'appliquer un fix, le système:
```python
compile(fixed_code, filename, 'exec')
```

Si syntaxe invalide → Restauration automatique du backup.

### Git History

Chaque fix est dans l'historique Git:
```bash
git log --oneline | grep "Auto-fix"
```

Vous pouvez revert n'importe quel fix:
```bash
git revert <commit_hash>
```

---

## 📈 Monitoring

### Logs d'Erreur

Toutes les erreurs sont sauvegardées:
```
storage/errors/{error_id}.json
```

Contient:
- Erreur complète
- Contexte
- Traceback
- Tentative de fix
- Résultat

### Dashboard (futur)

Visualiser:
- Nombre d'erreurs par jour
- Taux de succès auto-fix
- Types d'erreurs les plus fréquents
- Temps de résolution moyen

---

## ⚙️ Configuration Avancée

### Désactiver pour des Modules Spécifiques

Éditer `engine/self_healing.py`:

```python
# Liste noire de fichiers
BLACKLIST_FILES = [
    "config/client_rules_schema.md",  # Jamais modifier
    "secrets/",  # Jamais toucher
]
```

### Seuil de Confiance

Par défaut, Claude doit avoir confiance "high" ou "medium".

Ajuster dans `.env`:
```env
AUTO_FIX_MIN_CONFIDENCE=high  # high, medium, low
```

### Rate Limiting Claude

Limiter les appels Claude par heure:
```env
MAX_CLAUDE_CALLS_PER_HOUR=10
```

---

## 🧪 Testing

### Test du Système

Créer une erreur intentionnelle:

```python
# Dans un fichier test_self_healing.py
def test_error():
    x = undefined_variable  # ❌ Erreur intentionnelle
    return x

test_error()
```

Lancer:
```bash
python test_self_healing.py
```

Observer:
1. Slack reçoit l'alerte
2. Claude analyse
3. Fix généré et appliqué
4. Commit GitHub
5. Notification finale

### Désactiver Temporairement

```env
ENABLE_AUTO_HEALING=false
```

Les erreurs seront notifiées mais pas corrigées.

---

## 💡 Best Practices

### 1. Commencer avec Monitoring Seul

```env
ENABLE_AUTO_HEALING=true
AUTO_FIX_MIN_CONFIDENCE=high  # Seulement haute confiance
```

Observer pendant 1 semaine.

### 2. Activer Progressivement

Semaine 2:
```env
AUTO_FIX_MIN_CONFIDENCE=medium
```

### 3. Réviser les Fixes

Chaque jour, vérifier:
```bash
git log --oneline --since="1 day ago" | grep "Auto-fix"
```

### 4. Garder les Backups

Ne jamais supprimer `storage/errors/` avant 30 jours.

---

## 📞 Support

### Problèmes Courants

**Q: Claude ne répond pas**
- Vérifier `ANTHROPIC_API_KEY`
- Vérifier quota API Anthropic
- Voir logs: `storage/errors/{error_id}.json`

**Q: Fix appliqué mais erreur persiste**
- Claude a peut-être mal analysé
- Restaurer backup manuellement
- Signaler l'erreur dans Slack

**Q: Trop de fixes inutiles**
- Augmenter seuil: `AUTO_FIX_MIN_CONFIDENCE=high`
- Ajouter fichiers à la blacklist

---

## 🎉 Avantages

✅ **Disponibilité 24/7**: Erreurs corrigées même la nuit  
✅ **Temps de résolution**: 20-30 secondes vs heures/jours  
✅ **Apprentissage**: Historique complet des fixes  
✅ **Transparence**: Chaque action tracée et notifiée  
✅ **Sécurité**: Backups + validation syntaxe  
✅ **Évolutif**: S'améliore avec le temps  

---

**Version**: 1.0 - Growth OS  
**Dernière mise à jour**: Janvier 2026  
**Propriétaire**: Self-Healing Engine
