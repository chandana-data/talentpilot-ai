from pypdf import PdfReader
from sentence_transformers import SentenceTransformer, util
import networkx as nx

from skills_db import SKILLS, SKILL_GRAPH, SKILL_SYNONYMS

model = SentenceTransformer("all-MiniLM-L6-v2")


def extract_text_from_pdf(uploaded_file):
    try:
        reader = PdfReader(uploaded_file)
        text = ""

        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

        return text.strip()
    except Exception:
        return ""


def exact_skill_match(text):
    text_lower = text.lower()
    found = set()

    for skill, aliases in SKILL_SYNONYMS.items():
        for alias in aliases:
            if alias in text_lower:
                found.add(skill)
                break

    for skill in SKILLS.keys():
        if skill in text_lower:
            found.add(skill)

    return found


def semantic_skill_match(text, threshold=0.38):
    if not text.strip():
        return set()

    found = set()
    text_embedding = model.encode(text.lower(), convert_to_tensor=True)

    for skill in SKILLS.keys():
        skill_embedding = model.encode(skill, convert_to_tensor=True)
        score = util.cos_sim(skill_embedding, text_embedding).item()

        if score >= threshold:
            found.add(skill)

    return found


def explain_skill_matching(text):
    text_lower = text.lower()
    explanation = []

    for skill, aliases in SKILL_SYNONYMS.items():
        for alias in aliases:
            if alias in text_lower:
                explanation.append({
                    "skill": skill,
                    "method": "Exact Match",
                    "match": alias
                })
                break

    return explanation


def extract_skills(text):
    if not text:
        return []

    exact_found = exact_skill_match(text)
    semantic_found = semantic_skill_match(text)

    final_skills = exact_found.union(semantic_found)

    filtered = []
    for skill in final_skills:
        if skill in SKILLS:
            filtered.append(skill)

    return sorted(list(set(filtered)))


def skill_gap(resume_skills, jd_skills):
    gap = []

    for skill in jd_skills:
        if skill in resume_skills:
            gap.append((skill, "Known"))
        else:
            gap.append((skill, "Missing"))

    return gap


def skill_coverage(resume_skills, jd_skills):
    if not jd_skills:
        return 0

    matched = len([skill for skill in jd_skills if skill in resume_skills])
    return int((matched / len(jd_skills)) * 100)


def generate_path(missing_skills):
    roadmap = []
    seen = set()

    def add_skill(skill):
        if skill in seen:
            return

        if skill in SKILL_GRAPH:
            for prereq in SKILL_GRAPH[skill]:
                if prereq in SKILLS:
                    add_skill(prereq)

        seen.add(skill)
        roadmap.append(skill)

    for skill in missing_skills:
        add_skill(skill)

    roadmap = sorted(
        roadmap,
        key=lambda s: (
            0 if s in missing_skills else 1,
            -SKILLS.get(s, {}).get("priority", 1),
            SKILLS.get(s, {}).get("time", 10)
        )
    )

    return roadmap


def build_roadmap_details(path, missing_skills):
    details = []

    for skill in path:
        meta = SKILLS.get(skill, {})
        details.append({
            "skill": skill,
            "type": "Target Skill" if skill in missing_skills else "Prerequisite",
            "level": meta.get("level", "Intermediate"),
            "priority": meta.get("priority", 3),
            "time": meta.get("time", 10)
        })

    return details


def build_weekly_plan(roadmap_details, hours_per_week=15):
    weeks = []
    current_week = []
    current_hours = 0

    for item in roadmap_details:
        item_hours = item["time"]

        if current_hours + item_hours > hours_per_week and current_week:
            weeks.append(current_week)
            current_week = []
            current_hours = 0

        current_week.append(item)
        current_hours += item_hours

    if current_week:
        weeks.append(current_week)

    return weeks


def calculate_time(path):
    total = 0
    for skill in path:
        if skill in SKILLS:
            total += SKILLS[skill]["time"]
    return total


def training_compression(traditional_time, optimized_time):
    if traditional_time == 0:
        return 0
    saved = max(0, traditional_time - optimized_time)
    return int((saved / traditional_time) * 100)


def generate_reasoning(gap, path):
    reasoning = []

    for skill, status in gap:
        if status == "Missing":
            priority = SKILLS.get(skill, {}).get("priority", 3)
            level = SKILLS.get(skill, {}).get("level", "Intermediate")
            reasoning.append(
                f"{skill} is required for the role but missing in the candidate profile, so it was prioritized at {level} level with priority score {priority}."
            )

    for skill in path:
        if skill in SKILL_GRAPH and SKILL_GRAPH[skill]:
            prereqs = ", ".join(SKILL_GRAPH[skill])
            reasoning.append(
                f"{skill} is dependency-linked, so supporting skills ({prereqs}) were considered before or alongside it."
            )

    return reasoning


def get_course_recommendations(path):
    recommendations = {}

    for skill in path:
        if skill in SKILLS:
            recommendations[skill] = {
                "level": SKILLS[skill].get("level", "Intermediate"),
                "courses": SKILLS[skill].get("courses", [f"Learn {skill.title()}"])
            }

    return recommendations


def modules_skipped(resume_skills, jd_skills):
    return len([skill for skill in jd_skills if skill in resume_skills])


def evaluate_matching_quality(resume_text, resume_skills, jd_skills, explanations):
    exact_matches = len(explanations)
    total_resume_skills = len(resume_skills)
    total_jd_skills = len(jd_skills)

    if total_resume_skills == 0:
        exact_ratio = 0
    else:
        exact_ratio = int((exact_matches / total_resume_skills) * 100)

    if total_jd_skills == 0:
        role_alignment_signal = 0
    else:
        role_alignment_signal = int((len([s for s in jd_skills if s in resume_skills]) / total_jd_skills) * 100)

    overall_confidence = int((exact_ratio * 0.4) + (role_alignment_signal * 0.6))

    if overall_confidence >= 80:
        confidence_band = "High"
    elif overall_confidence >= 55:
        confidence_band = "Moderate"
    else:
        confidence_band = "Low"

    return {
        "exact_match_count": exact_matches,
        "resume_skill_count": total_resume_skills,
        "jd_skill_count": total_jd_skills,
        "exact_match_ratio": exact_ratio,
        "role_alignment_signal": role_alignment_signal,
        "overall_confidence": overall_confidence,
        "confidence_band": confidence_band
    }


def draw_graph(path, missing):
    graph = nx.DiGraph()

    for skill in path:
        node_type = "missing" if skill in missing else "prerequisite"
        graph.add_node(skill, node_type=node_type)

    for skill in missing:
        if skill in SKILL_GRAPH:
            for prereq in SKILL_GRAPH[skill]:
                if prereq in path:
                    graph.add_edge(prereq, skill)

    return graph