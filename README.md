# Resume Keyword Analyzer 📄🌐

A modern, responsive web application built with **Streamlit, Python, and NLP-based text processing** that compares resumes against job descriptions, calculates an accurate keyword match percentage, detects missing competencies, and synthesizes a personalized, prioritized learning roadmap.

---

## 📌 Table of Contents
- [Overview](#-overview)
- [Key Features](#-key-features)
- [Supported Skills Matrix (33+ Skills)](#-supported-skills-matrix-33-skills)
- [Project Architecture](#-project-architecture)
- [Installation & Setup](#-installation--setup)
- [How to Run the Web Application](#-how-to-run-the-web-application)
- [How to Use the Web Application](#-how-to-use-the-web-application)
- [Automated Testing](#-automated-testing)
- [How It Works](#-how-it-works)
  - [Document Extraction (PDF, DOCX, TXT)](#document-extraction-pdf-docx-txt)
  - [NLP Normalization & Boundary-Safe Matching](#nlp-normalization--boundary-safe-matching)
  - [Match Score Calculation](#match-score-calculation)
  - [Roadmap Sequencing Algorithm](#roadmap-sequencing-algorithm)
- [ATS Limitations & Transparency](#-ats-limitations--transparency)
- [Publishing to GitHub](#-publishing-to-github)
- [License](#-license)

---

## 🌟 Overview

When applying for software engineering, data science, and technical roles, resumes are frequently scanned by Applicant Tracking Systems (ATS) and recruiters looking for explicit competencies.

**Resume Keyword Analyzer** provides a clean, private, and interactive browser-based dashboard where job seekers can:
1. **Upload their resume** in **PDF**, **DOCX**, or **TXT** format.
2. **Input a target job description** by pasting text or uploading a text file.
3. **Audit their skill alignment** in real time with visual match scores and progress bars.
4. **Discover matched skills, missing gaps, and bonus strengths**.
5. **Receive a structured, phased learning roadmap** with estimated study durations, core topics, and hands-on portfolio project ideas for missing competencies.
6. **Download a complete analysis report** directly from the browser.
7. **Run 100% locally and privately** with zero API keys or external paid subscriptions.

---

## ⚡ Key Features

- **Modern Blue-and-White Theme**: Clean, responsive layout with high-contrast typography, rounded cards, colored pill badges, and a custom dashboard header.
- **Multi-Format Document Parsing**:
  - **PDF**: Robust text extraction via `pypdf` with encrypted file detection.
  - **DOCX**: Complete extraction of paragraphs and table cells via `python-docx`.
  - **TXT**: Safe UTF-8 decoding with Latin-1 fallbacks.
- **Browser-Based Results (No Terminal Printing)**: All metrics, badges, roadmaps, and suggestions are rendered visually in the Streamlit web dashboard. Terminal logs are reserved strictly for server events.
- **Accurate Mathematical Matching**:
  $$\text{Match Percentage} = \left(\frac{\text{Unique Matched Skills}}{\text{Unique Job Description Skills}}\right) \times 100$$
  Gracefully handles edge cases where 0 skills are detected in the job description or resume.
- **Boundary-Safe NLP Extraction**:
  - Regex patterns prevent partial-word false positives (e.g., isolates `C++`, distinguishes `Java` from `JavaScript`, `SQL` from `MySQL`, and recognizes acronyms like `DSA` and `GenAI`).
- **Personalized 3-Phase Upskilling Roadmap**:
  - **Phase 1: Essential Foundations & Prerequisite Tools** (Languages, CS fundamentals).
  - **Phase 2: Core Frameworks, Libraries & Data Layers** (Web frameworks, databases, data tools).
  - **Phase 3: Cloud, Production Systems & Advanced AI** (Docker, AWS, Deep Learning, GenAI).
- **One-Click Sample Testing**: Instant buttons to test with realistic bundled samples (`sample_resume.txt`, `sample_resume.docx`, and `sample_job_description.txt`).
- **Downloadable Reports**: One-click `.txt` report export directly in the browser.

---

## 📊 Supported Skills Matrix (33+ Skills)

The built-in skill dictionary covers **33 core skills** across 9 tech domains:

| Category | Supported Skills |
| :--- | :--- |
| **Programming Languages** | Python, Java, C++, JavaScript |
| **Frontend & Web Development** | HTML, CSS, React, Node.js |
| **Backend Frameworks & APIs** | Flask, Django, FastAPI, REST API |
| **Databases & Storage** | SQL, MySQL, MongoDB |
| **Data Science, AI & ML** | Machine Learning, Deep Learning, NLP, Generative AI, Pandas, NumPy, TensorFlow, PyTorch |
| **Data Analytics & BI** | Power BI, Excel |
| **DevOps & Cloud** | Git, GitHub, Docker, AWS, Linux |
| **Computer Science Fundamentals** | Data Structures, Algorithms |
| **Professional & Soft Skills** | Communication Skills |

---

## 📂 Project Architecture

```text
resume-keyword-analyzer/
│
├── app.py                           # Streamlit web application & UI dashboard
├── skill_extractor.py               # NLP normalization, regex dictionary & matching logic
├── roadmap.py                       # Prioritized upskilling roadmap & tips generator
├── test_analyzer.py                 # Automated unit test suite (17 tests)
├── requirements.txt                 # Dependencies: streamlit, pypdf, python-docx
├── .gitignore                       # Git exclusions for Python & Streamlit artifacts
├── README.md                        # Documentation & setup guide
│
└── samples/
    ├── sample_resume.txt            # Candidate sample resume (Plain text)
    ├── sample_resume.docx           # Candidate sample resume (Microsoft Word)
    └── sample_job_description.txt   # Target job description (Plain text)
```

---

## 🚀 Installation & Setup

### 1. Prerequisites
- Python **3.8** or higher (tested on Python 3.12).
- Pip package manager.

### 2. Clone the Repository
```bash
git clone https://github.com/your-username/resume-keyword-analyzer.git
cd resume-keyword-analyzer
```

### 3. Install Dependencies
Install all required libraries via `requirements.txt`:

```bash
pip install -r requirements.txt
```

**Required packages:**
- `streamlit>=1.35.0`
- `pypdf>=4.2.0`
- `python-docx>=1.1.0`

---

## 🌐 How to Run the Web Application

Launch the application using Streamlit:

```bash
streamlit run app.py
```

Streamlit will start the local development server and automatically open the application in your browser at:

```text
http://localhost:8501
```

*(If the browser doesn't open automatically, open your browser and navigate to `http://localhost:8501`).*

---

## 🖥️ How to Use the Web Application

1. **Upload Resume**:
   - In **Step 1 (Left Card)**, drag-and-drop or upload your resume file (`.pdf`, `.docx`, or `.txt`).
   - *Quick Test option*: You can also check the box *"💡 Or use built-in sample candidate resume"* to load Alex Morgan's pre-configured resume.
2. **Provide Job Description**:
   - In **Step 2 (Right Card)**, choose either:
     - **✍️ Paste Job Description**: Paste the target job posting into the text box (or check *"💡 Or load built-in sample job description"*).
     - **📂 Upload TXT File**: Upload a `.txt` file containing the job description.
3. **Analyze Resume**:
   - Click the prominent **"🚀 Analyze Resume & Generate Roadmap"** button.
4. **Review Results in the Browser**:
   - **Overall Match Score**: Visual percentage, progress bar, and candidate rating badge.
   - **Competency Breakdown**: Color-coded badges for **Matched Skills** (green), **Missing Gaps** (red), and **Bonus Strengths** (blue).
   - **Personalized Learning Roadmap**: Phase-by-phase curriculum showing estimated weeks, core concepts, and portfolio project suggestions for every missing skill.
   - **Strategic Resume Suggestions**: Proven strategies using the STAR framework, impact metrics, and adjacent skill positioning.
   - **Download Report**: Click *"📥 Download Complete Analysis Report (.txt)"* to save a copy to your computer.

---

## 🧪 Automated Testing

A comprehensive test suite of **17 unit tests** validates the skill dictionary, boundary matching, mathematical accuracy, roadmap sequencing, and document extraction:

```bash
python test_analyzer.py
```

Or run using Python's `unittest` runner:

```bash
python -m unittest -v test_analyzer.py
```

---

## 🧠 How It Works

### Document Extraction (PDF, DOCX, TXT)
- **PDF**: Uses `pypdf.PdfReader` to iterate through pages and extract textual streams safely. Decrypts empty-password PDFs and warns on password-protected or image-only scanned documents.
- **DOCX**: Uses `python-docx` to extract text from both body paragraphs and table cells.
- **TXT**: Reads raw bytes with UTF-8 decoding and falls back to Latin-1 with replacement characters.

### NLP Normalization & Boundary-Safe Matching
1. **Normalization (`normalize_text`)**:
   - Standardizes smart quotation marks (`‘`, `’`, `“`, `”`) to standard ASCII quotes.
   - Replaces en-dashes and em-dashes (`–`, `—`) with hyphens.
   - Lowercases all characters and condenses multi-line whitespace.
2. **Boundary Safeguards**:
   - Prevents partial-word false positives: `\bjava\b(?!\s*script)` ensures `Java` is never falsely detected inside `JavaScript`.
   - Handles special characters: `C++` uses `(?<![a-zA-Z0-9#+])c\+\+(?![a-zA-Z0-9#+])`.
   - Distinguishes `SQL` from `MySQL` and `PostgreSQL`.
   - Resolves industry aliases (`GenAI`, `LLMs`, `DSA`) to canonical skill names.

### Match Score Calculation
$$\text{Match Percentage} = \begin{cases} 
\left(\frac{|\text{Resume Skills} \cap \text{Job Skills}|}{|\text{Job Skills}|}\right) \times 100 & \text{if } |\text{Job Skills}| > 0 \\
0.0\% & \text{if } |\text{Job Skills}| = 0 
\end{cases}$$

### Roadmap Sequencing Algorithm
Missing skills are dynamically categorized into three progressive learning tiers:
- **Tier 1 (Foundations)**: Programming languages, core query languages, and algorithms.
- **Tier 2 (Core Tech)**: Frameworks, ORMs, document stores, and data analysis packages.
- **Tier 3 (Cloud & Advanced AI)**: Containerization, cloud infrastructure, and foundation models.

If a candidate already possesses prerequisite skills (such as knowing Python when learning FastAPI), the prerequisite warning is automatically resolved.

---

## ⚠️ ATS Limitations & Transparency

- **Keyword Matching vs. Commercial ATS**: Commercial ATS platforms (e.g., Workday, Greenhouse, Taleo) and human recruiters evaluate complete career trajectories, chronological experience, job title seniority, accredited degrees, and contextual business impact.
- **Heuristic Estimate**: The match score is an objective keyword-based heuristic designed to uncover technical blind spots, not an official ATS ranking.
- **Best Practice**: Always weave technical keywords into contextual accomplishment statements using the **STAR method** (Situation, Task, Action, Result) rather than merely appending keyword lists.

---

## 🐙 Publishing to GitHub

To push this project to your GitHub profile:

```bash
# 1. Initialize git
git init

# 2. Stage all files
git add .

# 3. Create initial commit
git commit -m "feat: Add Streamlit web application for Resume Keyword Analyzer"

# 4. Connect to your GitHub repository
git remote add origin https://github.com/<YOUR_GITHUB_USERNAME>/resume-keyword-analyzer.git

# 5. Push to main branch
git branch -M main
git push -u origin main
```

---

## 📄 License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT). You are free to modify, expand, and utilize it for personal or professional projects.
