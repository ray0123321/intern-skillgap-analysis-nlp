# Intern Skill Gap Analysis & Training Recommendation System 🎯

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.0%2B-orange?style=for-the-badge&logo=scikitlearn)
![NLP](https://img.shields.io/badge/NLP-TF--IDF-green?style=for-the-badge)
![Clustering](https://img.shields.io/badge/Model-K--Means%20%2B%20PCA-purple?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-brightgreen?style=for-the-badge)

An end-to-end AI application that leverages **Natural Language Processing (TF-IDF Vectorization)** and **Unsupervised Machine Learning (K-Means Clustering)** to analyze intern skill databases against real-time industry job descriptions, identify critical skill deficiencies, and generate personalized, actionable training roadmaps.

---

## 🌟 Key Features

- **🤖 Automated Dataset Pipeline**: Generates 100+ realistic industry job postings across 6 tech domains, 50+ intern profiles, and a catalog of curated training modules.
- **🔤 TF-IDF Text Vectorization**: Mined text features using 1-gram & 2-gram TF-IDF n-gram extraction, stop-word removal, and skill vocabulary weighting.
- **📊 K-Means Role Clustering**: Discovers latent industry role groupings, computes cluster centroids, and evaluates cluster cohesion via Silhouette Score analysis.
- **🗺️ 2D PCA Cluster Map**: High-dimensional vector space reduced to an interactive 2D scatter plot for visualizing role relationships and centroid markers.
- **🎯 Precision Skill Gap Engine**: Calculates Cosine Similarity between intern profile vectors and cluster benchmarks to classify **Hard Gaps** (Missing Core Skills) and **Soft Gaps** (Proficiency Upgrades).
- **🎓 Personalized Training Roadmaps**: Automatically ranks skill gaps by cluster weight and constructs step-by-step learning modules with recommended durations, difficulty tiers, and hands-on capstone projects.
- **💻 Interactive Web Dashboard**: High-performance single-page web UI featuring glassmorphism aesthetics, Chart.js visualizations (Doughnut, Bar, Scatter, Radar), intern roster filtering, and an instant **Live Resume Evaluator Playground**.

---

## 📸 Dashboard Highlights

| Feature | Description |
| :--- | :--- |
| **Executive Overview** | Summary KPIs, K-Means cluster job count distribution, and global intern skill deficiencies. |
| **Industry Job Clusters** | 2D PCA scatter projection of job description vectors & cluster centroid keyword weights. |
| **Intern Gap Explorer** | Searchable intern roster with interactive Radar Chart comparing skills vs. industry benchmarks. |
| **Training Roadmaps** | Step-by-step personalized learning paths complete with capstone project specifications. |
| **Live Candidate Evaluator** | Real-time text playground for evaluating custom resumes/skills against target role benchmarks. |

---

## 📂 Project Architecture

```
intern-skillgap-analysis-nlp/
├── data/
│   ├── analysis_results.json    # Exported NLP analysis & clustering results
│   ├── intern_skills.json       # 50+ intern skill profiles database
│   ├── job_descriptions.json    # 100+ industry job descriptions
│   └── training_courses.json    # Catalog of training courses & capstone projects
├── src/
│   ├── data_generator.py        # Dataset generator script
│   └── nlp_clustering_engine.py # TF-IDF, K-Means, PCA & Skill Gap engine
├── index.html                   # Single-page web dashboard HTML layout
├── styles.css                   # Modern dark-theme glassmorphism CSS design system
├── app.js                       # Frontend interactive logic & Chart.js instances
├── run_pipeline.py              # CLI pipeline runner script
├── requirements.txt             # Python dependencies
└── README.md                    # Project documentation
```

---

## 🚀 Quickstart & Installation

### 1. Prerequisites
Ensure you have Python 3.9+ installed on your system.

### 2. Clone Repository
```bash
git clone https://github.com/ray0123321/intern-skillgap-analysis-nlp.git
cd intern-skillgap-analysis-nlp
```

### 3. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 4. Execute NLP & Machine Learning Pipeline
To run data generation, train TF-IDF & K-Means clustering models, and compute gap matrices:
```bash
python run_pipeline.py
```

### 5. Launch Interactive Web Dashboard
Start a local web server:
```bash
python -m http.server 8080
```
Open **[http://localhost:8080](http://localhost:8080)** in your web browser to explore the dashboard!

---

## 🛠️ Built With

- **Python**: Core Machine Learning and Data Analysis pipeline.
- **scikit-learn**: `TfidfVectorizer`, `KMeans`, `PCA`, `silhouette_score`, `cosine_similarity`.
- **Chart.js**: Client-side interactive data visualizations (Radar, Scatter, Bar, Doughnut).
- **HTML5 & Vanilla CSS**: Custom responsive dark-mode UI with glassmorphism design tokens.

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
