# 🧠 TalentPilot AI  
### Adaptive Onboarding Intelligence Engine  

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red)
![ML](https://img.shields.io/badge/MachineLearning-NLP-green)

---

## 🏆 Overview

TalentPilot AI is an intelligent onboarding platform that personalizes training for candidates based on their resume and a target job description.

Instead of static training, the system dynamically:
- identifies skill gaps  
- generates dependency-aware learning paths  
- creates structured weekly onboarding plans  
- evaluates onboarding efficiency using real metrics  

---

## 🎯 Problem Statement

Traditional onboarding systems are:
- static and one-size-fits-all  
- inefficient for experienced candidates  
- overwhelming for beginners  
- lacking measurable effectiveness  

---

## 💡 Solution

TalentPilot AI introduces adaptive onboarding intelligence by:

- Extracting skills from resumes and job descriptions  
- Identifying missing competencies  
- Generating structured learning roadmaps  
- Creating weekly onboarding plans  
- Providing explainable AI-based reasoning  
- Measuring onboarding efficiency  

---

## ⚙️ System Workflow
Resume + Job Description
↓
Hybrid Skill Extraction
↓
Skill Gap Analysis
↓
Dependency Graph Engine
↓
Adaptive Roadmap Generation
↓
Weekly Plan + Evaluation Dashboard

---

## 🧠 Core Logic (Skill-Gap Analysis)

The system operates in five stages:

### 1. Skill Extraction
- Exact keyword matching  
- Synonym mapping  
- Semantic similarity using Sentence Transformers  

### 2. Skill Gap Analysis
- Compare candidate vs job skills  
- Label skills as:
  - Known  
  - Missing  

### 3. Adaptive Pathing (Key Innovation)
- Graph-based dependency modeling  
- Ensures prerequisite skills before advanced skills  

### 4. Roadmap Generation
- Prioritizes skills based on:
  - importance  
  - level  
  - learning time  

### 5. Evaluation Engine
- Role Match Score  
- Training Compression  
- Modules Skipped  
- System Confidence  

---

## 🧪 Demo Scenario

Python Developer → Machine Learning Engineer  

The system:
- detects existing programming skills  
- identifies missing ML concepts  
- generates a structured roadmap  
- builds a weekly onboarding plan  
- evaluates readiness  

---

## 📊 Key Features

- Resume parsing (Text + PDF)  
- Hybrid skill extraction (Exact + Semantic)  
- Skill gap analysis  
- Dependency-aware roadmap  
- Weekly onboarding plan  
- Learning resource recommendations  
- Explainable AI reasoning  
- Candidate comparison mode  
- Evaluation dashboard  
- Downloadable onboarding report  

---

## 📦 Dependencies

The project relies on the following core dependencies:

- streamlit  
- pandas  
- sentence-transformers  
- networkx  
- matplotlib  
- pypdf  
- torch  
- scikit-learn  

Install all dependencies using:

```bash
pip install -r requirements.txt
```

---


##📊 Datasets Used

- Kaggle Resume Dataset  
- Kaggle Job Description Dataset  
- O*NET Occupational Database  

---

## 📸 Screenshots

### 🏗️ Architecture
![Architecture](assets/architecture.png)

### 💻 Application UI
![Application UI](assets/screenshot.png)

---

## 🛠️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/nishakeerthi/TalentPilot-AI.git
cd TalentPilot-AI
