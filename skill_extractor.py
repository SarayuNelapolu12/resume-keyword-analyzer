"""
skill_extractor.py - Skill Extraction & Text Normalization Engine
==================================================================
Provides text normalization, regex-based skill pattern matching,
and match percentage calculation for the Resume Keyword Analyzer.
"""

import re
from typing import Dict, List, Set, Tuple, Any


class SkillDefinition:
    """Represents a canonical skill definition with matching patterns and metadata."""

    def __init__(
        self,
        name: str,
        category: str,
        patterns: List[str],
        tier: int,
        description: str,
        prerequisites: List[str] = None,
        key_topics: List[str] = None,
        project_idea: str = "",
        estimated_weeks: int = 2,
    ):
        self.name = name
        self.category = category
        self.patterns = patterns
        self.tier = tier  # 1: Foundational, 2: Core/Framework, 3: Advanced/Cloud/AI
        self.description = description
        self.prerequisites = prerequisites or []
        self.key_topics = key_topics or []
        self.project_idea = project_idea
        self.estimated_weeks = estimated_weeks

        # Compile regex patterns for performance and boundary safety
        self.compiled_regexes = [
            re.compile(pattern, re.IGNORECASE) for pattern in patterns
        ]

    def matches(self, text: str) -> bool:
        """Check if any compiled pattern matches the normalized text."""
        for regex in self.compiled_regexes:
            if regex.search(text):
                return True
        return False


# =====================================================================
# Comprehensive Skill Dictionary
# Supports all 33 required skills with aliases, edge-case boundaries,
# and structured learning metadata.
# =====================================================================
SKILL_DICTIONARY: Dict[str, SkillDefinition] = {
    # -------------------------------------------------------------
    # 1. Programming Languages
    # -------------------------------------------------------------
    "Python": SkillDefinition(
        name="Python",
        category="Programming Languages",
        patterns=[r"\bpython(?:\d(?:\.\d+)?)?\b"],
        tier=1,
        description="High-level, versatile programming language renowned for backend, automation, and AI/ML.",
        prerequisites=[],
        key_topics=["Syntax & Data Structures", "OOP Concepts", "Generators & Decorators", "Virtual Environments"],
        project_idea="Build a multi-threaded CLI web scraper or backend automation tool.",
        estimated_weeks=2,
    ),
    "Java": SkillDefinition(
        name="Java",
        category="Programming Languages",
        patterns=[r"\bjava\b(?!\s*script)"],
        tier=1,
        description="Class-based, object-oriented language widely used in enterprise backend systems and Android.",
        prerequisites=[],
        key_topics=["OOP Principles", "JVM Architecture", "Collections Framework", "Streams API & Multithreading"],
        project_idea="Build an enterprise inventory management service using Core Java and JDBC.",
        estimated_weeks=3,
    ),
    "C++": SkillDefinition(
        name="C++",
        category="Programming Languages",
        patterns=[r"(?<![a-zA-Z0-9#+])c\+\+(?![a-zA-Z0-9#+])"],
        tier=1,
        description="High-performance compiled language used for game engines, low-latency trading, and systems programming.",
        prerequisites=[],
        key_topics=["Pointers & Memory Management", "STL (Standard Template Library)", "RAII & Smart Pointers", "Templates"],
        project_idea="Develop a custom memory allocator or low-latency cache system.",
        estimated_weeks=3,
    ),
    "JavaScript": SkillDefinition(
        name="JavaScript",
        category="Programming Languages",
        patterns=[
            r"\bjavascript\b",
            r"\becmascript\b",
            r"(?<![a-zA-Z0-9./])js(?![a-zA-Z0-9])",
        ],
        tier=1,
        description="Core language of the web enabling interactive client-side and asynchronous server-side applications.",
        prerequisites=[],
        key_topics=["ES6+ Syntax", "Event Loop & Promises", "Async/Await", "DOM Manipulation & Scope"],
        project_idea="Build an interactive task manager with local storage and asynchronous fetch API.",
        estimated_weeks=2,
    ),

    # -------------------------------------------------------------
    # 2. Frontend & Web Development
    # -------------------------------------------------------------
    "HTML": SkillDefinition(
        name="HTML",
        category="Frontend & Web Development",
        patterns=[r"\bhtml5?\b"],
        tier=1,
        description="Standard markup language used to structure web pages and applications.",
        prerequisites=[],
        key_topics=["Semantic Elements", "Forms & Input Validation", "Accessibility (a11y)", "SEO Tags"],
        project_idea="Build a semantic, fully accessible landing page adhering to WCAG standards.",
        estimated_weeks=1,
    ),
    "CSS": SkillDefinition(
        name="CSS",
        category="Frontend & Web Development",
        patterns=[r"\bcss3?\b"],
        tier=1,
        description="Style sheet language used for describing the presentation, styling, and responsive layout of web pages.",
        prerequisites=["HTML"],
        key_topics=["Flexbox & CSS Grid", "Responsive Design & Media Queries", "Animations & Transitions", "CSS Variables"],
        project_idea="Create a modern responsive dashboard layout using CSS Grid and Flexbox with dark mode.",
        estimated_weeks=1,
    ),
    "React": SkillDefinition(
        name="React",
        category="Frontend & Web Development",
        patterns=[r"\breact(?:\.?js|js)?\b"],
        tier=2,
        description="Component-based JavaScript UI library for building reactive, high-performance web frontends.",
        prerequisites=["JavaScript", "HTML", "CSS"],
        key_topics=["Hooks (useState, useEffect, useMemo)", "Component Lifecycle", "State Management", "Router"],
        project_idea="Build a responsive Kanban board web app with drag-and-drop and state persistence.",
        estimated_weeks=3,
    ),
    "Node.js": SkillDefinition(
        name="Node.js",
        category="Frontend & Web Development",
        patterns=[r"\bnode(?:\.?js|js)?\b"],
        tier=2,
        description="JavaScript runtime built on Chrome's V8 engine allowing server-side JavaScript execution.",
        prerequisites=["JavaScript"],
        key_topics=["Event-Driven Architecture", "File System (fs) & Streams", "NPM Ecosystem", "Express Integration"],
        project_idea="Develop a real-time collaborative chat server using Node.js and WebSockets.",
        estimated_weeks=2,
    ),

    # -------------------------------------------------------------
    # 3. Backend Frameworks & APIs
    # -------------------------------------------------------------
    "Flask": SkillDefinition(
        name="Flask",
        category="Backend Frameworks & APIs",
        patterns=[r"\bflask\b"],
        tier=2,
        description="Lightweight Python micro-framework designed for building agile web services and APIs.",
        prerequisites=["Python"],
        key_topics=["Routing & Request Handling", "Blueprints", "Jinja2 Templating", "SQLAlchemy Integration"],
        project_idea="Build a modular blog or RESTful microservice with database migrations.",
        estimated_weeks=2,
    ),
    "Django": SkillDefinition(
        name="Django",
        category="Backend Frameworks & APIs",
        patterns=[r"\bdjango\b"],
        tier=2,
        description="Batteries-included Python web framework prioritizing rapid development and clean design.",
        prerequisites=["Python", "SQL"],
        key_topics=["MVT Architecture", "Django ORM", "Built-in Admin & Auth", "Django REST Framework (DRF)"],
        project_idea="Construct an e-commerce backend platform with authentication, orders, and payment webhooks.",
        estimated_weeks=3,
    ),
    "FastAPI": SkillDefinition(
        name="FastAPI",
        category="Backend Frameworks & APIs",
        patterns=[r"\bfastapi\b"],
        tier=2,
        description="High-performance modern Python web framework for building APIs with automatic OpenAPI docs and type hints.",
        prerequisites=["Python"],
        key_topics=["Pydantic Schema Validation", "Asyncio & Async Endpoints", "Dependency Injection", "OpenAPI/Swagger"],
        project_idea="Create an asynchronous AI inference API service with rate limiting and automated docs.",
        estimated_weeks=2,
    ),
    "REST API": SkillDefinition(
        name="REST API",
        category="Backend Frameworks & APIs",
        patterns=[
            r"\brest\s*apis?\b",
            r"\brestful(?:\s*apis?)?\b",
            r"\brestful\s+web\s+services?\b",
        ],
        tier=2,
        description="Architectural style for designing networked web services communicating via HTTP methods.",
        prerequisites=[],
        key_topics=["HTTP Methods (GET, POST, PUT, DELETE)", "Status Codes", "Resource Routing", "Authentication (JWT/OAuth)"],
        project_idea="Design and document a production-ready CRUD API with Swagger documentation and JWT auth.",
        estimated_weeks=1,
    ),

    # -------------------------------------------------------------
    # 4. Databases & Storage
    # -------------------------------------------------------------
    "SQL": SkillDefinition(
        name="SQL",
        category="Databases & Storage",
        patterns=[r"\bsql\b", r"\bstructured\s+query\s+language\b"],
        tier=1,
        description="Standard language for querying, updating, and managing relational database management systems.",
        prerequisites=[],
        key_topics=["Complex Joins", "Aggregations & Group By", "Indexes & Query Plans", "Transactions (ACID)"],
        project_idea="Perform complex analytics queries and database normalization on a retail sales dataset.",
        estimated_weeks=2,
    ),
    "MySQL": SkillDefinition(
        name="MySQL",
        category="Databases & Storage",
        patterns=[r"\bmysql\b"],
        tier=2,
        description="Popular open-source relational database management system powered by Oracle.",
        prerequisites=["SQL"],
        key_topics=["InnoDB Engine", "Foreign Keys & Constraints", "Stored Procedures", "Replication & Backup"],
        project_idea="Design a normalized relational schema with indexing strategies for high-frequency queries.",
        estimated_weeks=1,
    ),
    "MongoDB": SkillDefinition(
        name="MongoDB",
        category="Databases & Storage",
        patterns=[r"\bmongodb\b", r"\bmongo\b"],
        tier=2,
        description="Leading NoSQL document-oriented database utilizing flexible JSON-like documents.",
        prerequisites=[],
        key_topics=["BSON Document Model", "Aggregation Pipelines", "Indexing & Sharding", "Mongoose/PyMongo ORMs"],
        project_idea="Build a flexible user profile and activity logging datastore using MongoDB and PyMongo.",
        estimated_weeks=2,
    ),

    # -------------------------------------------------------------
    # 5. Data Science, AI & ML
    # -------------------------------------------------------------
    "Machine Learning": SkillDefinition(
        name="Machine Learning",
        category="Data Science & AI",
        patterns=[
            r"\bmachine\s+learning\b",
            r"(?<![a-zA-Z0-9])ml(?![a-zA-Z0-9])",
        ],
        tier=2,
        description="Field of AI focusing on statistical algorithms that learn patterns from data to make predictions.",
        prerequisites=["Python", "NumPy", "Pandas"],
        key_topics=["Supervised & Unsupervised Learning", "Feature Engineering", "Cross-Validation", "Scikit-Learn"],
        project_idea="Build and evaluate an end-to-end customer churn classification pipeline with Scikit-Learn.",
        estimated_weeks=3,
    ),
    "Deep Learning": SkillDefinition(
        name="Deep Learning",
        category="Data Science & AI",
        patterns=[r"\bdeep\s+learning\b"],
        tier=3,
        description="Subset of ML utilizing multi-layered artificial neural networks inspired by human brain architecture.",
        prerequisites=["Machine Learning", "Python"],
        key_topics=["Neural Network Architecture", "Backpropagation & Optimizers", "CNNs & RNNs", "Transfer Learning"],
        project_idea="Train a Convolutional Neural Network (CNN) for image recognition and deploy with ONNX.",
        estimated_weeks=3,
    ),
    "NLP": SkillDefinition(
        name="NLP",
        category="Data Science & AI",
        patterns=[
            r"\bnlp\b",
            r"\bnatural\s+language\s+processing\b",
        ],
        tier=3,
        description="Branch of AI focused on giving computers the ability to understand text and spoken words.",
        prerequisites=["Python", "Machine Learning"],
        key_topics=["Tokenization & Lemmatization", "TF-IDF & Embeddings", "Transformers (BERT/GPT)", "Hugging Face"],
        project_idea="Build an automated sentiment analysis and key entity extractor for customer reviews.",
        estimated_weeks=3,
    ),
    "Generative AI": SkillDefinition(
        name="Generative AI",
        category="Data Science & AI",
        patterns=[
            r"\bgenerative\s+ai\b",
            r"\bgen\s*ai\b",
            r"\bgenai\b",
            r"\bllms?\b",
            r"\blarge\s+language\s+models?\b",
        ],
        tier=3,
        description="Cutting-edge AI capable of creating new text, code, images, and audio using foundation models.",
        prerequisites=["Python", "NLP"],
        key_topics=["Prompt Engineering", "RAG (Retrieval-Augmented Generation)", "Fine-Tuning", "LangChain/LlamaIndex"],
        project_idea="Build a document Q&A assistant with Retrieval-Augmented Generation (RAG) and vector search.",
        estimated_weeks=3,
    ),
    "Pandas": SkillDefinition(
        name="Pandas",
        category="Data Science & AI",
        patterns=[r"\bpandas\b"],
        tier=2,
        description="Fast, powerful, and flexible open source data analysis and manipulation tool for Python.",
        prerequisites=["Python"],
        key_topics=["DataFrames & Series", "Data Cleaning & Imputation", "GroupBy Operations", "Time Series Handling"],
        project_idea="Perform exploratory data analysis (EDA) and data wrangling on a 100,000+ row dataset.",
        estimated_weeks=2,
    ),
    "NumPy": SkillDefinition(
        name="NumPy",
        category="Data Science & AI",
        patterns=[r"\bnumpy\b"],
        tier=2,
        description="Fundamental package for scientific computing with Python providing multi-dimensional array objects.",
        prerequisites=["Python"],
        key_topics=["N-dimensional Arrays", "Broadcasting & Vectorization", "Linear Algebra Operations", "Random Sampling"],
        project_idea="Implement standard machine learning algorithms from scratch using pure NumPy vectorization.",
        estimated_weeks=1,
    ),
    "TensorFlow": SkillDefinition(
        name="TensorFlow",
        category="Data Science & AI",
        patterns=[r"\btensorflow\b", r"(?<![a-zA-Z0-9])tf(?![a-zA-Z0-9])"],
        tier=3,
        description="End-to-end open source platform for machine learning developed by Google.",
        prerequisites=["Python", "Machine Learning"],
        key_topics=["Keras Sequential & Functional APIs", "Custom Training Loops", "TensorBoard", "Model Export/Serving"],
        project_idea="Build and train a neural network using TensorFlow/Keras and visualize training in TensorBoard.",
        estimated_weeks=3,
    ),
    "PyTorch": SkillDefinition(
        name="PyTorch",
        category="Data Science & AI",
        patterns=[r"\bpytorch\b"],
        tier=3,
        description="Dynamic, optimized tensor library for deep learning commonly preferred in modern AI research.",
        prerequisites=["Python", "Machine Learning"],
        key_topics=["Tensors & Autograd", "nn.Module Architecture", "DataLoaders & Datasets", "CUDA GPU Acceleration"],
        project_idea="Build and train a custom PyTorch image classification model using transfer learning.",
        estimated_weeks=3,
    ),

    # -------------------------------------------------------------
    # 6. Data Analytics & BI
    # -------------------------------------------------------------
    "Power BI": SkillDefinition(
        name="Power BI",
        category="Data Analytics & BI",
        patterns=[r"\bpower\s*bi\b", r"\bpowerbi\b"],
        tier=2,
        description="Microsoft business analytics service providing interactive visualizations and BI dashboards.",
        prerequisites=["Excel", "SQL"],
        key_topics=["DAX Formulas", "Power Query Transformations", "Data Modeling (Star Schema)", "Interactive Dashboards"],
        project_idea="Build an interactive executive sales KPI dashboard with custom DAX calculations.",
        estimated_weeks=2,
    ),
    "Excel": SkillDefinition(
        name="Excel",
        category="Data Analytics & BI",
        patterns=[
            r"\bexcel\b",
            r"\bms\s*excel\b",
            r"\bmicrosoft\s*excel\b",
        ],
        tier=1,
        description="Standard spreadsheet application for calculations, pivot tables, data modeling, and business analysis.",
        prerequisites=[],
        key_topics=["XLOOKUP & VLOOKUP", "Pivot Tables & Slicers", "Conditional Formatting", "Power Query Basics"],
        project_idea="Create an automated financial budget and forecasting workbook with dynamic charts and pivot tables.",
        estimated_weeks=1,
    ),

    # -------------------------------------------------------------
    # 7. DevOps & Cloud
    # -------------------------------------------------------------
    "Docker": SkillDefinition(
        name="Docker",
        category="DevOps & Cloud",
        patterns=[r"\bdocker\b"],
        tier=3,
        description="Platform for packaging, shipping, and running applications in lightweight isolated containers.",
        prerequisites=["Linux"],
        key_topics=["Dockerfile Best Practices", "Multi-stage Builds", "Docker Compose", "Volume & Network Management"],
        project_idea="Containerize a multi-service web application (Flask/FastAPI + PostgreSQL + Redis) using Docker Compose.",
        estimated_weeks=2,
    ),
    "AWS": SkillDefinition(
        name="AWS",
        category="DevOps & Cloud",
        patterns=[
            r"\baws\b",
            r"\bamazon\s+web\s+services\b",
        ],
        tier=3,
        description="Comprehensive cloud computing platform offering compute, storage, networking, and managed services.",
        prerequisites=["Linux"],
        key_topics=["EC2, S3 & IAM Security", "AWS Lambda & Serverless", "RDS Databases", "CloudWatch Monitoring"],
        project_idea="Deploy a containerized API on AWS ECS or EC2 with an S3 static asset bucket and CloudFront CDN.",
        estimated_weeks=3,
    ),
    "Linux": SkillDefinition(
        name="Linux",
        category="DevOps & Cloud",
        patterns=[r"\blinux\b", r"\bubuntu\b", r"\bdebian\b", r"\bcentos\b"],
        tier=1,
        description="Dominant operating system kernel powering servers, containers, cloud infrastructure, and developer tools.",
        prerequisites=[],
        key_topics=["Bash Commands & Navigation", "File Permissions & Ownership", "Process Management (systemd)", "SSH & Shell Scripting"],
        project_idea="Write automated Bash scripts for system health checks, log rotation, and automated deployment.",
        estimated_weeks=1,
    ),
    "Git": SkillDefinition(
        name="Git",
        category="DevOps & Cloud",
        patterns=[r"\bgit\b(?!\s*hub)"],
        tier=1,
        description="Distributed version control system tracking source code modifications across software projects.",
        prerequisites=[],
        key_topics=["Branching & Merging", "Rebase & Cherry-pick", "Resolving Conflicts", "Git Flow / Trunk Based Dev"],
        project_idea="Manage complex multi-branch feature workflows, interactive rebases, and merge conflict resolution.",
        estimated_weeks=1,
    ),
    "GitHub": SkillDefinition(
        name="GitHub",
        category="DevOps & Cloud",
        patterns=[r"\bgithub\b"],
        tier=1,
        description="Cloud hosting service for Git repositories featuring pull requests, issues, and CI/CD pipelines.",
        prerequisites=["Git"],
        key_topics=["Pull Requests & Code Reviews", "GitHub Actions CI/CD", "Project Boards", "Release Tagging"],
        project_idea="Configure a complete GitHub Actions CI/CD pipeline running automated tests and linting on PRs.",
        estimated_weeks=1,
    ),

    # -------------------------------------------------------------
    # 8. Computer Science Fundamentals
    # -------------------------------------------------------------
    "Data Structures": SkillDefinition(
        name="Data Structures",
        category="Computer Science Fundamentals",
        patterns=[
            r"\bdata\s+structures?\b",
            r"(?<![a-zA-Z0-9])dsa(?![a-zA-Z0-9])",
        ],
        tier=1,
        description="Organized methods of storing and accessing data efficiently (Arrays, Linked Lists, Trees, Hash Maps).",
        prerequisites=[],
        key_topics=["Arrays & Strings", "Linked Lists", "Stacks & Queues", "Trees & Graphs", "Hash Maps"],
        project_idea="Implement custom LRU Cache and Trie data structures with optimal time complexity.",
        estimated_weeks=3,
    ),
    "Algorithms": SkillDefinition(
        name="Algorithms",
        category="Computer Science Fundamentals",
        patterns=[r"\balgorithms?\b"],
        tier=1,
        description="Step-by-step computational procedures for solving problems, searching, sorting, and optimization.",
        prerequisites=["Data Structures"],
        key_topics=["Big O Complexity Analysis", "Binary Search & Sorting", "Recursion & Backtracking", "Dynamic Programming"],
        project_idea="Solve classic algorithmic challenges (e.g. Dijkstra shortest path, knapsack DP) and benchmark runtime.",
        estimated_weeks=3,
    ),

    # -------------------------------------------------------------
    # 9. Professional & Soft Skills
    # -------------------------------------------------------------
    "Communication Skills": SkillDefinition(
        name="Communication Skills",
        category="Professional & Soft Skills",
        patterns=[
            r"\bcommunication(?:\s+skills?)?\b",
            r"\beffective\s+communication\b",
            r"\bverbal\s+communication\b",
            r"\bwritten\s+communication\b",
            r"\binterpersonal\s+skills?\b",
            r"\bcollaboration\s+skills?\b",
            r"\bteam\s+communication\b",
        ],
        tier=1,
        description="Ability to convey technical ideas clearly, write documentation, actively listen, and collaborate with teams.",
        prerequisites=[],
        key_topics=["Technical Writing", "Cross-Functional Collaboration", "Active Listening", "Presenting Architecture"],
        project_idea="Author comprehensive system architecture design docs (ADRs) and lead a technical walkthrough.",
        estimated_weeks=1,
    ),
}


# =====================================================================
# NLP & Text Normalization Functions
# =====================================================================

def normalize_text(text: str) -> str:
    """
    Applies standard NLP preprocessing and text normalization:
    - Normalizes unicode characters and quotes
    - Converts to lowercase for uniform matching
    - Converts tabs and newlines to whitespace
    - Condenses multiple consecutive spaces
    - Preserves crucial symbols (e.g., C++, .NET, C#)
    """
    if not text:
        return ""

    cleaned = text
    # Replace smart quotes and special typographical punctuation
    for q in ["\u2018", "\u2019", "\u201a", "\u201b", "`", "‘", "’"]:
        cleaned = cleaned.replace(q, "'")
    for dq in ["\u201c", "\u201d", "\u201e", "\u201f", "“", "”"]:
        cleaned = cleaned.replace(dq, '"')
    for dash in ["\u2013", "\u2014", "\u2015", "–", "—"]:
        cleaned = cleaned.replace(dash, "-")

    # Lowercase
    cleaned = cleaned.lower()

    # Replace newlines, tabs, and carriage returns with spaces
    cleaned = re.sub(r"[\r\n\t]+", " ", cleaned)

    # Condense multiple whitespaces
    cleaned = re.sub(r"\s+", " ", cleaned).strip()

    return cleaned


def extract_skills(text: str) -> Dict[str, SkillDefinition]:
    """
    Extracts all recognized skills from the provided text using the skill dictionary.
    Returns a dictionary mapping canonical skill names to their SkillDefinition.
    """
    if not text or not text.strip():
        return {}

    normalized = normalize_text(text)
    detected: Dict[str, SkillDefinition] = {}

    for skill_name, skill_def in SKILL_DICTIONARY.items():
        if skill_def.matches(normalized):
            detected[skill_name] = skill_def

    return detected


def calculate_match(
    resume_skills: Set[str], job_skills: Set[str]
) -> Dict[str, Any]:
    """
    Calculates the keyword match statistics between resume skills and job description skills.

    Rule:
    Match percentage = (Matched Unique Required Skills / Unique Job Skills) * 100
    Handles cases where 0 skills are detected in the job description.

    Returns:
        Dict containing:
        - match_percentage: float (0.0 to 100.0)
        - matched_skills: sorted list of skills found in both
        - missing_skills: sorted list of skills in job description but missing from resume
        - bonus_skills: sorted list of resume skills not required by job description
        - total_job_skills: int
        - total_resume_skills: int
        - match_count: int
        - missing_count: int
        - has_job_skills: bool
    """
    matched = sorted(list(resume_skills.intersection(job_skills)))
    missing = sorted(list(job_skills.difference(resume_skills)))
    bonus = sorted(list(resume_skills.difference(job_skills)))

    total_job = len(job_skills)
    total_resume = len(resume_skills)
    match_count = len(matched)
    missing_count = len(missing)

    if total_job > 0:
        match_percentage = round((match_count / total_job) * 100, 1)
        has_job_skills = True
    else:
        match_percentage = 0.0
        has_job_skills = False

    return {
        "match_percentage": match_percentage,
        "matched_skills": matched,
        "missing_skills": missing,
        "bonus_skills": bonus,
        "total_job_skills": total_job,
        "total_resume_skills": total_resume,
        "match_count": match_count,
        "missing_count": missing_count,
        "has_job_skills": has_job_skills,
    }


def get_all_skills_by_category() -> Dict[str, List[str]]:
    """Returns a dictionary mapping categories to lists of skill names."""
    categories: Dict[str, List[str]] = {}
    for skill_name, skill_def in SKILL_DICTIONARY.items():
        categories.setdefault(skill_def.category, []).append(skill_name)
    for cat in categories:
        categories[cat].sort()
    return categories
