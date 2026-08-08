import os
import sys
from src.data_generator import generate_datasets
from src.nlp_clustering_engine import SkillGapNLPEngine

def main():
    print("=" * 60)
    print(" INTERN SKILL GAP ANALYSIS & TRAINING RECOMMENDATION SYSTEM ")
    print(" NLP (TF-IDF) + K-MEANS CLUSTERING PIPELINE ")
    print("=" * 60)
    
    data_dir = "data"
    print("\n[Step 1/3] Generating synthetic datasets (Jobs, Interns, Courses)...")
    generate_datasets(data_dir=data_dir)
    
    print("\n[Step 2/3] Initializing & executing NLP Clustering & Gap Analysis Engine...")
    engine = SkillGapNLPEngine(data_dir=data_dir, n_clusters=6)
    results = engine.generate_full_analysis()
    
    print("\n[Step 3/3] Pipeline Summary Statistics:")
    stats = results["global_stats"]
    print(f"  • Total Industry Jobs Analyzed  : {stats['total_jobs']}")
    print(f"  • Total Interns Evaluated       : {stats['total_interns']}")
    print(f"  • Discovered Role Clusters      : {stats['n_clusters']}")
    print(f"  • Clustering Silhouette Score   : {stats['silhouette_score']}")
    print(f"  • Average Intern Readiness Score: {stats['avg_readiness_score']}%")
    
    print("\nTop 5 Skill Deficiencies Across All Interns:")
    for idx, gap in enumerate(stats['top_missing_skills'][:5], 1):
        print(f"  {idx}. {gap['skill']} - Affected Interns: {gap['affected_interns']}/{stats['total_interns']}")
        
    print("\n" + "=" * 60)
    print("Pipeline Execution Completed Successfully!")
    print("Analysis data written to 'data/analysis_results.json'")
    print("=" * 60)

if __name__ == "__main__":
    main()
