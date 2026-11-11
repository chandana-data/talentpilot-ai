import streamlit as st
import matplotlib.pyplot as plt
import networkx as nx

from logic import (
    extract_text_from_pdf,
    extract_skills,
    explain_skill_matching,
    skill_gap,
    skill_coverage,
    generate_path,
    build_roadmap_details,
    build_weekly_plan,
    calculate_time,
    training_compression,
    generate_reasoning,
    get_course_recommendations,
    modules_skipped,
    evaluate_matching_quality,
    draw_graph,
)

st.set_page_config(
    page_title="TalentPilot AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
:root {
    --bg: #081120;
    --panel: rgba(15, 23, 42, 0.78);
    --text: #e5eefc;
    --muted: #9fb0c8;
    --line: rgba(255,255,255,0.08);
    --blue: #4f8cff;
    --violet: #8b5cf6;
}

.stApp {
    background:
        radial-gradient(circle at 0% 0%, rgba(79,140,255,0.20), transparent 28%),
        radial-gradient(circle at 100% 0%, rgba(139,92,246,0.18), transparent 24%),
        linear-gradient(180deg, #06101d 0%, #0b1324 50%, #111827 100%);
    color: var(--text);
}

header, footer {
    visibility: hidden;
}

.block-container {
    max-width: 1380px;
    padding-top: 1.2rem;
    padding-bottom: 2rem;
}

.hero {
    border-radius: 28px;
    padding: 34px;
    background: linear-gradient(135deg, rgba(15,23,42,0.95), rgba(30,41,59,0.90));
    border: 1px solid var(--line);
    box-shadow: 0 14px 36px rgba(0,0,0,0.30);
    margin-bottom: 18px;
}

.hero h1 {
    font-size: 3rem;
    margin-bottom: 10px;
    color: #f8fbff;
}

.hero p {
    color: #c8d6ea;
    line-height: 1.7;
    font-size: 1.05rem;
    margin-bottom: 0;
    max-width: 980px;
}

.badges {
    margin-top: 18px;
}

.badge {
    display: inline-block;
    padding: 8px 14px;
    margin-right: 10px;
    margin-bottom: 10px;
    border-radius: 999px;
    background: rgba(79,140,255,0.10);
    border: 1px solid rgba(79,140,255,0.22);
    color: #dbeafe;
    font-size: 0.9rem;
    font-weight: 600;
}

.panel {
    background: var(--panel);
    border: 1px solid var(--line);
    border-radius: 24px;
    padding: 22px;
    box-shadow: 0 10px 28px rgba(0,0,0,0.24);
    margin-bottom: 18px;
}

.mini-panel {
    background: rgba(17, 24, 39, 0.88);
    border: 1px solid var(--line);
    border-radius: 18px;
    padding: 16px 18px;
    box-shadow: 0 8px 20px rgba(0,0,0,0.20);
    margin-bottom: 18px;
}

.panel h3, .mini-panel h4 {
    margin-top: 0;
    color: #f8fbff;
}

.kpi {
    background: linear-gradient(180deg, rgba(17,24,39,0.94), rgba(15,23,42,0.95));
    border: 1px solid var(--line);
    border-radius: 22px;
    padding: 18px;
    min-height: 110px;
    box-shadow: 0 10px 24px rgba(0,0,0,0.20);
}

.kpi-label {
    color: var(--muted);
    font-size: 0.92rem;
    margin-bottom: 8px;
}

.kpi-value {
    color: #f8fbff;
    font-size: 1.8rem;
    font-weight: 800;
    margin-bottom: 6px;
}

.kpi-sub {
    color: #cbd5e1;
    font-size: 0.9rem;
}

.pill {
    display: inline-block;
    padding: 8px 12px;
    margin: 6px 8px 0 0;
    border-radius: 999px;
    border: 1px solid var(--line);
    font-size: 0.9rem;
    font-weight: 600;
}

.pill-default {
    background: rgba(30,41,59,0.78);
    color: #e2e8f0;
}

.pill-known {
    background: rgba(34,197,94,0.14);
    border: 1px solid rgba(34,197,94,0.28);
    color: #dcfce7;
}

.pill-missing {
    background: rgba(239,68,68,0.14);
    border: 1px solid rgba(239,68,68,0.28);
    color: #fee2e2;
}

.roadmap-step, .course-box, .reason-box, .week-box {
    background: rgba(17,24,39,0.90);
    border: 1px solid var(--line);
    border-radius: 18px;
    padding: 16px;
    margin-bottom: 14px;
}

.roadmap-step {
    border-left: 4px solid var(--blue);
}

.small-note {
    color: var(--muted);
    font-size: 0.9rem;
}

.score-bar {
    width: 100%;
    height: 13px;
    background: rgba(255,255,255,0.08);
    border-radius: 999px;
    overflow: hidden;
    margin-bottom: 12px;
}

.score-fill {
    height: 100%;
    border-radius: 999px;
    background: linear-gradient(90deg, var(--blue), var(--violet));
}

div[data-testid="stTextArea"] textarea {
    border-radius: 16px !important;
    background: rgba(15,23,42,0.72) !important;
    color: #f8fbff !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
}

div[data-testid="stFileUploader"] section {
    background: rgba(15,23,42,0.58);
    border: 1px dashed rgba(255,255,255,0.14);
    border-radius: 16px;
}

.stButton > button {
    width: 100%;
    border-radius: 16px;
    padding: 0.95rem 1rem;
    background: linear-gradient(135deg, var(--blue), var(--violet));
    color: white;
    border: none;
    font-weight: 700;
    font-size: 1rem;
    box-shadow: 0 12px 24px rgba(79,140,255,0.22);
}

.stButton > button:hover {
    color: white;
    background: linear-gradient(135deg, #3b82f6, #7c3aed);
}

.stTabs [data-baseweb="tab-list"] {
    gap: 10px;
    margin-bottom: 8px;
}

.stTabs [data-baseweb="tab"] {
    border-radius: 12px;
    background: rgba(15,23,42,0.82);
    padding: 10px 16px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
    <h1>TalentPilot AI</h1>
    <p>
        Enterprise-style adaptive onboarding platform with hybrid skill intelligence,
        dependency-aware learning plans, weekly upskilling structure, measurable onboarding optimization,
        and explainable recommendations.
    </p>
    <div class="badges">
        <span class="badge">Hybrid Skill Matching</span>
        <span class="badge">Adaptive Roadmaps</span>
        <span class="badge">Weekly Planning</span>
        <span class="badge">Explainable AI</span>
        <span class="badge">Kaggle + O*NET</span>
    </div>
</div>
""", unsafe_allow_html=True)

info1, info2 = st.columns(2, gap="large")

with info1:
    st.markdown("""
    <div class="panel">
        <h3>🎯 Why This Matters</h3>
        <p>
            Traditional onboarding is static, one-size-fits-all, and inefficient.
            Experienced hires waste time relearning known topics, while beginners often receive advanced content too early.
        </p>
        <p>
            TalentPilot AI personalizes onboarding by understanding the candidate, understanding the target role,
            and generating a learning sequence that closes the exact skill gap.
        </p>
    </div>
    """, unsafe_allow_html=True)

with info2:
    st.markdown("""
    <div class="panel">
        <h3>📦 What the Platform Delivers</h3>
        <p>After analysis, the system produces:</p>
        <ul>
            <li>Role match score and skill coverage</li>
            <li>Missing skill identification</li>
            <li>Dependency-aware learning roadmap</li>
            <li>Weekly onboarding plan</li>
            <li>Resource recommendations by skill and level</li>
            <li>Explainable reasoning for every recommendation</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

m1, m2, m3 = st.columns(3, gap="large")

with m1:
    st.markdown("""
    <div class="mini-panel">
        <h4>⚡ Personalized</h4>
        <p>Every candidate gets a different roadmap based on current capability and role requirements.</p>
    </div>
    """, unsafe_allow_html=True)

with m2:
    st.markdown("""
    <div class="mini-panel">
        <h4>🧠 Explainable</h4>
        <p>The system shows why a skill was recommended, prioritized, or dependency-linked.</p>
    </div>
    """, unsafe_allow_html=True)

with m3:
    st.markdown("""
    <div class="mini-panel">
        <h4>📉 Efficient</h4>
        <p>Reduces redundant learning time by skipping already-known modules and compressing training.</p>
    </div>
    """, unsafe_allow_html=True)

compare_mode = st.checkbox("Compare Two Candidates")

if compare_mode:
    c_left, c_right = st.columns(2, gap="large")

    with c_left:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.subheader("📄 Candidate 1")
        resume1 = st.text_area("Candidate 1 Resume", height=220, placeholder="Paste candidate 1 resume...")
        st.markdown('</div>', unsafe_allow_html=True)

    with c_right:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.subheader("📄 Candidate 2")
        resume2 = st.text_area("Candidate 2 Resume", height=220, placeholder="Paste candidate 2 resume...")
        st.markdown('</div>', unsafe_allow_html=True)

    resume_text = ""
else:
    left, right = st.columns([1.15, 0.85], gap="large")

    with left:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.subheader("📄 Candidate Profile Input")

        resume_mode = st.radio(
            "Resume input mode",
            ["Paste Resume Text", "Upload Resume PDF"],
            horizontal=True
        )

        resume_text = ""

        if resume_mode == "Paste Resume Text":
            resume_text = st.text_area("Resume", height=240, placeholder="Paste resume here...")
        else:
            uploaded_pdf = st.file_uploader("Upload PDF Resume", type=["pdf"])
            if uploaded_pdf is not None:
                resume_text = extract_text_from_pdf(uploaded_pdf)
                if resume_text:
                    st.success("Resume PDF processed successfully.")
                    with st.expander("Preview extracted resume text"):
                        st.write(resume_text)
                else:
                    st.error("Could not extract text from this PDF.")
        st.markdown('</div>', unsafe_allow_html=True)

    with right:
        st.markdown("""
        <div class="panel">
            <h3>⚙️ Brain Upgrades</h3>
            <ul>
                <li>Hybrid exact + semantic skill extraction</li>
                <li>Priority-based adaptive roadmap</li>
                <li>Weekly skill-building plan</li>
                <li>Skill coverage and readiness scoring</li>
                <li>Training compression metrics</li>
                <li>Explainable AI reasoning trace</li>
            </ul>
            <p class="small-note">Best demo flow: compare a beginner resume with a strong resume to show the platform adapting live.</p>
        </div>
        """, unsafe_allow_html=True)

st.markdown('<div class="panel">', unsafe_allow_html=True)
st.subheader("🎯 Target Role Definition")
jd_text = st.text_area("Job Description", height=190, placeholder="Paste the target job description here...")
st.markdown('</div>', unsafe_allow_html=True)

analyze = st.button("🚀 Analyze Candidate & Generate Roadmap")


def generate_report(coverage, missing, compression, weeks):
    report = f"""
TALENTPILOT AI REPORT

Role Match Score: {coverage}%
Missing Skills: {', '.join(missing) if missing else 'None'}
Training Compression: {compression}%
Estimated Duration: {weeks} weeks

Summary:
Candidate requires focused training in key missing skills.
Adaptive roadmap reduces onboarding time significantly.
"""
    return report


if analyze:
    if compare_mode:
        if not resume1.strip() or not resume2.strip():
            st.warning("Please paste both candidate resumes.")
        elif not jd_text.strip():
            st.warning("Please paste the target job description.")
        else:
            jd_skills = extract_skills(jd_text)

            skills1 = extract_skills(resume1)
            skills2 = extract_skills(resume2)

            score1 = skill_coverage(skills1, jd_skills)
            score2 = skill_coverage(skills2, jd_skills)

            st.markdown("## 🆚 Candidate Comparison")

            col1, col2 = st.columns(2)

            with col1:
                st.metric("Candidate 1 Score", f"{score1}%")
                st.write("Detected Skills:")
                st.write(skills1)

            with col2:
                st.metric("Candidate 2 Score", f"{score2}%")
                st.write("Detected Skills:")
                st.write(skills2)

            if score1 > score2:
                st.success("Candidate 1 is currently a better fit for the target role.")
            elif score2 > score1:
                st.success("Candidate 2 is currently a better fit for the target role.")
            else:
                st.info("Both candidates currently show equal role-match scores.")

    else:
        if not resume_text.strip():
            st.warning("Please paste resume text or upload a readable PDF.")
        elif not jd_text.strip():
            st.warning("Please paste the target job description.")
        else:
            with st.spinner("Running upgraded intelligence engine..."):
                resume_skills = extract_skills(resume_text)
                jd_skills = extract_skills(jd_text)
                gap = skill_gap(resume_skills, jd_skills)
                missing = [skill for skill, status in gap if status == "Missing"]

                path = generate_path(missing)
                roadmap_details = build_roadmap_details(path, missing)
                weekly_plan = build_weekly_plan(roadmap_details)

                total_time = calculate_time(path)
                traditional_time = len(jd_skills) * 15
                coverage = skill_coverage(resume_skills, jd_skills)
                compression = training_compression(traditional_time, total_time)
                skipped = modules_skipped(resume_skills, jd_skills)

                reasoning = generate_reasoning(gap, path)
                courses = get_course_recommendations(path)
                explanations = explain_skill_matching(resume_text)
                eval_metrics = evaluate_matching_quality(
                    resume_text,
                    resume_skills,
                    jd_skills,
                    explanations
                )

            st.markdown("## Executive Dashboard")

            st.markdown("""
            <div class="panel">
                <h3>🧾 Candidate Executive Summary</h3>
            </div>
            """, unsafe_allow_html=True)

            focus_skills = ", ".join(missing[:3]) if missing else "No major gaps"
            estimated_weeks = max(1, len(weekly_plan))

            st.markdown(f"""
            <div class="mini-panel">
                <b>Candidate Readiness:</b> {coverage}% match for target role<br><br>
                <b>Primary Skill Gaps:</b> {focus_skills}<br><br>
                <b>Estimated Onboarding Duration:</b> {estimated_weeks} weeks<br><br>
                <b>Training Time Reduction:</b> {compression}% compared to traditional onboarding
            </div>
            """, unsafe_allow_html=True)

            report = generate_report(coverage, missing, compression, estimated_weeks)
            st.download_button(
                label="📥 Download Onboarding Report",
                data=report,
                file_name="onboarding_report.txt"
            )

            k1, k2, k3, k4 = st.columns(4)

            with k1:
                st.markdown(f"""
                <div class="kpi">
                    <div class="kpi-label">Role Match Score</div>
                    <div class="kpi-value">{coverage}%</div>
                    <div class="kpi-sub">Skill coverage against target role</div>
                </div>
                """, unsafe_allow_html=True)

            with k2:
                st.markdown(f"""
                <div class="kpi">
                    <div class="kpi-label">Missing Skills</div>
                    <div class="kpi-value">{len(missing)}</div>
                    <div class="kpi-sub">Competencies still required</div>
                </div>
                """, unsafe_allow_html=True)

            with k3:
                st.markdown(f"""
                <div class="kpi">
                    <div class="kpi-label">Training Compression</div>
                    <div class="kpi-value">{compression}%</div>
                    <div class="kpi-sub">Reduction from static onboarding</div>
                </div>
                """, unsafe_allow_html=True)

            with k4:
                st.markdown(f"""
                <div class="kpi">
                    <div class="kpi-label">Skipped Modules</div>
                    <div class="kpi-value">{skipped}</div>
                    <div class="kpi-sub">Already-known topics avoided</div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("### Readiness Snapshot")
            st.markdown(f"**Role Match Score:** {coverage}%")
            st.markdown(
                f'<div class="score-bar"><div class="score-fill" style="width:{coverage}%;"></div></div>',
                unsafe_allow_html=True
            )
            st.markdown(f"**Training Compression:** {compression}%")
            st.markdown(
                f'<div class="score-bar"><div class="score-fill" style="width:{compression}%;"></div></div>',
                unsafe_allow_html=True
            )

            tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
                "Evaluation Dashboard",
                "Skill Confidence",
                "Skill Intelligence",
                "Adaptive Roadmap",
                "Weekly Plan",
                "Learning Resources",
                "Reasoning Trace",
                "Dependency Graph"
            ])

            with tab1:
                st.markdown('<div class="panel">', unsafe_allow_html=True)
                st.markdown("### 📊 Evaluation Dashboard")

                e1, e2, e3 = st.columns(3)

                with e1:
                    st.metric("Exact Match Count", eval_metrics["exact_match_count"])
                    st.metric("Resume Skill Count", eval_metrics["resume_skill_count"])

                with e2:
                    st.metric("JD Skill Count", eval_metrics["jd_skill_count"])
                    st.metric("Exact Match Ratio", f'{eval_metrics["exact_match_ratio"]}%')

                with e3:
                    st.metric("Alignment Signal", f'{eval_metrics["role_alignment_signal"]}%')
                    st.metric("System Confidence", f'{eval_metrics["overall_confidence"]}%')

                st.markdown(f"**Confidence Band:** {eval_metrics['confidence_band']}")
                st.markdown(
                    f'<div class="score-bar"><div class="score-fill" style="width:{eval_metrics["overall_confidence"]}%;"></div></div>',
                    unsafe_allow_html=True
                )

                st.markdown("""
                **How to interpret this**
                - Exact Match Count: skills directly found using exact phrases or synonyms
                - Exact Match Ratio: proportion of detected resume skills supported by exact matches
                - Alignment Signal: overlap between candidate skills and role-required skills
                - System Confidence: combined trust signal derived from match evidence and role alignment
                """)

                st.markdown('</div>', unsafe_allow_html=True)

            with tab2:
                st.markdown('<div class="panel">', unsafe_allow_html=True)
                st.markdown("### 🔍 Skill Matching Confidence")

                if explanations:
                    for item in explanations:
                        st.markdown(f"""
                        <div class="reason-box">
                            <b>{item['skill'].title()}</b><br>
                            Detected via: {item['method']}<br>
                            Match phrase: "{item['match']}"
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.info("No clear exact matches found.")

                st.markdown('</div>', unsafe_allow_html=True)

            with tab3:
                c1, c2 = st.columns(2)

                with c1:
                    st.markdown('<div class="panel">', unsafe_allow_html=True)
                    st.markdown("### ✅ Candidate Skill Inventory")
                    if resume_skills:
                        for skill in resume_skills:
                            st.markdown(f'<span class="pill pill-known">{skill}</span>', unsafe_allow_html=True)
                    else:
                        st.info("No resume skills detected.")
                    st.markdown('</div>', unsafe_allow_html=True)

                with c2:
                    st.markdown('<div class="panel">', unsafe_allow_html=True)
                    st.markdown("### 🎯 Target Role Competencies")
                    if jd_skills:
                        for skill in jd_skills:
                            st.markdown(f'<span class="pill pill-default">{skill}</span>', unsafe_allow_html=True)
                    else:
                        st.info("No JD skills detected.")
                    st.markdown('</div>', unsafe_allow_html=True)

                st.markdown('<div class="panel">', unsafe_allow_html=True)
                st.markdown("### ❌ Missing Skills")
                if missing:
                    for skill in missing:
                        st.markdown(f'<span class="pill pill-missing">{skill}</span>', unsafe_allow_html=True)
                else:
                    st.success("No missing skills found.")
                st.markdown('</div>', unsafe_allow_html=True)

            with tab4:
                st.markdown('<div class="panel">', unsafe_allow_html=True)
                st.markdown("### 🚀 Priority-Based Learning Roadmap")

                if roadmap_details:
                    for idx, item in enumerate(roadmap_details, start=1):
                        color = "#4f8cff" if item["type"] == "Target Skill" else "#22c55e"

                        st.markdown(f"""
                        <div class="roadmap-step" style="border-left:4px solid {color};">
                            <b>Step {idx}: {item['skill'].title()}</b><br><br>
                            <b>Type:</b> {item['type']}<br>
                            <b>Level:</b> {item['level']}<br>
                            <b>Priority:</b> {item['priority']} / 5<br>
                            <b>Duration:</b> {item['time']} hrs
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.success("No roadmap required.")

                st.markdown('</div>', unsafe_allow_html=True)

            with tab5:
                st.markdown('<div class="panel">', unsafe_allow_html=True)
                st.markdown("### 📅 Weekly Learning Plan")

                if weekly_plan:
                    for week_idx, week_items in enumerate(weekly_plan, start=1):
                        week_hours = sum(item["time"] for item in week_items)

                        if week_hours <= 10:
                            load = "Light"
                        elif week_hours <= 20:
                            load = "Balanced"
                        else:
                            load = "Intensive"

                        st.markdown(
                            f'<div class="week-box"><b>Week {week_idx}</b> — {week_hours} hrs ({load} workload)',
                            unsafe_allow_html=True
                        )

                        for item in week_items:
                            st.markdown(
                                f"- {item['skill'].title()} ({item['level']}, {item['time']} hrs, {item['type']})"
                            )

                        st.markdown("</div>", unsafe_allow_html=True)
                else:
                    st.info("No weekly plan required.")

                st.markdown('</div>', unsafe_allow_html=True)

            with tab6:
                st.markdown('<div class="panel">', unsafe_allow_html=True)
                st.markdown("### 📚 Recommended Learning Resources")

                if courses:
                    for skill, info in courses.items():
                        st.markdown(f"""
                        <div class="course-box">
                            <b>{skill.title()}</b><br>
                            Level: {info["level"]}
                        """, unsafe_allow_html=True)

                        for course in info["courses"]:
                            st.markdown(f"- {course}")

                        st.markdown("</div>", unsafe_allow_html=True)
                else:
                    st.info("No learning resources required.")

                st.markdown('</div>', unsafe_allow_html=True)

            with tab7:
                st.markdown('<div class="panel">', unsafe_allow_html=True)
                st.markdown("### 🧾 Explainable AI Reasoning Trace")
                if reasoning:
                    for item in reasoning:
                        st.markdown(f'<div class="reason-box">{item}</div>', unsafe_allow_html=True)
                else:
                    st.info("No reasoning generated.")
                st.markdown('</div>', unsafe_allow_html=True)

            with tab8:
                st.markdown('<div class="panel">', unsafe_allow_html=True)
                st.markdown("### 🧠 Skill Dependency Graph")

                graph = draw_graph(path, missing)

                if len(graph.nodes) > 0:
                    fig, ax = plt.subplots(figsize=(13, 7))
                    pos = nx.spring_layout(graph, seed=42, k=2.2)

                    missing_nodes = [n for n, d in graph.nodes(data=True) if d.get("node_type") == "missing"]
                    prereq_nodes = [n for n, d in graph.nodes(data=True) if d.get("node_type") == "prerequisite"]

                    nx.draw_networkx_nodes(
                        graph, pos, nodelist=prereq_nodes,
                        node_size=2800, node_color="#93c5fd",
                        edgecolors="#1e3a8a", linewidths=2, ax=ax
                    )
                    nx.draw_networkx_nodes(
                        graph, pos, nodelist=missing_nodes,
                        node_size=3200, node_color="#fca5a5",
                        edgecolors="#7f1d1d", linewidths=2.2, ax=ax
                    )
                    nx.draw_networkx_edges(
                        graph, pos, edge_color="#64748b",
                        width=2.5, arrows=True, arrowsize=22,
                        arrowstyle="-|>", ax=ax
                    )
                    nx.draw_networkx_labels(
                        graph, pos, font_size=10,
                        font_weight="bold", font_color="#111827", ax=ax
                    )

                    ax.set_title("Skill Dependency Roadmap", fontsize=16, fontweight="bold", pad=20)
                    ax.set_facecolor("#f8fafc")
                    fig.patch.set_facecolor("#f8fafc")
                    ax.axis("off")

                    st.pyplot(fig, use_container_width=True)
                    st.markdown(
                        '<div class="small-note">Blue = prerequisites • Red = missing target skills</div>',
                        unsafe_allow_html=True
                    )
                else:
                    st.info("No graph available.")

                st.markdown('</div>', unsafe_allow_html=True)