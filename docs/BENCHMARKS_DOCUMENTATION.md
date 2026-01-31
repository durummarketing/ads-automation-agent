# 📊 SYSTÈME DE BENCHMARKS DYNAMIQUES - Documentation Complète

## 🎯 Vue d'Ensemble

Le système de benchmarks calcule automatiquement des références de performance **contextuelles** pour chaque métrique, permettant une analyse **relative** plutôt qu'absolue.

**Principe clé**: Pas de seuils fixes. Tout est comparé à des benchmarks **calculés dynamiquement** à partir de vos données réelles.

---

## 🏗️ Architecture du Système

### Composants

```
┌─────────────────────────────────┐
│  PERFORMANCE_SNAPSHOTS          │
│  (Données quotidiennes)         │
│  • Tous les clients             │
│  • Toutes les métriques         │
│  • Enrichi avec contexte        │
└─────────────────────────────────┘
              ↓
┌─────────────────────────────────┐
│  BENCHMARK CALCULATOR           │
│  • Calcule percentiles          │
│  • Multi-niveaux                │
│  • Multi-périodes               │
└─────────────────────────────────┘
              ↓
┌─────────────────────────────────┐
│  BENCHMARKS (JSON)              │
│  • benchmarks_7d.json           │
│  • benchmarks_30d.json          │
│  • benchmarks_90d.json          │
└─────────────────────────────────┘
              ↓
┌─────────────────────────────────┐
│  INTELLIGENT ANALYTICS ENGINE   │
│  • Utilise benchmarks           │
│  • Comparaisons contextuelles   │
│  • Recommandations relatives    │
└─────────────────────────────────┘
```

---

## 📐 Niveaux de Benchmarks

### Niveau 1: Global (Tous les Comptes)

**Usage**: Référence de base, comparaison large

**Exemple**:
```json
{
  "metric": "roi_vendu",
  "level": "global",
  "segment": null,
  "percentiles": {
    "p10": 1.2,
    "p25": 1.8,
    "p50": 2.5,  // Médiane
    "p75": 3.8,
    "p90": 5.2
  },
  "sample_size": 45  // 45 comptes
}
```

**Interprétation**:
- ROI < 1.2x = Bottom 10% (très mauvais)
- ROI 1.2-1.8x = Bottom 25%
- ROI 1.8-2.5x = Sous médiane
- ROI 2.5-3.8x = Au-dessus médiane
- ROI 3.8-5.2x = Top 25%
- ROI > 5.2x = Top 10% (excellent)

---

### Niveau 2: Par Industrie

**Usage**: Comparaison avec pairs du même secteur

**Exemple**:
```json
{
  "metric": "cpa",
  "level": "industry",
  "segment": "coaching",
  "percentiles": {
    "p10": 80,
    "p25": 120,
    "p50": 180,
    "p75": 250,
    "p90": 350
  },
  "sample_size": 12  // 12 comptes coaching
}
```

**Pourquoi important?**

Différentes industries ont des économies différentes:
- **Coaching high-ticket**: CPA $150-300 normal
- **E-commerce**: CPA $20-50 normal
- **SaaS B2B**: CPA $80-150 normal

Sans segmentation par industrie, comparaison non pertinente.

---

### Niveau 3: Par Type d'Offre

**Usage**: Ajustement selon modèle économique

**Exemple**:
```json
{
  "metric": "close_rate",
  "level": "offer_type",
  "segment": "high-ticket",
  "percentiles": {
    "p10": 8,
    "p25": 15,
    "p50": 22,  // Médiane: 22%
    "p75": 30,
    "p90": 40
  },
  "sample_size": 18
}
```

**Pourquoi important?**

Type d'offre impact fortement les métriques:
- **High-ticket** ($3K+): Close rate 15-30% normal
- **Low-ticket** (<$100): Close rate 40-70% normal
- **Subscription**: Churn mensuel 3-8% normal

---

### Niveau 4: Par Géographie

**Usage**: Ajustement selon marché géographique

**Exemple**:
```json
{
  "metric": "cpc",
  "level": "geo",
  "segment": "CA-QC",
  "percentiles": {
    "p10": 0.35,
    "p25": 0.55,
    "p50": 0.85,
    "p75": 1.20,
    "p90": 1.80
  },
  "sample_size": 8
}
```

**Pourquoi important?**

Coûts publicitaires varient énormément:
- **US**: CPC $1.50-3.00 (compétitif)
- **CA-QC**: CPC $0.50-1.20 (moins compétitif)
- **FR**: CPC $0.80-1.80 (variable)

---

### Niveau 5: Segment Exact (Le Plus Précis)

**Usage**: Benchmark ultra-précis si assez de données

**Format segment**: `{industry}_{offer_type}_{geo}`

**Exemple**:
```json
{
  "metric": "roi_vendu",
  "level": "exact_segment",
  "segment": "coaching_high-ticket_CA",
  "percentiles": {
    "p10": 1.5,
    "p25": 2.1,
    "p50": 2.9,
    "p75": 4.2,
    "p90": 6.0
  },
  "sample_size": 7  // 7 comptes dans ce segment
}
```

**Avantage**:

Comparaison **hyper-pertinente** car:
- Même industrie (coaching)
- Même modèle économique (high-ticket)
- Même marché géographique (Canada)

**Inconvénient**:

Nécessite minimum 3 comptes dans le segment (idéalement 5+)

---

## 🔢 Métriques Benchmarkées

### Catégorie 1: ROI & Profitabilité

| Métrique | Description | Benchmark Typique (Médiane) |
|----------|-------------|------------------------------|
| **roi_vendu** | Revenus / Ad Spend | 2.5x |
| **roi_cash** | Cash collecté / Ad Spend | 2.0x |
| **roi_ltv** | LTV estimé / Ad Spend | 4.0x |

**Higher is better**: Oui

---

### Catégorie 2: Coûts par Acquisition

| Métrique | Description | Benchmark Typique |
|----------|-------------|-------------------|
| **cpa** | Coût par acquisition (vente) | $150 |
| **cpb** | Coût par booking | $80 |
| **cpapp** | Coût par application | $45 |
| **cpl** | Coût par lead | $25 |
| **cpc** | Coût par clic | $0.85 |
| **cpm** | Coût par 1000 impressions | $12 |

**Higher is better**: Non (plus bas = meilleur)

**Note**: Varie ÉNORMÉMENT selon industrie/offre

---

### Catégorie 3: Taux de Conversion

| Métrique | Description | Benchmark Typique |
|----------|-------------|-------------------|
| **close_rate** | Bookings → Sales | 22% |
| **booking_rate** | Applications → Bookings | 45% |
| **application_rate** | Leads → Applications | 35% |
| **lead_rate** | Clics → Leads | 8% |

**Higher is better**: Oui

---

### Catégorie 4: Créatives

| Métrique | Description | Benchmark Typique |
|----------|-------------|-------------------|
| **ctr** | Click-through rate | 2.5% |
| **hook_rate** | 3-sec video view rate | 50% |
| **completion_rate** | Video completion rate | 25% |
| **engagement_rate** | Likes+comments+shares / impressions | 1.8% |

**Higher is better**: Oui

---

### Catégorie 5: Qualité

| Métrique | Description | Benchmark Typique |
|----------|-------------|-------------------|
| **relevance_score** | Meta relevance score | 7/10 |
| **quality_ranking** | Meta quality ranking | "average" |
| **no_show_rate** | Bookings no-show % | 25% |

**Higher is better**: Dépend de la métrique

---

## 📊 Structure du Fichier Benchmark (JSON)

### Exemple Complet

```json
{
  "roi_vendu": {
    "global": {
      "metric": "roi_vendu",
      "level": "global",
      "segment": null,
      "period_days": 30,
      "percentiles": {
        "p10": 1.2,
        "p25": 1.8,
        "p50": 2.5,
        "p75": 3.8,
        "p90": 5.2
      },
      "stats": {
        "mean": 2.7,
        "median": 2.5,
        "std_dev": 1.4,
        "min": 0.5,
        "max": 8.2
      },
      "metadata": {
        "sample_size": 45,
        "calculated_at": "2025-01-31T10:30:00"
      },
      "interpretation": {
        "excellent": "Top 10%: ≥ 5.20",
        "good": "Top 25%: 3.80 - 5.20",
        "average": "Médiane: 1.80 - 3.80",
        "below_average": "Bottom 25%: 1.20 - 1.80",
        "poor": "Bottom 10%: < 1.20",
        "target": "Minimum viable: 2.0x",
        "excellent_threshold": "≥ 3.0x"
      }
    },
    "industry_coaching": {
      "metric": "roi_vendu",
      "level": "industry",
      "segment": "coaching",
      "period_days": 30,
      "percentiles": {
        "p10": 1.5,
        "p25": 2.1,
        "p50": 2.9,
        "p75": 4.2,
        "p90": 6.0
      },
      "stats": {
        "mean": 3.1,
        "median": 2.9,
        "std_dev": 1.6,
        "min": 0.8,
        "max": 8.5
      },
      "metadata": {
        "sample_size": 12,
        "calculated_at": "2025-01-31T10:30:00"
      },
      "interpretation": {
        "excellent": "Top 10%: ≥ 6.00",
        "good": "Top 25%: 4.20 - 6.00",
        "average": "Médiane: 2.10 - 4.20",
        "below_average": "Bottom 25%: 1.50 - 2.10",
        "poor": "Bottom 10%: < 1.50"
      }
    },
    "offer_high-ticket": {
      // ... similaire
    },
    "exact_coaching_high-ticket_CA": {
      // ... similaire
    }
  },
  "cpa": {
    // ... toutes les variations
  },
  // ... toutes les autres métriques
}
```

---

## 🔄 Mise à Jour des Benchmarks

### Fréquence Recommandée

| Période Benchmark | Fréquence Update | Raison |
|-------------------|------------------|---------|
| **7 jours** | Quotidien | Détection rapide tendances |
| **30 jours** | Quotidien | Benchmark principal |
| **90 jours** | Hebdomadaire | Vue long-terme, stabilité |

### Script de Mise à Jour

```bash
# Lancer manuellement
python3 update_benchmarks.py

# Ou via cron (quotidien à 3h du matin)
0 3 * * * cd /path/to/agent && python3 update_benchmarks.py
```

### Processus

1. **Charger snapshots** (90 derniers jours)
2. **Enrichir avec contexte client** (industrie, offer, geo)
3. **Calculer percentiles** pour chaque métrique
4. **Générer tous niveaux** (global, industrie, etc.)
5. **Sauvegarder JSON** (benchmarks_7d.json, etc.)
6. **Valider qualité** (sample_size minimum)

---

## 🎯 Utilisation dans l'Analyse

### Exemple: Analyser ROI d'un Client

```python
from benchmark_calculator import BenchmarkCalculator, MetricType

# 1. Charger benchmarks
calculator = BenchmarkCalculator(snapshots, clients)
benchmarks = calculator.load_benchmarks('storage/benchmarks/benchmarks_30d.json')

# 2. Métrique actuelle du client
client_roi = 2.1

# 3. Récupérer benchmark le plus pertinent
benchmark = calculator.get_benchmark_for_client(
    client_key='avego',
    metric=MetricType.ROI_VENDU,
    all_benchmarks=benchmarks
)

# 4. Comparer
comparison = calculator.compare_to_benchmark(
    value=client_roi,
    benchmark=benchmark,
    higher_is_better=True
)

print(comparison['interpretation'])
# Output: "📊 Légèrement sous la médiane (-14.0%). Focus sur optimisation."
```

### Exemple: Identifier Position Percentile

```python
percentile = calculator.calculate_percentile_rank(
    value=2.1,
    benchmark=benchmark
)

print(f"Position: {percentile}e percentile")
# Output: "Position: 42e percentile"
# Signifie: Meilleur que 42% des comptes, moins bon que 58%
```

### Exemple: Calculer Z-Score

```python
z_score = calculator.calculate_z_score(
    value=2.1,
    benchmark=benchmark
)

print(f"Z-Score: {z_score}σ")
# Output: "Z-Score: -0.29σ"
# Signifie: 0.29 écart-types SOUS la moyenne
```

---

## 🧠 Logique de Sélection du Benchmark

Quand l'agent analyse un client, il choisit le benchmark **le plus spécifique** avec **assez de données**:

### Ordre de Préférence

```
1. Exact Segment (coaching_high-ticket_CA)
   └─ SI sample_size ≥ 3
   
2. Type d'Offre (high-ticket)
   └─ SI exact segment indisponible
   
3. Industrie (coaching)
   └─ SI type d'offre indisponible
   
4. Global (tous)
   └─ Toujours disponible (fallback)
```

### Exemple Concret

**Client**: Avego
- Industrie: coaching
- Offre: high-ticket
- Geo: CA

**Benchmarks disponibles**:
- `exact_coaching_high-ticket_CA`: sample_size = 2 ❌ (trop peu)
- `offer_high-ticket`: sample_size = 18 ✅
- `industry_coaching`: sample_size = 12 ✅
- `global`: sample_size = 45 ✅

**Benchmark choisi**: `offer_high-ticket` (le plus spécifique avec assez de données)

---

## 📋 Validation de Qualité

### Critères de Qualité

Un benchmark est considéré **fiable** si:

| Critère | Valeur Minimum | Optimal |
|---------|----------------|---------|
| **Sample size** | 3 comptes | 10+ comptes |
| **Data points** | 90 snapshots | 300+ snapshots |
| **Std deviation** | < 50% de mean | < 30% de mean |
| **Outlier ratio** | < 10% | < 5% |

### Gestion des Outliers

Valeurs extrêmes sont **incluses** mais leur impact est **limité** via percentiles:

**Exemple**:
```
Valeurs ROI: [0.5, 1.8, 2.1, 2.3, 2.5, 2.8, 3.1, 15.2]
                                                   ↑ outlier
Médiane (p50): 2.4  ← Non affectée par outlier
Moyenne: 3.8        ← Affectée (biaisée vers haut)
```

**Solution**: Utiliser médiane (p50) comme référence principale, pas la moyenne.

---

## 🔧 Configuration & Paramètres

### Variables d'Environnement

```env
# Fichiers benchmarks
BENCHMARKS_DIR=storage/benchmarks
BENCHMARKS_UPDATE_HOUR=3  # Heure de mise à jour (3h du matin)

# Calcul
BENCHMARK_MIN_SAMPLE_SIZE=3
BENCHMARK_PERIODS=7,30,90  # Périodes en jours
```

### Paramètres Avancés

```python
# Dans update_benchmarks.py

# Minimum de comptes par segment
MIN_SAMPLE_SIZE = 3

# Périodes à calculer
PERIODS = [7, 30, 90]

# Exclure comptes inactifs
EXCLUDE_INACTIVE_DAYS = 30

# Outlier detection (optionnel)
OUTLIER_Z_THRESHOLD = 3.0  # Exclure si |z| > 3
```

---

## 📊 Dashboard Benchmarks (Optionnel)

### Visualisations Utiles

1. **Distribution Chart**: Voir où se situe le client
2. **Trend Over Time**: Évolution vs benchmark
3. **Segment Comparison**: Comparer segments entre eux
4. **Percentile Journey**: Tracking de la progression

### Exemple Output Dashboard

```
ROI VENDU - Avego vs Benchmarks

Client: 2.1x
                                    ↓ Vous
Global:     1.2 ──── 1.8 ──── 2.5 ──── 3.8 ──── 5.2
            p10     p25     p50     p75     p90

Industry:   1.5 ──── 2.1 ──── 2.9 ──── 4.2 ──── 6.0
            p10     p25     p50     p75     p90

Status: Légèrement sous médiane industrie
Percentile: 42 (meilleur que 42% des comptes coaching)
Objectif: Atteindre p50 (2.9x) = +38% amélioration
```

---

## ✅ Checklist Setup

- [ ] Performance snapshots configurés
- [ ] Client master enrichi (industry, offer_type, geo)
- [ ] Script update_benchmarks.py testé
- [ ] Benchmarks initiaux calculés
- [ ] Cron job configuré (quotidien)
- [ ] Validation sample_size (minimum 3 par segment)
- [ ] Intelligent Analytics Engine intégré

---

## 🚀 Prochaines Étapes

1. **Initialiser benchmarks** (première fois)
   ```bash
   python3 update_benchmarks.py
   ```

2. **Vérifier fichiers générés**
   ```bash
   ls -lh storage/benchmarks/
   # benchmarks_7d.json
   # benchmarks_30d.json
   # benchmarks_90d.json
   ```

3. **Intégrer dans analyse**
   ```python
   # Dans intelligent_analytics_engine.py
   benchmarks = calculator.load_benchmarks('storage/benchmarks/benchmarks_30d.json')
   ```

4. **Automatiser updates** (cron)

---

**Le système est maintenant prêt à fournir des analyses contextuelles intelligentes! 🎉**
