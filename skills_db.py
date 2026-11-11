from data_loader import load_kaggle_skills, load_onet_skills

kaggle_skills = load_kaggle_skills()
onet_skills = load_onet_skills()

BASE_SKILLS = {
    "python": {
        "time": 10,
        "level": "Beginner",
        "priority": 5,
        "courses": [
            "Python for Everybody (Coursera)",
            "Automate the Boring Stuff with Python (Book/YouTube)"
        ]
    },
    "sql": {
        "time": 8,
        "level": "Beginner",
        "priority": 4,
        "courses": [
            "SQL for Data Analysis (Coursera)",
            "Intro to SQL (Kaggle Learn)"
        ]
    },
    "statistics": {
        "time": 12,
        "level": "Intermediate",
        "priority": 5,
        "courses": [
            "Statistics Fundamentals (Coursera)",
            "Probability and Statistics Basics (YouTube)"
        ]
    },
    "machine learning": {
        "time": 20,
        "level": "Intermediate",
        "priority": 5,
        "courses": [
            "Machine Learning by Andrew Ng (Coursera)",
            "Intro to Machine Learning (Kaggle Learn)"
        ]
    },
    "deep learning": {
        "time": 25,
        "level": "Advanced",
        "priority": 4,
        "courses": [
            "Deep Learning Specialization (Coursera)",
            "Practical Deep Learning for Coders (YouTube)"
        ]
    },
    "data analysis": {
        "time": 15,
        "level": "Intermediate",
        "priority": 4,
        "courses": [
            "Data Analysis with Python (Coursera)",
            "Pandas for Data Analysis (YouTube)"
        ]
    },
    "communication": {
        "time": 5,
        "level": "Beginner",
        "priority": 3,
        "courses": [
            "Business Communication Basics (Coursera)",
            "Workplace Communication Skills (Internal Module)"
        ]
    },
    "teamwork": {
        "time": 5,
        "level": "Beginner",
        "priority": 2,
        "courses": [
            "Team Collaboration Essentials (Coursera)",
            "Effective Teamwork Skills (Internal Module)"
        ]
    },
    "pandas": {
        "time": 8,
        "level": "Intermediate",
        "priority": 3,
        "courses": [
            "Pandas Foundations (YouTube)",
            "Data Wrangling with Pandas (Kaggle Learn)"
        ]
    },
    "excel": {
        "time": 6,
        "level": "Beginner",
        "priority": 2,
        "courses": [
            "Excel Essentials (Coursera)",
            "Data Analysis in Excel (YouTube)"
        ]
    },
}

SKILLS = {}

for skill in kaggle_skills:
    SKILLS[skill] = {
        "time": 10,
        "level": "Intermediate",
        "priority": 3,
        "courses": [
            f"{skill.title()} Foundations (Coursera)",
            f"{skill.title()} Practice Track (YouTube)"
        ]
    }

for skill, importance in onet_skills.items():
    SKILLS[skill] = {
        "time": max(5, int(importance * 5)),
        "level": "Intermediate",
        "priority": min(5, max(1, int(round(importance)))),
        "courses": [
            f"{skill.title()} Foundations (Coursera)",
            f"{skill.title()} Applied Learning (Internal Module)"
        ]
    }

SKILLS.update(BASE_SKILLS)

SKILL_GRAPH = {
    "machine learning": ["python", "statistics"],
    "deep learning": ["machine learning"],
    "data analysis": ["python", "excel"],
    "pandas": ["python"],
    "sql": [],
    "python": [],
    "statistics": [],
    "communication": [],
    "teamwork": [],
    "excel": []
}

SKILL_SYNONYMS = {
    "machine learning": ["ml", "machine learning", "ml engineer", "predictive modeling"],
    "deep learning": ["deep learning", "neural networks", "cnn", "rnn"],
    "python": ["python", "python programming"],
    "sql": ["sql", "mysql", "postgresql", "database querying"],
    "statistics": ["statistics", "probability", "statistical analysis"],
    "data analysis": ["data analysis", "data analytics", "analytics"],
    "communication": ["communication", "presentation", "verbal communication"],
    "teamwork": ["teamwork", "collaboration", "team collaboration"],
    "pandas": ["pandas"],
    "excel": ["excel", "ms excel", "microsoft excel"]
}