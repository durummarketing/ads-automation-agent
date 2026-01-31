"""
Benchmark Calculator - Calcule tous les benchmarks dynamiques
Multi-niveaux: Global, Industrie, Type d'offre, Segment exact
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum
import json


class BenchmarkLevel(Enum):
    """Niveaux de benchmarks"""
    GLOBAL = "global"  # Tous les comptes
    INDUSTRY = "industry"  # Par industrie
    OFFER_TYPE = "offer_type"  # Par type d'offre
    GEO = "geo"  # Par géographie
    EXACT_SEGMENT = "exact_segment"  # Combinaison précise


class MetricType(Enum):
    """Types de métriques à benchmarker"""
    # ROI & Profitabilité
    ROI_VENDU = "roi_vendu"
    ROI_CASH = "roi_cash"
    ROI_LTV = "roi_ltv"
    
    # Coûts
    CPA = "cpa"
    CPL = "cpl"
    CPAPP = "cpapp"
    CPB = "cpb"
    CPC = "cpc"
    CPM = "cpm"
    
    # Taux de conversion
    CLOSE_RATE = "close_rate"
    BOOKING_RATE = "booking_rate"
    APPLICATION_RATE = "application_rate"
    LEAD_RATE = "lead_rate"
    
    # Métriques créatives
    CTR = "ctr"
    HOOK_RATE = "hook_rate"
    COMPLETION_RATE = "completion_rate"
    ENGAGEMENT_RATE = "engagement_rate"
    
    # Métriques qualité Meta
    RELEVANCE_SCORE = "relevance_score"
    QUALITY_RANKING = "quality_ranking"
    
    # Métriques funnel
    NO_SHOW_RATE = "no_show_rate"
    FUNNEL_VELOCITY = "funnel_velocity"
    
    # Métriques globales
    HEALTH_SCORE = "health_score"
    FREQUENCY = "frequency"


@dataclass
class BenchmarkResult:
    """Résultat d'un calcul de benchmark"""
    metric: MetricType
    level: BenchmarkLevel
    segment: Optional[str]  # Ex: "coaching", "high-ticket"
    period_days: int
    
    # Statistiques
    percentile_10: float
    percentile_25: float
    percentile_50: float  # Médiane
    percentile_75: float
    percentile_90: float
    mean: float
    median: float
    std_dev: float
    
    # Métadonnées
    sample_size: int
    min_value: float
    max_value: float
    calculated_at: datetime
    
    # Pour interprétation
    interpretation: Dict[str, str]


class BenchmarkCalculator:
    """
    Calcule tous les benchmarks nécessaires pour analyse intelligente
    """
    
    def __init__(
        self,
        performance_snapshots: pd.DataFrame,
        client_master: pd.DataFrame
    ):
        """
        Args:
            performance_snapshots: DataFrame avec snapshots quotidiens
            client_master: DataFrame avec infos clients
        """
        self.snapshots = performance_snapshots
        self.clients = client_master
        
        # Enrichir snapshots avec infos client
        self.enriched_data = self._enrich_snapshots()
    
    def _enrich_snapshots(self) -> pd.DataFrame:
        """
        Enrichit les snapshots avec infos client (industrie, offer_type, etc.)
        """
        # Merger snapshots avec client info
        enriched = self.snapshots.merge(
            self.clients[['client_key', 'industry', 'offer_type', 'target_geo', 'maturity_stage']],
            on='client_key',
            how='left'
        )
        
        # Créer segment exact
        enriched['exact_segment'] = (
            enriched['industry'].astype(str) + '_' +
            enriched['offer_type'].astype(str) + '_' +
            enriched['target_geo'].astype(str)
        )
        
        return enriched
    
    def calculate_all_benchmarks(
        self,
        period_days: int = 30,
        min_sample_size: int = 3
    ) -> Dict[str, Dict[str, BenchmarkResult]]:
        """
        Calcule TOUS les benchmarks pour toutes les métriques et tous les niveaux
        
        Args:
            period_days: Période à considérer
            min_sample_size: Minimum de comptes pour benchmark valide
            
        Returns:
            Structure:
            {
                'roi_vendu': {
                    'global': BenchmarkResult,
                    'industry_coaching': BenchmarkResult,
                    'offer_high-ticket': BenchmarkResult,
                    'exact_coaching_high-ticket_CA': BenchmarkResult
                },
                'cpa': {...},
                ...
            }
        """
        all_benchmarks = {}
        
        # Pour chaque métrique
        for metric in MetricType:
            all_benchmarks[metric.value] = {}
            
            # Niveau 1: Global
            global_bench = self.calculate_benchmark(
                metric=metric,
                level=BenchmarkLevel.GLOBAL,
                period_days=period_days,
                min_sample_size=min_sample_size
            )
            if global_bench:
                all_benchmarks[metric.value]['global'] = global_bench
            
            # Niveau 2: Par industrie
            for industry in self.clients['industry'].dropna().unique():
                industry_bench = self.calculate_benchmark(
                    metric=metric,
                    level=BenchmarkLevel.INDUSTRY,
                    segment=industry,
                    period_days=period_days,
                    min_sample_size=min_sample_size
                )
                if industry_bench:
                    all_benchmarks[metric.value][f'industry_{industry}'] = industry_bench
            
            # Niveau 3: Par type d'offre
            for offer_type in self.clients['offer_type'].dropna().unique():
                offer_bench = self.calculate_benchmark(
                    metric=metric,
                    level=BenchmarkLevel.OFFER_TYPE,
                    segment=offer_type,
                    period_days=period_days,
                    min_sample_size=min_sample_size
                )
                if offer_bench:
                    all_benchmarks[metric.value][f'offer_{offer_type}'] = offer_bench
            
            # Niveau 4: Segments exacts (si assez de données)
            exact_segments = self.enriched_data['exact_segment'].value_counts()
            for segment, count in exact_segments.items():
                if count >= min_sample_size * 30:  # 3 comptes × 30 jours = 90 snapshots minimum
                    exact_bench = self.calculate_benchmark(
                        metric=metric,
                        level=BenchmarkLevel.EXACT_SEGMENT,
                        segment=segment,
                        period_days=period_days,
                        min_sample_size=min_sample_size
                    )
                    if exact_bench:
                        all_benchmarks[metric.value][f'exact_{segment}'] = exact_bench
        
        return all_benchmarks
    
    def calculate_benchmark(
        self,
        metric: MetricType,
        level: BenchmarkLevel,
        segment: Optional[str] = None,
        period_days: int = 30,
        min_sample_size: int = 3
    ) -> Optional[BenchmarkResult]:
        """
        Calcule un benchmark spécifique
        
        Args:
            metric: Métrique à benchmarker
            level: Niveau de benchmark
            segment: Segment si applicable
            period_days: Période
            min_sample_size: Minimum de comptes
            
        Returns:
            BenchmarkResult ou None si pas assez de données
        """
        # Filtrer données par période
        cutoff_date = datetime.now() - timedelta(days=period_days)
        df = self.enriched_data[self.enriched_data['date'] >= cutoff_date].copy()
        
        # Filtrer par niveau/segment
        if level == BenchmarkLevel.INDUSTRY and segment:
            df = df[df['industry'] == segment]
        elif level == BenchmarkLevel.OFFER_TYPE and segment:
            df = df[df['offer_type'] == segment]
        elif level == BenchmarkLevel.GEO and segment:
            df = df[df['target_geo'] == segment]
        elif level == BenchmarkLevel.EXACT_SEGMENT and segment:
            df = df[df['exact_segment'] == segment]
        # GLOBAL = pas de filtre
        
        # Vérifier nombre de comptes uniques
        unique_clients = df['client_key'].nunique()
        if unique_clients < min_sample_size:
            return None  # Pas assez de données
        
        # Extraire valeurs de la métrique
        metric_col = metric.value
        if metric_col not in df.columns:
            return None  # Métrique pas disponible
        
        values = df[metric_col].dropna()
        
        if len(values) == 0:
            return None
        
        # Calculer statistiques
        percentiles = np.percentile(values, [10, 25, 50, 75, 90])
        
        result = BenchmarkResult(
            metric=metric,
            level=level,
            segment=segment,
            period_days=period_days,
            percentile_10=float(percentiles[0]),
            percentile_25=float(percentiles[1]),
            percentile_50=float(percentiles[2]),
            percentile_75=float(percentiles[3]),
            percentile_90=float(percentiles[4]),
            mean=float(values.mean()),
            median=float(values.median()),
            std_dev=float(values.std()),
            sample_size=unique_clients,
            min_value=float(values.min()),
            max_value=float(values.max()),
            calculated_at=datetime.now(),
            interpretation=self._generate_interpretation(metric, percentiles)
        )
        
        return result
    
    def _generate_interpretation(
        self,
        metric: MetricType,
        percentiles: np.ndarray
    ) -> Dict[str, str]:
        """
        Génère interprétation des benchmarks
        """
        p10, p25, p50, p75, p90 = percentiles
        
        interpretation = {
            'excellent': f'Top 10%: ≥ {p90:.2f}',
            'good': f'Top 25%: {p75:.2f} - {p90:.2f}',
            'average': f'Médiane: {p25:.2f} - {p75:.2f}',
            'below_average': f'Bottom 25%: {p10:.2f} - {p25:.2f}',
            'poor': f'Bottom 10%: < {p10:.2f}'
        }
        
        # Ajouter contexte selon métrique
        if metric in [MetricType.ROI_VENDU, MetricType.ROI_CASH]:
            interpretation['target'] = f'Minimum viable: 2.0x'
            interpretation['excellent_threshold'] = f'≥ 3.0x'
        
        elif metric in [MetricType.CPA, MetricType.CPL]:
            interpretation['note'] = 'Plus bas = meilleur'
        
        return interpretation
    
    def get_benchmark_for_client(
        self,
        client_key: str,
        metric: MetricType,
        all_benchmarks: Dict[str, Dict[str, BenchmarkResult]]
    ) -> BenchmarkResult:
        """
        Récupère le benchmark le plus pertinent pour un client
        
        Ordre de préférence:
        1. Segment exact (si assez de données)
        2. Type d'offre
        3. Industrie
        4. Global
        """
        # Récupérer infos client
        client_info = self.clients[self.clients['client_key'] == client_key].iloc[0]
        
        # Construire priorités
        exact_segment = f"{client_info['industry']}_{client_info['offer_type']}_{client_info['target_geo']}"
        
        priorities = [
            f'exact_{exact_segment}',
            f'offer_{client_info["offer_type"]}',
            f'industry_{client_info["industry"]}',
            'global'
        ]
        
        # Chercher premier benchmark disponible
        metric_benchmarks = all_benchmarks.get(metric.value, {})
        
        for priority in priorities:
            if priority in metric_benchmarks:
                return metric_benchmarks[priority]
        
        # Fallback: global
        return metric_benchmarks.get('global')
    
    def calculate_percentile_rank(
        self,
        value: float,
        benchmark: BenchmarkResult
    ) -> int:
        """
        Calcule le rang percentile d'une valeur (0-100)
        100 = top performer
        """
        if value >= benchmark.percentile_90:
            return 95
        elif value >= benchmark.percentile_75:
            # Interpoler entre 75 et 90
            range_size = benchmark.percentile_90 - benchmark.percentile_75
            if range_size > 0:
                position = (value - benchmark.percentile_75) / range_size
                return int(75 + position * 20)
            return 82
        elif value >= benchmark.percentile_50:
            # Interpoler entre 50 et 75
            range_size = benchmark.percentile_75 - benchmark.percentile_50
            if range_size > 0:
                position = (value - benchmark.percentile_50) / range_size
                return int(50 + position * 25)
            return 62
        elif value >= benchmark.percentile_25:
            # Interpoler entre 25 et 50
            range_size = benchmark.percentile_50 - benchmark.percentile_25
            if range_size > 0:
                position = (value - benchmark.percentile_25) / range_size
                return int(25 + position * 25)
            return 37
        elif value >= benchmark.percentile_10:
            # Interpoler entre 10 et 25
            range_size = benchmark.percentile_25 - benchmark.percentile_10
            if range_size > 0:
                position = (value - benchmark.percentile_10) / range_size
                return int(10 + position * 15)
            return 17
        else:
            # Sous p10
            return 5
    
    def calculate_z_score(
        self,
        value: float,
        benchmark: BenchmarkResult
    ) -> float:
        """
        Calcule le z-score (écart en σ vs moyenne)
        """
        if benchmark.std_dev == 0:
            return 0.0
        
        z = (value - benchmark.mean) / benchmark.std_dev
        return round(z, 2)
    
    def compare_to_benchmark(
        self,
        value: float,
        benchmark: BenchmarkResult,
        higher_is_better: bool = True
    ) -> Dict[str, Any]:
        """
        Compare une valeur à un benchmark et retourne analyse complète
        
        Args:
            value: Valeur à comparer
            benchmark: Benchmark de référence
            higher_is_better: True si plus haut = meilleur (ex: ROI)
                             False si plus bas = meilleur (ex: CPA)
        """
        percentile = self.calculate_percentile_rank(value, benchmark)
        z_score = self.calculate_z_score(value, benchmark)
        
        # Ratio vs médiane
        vs_median = (value / benchmark.median) if benchmark.median > 0 else 1.0
        
        # Déterminer performance tier
        if higher_is_better:
            if value >= benchmark.percentile_90:
                tier = "excellent"
                status = "top_10_percent"
            elif value >= benchmark.percentile_75:
                tier = "good"
                status = "top_25_percent"
            elif value >= benchmark.percentile_50:
                tier = "average"
                status = "above_median"
            elif value >= benchmark.percentile_25:
                tier = "below_average"
                status = "below_median"
            else:
                tier = "poor"
                status = "bottom_25_percent"
        else:
            # Logique inversée pour métriques où bas = meilleur
            if value <= benchmark.percentile_10:
                tier = "excellent"
                status = "top_10_percent"
            elif value <= benchmark.percentile_25:
                tier = "good"
                status = "top_25_percent"
            elif value <= benchmark.percentile_50:
                tier = "average"
                status = "above_median"
            elif value <= benchmark.percentile_75:
                tier = "below_average"
                status = "below_median"
            else:
                tier = "poor"
                status = "bottom_25_percent"
        
        return {
            'value': value,
            'benchmark': {
                'median': benchmark.median,
                'mean': benchmark.mean,
                'p10': benchmark.percentile_10,
                'p25': benchmark.percentile_25,
                'p50': benchmark.percentile_50,
                'p75': benchmark.percentile_75,
                'p90': benchmark.percentile_90
            },
            'comparison': {
                'percentile_rank': percentile,
                'z_score': z_score,
                'vs_median': vs_median,
                'vs_median_pct': (vs_median - 1) * 100,  # % diff vs médiane
                'tier': tier,
                'status': status
            },
            'interpretation': self._interpret_comparison(
                tier,
                percentile,
                vs_median,
                benchmark.metric,
                higher_is_better
            )
        }
    
    def _interpret_comparison(
        self,
        tier: str,
        percentile: int,
        vs_median: float,
        metric: MetricType,
        higher_is_better: bool
    ) -> str:
        """
        Génère interprétation textuelle de la comparaison
        """
        if tier == "excellent":
            return f"🌟 Performance exceptionnelle (top {100-percentile}%). Continuer sur cette lancée!"
        
        elif tier == "good":
            return f"✅ Bonne performance (top {100-percentile}%). Opportunité d'optimiser vers top 10%."
        
        elif tier == "average":
            diff_pct = abs((vs_median - 1) * 100)
            if higher_is_better:
                if vs_median > 1:
                    return f"📊 Légèrement au-dessus de la médiane (+{diff_pct:.1f}%). Potentiel d'amélioration."
                else:
                    return f"📊 Légèrement sous la médiane (-{diff_pct:.1f}%). Focus sur optimisation."
            else:
                if vs_median < 1:
                    return f"📊 Légèrement meilleur que médiane (-{diff_pct:.1f}%). Continuer."
                else:
                    return f"📊 Légèrement moins bon que médiane (+{diff_pct:.1f}%). À améliorer."
        
        elif tier == "below_average":
            return f"⚠️ Performance sous la moyenne (bottom {percentile}%). Action corrective recommandée."
        
        else:  # poor
            return f"🚨 Performance critique (bottom {percentile}%). Intervention urgente requise."
    
    def save_benchmarks(
        self,
        benchmarks: Dict[str, Dict[str, BenchmarkResult]],
        filepath: str
    ):
        """
        Sauvegarde les benchmarks dans un fichier JSON
        """
        # Convertir en format sérialisable
        serializable = {}
        
        for metric, levels in benchmarks.items():
            serializable[metric] = {}
            
            for level_name, benchmark in levels.items():
                serializable[metric][level_name] = {
                    'metric': benchmark.metric.value,
                    'level': benchmark.level.value,
                    'segment': benchmark.segment,
                    'period_days': benchmark.period_days,
                    'percentiles': {
                        'p10': benchmark.percentile_10,
                        'p25': benchmark.percentile_25,
                        'p50': benchmark.percentile_50,
                        'p75': benchmark.percentile_75,
                        'p90': benchmark.percentile_90
                    },
                    'stats': {
                        'mean': benchmark.mean,
                        'median': benchmark.median,
                        'std_dev': benchmark.std_dev,
                        'min': benchmark.min_value,
                        'max': benchmark.max_value
                    },
                    'metadata': {
                        'sample_size': benchmark.sample_size,
                        'calculated_at': benchmark.calculated_at.isoformat()
                    },
                    'interpretation': benchmark.interpretation
                }
        
        with open(filepath, 'w') as f:
            json.dump(serializable, f, indent=2)
    
    def load_benchmarks(self, filepath: str) -> Dict[str, Dict[str, BenchmarkResult]]:
        """
        Charge les benchmarks depuis un fichier JSON
        """
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        benchmarks = {}
        
        for metric, levels in data.items():
            benchmarks[metric] = {}
            
            for level_name, bench_data in levels.items():
                benchmarks[metric][level_name] = BenchmarkResult(
                    metric=MetricType(bench_data['metric']),
                    level=BenchmarkLevel(bench_data['level']),
                    segment=bench_data['segment'],
                    period_days=bench_data['period_days'],
                    percentile_10=bench_data['percentiles']['p10'],
                    percentile_25=bench_data['percentiles']['p25'],
                    percentile_50=bench_data['percentiles']['p50'],
                    percentile_75=bench_data['percentiles']['p75'],
                    percentile_90=bench_data['percentiles']['p90'],
                    mean=bench_data['stats']['mean'],
                    median=bench_data['stats']['median'],
                    std_dev=bench_data['stats']['std_dev'],
                    sample_size=bench_data['metadata']['sample_size'],
                    min_value=bench_data['stats']['min'],
                    max_value=bench_data['stats']['max'],
                    calculated_at=datetime.fromisoformat(bench_data['metadata']['calculated_at']),
                    interpretation=bench_data['interpretation']
                )
        
        return benchmarks


class BenchmarkUpdater:
    """
    Met à jour les benchmarks automatiquement selon un schedule
    """
    
    def __init__(self, calculator: BenchmarkCalculator):
        self.calculator = calculator
    
    def should_update(self, last_update: datetime, update_frequency_hours: int = 24) -> bool:
        """
        Détermine si les benchmarks doivent être mis à jour
        """
        now = datetime.now()
        hours_since_update = (now - last_update).total_seconds() / 3600
        
        return hours_since_update >= update_frequency_hours
    
    def update_all(
        self,
        output_filepath: str,
        period_days: int = 30
    ):
        """
        Met à jour tous les benchmarks et les sauvegarde
        """
        print(f"🔄 Calcul des benchmarks (période: {period_days} jours)...")
        
        benchmarks = self.calculator.calculate_all_benchmarks(
            period_days=period_days,
            min_sample_size=3
        )
        
        print(f"✅ {len(benchmarks)} métriques benchmarkées")
        
        # Compter total de benchmarks
        total_benchmarks = sum(len(levels) for levels in benchmarks.values())
        print(f"📊 {total_benchmarks} benchmarks calculés au total")
        
        # Sauvegarder
        self.calculator.save_benchmarks(benchmarks, output_filepath)
        print(f"💾 Benchmarks sauvegardés: {output_filepath}")
        
        return benchmarks


# Helper functions pour analyse

def print_benchmark_summary(benchmark: BenchmarkResult):
    """
    Affiche un résumé d'un benchmark
    """
    print(f"\n📊 Benchmark: {benchmark.metric.value}")
    print(f"   Niveau: {benchmark.level.value}")
    if benchmark.segment:
        print(f"   Segment: {benchmark.segment}")
    print(f"   Période: {benchmark.period_days} jours")
    print(f"   Échantillon: {benchmark.sample_size} comptes")
    print(f"\n   Percentiles:")
    print(f"   • Top 10%: ≥ {benchmark.percentile_90:.2f}")
    print(f"   • Top 25%: {benchmark.percentile_75:.2f}")
    print(f"   • Médiane: {benchmark.percentile_50:.2f}")
    print(f"   • Bottom 25%: {benchmark.percentile_25:.2f}")
    print(f"   • Bottom 10%: ≤ {benchmark.percentile_10:.2f}")
    print(f"\n   Stats:")
    print(f"   • Moyenne: {benchmark.mean:.2f}")
    print(f"   • Écart-type: {benchmark.std_dev:.2f}")
    print(f"   • Min: {benchmark.min_value:.2f}")
    print(f"   • Max: {benchmark.max_value:.2f}")


def compare_client_to_benchmarks(
    client_metrics: Dict[str, float],
    all_benchmarks: Dict[str, Dict[str, BenchmarkResult]],
    calculator: BenchmarkCalculator,
    client_key: str
):
    """
    Compare un client à tous les benchmarks pertinents
    """
    print(f"\n🔍 Analyse Benchmark - Client: {client_key}")
    print("=" * 60)
    
    for metric_name, value in client_metrics.items():
        try:
            metric = MetricType(metric_name)
        except ValueError:
            continue  # Métrique non reconnue
        
        # Récupérer benchmark le plus pertinent
        benchmark = calculator.get_benchmark_for_client(
            client_key,
            metric,
            all_benchmarks
        )
        
        if not benchmark:
            continue
        
        # Déterminer si higher is better
        higher_is_better = metric not in [
            MetricType.CPA, MetricType.CPL, MetricType.CPAPP,
            MetricType.CPB, MetricType.CPC, MetricType.CPM,
            MetricType.NO_SHOW_RATE
        ]
        
        # Comparer
        comparison = calculator.compare_to_benchmark(
            value,
            benchmark,
            higher_is_better
        )
        
        # Afficher
        print(f"\n📈 {metric.value.upper()}")
        print(f"   Valeur: {value:.2f}")
        print(f"   Benchmark: {benchmark.level.value}")
        if benchmark.segment:
            print(f"   Segment: {benchmark.segment}")
        print(f"   Médiane: {comparison['benchmark']['median']:.2f}")
        print(f"   Percentile: {comparison['comparison']['percentile_rank']}")
        print(f"   vs Médiane: {comparison['comparison']['vs_median_pct']:+.1f}%")
        print(f"   Status: {comparison['comparison']['tier'].upper()}")
        print(f"   {comparison['interpretation']}")


# Export
__all__ = [
    'BenchmarkCalculator',
    'BenchmarkUpdater',
    'BenchmarkResult',
    'BenchmarkLevel',
    'MetricType',
    'print_benchmark_summary',
    'compare_client_to_benchmarks'
]
