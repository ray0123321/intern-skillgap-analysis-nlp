import json
import os
import random

def generate_datasets(data_dir="data", output_dir=None):
    if output_dir:
        data_dir = output_dir
    os.makedirs(data_dir, exist_ok=True)
    random.seed(42)

    # 1. Job Descriptions Generation
    role_templates = {
        "Full-Stack Web Engineering": {
            "titles": ["Frontend Developer", "Backend Engineer", "Full Stack Engineer", "React Developer", "Node.js Developer"],
            "core_skills": ["React", "JavaScript", "TypeScript", "Node.js", "Express", "HTML5", "CSS3", "PostgreSQL", "REST API", "GraphQL", "Git", "Docker", "Jest"],
            "descriptions": [
                "Responsible for building responsive web interfaces with React, managing Node.js backend services, designing RESTful APIs, and implementing database queries in PostgreSQL. Experience with TypeScript and Docker is preferred.",
                "Seeking a Full Stack Engineer proficient in JavaScript/TypeScript ecosystem. You will develop modern web applications using React on the frontend and Express/Node.js on the backend, alongside CI/CD workflows and automated testing.",
                "Join our web team to write clean frontend HTML5/CSS3/React components and optimize backend Node.js microservices. Deep understanding of state management, REST APIs, and database design required."
            ]
        },
        "Data Science & Machine Learning": {
            "titles": ["Machine Learning Engineer", "Data Scientist", "NLP Engineer", "AI Researcher", "Data Analyst"],
            "core_skills": ["Python", "PyTorch", "TensorFlow", "Scikit-Learn", "Pandas", "NumPy", "NLP", "Machine Learning", "Deep Learning", "SQL", "Feature Engineering", "Data Visualization", "Matplotlib"],
            "descriptions": [
                "Designing and training machine learning models using Python, Scikit-Learn, and PyTorch. Tasks include feature extraction, natural language processing (NLP), statistical modeling, and data analysis using Pandas and NumPy.",
                "Looking for a Data Scientist to build predictive ML algorithms, evaluate clustering models, analyze large datasets with SQL and Pandas, and present insights via interactive data visualizations.",
                "Develop state-of-the-art NLP pipelines and deep learning solutions using PyTorch/TensorFlow. Must have strong foundational knowledge in mathematics, statistical inference, and Scikit-Learn."
            ]
        },
        "Cloud & DevOps Infrastructure": {
            "titles": ["DevOps Engineer", "Cloud Infrastructure Specialist", "Site Reliability Engineer", "System Administrator"],
            "core_skills": ["AWS", "Kubernetes", "Docker", "Terraform", "CI/CD", "Linux", "Python", "Bash", "Ansible", "CloudWatch", "Prometheus", "Networking"],
            "descriptions": [
                "Automate cloud deployments on AWS using Kubernetes, Terraform, and Docker containers. Maintain CI/CD pipelines, optimize server infrastructure, and write operational automation scripts in Python/Bash.",
                "Seeking a DevOps Engineer experienced in cloud architecture, infrastructure as code (IaC), container orchestration with Kubernetes, and continuous deployment workflows.",
                "Manage cloud infrastructure reliability, configure Linux servers, implement monitoring tools like Prometheus and CloudWatch, and secure network gateways."
            ]
        },
        "Mobile Application Development": {
            "titles": ["Mobile App Developer", "React Native Developer", "iOS Engineer", "Android Engineer", "Flutter Developer"],
            "core_skills": ["React Native", "Flutter", "Swift", "Kotlin", "JavaScript", "TypeScript", "iOS", "Android", "REST API", "Mobile UI/UX", "Firebase", "Redux"],
            "descriptions": [
                "Build cross-platform mobile apps using React Native or Flutter. Integrate with RESTful microservices, optimize UI responsiveness, and manage app store release lifecycles for iOS and Android.",
                "Mobile developer needed for creating intuitive native or cross-platform smartphone applications. Expertise in React Native, Swift/Kotlin, state management, and mobile push notifications required.",
                "Develop high-performance mobile features with Flutter/Dart, implement modern UI/UX design components, and perform local caching with SQLite or Firebase."
            ]
        },
        "Cyber Security & InfoSec": {
            "titles": ["Security Analyst", "Penetration Tester", "Information Security Engineer", "SOC Analyst"],
            "core_skills": ["Cyber Security", "Penetration Testing", "Network Security", "Python", "Linux", "Wireshark", "Metasploit", "Cryptography", "SIEM", "Vulnerability Assessment", "Firewalls"],
            "descriptions": [
                "Perform vulnerability assessments, penetration testing, and network security audits. Analyze threats using SIEM tools, investigate security logs with Wireshark, and write automation scripts in Python.",
                "Protect corporate digital assets by conducting security audits, configuring firewalls, implementing cryptographic standards, and performing ethical hacking exercises on web/cloud infrastructure.",
                "Monitor security event logs, analyze malware samples, enforce network protocol compliance, and develop security incident response protocols."
            ]
        },
        "Data & Analytics Engineering": {
            "titles": ["Data Engineer", "ETL Developer", "Big Data Specialist", "Analytics Engineer"],
            "core_skills": ["SQL", "Snowflake", "Apache Spark", "Airflow", "dbt", "Python", "Data Warehousing", "ETL", "BigQuery", "Kafka", "Data Modeling"],
            "descriptions": [
                "Build scalable ETL/ELT pipelines using SQL, Python, Apache Spark, and dbt. Data warehousing experience with Snowflake or BigQuery and orchestration with Apache Airflow required.",
                "Design robust data architectures, write optimized SQL queries, manage streaming datasets with Kafka, and maintain data warehouse schema modeling.",
                "Data Engineer to construct automated ingestion pipelines, clean structured and unstructured data sources, and ensure high data quality for business intelligence dashboards."
            ]
        }
    }

    job_descriptions = []
    job_id = 1
    for category, info in role_templates.items():
        # Generate 17-18 jobs per category to get ~100 jobs
        for i in range(17):
            title = random.choice(info["titles"])
            desc_sample = random.choice(info["descriptions"])
            # select a subset of core skills + random extra skill
            sampled_skills = random.sample(info["core_skills"], k=min(len(info["core_skills"]), random.randint(5, 8)))
            
            # create full text combining title, skills, description
            full_text = f"{title} Role: {desc_sample} Key required skills: {', '.join(sampled_skills)}. Experience: {random.choice(['Entry-Level', 'Junior', 'Internship', 'Associate'])}."

            job_descriptions.append({
                "job_id": f"JOB_{job_id:03d}",
                "title": title,
                "domain_category": category,
                "skills": sampled_skills,
                "experience_level": random.choice(["Internship", "Entry-Level", "Junior"]),
                "description_text": full_text
            })
            job_id += 1

    # 2. Intern Skills Generation
    names = [
        "Alex Rivera", "Brenda Chen", "Carlos Gomez", "Diana Patel", "Ethan Hunt", 
        "Fiona Wang", "George Miller", "Hannah Smith", "Ian Wright", "Julia Roberts",
        "Kevin Zhang", "Laura Kim", "Michael Brown", "Nina Davis", "Oscar Garcia",
        "Priya Sharma", "Quinn Taylor", "Rachel Green", "Sam Wilson", "Tina Fey",
        "Umar Khan", "Valerie Scott", "Will Jackson", "Xavier Lopez", "Yara Ahmed",
        "Zack Snyder", "Amy Adams", "Ben Affleck", "Chloe Bennett", "David Miller",
        "Emma Watson", "Frank Castle", "Grace Hopper", "Harry Potter", "Isla Fisher",
        "Jack Ryan", "Karen Gillan", "Liam Neeson", "Mia Khalifa", "Nathan Drake",
        "Olivia Wilde", "Peter Parker", "Queen Latifah", "Ryan Reynolds", "Sarah Connor",
        "Tom Holland", "Uma Thurman", "Victor Stone", "Wanda Maximoff", "Yolanda Adams"
    ]

    interns = []
    for idx, name in enumerate(names, 1):
        target_domain = random.choice(list(role_templates.keys()))
        target_info = role_templates[target_domain]
        
        # Intern possesses 60% of core skills for their target domain (some strong, some weak) + 1-2 cross domain skills
        known_skills = random.sample(target_info["core_skills"], k=random.randint(3, 5))
        other_domain = random.choice([k for k in role_templates.keys() if k != target_domain])
        known_skills.extend(random.sample(role_templates[other_domain]["core_skills"], k=random.randint(1, 2)))
        
        skill_dict = {}
        for skill in set(known_skills):
            # 1: Beginner, 2: Basic, 3: Intermediate, 4: Advanced, 5: Expert
            # Most interns are 1-3 level
            skill_dict[skill] = random.choice([1, 2, 2, 3, 3, 4])
            
        resume_summary = f"{name} is a passionate computer science graduate aiming for a role in {target_domain}. Proficient in {', '.join(skill_dict.keys())}. Looking to upskill in modern industry standards and hands-on production toolings."
        
        interns.append({
            "intern_id": f"INT_{idx:03d}",
            "name": name,
            "email": f"{name.lower().replace(' ', '.')}@university.edu",
            "target_domain": target_domain,
            "degree": random.choice(["B.S. Computer Science", "B.S. Software Engineering", "B.S. Data Science", "B.Tech Information Technology"]),
            "skills": skill_dict,
            "resume_text": resume_summary,
            "confidence_score": round(random.uniform(0.55, 0.90), 2)
        })

    # 3. Training Catalog Generation
    training_catalog = [
        # Web Dev Courses
        {
            "course_id": "CRS_WEB_01",
            "skill_name": "React",
            "title": "Mastering React 18 & Modern State Management",
            "provider": "TechAcademy",
            "duration_hours": 24,
            "difficulty": "Intermediate",
            "description": "Deep dive into React functional components, Hooks, Context API, Redux Toolkit, and performance optimization.",
            "project_name": "E-Commerce Dashboard SPA"
        },
        {
            "course_id": "CRS_WEB_02",
            "skill_name": "Node.js",
            "title": "Backend Engineering with Node.js & Express",
            "provider": "NodeMasters",
            "duration_hours": 30,
            "difficulty": "Intermediate",
            "description": "Build production-ready RESTful APIs, JWT authentication, rate limiting, and PostgreSQL integration.",
            "project_name": "Microservices Authentication Gateway"
        },
        {
            "course_id": "CRS_WEB_03",
            "skill_name": "TypeScript",
            "title": "TypeScript Fundamentals to Advanced Systems",
            "provider": "Frontend Masters",
            "duration_hours": 15,
            "difficulty": "Beginner-Intermediate",
            "description": "Learn strict typing, generics, interfaces, decorators, and integrating TypeScript into full-stack web applications.",
            "project_name": "Typed Data Modeling Library"
        },
        {
            "course_id": "CRS_WEB_04",
            "skill_name": "GraphQL",
            "title": "Modern GraphQL API Design with Apollo",
            "provider": "GraphQL Institute",
            "duration_hours": 18,
            "difficulty": "Intermediate",
            "description": "Schema definition language, query resolvers, mutations, subscriptions, and caching strategies.",
            "project_name": "Real-time Collaboration Platform API"
        },

        # Data Science & ML Courses
        {
            "course_id": "CRS_ML_01",
            "skill_name": "PyTorch",
            "title": "Deep Learning with PyTorch in Practice",
            "provider": "DeepLearning.AI",
            "duration_hours": 35,
            "difficulty": "Intermediate-Advanced",
            "description": "Train neural networks, CNNs, RNNs, and Transformers using PyTorch framework with GPU acceleration.",
            "project_name": "Image Classification & NLP Classifier"
        },
        {
            "course_id": "CRS_ML_02",
            "skill_name": "Scikit-Learn",
            "title": "Applied Machine Learning & Clustering Algorithms",
            "provider": "ML Academy",
            "duration_hours": 20,
            "difficulty": "Intermediate",
            "description": "Supervised & unsupervised learning, TF-IDF vectorization, K-Means clustering, PCA, and model evaluation.",
            "project_name": "Customer Segmentation & Clustering Pipeline"
        },
        {
            "course_id": "CRS_ML_03",
            "skill_name": "NLP",
            "title": "Natural Language Processing with Transformers & TF-IDF",
            "provider": "NLP Edge",
            "duration_hours": 28,
            "difficulty": "Intermediate",
            "description": "Text pre-processing, TF-IDF feature extraction, sentiment analysis, named entity recognition, and BERT fine-tuning.",
            "project_name": "Resume & Job Description Skill Matcher"
        },
        {
            "course_id": "CRS_ML_04",
            "skill_name": "Feature Engineering",
            "title": "Advanced Feature Engineering for Machine Learning",
            "provider": "DataCamp",
            "duration_hours": 16,
            "difficulty": "Intermediate",
            "description": "Categorical encoding, numerical scaling, dimensionality reduction, missing data imputation, and automated feature selection.",
            "project_name": "Predictive Analytics Feature Pipeline"
        },

        # Cloud & DevOps Courses
        {
            "course_id": "CRS_DO_01",
            "skill_name": "Kubernetes",
            "title": "Kubernetes Container Orchestration Mastery",
            "provider": "Cloud Native Academy",
            "duration_hours": 32,
            "difficulty": "Intermediate-Advanced",
            "description": "Deploying, scaling, and managing containerized applications with Pods, Deployments, Services, and Helm charts.",
            "project_name": "Production Kubernetes Cluster Deployment"
        },
        {
            "course_id": "CRS_DO_02",
            "skill_name": "AWS",
            "title": "AWS Certified Solutions Architect Training",
            "provider": "AWS Education",
            "duration_hours": 40,
            "difficulty": "Intermediate",
            "description": "Core cloud architecture: EC2, S3, RDS, Lambda, VPC, IAM security, and auto-scaling infrastructure.",
            "project_name": "Serverless Cloud Architecture Setup"
        },
        {
            "course_id": "CRS_DO_03",
            "skill_name": "Terraform",
            "title": "Infrastructure as Code (IaC) with Terraform",
            "provider": "HashiCorp Learn",
            "duration_hours": 18,
            "difficulty": "Intermediate",
            "description": "Provision and manage cloud resources declaratively using Terraform modules and state management.",
            "project_name": "Automated AWS Multi-Region Environment"
        },
        {
            "course_id": "CRS_DO_04",
            "skill_name": "CI/CD",
            "title": "Building Production CI/CD Pipelines with GitHub Actions",
            "provider": "DevOps Hub",
            "duration_hours": 14,
            "difficulty": "Beginner-Intermediate",
            "description": "Automate testing, linting, Docker container builds, and cloud deployments with matrix workflows.",
            "project_name": "End-to-End Automated Release Pipeline"
        },

        # Mobile Courses
        {
            "course_id": "CRS_MOB_01",
            "skill_name": "React Native",
            "title": "Cross-Platform Mobile Apps with React Native",
            "provider": "Mobile Devs",
            "duration_hours": 25,
            "difficulty": "Intermediate",
            "description": "Build iOS and Android native apps with JavaScript/TypeScript, Expo, navigation, and device APIs.",
            "project_name": "Fitness Tracking Mobile App"
        },
        {
            "course_id": "CRS_MOB_02",
            "skill_name": "Flutter",
            "title": "Flutter & Dart Complete Mobile Bootcamp",
            "provider": "AppBrewery",
            "duration_hours": 28,
            "difficulty": "Beginner-Intermediate",
            "description": "Dart language fundamentals, widget hierarchy, state management with Bloc/Provider, and native integration.",
            "project_name": "Real-time Messaging App"
        },

        # Cyber Security Courses
        {
            "course_id": "CRS_SEC_01",
            "skill_name": "Penetration Testing",
            "title": "Practical Ethical Hacking & Penetration Testing",
            "provider": "CyberSec Institute",
            "duration_hours": 36,
            "difficulty": "Intermediate-Advanced",
            "description": "Reconnaissance, network scanning, vulnerability exploitation, web application security, and report writing.",
            "project_name": "Vulnerable Machine Exploitation Lab"
        },
        {
            "course_id": "CRS_SEC_02",
            "skill_name": "Network Security",
            "title": "Network Traffic Analysis & Security Protocols",
            "provider": "InfoSec Academy",
            "duration_hours": 22,
            "difficulty": "Intermediate",
            "description": "Packet inspection using Wireshark, firewalls setup, intrusion detection systems (IDS), and encryption standards.",
            "project_name": "Network Threat Detection System"
        },

        # Data Engineering Courses
        {
            "course_id": "CRS_DE_01",
            "skill_name": "Apache Spark",
            "title": "Big Data Processing with Apache Spark & PySpark",
            "provider": "Databricks Academy",
            "duration_hours": 30,
            "difficulty": "Intermediate-Advanced",
            "description": "Distributed computing, RDDs, DataFrames, Spark SQL, streaming data processing, and cluster optimization.",
            "project_name": "Large-Scale Log Analysis Pipeline"
        },
        {
            "course_id": "CRS_DE_02",
            "skill_name": "Snowflake",
            "title": "Snowflake Cloud Data Warehousing Essentials",
            "provider": "Snowflake University",
            "duration_hours": 16,
            "difficulty": "Beginner-Intermediate",
            "description": "Architecture, virtual warehouses, data sharing, JSON parsing, and loading bulk staging files.",
            "project_name": "Cloud Enterprise Data Mart"
        },
        {
            "course_id": "CRS_DE_03",
            "skill_name": "Airflow",
            "title": "Data Pipeline Orchestration with Apache Airflow",
            "provider": "Astronomer",
            "duration_hours": 20,
            "difficulty": "Intermediate",
            "description": "Writing DAGs, custom operators, task dependencies, sensor triggers, and scheduling production ETL workflows.",
            "project_name": "Automated Daily Financial ETL Workflow"
        }
    ]

    # Save to JSON files
    with open(os.path.join(data_dir, "job_descriptions.json"), "w", encoding="utf-8") as f:
        json.dump(job_descriptions, f, indent=2)

    with open(os.path.join(data_dir, "intern_skills.json"), "w", encoding="utf-8") as f:
        json.dump(interns, f, indent=2)

    with open(os.path.join(data_dir, "training_courses.json"), "w", encoding="utf-8") as f:
        json.dump(training_catalog, f, indent=2)

    print(f"Generated {len(job_descriptions)} job descriptions, {len(interns)} intern profiles, and {len(training_catalog)} training courses in '{data_dir}/'.")

if __name__ == "__main__":
    generate_datasets()
