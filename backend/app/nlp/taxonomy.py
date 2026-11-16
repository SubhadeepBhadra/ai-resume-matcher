"""
Comprehensive Skills and Technical Competency Taxonomy.
Provides canonical names, aliases, and categorized skill mappings for accurate extraction.
"""

from typing import Dict, List, Set, Tuple
import re

# Mapping canonical skill -> list of aliases / synonyms
SKILL_TAXONOMY: Dict[str, Dict[str, any]] = {
    # Programming Languages
    "Python": {"category": "Programming Languages", "aliases": ["python", "python3", "python 3", "py"]},
    "Java": {"category": "Programming Languages", "aliases": ["java", "core java", "j2ee", "java 8", "java 11", "java 17", "java 21"]},
    "JavaScript": {"category": "Programming Languages", "aliases": ["javascript", "js", "ecmascript", "es6", "es6+"]},
    "TypeScript": {"category": "Programming Languages", "aliases": ["typescript", "ts"]},
    "C++": {"category": "Programming Languages", "aliases": ["c++", "cpp", "modern c++"]},
    "C#": {"category": "Programming Languages", "aliases": ["c#", "csharp", ".net c#"]},
    "Go": {"category": "Programming Languages", "aliases": ["go", "golang"]},
    "Rust": {"category": "Programming Languages", "aliases": ["rust", "rustlang"]},
    "SQL": {"category": "Programming Languages", "aliases": ["sql", "t-sql", "pl/sql", "plsql", "structured query language"]},
    "HTML/CSS": {"category": "Programming Languages", "aliases": ["html", "html5", "css", "css3", "sass", "scss"]},
    "Bash/Shell": {"category": "Programming Languages", "aliases": ["bash", "shell", "powershell", "zsh", "shell scripting"]},
    "PHP": {"category": "Programming Languages", "aliases": ["php", "php8"]},
    "Kotlin": {"category": "Programming Languages", "aliases": ["kotlin"]},
    "Swift": {"category": "Programming Languages", "aliases": ["swift"]},
    "R": {"category": "Programming Languages", "aliases": ["r language", "r-lang", " r "]},

    # Frameworks & Libraries
    "FastAPI": {"category": "Backend Frameworks", "aliases": ["fastapi", "fast-api"]},
    "Flask": {"category": "Backend Frameworks", "aliases": ["flask"]},
    "Django": {"category": "Backend Frameworks", "aliases": ["django", "django rest framework", "drf"]},
    "Spring Boot": {"category": "Backend Frameworks", "aliases": ["spring boot", "springboot", "spring-boot", "spring framework", "spring"]},
    "Node.js": {"category": "Backend Frameworks", "aliases": ["node.js", "nodejs", "node js", "node"]},
    "Express.js": {"category": "Backend Frameworks", "aliases": ["express", "express.js", "expressjs"]},
    "ASP.NET": {"category": "Backend Frameworks", "aliases": ["asp.net", "asp.net core", ".net core", "dotnet"]},
    "React": {"category": "Frontend Frameworks", "aliases": ["react", "react.js", "reactjs", "react native"]},
    "Angular": {"category": "Frontend Frameworks", "aliases": ["angular", "angular.js", "angularjs", "angular 2+"]},
    "Vue.js": {"category": "Frontend Frameworks", "aliases": ["vue", "vue.js", "vuejs", "vue3"]},
    "Next.js": {"category": "Frontend Frameworks", "aliases": ["next.js", "nextjs", "next js"]},
    "Redux": {"category": "Frontend Frameworks", "aliases": ["redux", "redux toolkit", "rtk"]},
    "Tailwind CSS": {"category": "Frontend Frameworks", "aliases": ["tailwind", "tailwind css", "tailwindcss"]},
    "Bootstrap": {"category": "Frontend Frameworks", "aliases": ["bootstrap", "bootstrap 5"]},

    # AI, ML & NLP
    "Sentence Transformers": {"category": "AI / ML & NLP", "aliases": ["sentence transformers", "sentence-transformers", "sbert", "bi-encoder", "cross-encoder"]},
    "spaCy": {"category": "AI / ML & NLP", "aliases": ["spacy", "spacy nlp"]},
    "Natural Language Processing (NLP)": {"category": "AI / ML & NLP", "aliases": ["nlp", "natural language processing", "text mining", "text analysis"]},
    "Machine Learning": {"category": "AI / ML & NLP", "aliases": ["machine learning", "ml", "statistical learning"]},
    "Deep Learning": {"category": "AI / ML & NLP", "aliases": ["deep learning", "neural networks", "ann", "cnn", "rnn", "lstm"]},
    "Large Language Models (LLMs)": {"category": "AI / ML & NLP", "aliases": ["llm", "llms", "large language models", "gpt", "gpt-4", "claude", "gemini", "llama", "mistral"]},
    "Retrieval-Augmented Generation (RAG)": {"category": "AI / ML & NLP", "aliases": ["rag", "retrieval augmented generation", "retrieval-augmented generation", "vector search"]},
    "Vector Databases": {"category": "AI / ML & NLP", "aliases": ["vector db", "vector database", "chroma", "chromadb", "pinecone", "qdrant", "weaviate", "milvus", "faiss"]},
    "PyTorch": {"category": "AI / ML & NLP", "aliases": ["pytorch", "torch"]},
    "TensorFlow": {"category": "AI / ML & NLP", "aliases": ["tensorflow", "tf", "keras"]},
    "Scikit-Learn": {"category": "AI / ML & NLP", "aliases": ["scikit-learn", "sklearn", "scikit learn"]},
    "Hugging Face": {"category": "AI / ML & NLP", "aliases": ["hugging face", "huggingface", "transformers", "hf"]},
    "Computer Vision": {"category": "AI / ML & NLP", "aliases": ["computer vision", "cv", "opencv", "yolo", "object detection"]},
    "LangChain": {"category": "AI / ML & NLP", "aliases": ["langchain", "llamaindex", "llama-index"]},
    "Prompt Engineering": {"category": "AI / ML & NLP", "aliases": ["prompt engineering", "prompt tuning", "few-shot learning"]},
    "Data Science": {"category": "AI / ML & NLP", "aliases": ["data science", "pandas", "numpy", "matplotlib", "seaborn", "scipy"]},

    # Databases & Storage
    "PostgreSQL": {"category": "Databases & Storage", "aliases": ["postgresql", "postgres", "psql"]},
    "MySQL": {"category": "Databases & Storage", "aliases": ["mysql", "mariadb"]},
    "MongoDB": {"category": "Databases & Storage", "aliases": ["mongodb", "mongo", "nosql"]},
    "Redis": {"category": "Databases & Storage", "aliases": ["redis", "in-memory cache"]},
    "Elasticsearch": {"category": "Databases & Storage", "aliases": ["elasticsearch", "elastic search", "opensearch", "elk", "kibana"]},
    "SQLite": {"category": "Databases & Storage", "aliases": ["sqlite", "sqlite3"]},
    "Oracle": {"category": "Databases & Storage", "aliases": ["oracle db", "oracle database", "oracle"]},
    "Cassandra": {"category": "Databases & Storage", "aliases": ["cassandra", "apache cassandra"]},
    "DynamoDB": {"category": "Databases & Storage", "aliases": ["dynamodb", "aws dynamodb"]},

    # Cloud & DevOps
    "AWS": {"category": "Cloud & DevOps", "aliases": ["aws", "amazon web services", "ec2", "s3", "lambda", "ecs", "eks", "rds", "sqs", "sns"]},
    "Azure": {"category": "Cloud & DevOps", "aliases": ["azure", "microsoft azure", "azure devops", "azure functions", "blob storage"]},
    "Google Cloud (GCP)": {"category": "Cloud & DevOps", "aliases": ["gcp", "google cloud", "google cloud platform", "bigquery", "cloud run", "gke"]},
    "Docker": {"category": "Cloud & DevOps", "aliases": ["docker", "containerization", "containers", "docker-compose", "dockerfile"]},
    "Kubernetes": {"category": "Cloud & DevOps", "aliases": ["kubernetes", "k8s", "helm"]},
    "CI/CD": {"category": "Cloud & DevOps", "aliases": ["ci/cd", "ci cd", "cicd", "continuous integration", "continuous deployment", "jenkins", "github actions", "gitlab ci"]},
    "Terraform": {"category": "Cloud & DevOps", "aliases": ["terraform", "iac", "infrastructure as code"]},
    "Linux": {"category": "Cloud & DevOps", "aliases": ["linux", "ubuntu", "debian", "redhat", "centos"]},
    "Git": {"category": "Cloud & DevOps", "aliases": ["git", "github", "gitlab", "bitbucket", "version control"]},

    # Architecture & Practices
    "RESTful APIs": {"category": "Architecture & Engineering", "aliases": ["rest", "rest api", "restful api", "restful apis", "rest apis", "web apis"]},
    "GraphQL": {"category": "Architecture & Engineering", "aliases": ["graphql", "apollo"]},
    "Microservices": {"category": "Architecture & Engineering", "aliases": ["microservices", "microservice architecture", "distributed systems", "event-driven architecture"]},
    "System Design": {"category": "Architecture & Engineering", "aliases": ["system design", "software architecture", "scalability", "high availability"]},
    "Agile / Scrum": {"category": "Architecture & Engineering", "aliases": ["agile", "scrum", "kanban", "sprints", "jira"]},
    "Unit Testing / TDD": {"category": "Architecture & Engineering", "aliases": ["tdd", "test driven development", "unit testing", "pytest", "junit", "jest", "cypress", "mocha"]},
    "Kafka / Messaging": {"category": "Architecture & Engineering", "aliases": ["kafka", "apache kafka", "rabbitmq", "message queues", "pub/sub", "event driven"]},
    "ETL / Data Pipelines": {"category": "Architecture & Engineering", "aliases": ["etl", "data pipelines", "airflow", "apache airflow", "spark", "apache spark"]}
}

# Precompile regex searchers for each canonical skill
COMPILED_SKILL_PATTERNS = []

for canon_name, data in SKILL_TAXONOMY.items():
    patterns = []
    for alias in data["aliases"]:
        escaped = re.escape(alias)
        # Word boundary match, handling symbols like C++, C#, .NET
        if alias.startswith(".") or alias.endswith("+") or alias.endswith("#"):
            pat = r"(?<!\w)" + escaped + r"(?!\w)"
        else:
            pat = r"\b" + escaped + r"\b"
        patterns.append(pat)
    full_pattern = re.compile("|".join(patterns), re.IGNORECASE)
    COMPILED_SKILL_PATTERNS.append((canon_name, data["category"], full_pattern))


def extract_skills_from_text(text: str) -> List[Dict[str, str]]:
    """
    Extracts all canonical skills matching the taxonomy from the input text.
    Returns list of dicts with name and category.
    """
    found_skills = []
    seen = set()
    
    # Normalize text spaces
    clean_text = " " + text.replace("/", " / ") + " "
    
    for canon_name, category, regex in COMPILED_SKILL_PATTERNS:
        if canon_name not in seen and regex.search(clean_text):
            found_skills.append({
                "name": canon_name,
                "category": category
            })
            seen.add(canon_name)
            
    return found_skills


def get_skill_names(skills_list: List[Dict[str, str]]) -> List[str]:
    """Helper to get just names list"""
    return [s["name"] for s in skills_list]
