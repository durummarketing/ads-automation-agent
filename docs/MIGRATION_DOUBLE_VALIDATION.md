# 🔄 MIGRATION - Double Validation

## 📋 Checklist de Migration

Temps estimé: **10 minutes**

---

## 🗂️ ÉTAPE 1: Airtable - Nouvelles Colonnes (5 min)

### Table: **ads**

Ouvrir Airtable → Base → Table **ads** → Ajouter colonnes:

#### Colonnes Validation Client

```
Nom                      | Type      | Description
-------------------------|-----------|---------------------------
validated_by_client      | Text      | Nom du client qui a approuvé
validated_at_client      | DateTime  | Quand client a approuvé
reminder_sent_at         | DateTime  | Dernier rappel envoyé au client
```

#### Colonnes Validation Finale (DURUM)

```
Nom                        | Type      | Description
---------------------------|-----------|---------------------------
final_validation_sent_at   | DateTime  | Quand envoyé à DURUM pour validation finale
final_validation_msg_ts    | Text      | Timestamp du message Slack validation finale
validated_by_final         | Text      | Qui a approuvé final (Alex, etc.)
validated_at_final         | DateTime  | Quand approuvé final
final_reminder_sent_at     | DateTime  | Dernier rappel validation finale
```

### Colonnes Optionnelles (Utiles)

```
Nom                    | Type      | Description
-----------------------|-----------|---------------------------
approval_duration_h    | Formula   | Temps entre envoi et validation client (heures)
final_duration_h       | Formula   | Temps entre validation client et finale (heures)
total_duration_h       | Formula   | Temps total création → publication (heures)
```

**Formules**:

```javascript
// approval_duration_h
IF(
  {validated_at_client},
  DATETIME_DIFF(
    {validated_at_client},
    {validation_sent_at},
    'hours'
  ),
  ""
)

// final_duration_h
IF(
  AND({validated_at_client}, {validated_at_final}),
  DATETIME_DIFF(
    {validated_at_final},
    {validated_at_client},
    'hours'
  ),
  ""
)

// total_duration_h
IF(
  {published_at},
  DATETIME_DIFF(
    {published_at},
    {validation_sent_at},
    'hours'
  ),
  ""
)
```

---

## 🔄 ÉTAPE 2: Mettre à Jour Status (2 min)

### Modifier Colonne **status**

1. Cliquer sur colonne **status** → Customize field type
2. Ajouter nouvelles options:

**Ajouter**:
- `Approuvé Client` (couleur: jaune/orange)
- `Approuvé Final` (couleur: vert foncé)

**Ordre recommandé**:
```
1. Brouillon
2. Prêt pour Validation
3. En Validation
4. Approuvé Client          ← NOUVEAU
5. Approuvé Final           ← NOUVEAU
6. Commentaire Client
7. Publié
8. Actif
9. Pause
10. Archivé
11. Erreur Publication
```

---

## ⚙️ ÉTAPE 3: Configuration .env (2 min)

Ajouter dans votre `.env`:

```env
# === DOUBLE VALIDATION ===

# Délais pour rappels (en heures)
REMINDER_CLIENT_HOURS=24           # Rappel client si pas de réponse après 24h
REMINDER_FINAL_HOURS=24            # Rappel équipe si validation finale pas faite après 24h
REMINDER_FREQUENCY_HOURS=24        # Fréquence max des rappels (éviter spam)

# Canal Slack pour validations finales
SLACK_CHANNEL_TEAM=team-durum      # Canal où VOUS recevez validations finales
```

---

## 🧪 ÉTAPE 4: Test Complet (10 min)

### Test 1: Validation Client

```
1. Dans Airtable:
   - Créer ad test (Ads T99 - V1)
   - Remplir tous champs
   - Status: "Brouillon" → "Prêt pour Validation"

2. Attendre 60s max

3. Dans Slack (canal client):
   - ✅ Message reçu
   - Cliquer "✅ Approuver"

4. Vérifier Airtable:
   - status = "Approuvé Client"
   - validated_by_client = rempli
   - validated_at_client = rempli

✅ Test 1 réussi!
```

### Test 2: Validation Finale (DURUM)

```
5. Attendre 60s max

6. Dans Slack (#team-durum):
   - ✅ Message "VALIDATION FINALE REQUISE" reçu
   - Voir preview complète ad
   - Cliquer "✅ Approuver & Publier"

7. Vérifier Airtable:
   - status = "Approuvé Final"
   - validated_by_final = rempli
   - validated_at_final = rempli

✅ Test 2 réussi!
```

### Test 3: Publication

```
8. Attendre 60s max

9. Vérifier:
   - status = "Publié"
   - meta_ad_id = rempli
   - meta_status = ACTIVE ou PAUSED
   - Message confirmation dans Slack

✅ Test 3 réussi!
```

### Test 4: Rappel Client (Optionnel - Passer en prod)

```
Pour tester rappels (FAST TRACK):

1. Modifier .env temporairement:
   REMINDER_CLIENT_HOURS=0.1    # 6 minutes au lieu de 24h

2. Créer ad test
3. Passer en "Prêt pour Validation"
4. NE PAS APPROUVER
5. Attendre 10 minutes

6. Vérifier:
   - Rappel reçu dans canal client
   - Message dans #team-durum (info)
   - reminder_sent_at rempli dans Airtable

7. Remettre .env:
   REMINDER_CLIENT_HOURS=24

✅ Test 4 réussi!
```

---

## 📊 ÉTAPE 5: Views Airtable Recommandées (5 min)

Créer ces vues pour faciliter le monitoring:

### Vue: "⏳ En Attente Client"

**Filtre**:
```
status = "En Validation"
```

**Grouper par**: `client_key`

**Trier par**: `validation_sent_at` (ascending)

→ Voir quelles ads attendent validation client

---

### Vue: "🎯 Validation Finale Requise"

**Filtre**:
```
status = "Approuvé Client"
```

**Trier par**: `validated_at_client` (ascending)

→ **VUE LA PLUS IMPORTANTE POUR VOUS!**

---

### Vue: "⏰ Délais >24h"

**Filtre**:
```
OR(
  AND(
    status = "En Validation",
    DATETIME_DIFF(NOW(), {validation_sent_at}, 'hours') > 24
  ),
  AND(
    status = "Approuvé Client",
    DATETIME_DIFF(NOW(), {validated_at_client}, 'hours') > 24
  )
)
```

**Couleur conditionnelle**:
- Rouge si délai >48h
- Orange si délai 24-48h

→ Voir rapidement les blocages

---

### Vue: "📊 Statistiques Validation"

**Champs à afficher**:
- ad_name
- client_key
- status
- approval_duration_h (formule)
- final_duration_h (formule)
- total_duration_h (formule)

**Filtre**:
```
status = "Publié" OR status = "Actif"
```

→ Analyser temps moyen de validation

---

## 🔔 ÉTAPE 6: Notifications Slack (2 min)

### Personnaliser Messages (Optionnel)

Éditer dans `publishing_workflow.py` si besoin:

**Ligne ~400** - Message validation client:
```python
"text": f"📢 Nouvelle Publicité à Valider - {request.client_name}"
```

**Ligne ~600** - Message validation finale:
```python
"text": f"🎯 VALIDATION FINALE REQUISE"
```

**Ligne ~800** - Rappel client:
```python
"text": f"⏰ *RAPPEL - Validation en Attente*"
```

**Ligne ~850** - Rappel équipe:
```python
"text": f"⏰🚨 *RAPPEL URGENT - Validation Finale en Attente*"
```

---

## 📈 ÉTAPE 7: Monitoring (Continu)

### Indicateurs à Surveiller

**Dans Airtable**:
```
Vue "⏳ En Attente Client" → Doit être vide ou <3 ads
Vue "🎯 Validation Finale Requise" → VOUS devez valider rapidement
Vue "⏰ Délais >24h" → Idéalement vide
```

**Dans Slack**:
```
#team-durum → Notifications validations finales
Rappels urgents → Si >24h
```

**Temps moyens cibles**:
```
Validation client: <4h
Validation finale (vous): <2h
Total création → publication: <8h
```

---

## ✅ Checklist Finale

Migration Airtable:
- [ ] Nouvelles colonnes ajoutées (7 colonnes)
- [ ] Status mis à jour (2 nouveaux)
- [ ] Views créées (4 vues)

Configuration:
- [ ] .env mis à jour
- [ ] Bot redémarré

Tests:
- [ ] Test validation client ✅
- [ ] Test validation finale ✅
- [ ] Test publication ✅
- [ ] Test rappels (optionnel) ✅

Production:
- [ ] Bot qui tourne
- [ ] Équipe formée au workflow
- [ ] Clients informés (optionnel)

---

## 🎯 Prêt!

Le système de **double validation** est maintenant actif! 🎉

### Workflow résumé:

```
Vous créez → Client valide → VOUS validez → Bot publie
            (24h rappel)    (24h rappel)
```

**Temps typique**: 6-8h de bout en bout

**Support**: alex@durum-marketing.com
