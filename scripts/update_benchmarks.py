#!/usr/bin/env python3
"""
Update Benchmarks - Script pour calculer et mettre à jour les benchmarks
À lancer quotidiennement (ou via cron)
"""

import os
import sys
from datetime import datetime
from dotenv import load_dotenv
import pandas as pd

# Load environment
load_dotenv()

# Import modules
sys.path.insert(0, os.path.dirname(__file__))
from benchmark_calculator import (
    BenchmarkCalculator,
    BenchmarkUpdater,
    MetricType,
    print_benchmark_summary
)
from growthOS.growthOS_reader import GrowthOSReader


def load_performance_snapshots(reader: GrowthOSReader) -> pd.DataFrame:
    """
    Charge tous les snapshots de performance depuis Google Sheets
    """
    print("📥 Chargement des snapshots de performance...")
    
    # Lire depuis PERFORMANCE_SNAPSHOTS sheet (à créer)
    # Pour l'instant, construire depuis métriques existantes
    
    # Récupérer tous les clients
    clients = reader.get_clients()
    
    all_snapshots = []
    
    for _, client in clients.iterrows():
        client_key = client['key']
        
        print(f"   Loading {client_key}...")
        
        # Récupérer métriques des 90 derniers jours
        metrics_90d = reader.get_recent_metrics(
            client_key=client_key,
            period='D',
            days=90
        )
        
        if not metrics_90d.empty:
            # Ajouter infos client
            metrics_90d['industry'] = client.get('industry')
            metrics_90d['offer_type'] = client.get('offer_type')
            metrics_90d['target_geo'] = client.get('target_geo')
            metrics_90d['maturity_stage'] = client.get('maturity_stage')
            
            all_snapshots.append(metrics_90d)
    
    if all_snapshots:
        snapshots_df = pd.concat(all_snapshots, ignore_index=True)
        print(f"✅ {len(snapshots_df)} snapshots chargés")
        return snapshots_df
    else:
        print("⚠️ Aucun snapshot trouvé")
        return pd.DataFrame()


def main():
    """
    Main function pour update des benchmarks
    """
    print("\n" + "="*60)
    print("🎯 BENCHMARK CALCULATOR - Update")
    print("="*60 + "\n")
    
    # Initialiser reader
    try:
        reader = GrowthOSReader()
    except Exception as e:
        print(f"❌ Erreur initialisation reader: {e}")
        return 1
    
    # Charger snapshots
    snapshots = load_performance_snapshots(reader)
    
    if snapshots.empty:
        print("❌ Pas de données pour calculer benchmarks")
        return 1
    
    # Charger client master
    clients = reader.get_clients()
    
    if clients.empty:
        print("❌ Pas de clients configurés")
        return 1
    
    # Initialiser calculator
    calculator = BenchmarkCalculator(
        performance_snapshots=snapshots,
        client_master=clients
    )
    
    # Initialiser updater
    updater = BenchmarkUpdater(calculator)
    
    # Définir périodes à calculer
    periods = [7, 30, 90]  # 7 jours, 30 jours, 90 jours
    
    for period in periods:
        print(f"\n{'='*60}")
        print(f"📊 Calcul benchmarks - Période: {period} jours")
        print(f"{'='*60}\n")
        
        # Output filepath
        output_dir = "storage/benchmarks"
        os.makedirs(output_dir, exist_ok=True)
        output_file = f"{output_dir}/benchmarks_{period}d.json"
        
        # Calculer et sauvegarder
        benchmarks = updater.update_all(
            output_filepath=output_file,
            period_days=period
        )
        
        # Afficher quelques exemples
        if benchmarks:
            print(f"\n📋 Exemples de benchmarks calculés:\n")
            
            # ROI Global
            if 'roi_vendu' in benchmarks and 'global' in benchmarks['roi_vendu']:
                print_benchmark_summary(benchmarks['roi_vendu']['global'])
            
            # CPA Global
            if 'cpa' in benchmarks and 'global' in benchmarks['cpa']:
                print_benchmark_summary(benchmarks['cpa']['global'])
    
    print("\n" + "="*60)
    print("✅ Tous les benchmarks ont été mis à jour!")
    print("="*60)
    
    # Afficher statistiques
    print(f"\n📊 Statistiques:")
    print(f"   • Comptes analysés: {clients['key'].nunique()}")
    print(f"   • Snapshots analysés: {len(snapshots)}")
    print(f"   • Périodes calculées: {len(periods)}")
    print(f"   • Fichiers générés: {len(periods)}")
    
    print(f"\n💾 Fichiers sauvegardés dans: storage/benchmarks/")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
