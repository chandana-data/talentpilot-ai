import pandas as pd


def load_kaggle_skills():
    try:
        df = pd.read_csv("jobs.csv")
        skills = set()

        for col in df.columns:
            if "skill" in col.lower():
                for row in df[col].dropna():
                    for skill in str(row).split(","):
                        skill = skill.strip().lower()
                        if len(skill) > 2:
                            skills.add(skill)

        return list(skills)

    except Exception:
        return []


def load_onet_skills():
    try:
        df = pd.read_csv("Skills.txt", sep="\t")

        skill_data = {}

        for _, row in df.iterrows():
            skill = str(row["Element Name"]).strip().lower()
            importance = row["Data Value"]

            if skill and skill not in skill_data:
                try:
                    skill_data[skill] = float(importance)
                except Exception:
                    continue

        return skill_data

    except Exception:
        return {}