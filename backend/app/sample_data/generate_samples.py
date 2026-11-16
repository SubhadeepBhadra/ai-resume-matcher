"""
Synthetic Resume & Job Description Generator.
Generates realistic PDF and DOCX candidate resumes and sample JDs for demonstration.
"""

import os
from typing import List, Dict, Any
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from docx import Document
from docx.shared import Inches, Pt, RGBColor


SAMPLE_JDS = [
    {
        "id": "jd-1",
        "title": "Senior Full Stack Java Engineer",
        "category": "Backend / Enterprise",
        "min_experience_years": 4.0,
        "text": """Job Title: Senior Full Stack Java Engineer
Experience Required: Minimum 4+ years of industry experience
Location: Remote / Hybrid
Education: Bachelor's or Master's Degree in Computer Science or related field

Job Overview:
We are seeking an experienced Senior Full Stack Java Engineer to architect, build, and scale our enterprise microservices and customer-facing web applications. You will collaborate with cross-functional teams to deliver secure, resilient cloud solutions.

Key Responsibilities:
- Design and develop robust backend microservices using Java and Spring Boot.
- Build clean, responsive user interfaces using React, TypeScript, and modern frontend tools.
- Design database schemas and write optimized queries for PostgreSQL and MySQL.
- Deploy and containerize applications with Docker and manage workloads on AWS cloud infrastructure.
- Implement CI/CD pipelines, automated testing (JUnit, Mockito), and adhere to Agile/Scrum best practices.
- Collaborate on system design, RESTful API specifications, and code reviews.

Required Technical Skills:
- Java (Java 11 / 17 / 21)
- Spring Boot & Spring Framework
- SQL / PostgreSQL / MySQL
- React / JavaScript / TypeScript
- RESTful APIs & Microservices Architecture
- Docker & AWS Cloud Services
- Git & CI/CD Pipelines
- Agile / Scrum Methodology
"""
    },
    {
        "id": "jd-2",
        "title": "AI & NLP Software Engineer (Python / FastAPI)",
        "category": "AI / Machine Learning",
        "min_experience_years": 3.0,
        "text": """Job Title: AI & NLP Software Engineer
Experience Required: 3+ years of professional experience in Python & Machine Learning
Location: Remote
Education: Bachelor's or Master's in CS, AI, Data Science, or equivalent

Job Overview:
Join our AI Engineering team to build cutting-edge semantic search, document understanding, and resume intelligence systems. You will develop production AI pipelines combining transformer embeddings, LLM orchestration, and scalable REST APIs.

Key Responsibilities:
- Build high-throughput AI microservices with Python and FastAPI.
- Implement vector search, embedding models, and semantic similarity using Sentence Transformers and Hugging Face.
- Perform entity extraction, text normalization, and NLP pipeline modeling using spaCy and Scikit-Learn.
- Develop Retrieval-Augmented Generation (RAG) workflows and integrate Vector Databases (Chroma, Pinecone, or Qdrant).
- Containerize and deploy AI models with Docker on Cloud infrastructure (AWS/GCP).
- Work with product engineers to optimize inference latency, test accuracy, and monitor model performance.

Required Technical Skills:
- Python (Python 3.10+)
- FastAPI / RESTful APIs
- Sentence Transformers / spaCy / Hugging Face
- Scikit-Learn / PyTorch / Machine Learning
- Retrieval-Augmented Generation (RAG) & Vector Databases
- Docker & Git
- Natural Language Processing (NLP) & Large Language Models (LLMs)
"""
    },
    {
        "id": "jd-3",
        "title": "Senior Frontend React Engineer",
        "category": "Frontend Web",
        "min_experience_years": 4.0,
        "text": """Job Title: Senior Frontend React Engineer
Experience Required: 4+ years of dedicated web frontend engineering
Location: Hybrid
Education: Bachelor's Degree in Computer Science or equivalent practical experience

Job Overview:
We are looking for a Senior React Engineer to lead the development of intuitive, high-performance dashboards, analytics interfaces, and customer web applications.

Key Responsibilities:
- Build modular, maintainable UI components using React, Next.js, and TypeScript.
- Implement responsive modern styling using Tailwind CSS and CSS3.
- Manage complex client-side state using Redux Toolkit or React Query.
- Connect with backend microservices via RESTful APIs and GraphQL.
- Ensure cross-browser accessibility, responsive UX, and unit test coverage with Jest and React Testing Library.
- Mentor junior engineers and participate in architecture discussions.

Required Technical Skills:
- React (React 18+) & Next.js
- TypeScript & JavaScript (ES6+)
- Tailwind CSS & HTML/CSS
- Redux / State Management
- RESTful APIs & GraphQL
- Git & CI/CD
- Unit Testing / TDD (Jest / Cypress)
"""
    }
]


CANDIDATES = [
    {
        "name": "Sarah Jenkins",
        "format": "pdf",
        "title": "Senior Full Stack Java Developer",
        "experience_years": 6.0,
        "email": "sarah.jenkins@example.com",
        "phone": "(555) 234-5678",
        "linkedin": "linkedin.com/in/sarahjenkins-tech",
        "github": "github.com/sarahjenkins-dev",
        "education": "Master of Science in Computer Science, Georgia Tech",
        "summary": "Accomplished Full Stack Java Developer with 6+ years of experience architecting scalable distributed microservices, enterprise RESTful APIs, and responsive React frontend applications. Proven expertise in Spring Boot, PostgreSQL, Docker, and AWS.",
        "skills": ["Java", "Spring Boot", "SQL", "PostgreSQL", "React", "TypeScript", "RESTful APIs", "Microservices", "Docker", "AWS", "Git", "CI/CD", "Agile / Scrum", "Unit Testing / TDD"],
        "history": [
            ("Lead Software Engineer", "Apex Cloud Solutions", "2021 - Present", "Led migration of monolithic core systems to 15+ Spring Boot microservices on AWS ECS. Designed responsive React dashboards and optimized PostgreSQL database queries, reducing response times by 35%."),
            ("Full Stack Developer", "Nexient Digital", "2018 - 2021", "Engineered secure RESTful APIs using Java 11 and Spring MVC. Integrated Docker container pipelines and contributed to frontend React/TypeScript UI modules.")
        ]
    },
    {
        "name": "Marcus Chen",
        "format": "docx",
        "title": "Backend Java Engineer",
        "experience_years": 4.5,
        "email": "marcus.chen@example.com",
        "phone": "(555) 345-6789",
        "linkedin": "linkedin.com/in/marcus-chen-code",
        "github": "github.com/marcuschen-dev",
        "education": "Bachelor of Science in Computer Engineering, University of Illinois",
        "summary": "Backend Software Engineer with 4.5 years of experience developing enterprise Java services, high-throughput REST APIs, and database solutions using Spring Boot, SQL, and MySQL.",
        "skills": ["Java", "Spring Boot", "SQL", "MySQL", "Redis", "RESTful APIs", "Microservices", "Git", "Docker", "Agile / Scrum"],
        "history": [
            ("Backend Java Engineer", "OmniSoft Systems", "2020 - Present", "Designed transactional REST services using Java and Spring Boot. Implemented Redis distributed caching and MySQL schema indexing to support 100k daily active users."),
            ("Junior Software Engineer", "TechMatrix Inc.", "2019 - 2020", "Maintained enterprise Java codebase, wrote JUnit test suites, and created automated SQL data migration scripts.")
        ]
    },
    {
        "name": "Priya Sharma",
        "format": "pdf",
        "title": "Full Stack Software Developer",
        "experience_years": 3.0,
        "email": "priya.sharma@example.com",
        "phone": "(555) 456-7890",
        "linkedin": "linkedin.com/in/priyasharma-dev",
        "github": "github.com/priyasharma-code",
        "education": "Bachelor of Technology in Information Technology",
        "summary": "Full Stack Developer with 3 years of hands-on experience in Java, SQL databases, and React frontend development. Passionate about building user-friendly web applications and clean code.",
        "skills": ["Java", "SQL", "React", "JavaScript", "HTML/CSS", "PostgreSQL", "Git", "Agile / Scrum", "RESTful APIs"],
        "history": [
            ("Full Stack Developer", "FinTech Labs", "2021 - Present", "Developed customer onboarding web portals using React and Java backend services. Wrote complex SQL stored procedures and integrated REST endpoints."),
            ("Associate Developer", "CodeCraft", "2020 - 2021", "Assisted in frontend JavaScript bug fixes and automated test suite creation using Jest and JUnit.")
        ]
    },
    {
        "name": "David Kim",
        "format": "pdf",
        "title": "Lead AI & NLP Research Engineer",
        "experience_years": 7.0,
        "email": "david.kim@example.com",
        "phone": "(555) 567-8901",
        "linkedin": "linkedin.com/in/davidkim-ai",
        "github": "github.com/davidkim-nlp",
        "education": "Master of Science in Artificial Intelligence, Carnegie Mellon University",
        "summary": "Senior AI & NLP Engineer with 7+ years of experience engineering state-of-the-art transformer pipelines, semantic search engines, and scalable FastAPI microservices. Specialized in Sentence Transformers, spaCy, PyTorch, and RAG architectures.",
        "skills": ["Python", "FastAPI", "Sentence Transformers", "spaCy", "PyTorch", "Hugging Face", "Natural Language Processing (NLP)", "Large Language Models (LLMs)", "Retrieval-Augmented Generation (RAG)", "Vector Databases", "Scikit-Learn", "Docker", "AWS", "Git"],
        "history": [
            ("Lead AI Engineer", "Cognitive Horizon Labs", "2021 - Present", "Spearheaded semantic document search engine using Sentence Transformers (all-MiniLM-L6-v2) and Qdrant vector database. Built async FastAPI microservices handling 2M inference requests daily."),
            ("Machine Learning Engineer", "Synthetix AI", "2017 - 2021", "Built domain-specific named entity recognition (NER) pipelines with spaCy and fine-tuned BERT models in PyTorch. Automated model deployment with Docker on AWS.")
        ]
    },
    {
        "name": "Elena Rostova",
        "format": "docx",
        "title": "Machine Learning & Python Engineer",
        "experience_years": 4.0,
        "email": "elena.rostova@example.com",
        "phone": "(555) 678-9012",
        "linkedin": "linkedin.com/in/elenarostova",
        "github": "github.com/elena-ml",
        "education": "Bachelor of Science in Applied Mathematics & Statistics",
        "summary": "Data Scientist and Python Engineer with 4 years of experience applying Scikit-Learn, TensorFlow, and NLP algorithms to solve predictive analytics and text categorization problems.",
        "skills": ["Python", "Machine Learning", "Scikit-Learn", "TensorFlow", "FastAPI", "Natural Language Processing (NLP)", "SQL", "PostgreSQL", "Data Science", "Git", "Docker"],
        "history": [
            ("Machine Learning Engineer", "DataPulse Analytics", "2020 - Present", "Trained classification and regression models using Scikit-Learn and PyTorch. Exposed inference APIs using FastAPI and managed PostgreSQL training stores."),
            ("Data Analyst", "Stratix Insights", "2019 - 2020", "Engineered feature pipelines in Python with Pandas/NumPy and built automated reporting dashboards.")
        ]
    },
    {
        "name": "Alex Rivera",
        "format": "pdf",
        "title": "Senior Frontend React Architect",
        "experience_years": 5.5,
        "email": "alex.rivera@example.com",
        "phone": "(555) 789-0123",
        "linkedin": "linkedin.com/in/alexrivera-ui",
        "github": "github.com/alexrivera-frontend",
        "education": "Bachelor of Science in Computer Science, UC Berkeley",
        "summary": "Senior Frontend Engineer with 5.5 years specializing in modern React ecosystem, Next.js, TypeScript, and Tailwind CSS. Track record of creating polished, accessible, and performant web applications.",
        "skills": ["React", "TypeScript", "JavaScript", "Next.js", "Redux", "Tailwind CSS", "HTML/CSS", "RESTful APIs", "GraphQL", "Unit Testing / TDD", "Git", "CI/CD"],
        "history": [
            ("Senior Frontend Developer", "PixelFlow Studio", "2021 - Present", "Architected enterprise React 18 design system and multi-tenant Next.js web application. Integrated Tailwind CSS and Redux Toolkit, decreasing bundle size by 40%."),
            ("Frontend Developer", "WebSphere Media", "2018 - 2021", "Constructed interactive web dashboards in React and TypeScript. Collaborated with UX designers to achieve WCAG AAA accessibility compliance.")
        ]
    },
    {
        "name": "Michael Torres",
        "format": "docx",
        "title": "Cloud DevOps & Platform Engineer",
        "experience_years": 5.0,
        "email": "michael.torres@example.com",
        "phone": "(555) 890-1234",
        "linkedin": "linkedin.com/in/michaeltorres-devops",
        "github": "github.com/mtorres-cloud",
        "education": "Bachelor of Science in Systems Engineering",
        "summary": "DevOps Engineer with 5 years experience managing Kubernetes clusters, AWS cloud infrastructure, Terraform IaC, and continuous integration/continuous delivery pipelines.",
        "skills": ["AWS", "Kubernetes", "Docker", "Terraform", "CI/CD", "Linux", "Bash/Shell", "Python", "Git", "System Design"],
        "history": [
            ("DevOps Lead", "CloudScale Infra", "2021 - Present", "Provisioned multi-region AWS EKS Kubernetes clusters via Terraform. Maintained GitHub Actions CI/CD workflows and automated zero-downtime rolling deployments."),
            ("Cloud Engineer", "ServerNest", "2019 - 2021", "Managed Linux servers, Docker containers, and CloudWatch alerting infrastructure.")
        ]
    },
    {
        "name": "Ananya Patel",
        "format": "pdf",
        "title": "Junior Backend Developer",
        "experience_years": 1.5,
        "email": "ananya.patel@example.com",
        "phone": "(555) 901-2345",
        "linkedin": "linkedin.com/in/ananyapatel-tech",
        "github": "github.com/ananya-dev",
        "education": "Bachelor of Science in Computer Science, Class of 2023",
        "summary": "Motivated Junior Backend Developer with 1.5 years of industry experience working with Java, Spring Boot, and relational databases. Eager to expand skills in enterprise microservices.",
        "skills": ["Java", "Spring Boot", "SQL", "MySQL", "Git", "RESTful APIs"],
        "history": [
            ("Junior Software Engineer", "TechStars Inc", "2023 - Present", "Developed REST APIs in Spring Boot for internal HR tools. Wrote SQL queries and participated in daily Scrum standups.")
        ]
    },
    {
        "name": "Brian O'Connor",
        "format": "docx",
        "title": "Principal Data Platform Engineer",
        "experience_years": 8.0,
        "email": "brian.oconnor@example.com",
        "phone": "(555) 012-3456",
        "linkedin": "linkedin.com/in/brianoconnor-data",
        "github": "github.com/brian-bigdata",
        "education": "Master of Science in Software Engineering, MIT",
        "summary": "Principal Data Engineer with 8+ years experience designing real-time distributed data pipelines, ETL architectures, Apache Spark clusters, and Kafka streaming applications.",
        "skills": ["Python", "SQL", "ETL / Data Pipelines", "Kafka / Messaging", "PostgreSQL", "Docker", "AWS", "System Design", "Microservices", "Git"],
        "history": [
            ("Principal Data Engineer", "StreamData Systems", "2019 - Present", "Designed petabyte-scale Kafka and Spark streaming pipelines. Implemented automated data quality checks and managed AWS data lake."),
            ("Senior Data Engineer", "Enterprise Data Corp", "2016 - 2019", "Built resilient ETL pipelines using Python and SQL. Administered distributed PostgreSQL clusters.")
        ]
    },
    {
        "name": "Emily Watson",
        "format": "pdf",
        "title": "Data Analyst & Business Intelligence Specialist",
        "experience_years": 3.0,
        "email": "emily.watson@example.com",
        "phone": "(555) 123-4567",
        "linkedin": "linkedin.com/in/emilywatson-bi",
        "github": "github.com/emily-analytics",
        "education": "Bachelor of Science in Business Information Systems",
        "summary": "Data Analyst with 3 years of experience transforming complex datasets into actionable business insights using SQL, Python, and statistical modeling.",
        "skills": ["SQL", "Python", "Data Science", "PostgreSQL", "Agile / Scrum"],
        "history": [
            ("Business Intelligence Analyst", "MetricWave Analytics", "2021 - Present", "Created SQL reports and business intelligence dashboards for executive teams. Utilized Python for data cleaning and statistical variance analysis.")
        ]
    },
    {
        "name": "Carlos Gomez",
        "format": "docx",
        "title": "QA Automation & Test Engineer",
        "experience_years": 4.0,
        "email": "carlos.gomez@example.com",
        "phone": "(555) 234-8901",
        "linkedin": "linkedin.com/in/carlosgomez-qa",
        "github": "github.com/carlos-tests",
        "education": "Bachelor of Engineering in Computer Systems",
        "summary": "QA Automation Engineer with 4 years experience creating automated integration and end-to-end testing frameworks using Python, Selenium, PyTest, and CI/CD tools.",
        "skills": ["Python", "Unit Testing / TDD", "CI/CD", "Git", "SQL", "RESTful APIs", "Docker"],
        "history": [
            ("Senior QA Automation Engineer", "ReliableCode Ltd", "2020 - Present", "Created regression test suites in Python. Integrated automated testing into GitHub Actions CI pipelines, catching 95% of regressions before staging.")
        ]
    },
    {
        "name": "Thomas Wright",
        "format": "pdf",
        "title": "Web Developer (PHP / WordPress)",
        "experience_years": 5.0,
        "email": "thomas.wright@example.com",
        "phone": "(555) 345-0123",
        "linkedin": "linkedin.com/in/thomaswright-web",
        "github": "github.com/twright-web",
        "education": "Associate Degree in Web Development",
        "summary": "Web Developer with 5 years experience creating custom websites, themes, and eCommerce plugins using PHP, MySQL, JavaScript, and HTML/CSS.",
        "skills": ["PHP", "MySQL", "JavaScript", "HTML/CSS", "Git"],
        "history": [
            ("Web Developer", "Creative Agency Pro", "2019 - Present", "Developed custom client websites and CMS portals with PHP and MySQL. Managed site maintenance and responsive CSS layout design.")
        ]
    }
]


def create_pdf_resume(data: Dict[str, Any], filepath: str):
    """Generates a professional-looking PDF resume using ReportLab."""
    doc = SimpleDocTemplate(
        filepath,
        pagesize=letter,
        rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40
    )
    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'ResumeTitle',
        parent=styles['Heading1'],
        fontSize=20,
        leading=24,
        textColor=colors.HexColor('#1E293B'),
        fontName='Helvetica-Bold'
    )
    subtitle_style = ParagraphStyle(
        'ResumeSubtitle',
        parent=styles['Normal'],
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#2563EB'),
        fontName='Helvetica-Bold'
    )
    contact_style = ParagraphStyle(
        'ResumeContact',
        parent=styles['Normal'],
        fontSize=9,
        leading=13,
        textColor=colors.HexColor('#64748B')
    )
    heading_style = ParagraphStyle(
        'ResumeSectionHeading',
        parent=styles['Heading2'],
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#0F172A'),
        fontName='Helvetica-Bold',
        spaceBefore=10,
        spaceAfter=4
    )
    body_style = ParagraphStyle(
        'ResumeBody',
        parent=styles['Normal'],
        fontSize=9.5,
        leading=14,
        textColor=colors.HexColor('#334155')
    )
    bullet_style = ParagraphStyle(
        'ResumeBullet',
        parent=styles['Normal'],
        fontSize=9,
        leading=13,
        textColor=colors.HexColor('#475569'),
        leftIndent=12
    )

    story = []

    # Name and Title
    story.append(Paragraph(data["name"], title_style))
    story.append(Paragraph(f"{data['title']} • {data['experience_years']} Years Experience", subtitle_style))
    contact_line = f"Email: {data['email']} | Phone: {data['phone']} | LinkedIn: {data['linkedin']} | GitHub: {data['github']}"
    story.append(Paragraph(contact_line, contact_style))
    story.append(Spacer(1, 10))

    # Professional Summary
    story.append(Paragraph("PROFESSIONAL SUMMARY", heading_style))
    story.append(Paragraph(data["summary"], body_style))
    story.append(Spacer(1, 8))

    # Skills
    story.append(Paragraph("TECHNICAL SKILLS", heading_style))
    skills_str = " • ".join(data["skills"])
    story.append(Paragraph(skills_str, body_style))
    story.append(Spacer(1, 8))

    # Experience
    story.append(Paragraph("WORK EXPERIENCE", heading_style))
    for role, company, dates, desc in data["history"]:
        job_header = f"<b>{role}</b> — <i>{company}</i> ({dates})"
        story.append(Paragraph(job_header, body_style))
        story.append(Paragraph(f"• {desc}", bullet_style))
        story.append(Spacer(1, 4))

    # Education
    story.append(Paragraph("EDUCATION", heading_style))
    story.append(Paragraph(data["education"], body_style))

    doc.build(story)


def create_docx_resume(data: Dict[str, Any], filepath: str):
    """Generates a professional DOCX resume using python-docx."""
    doc = Document()
    
    # Title / Name
    name_p = doc.add_paragraph()
    name_run = name_p.add_run(data["name"])
    name_run.font.size = Pt(20)
    name_run.font.bold = True
    name_run.font.color.rgb = RGBColor(30, 41, 59)

    # Subtitle
    sub_p = doc.add_paragraph()
    sub_run = sub_p.add_run(f"{data['title']} • {data['experience_years']} Years Experience")
    sub_run.font.size = Pt(12)
    sub_run.font.bold = True
    sub_run.font.color.rgb = RGBColor(37, 99, 235)

    # Contact
    contact_p = doc.add_paragraph()
    contact_run = contact_p.add_run(
        f"Email: {data['email']} | Phone: {data['phone']} | LinkedIn: {data['linkedin']} | GitHub: {data['github']}"
    )
    contact_run.font.size = Pt(9)
    contact_run.font.color.rgb = RGBColor(100, 116, 139)

    # Summary
    doc.add_heading("PROFESSIONAL SUMMARY", level=2)
    doc.add_paragraph(data["summary"])

    # Skills
    doc.add_heading("TECHNICAL SKILLS", level=2)
    doc.add_paragraph(" • ".join(data["skills"]))

    # Experience
    doc.add_heading("WORK EXPERIENCE", level=2)
    for role, company, dates, desc in data["history"]:
        p = doc.add_paragraph()
        r1 = p.add_run(f"{role} — {company} ({dates})\n")
        r1.bold = True
        p.add_run(f"• {desc}")

    # Education
    doc.add_heading("EDUCATION", level=2)
    doc.add_paragraph(data["education"])

    doc.save(filepath)


def generate_all_samples(output_dir: str):
    """Generates both PDF and DOCX files in target directory."""
    os.makedirs(output_dir, exist_ok=True)
    generated_files = []

    for c in CANDIDATES:
        fmt = c["format"]
        clean_name = c["name"].replace(" ", "_").replace("'", "")
        filename = f"{clean_name}_Resume.{fmt}"
        target_path = os.path.join(output_dir, filename)

        if fmt == "pdf":
            create_pdf_resume(c, target_path)
        else:
            create_docx_resume(c, target_path)

        generated_files.append({
            "name": c["name"],
            "filename": filename,
            "filepath": target_path,
            "format": fmt
        })

    return generated_files


if __name__ == "__main__":
    import sys
    out_dir = sys.argv[1] if len(sys.argv) > 1 else "./sample_resumes"
    files = generate_all_samples(out_dir)
    print(f"Successfully generated {len(files)} synthetic resumes in '{out_dir}'.")
