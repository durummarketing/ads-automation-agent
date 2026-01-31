# 🔄 WORKFLOW COMPLET - Double Validation + Notifications Auto

## 📊 Diagramme du Workflow

```
┌─────────────────────────────────────────────────────────────────────┐
│ PHASE 1: CRÉATION (DURUM)                                           │
└─────────────────────────────────────────────────────────────────────┘

Vous dans Airtable:
│
├─ Créer nouvelle ad
├─ Status: "Brouillon"
├─ Remplir: hook, body, CTA, asset, etc.
├─ Travailler sur le copy...
│
└─ Quand prêt: Status → "Prêt pour Validation"

        ↓ (Bot détecte en 60s max)

┌─────────────────────────────────────────────────────────────────────┐
│ PHASE 2: VALIDATION CLIENT                                          │
└─────────────────────────────────────────────────────────────────────┘

Bot:
│
├─ Détecte status = "Prêt pour Validation"
├─ Valide structure & convention nommage
├─ Status → "En Validation"
│
└─ Envoie message Slack → Canal client (#client-XXX-validation)

        ↓

Client dans Slack:
│
├─ Reçoit notification avec preview ad complète
│
└─ 3 OPTIONS:
    │
    ├─ 1️⃣ ✅ APPROUVER
    │     ↓
    │     Status → "Approuvé Client"
    │     Message mis à jour: "✅ Approuvé par [Client]"
    │     ↓
    │     ⚠️ PAS ENCORE PUBLIÉ! → PHASE 3 (Validation DURUM)
    │
    ├─ 2️⃣ 💬 COMMENTAIRE
    │     ↓
    │     Modal s'ouvre
    │     Client écrit commentaire
    │     ↓
    │     Status → "Commentaire Client"
    │     Tâche créée dans Airtable
    │     Notif #team-durum
    │     ↓
    │     DURUM corrige → Status "Prêt pour Validation" → Re-cycle
    │
    └─ 3️⃣ ❌ REJETER
          ↓
          Status → "Archivé"
          Fin

        ↓ (Si client a approuvé)

┌─────────────────────────────────────────────────────────────────────┐
│ PHASE 3: VALIDATION FINALE (DURUM) - NOUVEAU!                       │
└─────────────────────────────────────────────────────────────────────┘

Bot:
│
├─ Détecte status = "Approuvé Client"
├─ Envoie message Slack → #team-durum (VOUS)
│
└─ Message contient:
    ├─ Info client qui a approuvé
    ├─ Preview complète ad
    ├─ Budget & mode publication
    └─ 2 BOUTONS:
        ├─ ✅ Approuver & Publier
        └─ ❌ Rejeter

        ↓

Vous dans Slack:
│
└─ 2 OPTIONS:
    │
    ├─ 1️⃣ ✅ APPROUVER & PUBLIER
    │     ↓
    │     Status → "Approuvé Final"
    │     ↓
    │     → PHASE 4 (Publication)
    │
    └─ 2️⃣ ❌ REJETER
          ↓
          Status → "Archivé"
          Client notifié (optionnel)
          Fin

        ↓ (Si vous avez approuvé)

┌─────────────────────────────────────────────────────────────────────┐
│ PHASE 4: PUBLICATION META                                           │
└─────────────────────────────────────────────────────────────────────┘

Bot:
│
├─ Détecte status = "Approuvé Final"
├─ Publie sur Meta Ads API
│   ├─ Mode "Auto" → Status ACTIVE (ON)
│   ├─ Mode "Manuel" → Status PAUSED (OFF)
│   └─ Mode "Test" → Status DRAFT
│
├─ Status → "Publié"
├─ Enregistre meta_ad_id
│
└─ Notifications:
    ├─ Confirmation canal client
    └─ Confirmation #team-durum

        ↓

┌─────────────────────────────────────────────────────────────────────┐
│ PHASE 5: MONITORING                                                 │
└─────────────────────────────────────────────────────────────────────┘

Bot surveille:
│
├─ Status "Actif" / "Pause" selon Meta
├─ Performance (via Growth OS)
└─ Alertes si problèmes
```

---

## ⏰ NOTIFICATIONS AUTOMATIQUES

### 1. Notification Client (24h sans validation)

**Déclencheur**: Ad en status "En Validation" depuis >24h

**Action**:
```
⏰ Bot vérifie toutes les heures

Si timeout détecté:
  1. Envoie RAPPEL dans canal client
  2. Notifie #team-durum (info)
  3. Update timestamp rappel
  
Fréquence rappels: 1x / 24h max
```

**Message envoyé au client**:
```
⏰ RAPPEL - Validation en Attente

La publicité suivante attend votre validation depuis plus de 24h:

Ad: Ads T4 - V1
Campaign: [BOOTCAMP] TOF _CONV.LEADS

Merci de valider dès que possible! 🙏
```

---

### 2. Notification DURUM (24h validation finale en attente)

**Déclencheur**: Ad en status "Approuvé Client" depuis >24h (en attente validation FINALE)

**Action**:
```
⏰🚨 Bot vérifie toutes les heures

Si délai détecté:
  1. Envoie RAPPEL URGENT dans #team-durum
  2. Update timestamp
  
Fréquence rappels: 1x / 24h max
```

**Message envoyé à l'équipe**:
```
⏰🚨 RAPPEL URGENT - Validation Finale en Attente

Cette ad attend VOTRE validation depuis plus de 24h:

Client: Avego
Ad: Ads T4 - V1
Approuvée par client: Marc Tremblay (2025-01-30)

⚠️ Le client attend la publication!
```

---

## 📊 Nouveaux Statuts Airtable

### Table: **ads**

**Nouvelles colonnes**:

```
# Validation CLIENT
validated_by_client       Text       Nom du client qui a approuvé
validated_at_client       DateTime   Quand client a approuvé
reminder_sent_at          DateTime   Dernier rappel envoyé au client

# Validation FINALE (DURUM)
final_validation_sent_at  DateTime   Quand envoyé à DURUM
final_validation_msg_ts   Text       Timestamp message Slack
validated_by_final        Text       Qui a approuvé final (vous)
validated_at_final        DateTime   Quand approuvé final
final_reminder_sent_at    DateTime   Dernier rappel validation finale
```

### Nouveaux Statuts

```
"Brouillon"               → Vous travaillez
"Prêt pour Validation"    → Bot va envoyer au client
"En Validation"           → Client n'a pas encore répondu
"Approuvé Client"         → ✅ Client OK, attente DURUM
"Approuvé Final"          → ✅✅ Client + DURUM OK, prêt publication
"Commentaire Client"      → Client a demandé modifications
"Publié"                  → Publié sur Meta
"Actif" / "Pause"         → Status Meta réel
"Archivé"                 → Rejeté ou terminé
```

---

## ⚙️ Configuration .env

**Nouvelles variables**:

```env
# Notifications
REMINDER_CLIENT_HOURS=24          # Rappel client après X heures
REMINDER_FINAL_HOURS=24           # Rappel validation finale après X heures
REMINDER_FREQUENCY_HOURS=24       # Fréquence max rappels

# Canaux
SLACK_CHANNEL_TEAM=team-durum     # Canal pour validations finales
```

---

## 🔄 Cycles du Bot

```
CYCLE 1 (toutes les 60s):
  ├─ Détecter "Prêt pour Validation" → Envoyer client
  ├─ Détecter "Approuvé Client" → Envoyer DURUM
  ├─ Détecter "Approuvé Final" → Publier Meta
  └─ Traiter commentaires

CYCLE 2 (toutes les heures):
  ├─ Check timeout validation client (24h)
  └─ Check délai validation finale (24h)
```

---

## 📱 Exemples de Messages Slack

### Message Validation Client

```
📢 Nouvelle Publicité à Valider - Avego

Campaign: [BOOTCAMP] TOF _CONV.LEADS
AdSet: STACK_H:25/65+ _QC _FEED+

🎨 CRÉATIVE
HOOK: "97% des traders..."
BODY: "Découvrez la stratégie..."
CTA: Télécharger Maintenant

🟢 Mode: Auto (Activée immédiatement)
💰 Budget: $150/jour

[✅ Approuver] [💬 Commentaire] [❌ Rejeter]
```

Après approbation client:
```
✅ APPROUVÉ PAR CLIENT (Marc Tremblay) le 2025-01-30 14:23
⏳ En attente validation finale équipe...
```

---

### Message Validation Finale (DURUM)

```
🎯 VALIDATION FINALE REQUISE

Client: Avego
Approuvé par: Marc Tremblay le 2025-01-30 14:23

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Campaign: [BOOTCAMP] TOF _CONV.LEADS
AdSet: STACK_H:25/65+ _QC _FEED+

🎨 CRÉATIVE
HOOK: "97% des traders..."
BODY: "Découvrez la stratégie..."
CTA: Télécharger Maintenant

Mode: Auto | Budget: $150/jour
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[✅ Approuver & Publier] [❌ Rejeter]
```

Après votre approbation:
```
✅ APPROUVÉ FINAL par Alex - Publication en cours...
```

---

## ⏱️ Timeline Typique

```
Jour 1 - 09h00: Vous créez ad (Brouillon)
Jour 1 - 10h00: Vous mettez "Prêt pour Validation"
Jour 1 - 10h01: Bot envoie au client (En Validation)

Jour 1 - 14h00: Client approuve (Approuvé Client)
Jour 1 - 14h01: Bot envoie validation finale à vous

Jour 1 - 15h00: Vous approuvez (Approuvé Final)
Jour 1 - 15h01: Bot publie sur Meta (Publié)

✅ Timeline normale: ~6h du début à publication
```

### Si Client Tarde

```
Jour 1 - 10h01: Envoi validation client
...
Jour 2 - 10h00: ⏰ RAPPEL automatique client (24h)
...
Jour 3 - 10h00: ⏰ RAPPEL automatique client (48h)
```

### Si Vous Tardez

```
Jour 1 - 14h01: Envoi validation finale
...
Jour 2 - 14h00: ⏰🚨 RAPPEL URGENT équipe (24h)
...
Jour 3 - 14h00: ⏰🚨 RAPPEL URGENT équipe (48h)
```

---

## ✅ Avantages de la Double Validation

1. **Client Rassuré** - Voit exactement ce qui sera publié
2. **DURUM Contrôle Final** - Vous validez avant publication
3. **Pas de Publication Surprise** - Rien ne se publie sans vos 2 OK
4. **Rappels Auto** - Plus de "j'ai oublié de valider"
5. **Historique Complet** - Qui a validé quand, tout tracé

---

## 🔧 Code Modifié

**Fichier**: `publishing_workflow.py`

**Changements principaux**:
1. ✅ Nouveau status "Approuvé Client"
2. ✅ Nouveau status "Approuvé Final"
3. ✅ Méthode `_send_final_validation()`
4. ✅ Méthode `handle_final_approval()`
5. ✅ Méthode `_check_client_validation_timeouts()`
6. ✅ Méthode `_check_final_validation_delays()`
7. ✅ Cycle mis à jour avec 6 étapes

---

**Le système est maintenant COMPLET avec double validation et notifications! 🎉**
