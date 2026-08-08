import json
import os
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score
from sklearn.metrics.pairwise import cosine_similarity

class SkillGapNLPEngine:
    def __init__(self, data_dir="data", n_clusters=6):
        self.data_dir = data_dir
        self.n_clusters = n_clusters
        
        # Paths
        self.jobs_path = os.path.join(data_dir, "job_descriptions.json")
        self.interns_path = os.path.join(data_dir, "intern_skills.json")
        self.courses_path = os.path.join(data_dir, "training_courses.json")
        
        # Data containers
        self.jobs_df = None
        self.interns = []
        self.courses = []
        
        # Models
        self.vectorizer = TfidfVectorizer(
            stop_words='english',
            ngram_range=(1, 2),
            min_df=1,
            max_df=0.9
        )
        self.kmeans = None
        self.pca = PCA(n_components=2, random_state=42)
        
        # Matrix and mappings
        self.tfidf_matrix = None
        self.feature_names = []
        self.cluster_labels = []
        self.cluster_centroids = None
        self.cluster_names = {}
        self.silhouette_avg = 0.0

    def load_data(self):
        with open(self.jobs_path, "r", encoding="utf-8") as f:
            jobs_data = json.load(f)
            self.jobs_df = pd.DataFrame(jobs_data)
            
        with open(self.interns_path, "r", encoding="utf-8") as f:
            self.interns = json.load(f)
            
        with open(self.courses_path, "r", encoding="utf-8") as f:
            self.courses = json.load(f)

    def train_clusters(self):
        # Prepare text representation for job descriptions
        # Combine domain_category, title, skills, description_text
        combined_texts = []
        for _, row in self.jobs_df.iterrows():
            skills_str = " ".join(row['skills'])
            text = f"{row['title']} {row['domain_category']} {skills_str} {row['description_text']}"
            combined_texts.append(text)
            
        # 1. TF-IDF Vectorization
        self.tfidf_matrix = self.vectorizer.fit_transform(combined_texts)
        self.feature_names = np.array(self.vectorizer.get_feature_names_out())
        
        # 2. K-Means Clustering
        self.kmeans = KMeans(n_clusters=self.n_clusters, random_state=42, n_init=10)
        self.cluster_labels = self.kmeans.fit_predict(self.tfidf_matrix)
        self.jobs_df['cluster'] = self.cluster_labels
        self.cluster_centroids = self.kmeans.cluster_centers_
        
        # Compute silhouette score
        if self.tfidf_matrix.shape[0] > self.n_clusters:
            self.silhouette_avg = float(silhouette_score(self.tfidf_matrix, self.cluster_labels))
            
        # 3. Dynamic Cluster Naming based on Top Keywords & Dominant Domain
        for c_id in range(self.n_clusters):
            c_jobs = self.jobs_df[self.jobs_df['cluster'] == c_id]
            dominant_domain = c_jobs['domain_category'].mode()[0] if not c_jobs.empty else f"Cluster {c_id}"
            
            # Top keywords from centroid
            centroid = self.cluster_centroids[c_id]
            top_indices = centroid.argsort()[-8:][::-1]
            top_words = [self.feature_names[i] for i in top_indices]
            
            self.cluster_names[c_id] = {
                "name": dominant_domain,
                "top_words": top_words
            }

        # 4. PCA for 2D visual layout
        coords_2d = self.pca.fit_transform(self.tfidf_matrix.toarray())
        centroid_2d = self.pca.transform(self.cluster_centroids)
        
        self.jobs_df['x'] = round_list(coords_2d[:, 0])
        self.jobs_df['y'] = round_list(coords_2d[:, 1])
        
        self.centroid_2d = centroid_2d

    def analyze_intern_gaps(self):
        intern_results = []
        global_skill_deficiencies = {}

        # Course lookup index by skill
        course_by_skill = {}
        for c in self.courses:
            s_name = c['skill_name'].lower()
            if s_name not in course_by_skill:
                course_by_skill[s_name] = []
            course_by_skill[s_name].append(c)

        for intern in self.interns:
            # Construct text representation of intern skills for vectorization
            intern_skills_text = " ".join([f"{k} " * v for k, v in intern['skills'].items()])
            full_intern_text = f"{intern['target_domain']} {intern['resume_text']} {intern_skills_text}"
            
            intern_vec = self.vectorizer.transform([full_intern_text])
            intern_vec_dense = intern_vec.toarray()[0]
            
            # Find target domain cluster ID
            target_cluster_id = 0
            for cid, cinfo in self.cluster_names.items():
                if cinfo['name'] == intern['target_domain']:
                    target_cluster_id = cid
                    break

            # Calculate cosine similarity with all cluster centroids
            sims = cosine_similarity(intern_vec, self.cluster_centroids)[0]
            matched_cluster_id = int(np.argmax(sims))
            matched_similarity = float(sims[matched_cluster_id])
            target_similarity = float(sims[target_cluster_id])

            # Get target cluster centroid feature weights
            centroid_weights = self.cluster_centroids[target_cluster_id]
            
            # Extract top benchmark skills for target cluster
            top_bench_indices = centroid_weights.argsort()[-15:][::-1]
            benchmark_skills = []
            
            skill_radar_data = []
            missing_skills = []
            soft_gaps = []
            
            intern_skills_lower = {k.lower(): v for k, v in intern['skills'].items()}

            for idx in top_bench_indices:
                feature_word = self.feature_names[idx]
                req_weight = float(centroid_weights[idx])
                
                # Check if intern has this skill or word
                current_level = 0
                for s_key, lvl in intern_skills_lower.items():
                    if feature_word in s_key or s_key in feature_word:
                        current_level = lvl
                        break

                # Benchmark required level (scale 1-5 based on weight)
                bench_level = min(5, max(2, int(req_weight * 15)))
                
                skill_radar_data.append({
                    "skill": feature_word.capitalize(),
                    "intern_level": current_level,
                    "benchmark_level": bench_level,
                    "weight": round(req_weight, 3)
                })

                if current_level == 0:
                    missing_skills.append({
                        "skill": feature_word.capitalize(),
                        "severity": "High" if req_weight > 0.15 else "Medium",
                        "weight": round(req_weight, 3),
                        "current_level": 0,
                        "required_level": bench_level
                    })
                    # Track globally
                    s_cap = feature_word.capitalize()
                    global_skill_deficiencies[s_cap] = global_skill_deficiencies.get(s_cap, 0) + 1
                elif current_level < bench_level:
                    soft_gaps.append({
                        "skill": feature_word.capitalize(),
                        "severity": "Low",
                        "weight": round(req_weight, 3),
                        "current_level": current_level,
                        "required_level": bench_level
                    })

            # Readiness score (ratio of matched skills to benchmark required)
            total_bench_score = sum([s['benchmark_level'] for s in skill_radar_data]) or 1
            total_intern_score = sum([min(s['intern_level'], s['benchmark_level']) for s in skill_radar_data])
            readiness_score = int((total_intern_score / total_bench_score) * 100)

            # Build Training Roadmap
            roadmap = []
            all_gaps = missing_skills + soft_gaps
            all_gaps.sort(key=lambda x: x['weight'], reverse=True)

            step_num = 1
            for gap in all_gaps[:5]: # Top 5 prioritized gaps
                skill_key = gap['skill'].lower()
                matched_courses = course_by_skill.get(skill_key, [])
                
                if not matched_courses:
                    # fallback generic course match
                    matched_courses = [{
                        "course_id": f"CRS_GEN_{step_num}",
                        "title": f"Applied {gap['skill']} Hands-on Specialization",
                        "provider": "Tech Skills Institute",
                        "duration_hours": 20,
                        "difficulty": "Intermediate",
                        "description": f"Master fundamental and practical concepts of {gap['skill']} for production software applications.",
                        "project_name": f"{gap['skill']} Industry Capstone Project"
                    }]

                course = matched_courses[0]
                roadmap.append({
                    "step": step_num,
                    "target_skill": gap['skill'],
                    "gap_type": "Missing Core Skill" if gap['current_level'] == 0 else "Proficiency Upgrade",
                    "severity": gap['severity'],
                    "course_id": course['course_id'],
                    "course_title": course['title'],
                    "provider": course['provider'],
                    "duration_hours": course['duration_hours'],
                    "difficulty": course['difficulty'],
                    "description": course['description'],
                    "project_name": course['project_name']
                })
                step_num += 1

            intern_results.append({
                "intern_id": intern['intern_id'],
                "name": intern['name'],
                "email": intern['email'],
                "target_domain": intern['target_domain'],
                "assigned_cluster_id": matched_cluster_id,
                "assigned_cluster_name": self.cluster_names[matched_cluster_id]['name'],
                "target_cluster_id": target_cluster_id,
                "readiness_score": readiness_score,
                "confidence_score": intern['confidence_score'],
                "current_skills": intern['skills'],
                "resume_summary": intern['resume_text'],
                "radar_benchmark": skill_radar_data,
                "missing_skills": missing_skills,
                "soft_gaps": soft_gaps,
                "training_roadmap": roadmap
            })

        return intern_results, global_skill_deficiencies

    def generate_full_analysis(self):
        self.load_data()
        self.train_clusters()
        intern_results, global_deficiencies = self.analyze_intern_gaps()

        # Format cluster overview
        clusters_export = []
        for cid in range(self.n_clusters):
            c_info = self.cluster_names[cid]
            c_jobs = self.jobs_df[self.jobs_df['cluster'] == cid]
            
            centroid = self.cluster_centroids[cid]
            top_indices = centroid.argsort()[-10:][::-1]
            top_keywords = [{
                "word": self.feature_names[i].capitalize(),
                "tfidf_weight": round(float(centroid[i]), 4)
            } for i in top_indices]

            clusters_export.append({
                "cluster_id": cid,
                "name": c_info['name'],
                "job_count": len(c_jobs),
                "top_keywords": top_keywords,
                "centroid_x": round(float(self.centroid_2d[cid, 0]), 4),
                "centroid_y": round(float(self.centroid_2d[cid, 1]), 4)
            })

        # Format job points for 2D plot
        job_points = []
        for _, r in self.jobs_df.iterrows():
            job_points.append({
                "job_id": r['job_id'],
                "title": r['title'],
                "domain": r['domain_category'],
                "cluster_id": int(r['cluster']),
                "x": round(float(r['x']), 4),
                "y": round(float(r['y']), 4)
            })

        # Format top global deficiencies
        sorted_deficiencies = sorted(global_deficiencies.items(), key=lambda x: x[1], reverse=True)
        top_global_missing = [{"skill": k, "affected_interns": v} for k, v in sorted_deficiencies[:10]]

        avg_readiness = round(float(np.mean([i['readiness_score'] for i in intern_results])), 1)

        output_data = {
            "global_stats": {
                "total_jobs": len(self.jobs_df),
                "total_interns": len(intern_results),
                "n_clusters": self.n_clusters,
                "silhouette_score": round(self.silhouette_avg, 3),
                "avg_readiness_score": avg_readiness,
                "top_missing_skills": top_global_missing
            },
            "clusters": clusters_export,
            "job_points_2d": job_points,
            "interns": intern_results,
            "courses_catalog": self.courses
        }

        output_file = os.path.join(self.data_dir, "analysis_results.json")
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(output_data, f, indent=2)

        print(f"Analysis pipeline completed successfully! Saved output to '{output_file}'.")
        return output_data

def round_list(arr):
    return [round(float(val), 4) for val in arr]

if __name__ == "__main__":
    engine = SkillGapNLPEngine()
    engine.generate_full_analysis()
