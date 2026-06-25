import streamlit as st
from recruiter import *

st.set_page_config(
page_title="HireSense AI",
page_icon="🎯",
layout="wide"
)

# ---------------- CSS ----------------

st.markdown("""

<style>

.hero {
    padding: 20px;
    border-radius: 15px;
    background: linear-gradient(90deg,#1f2937,#111827);
    margin-bottom: 20px;
}

.hero-title {
    font-size: 40px;
    font-weight: bold;
    color: white;
}

.hero-sub {
    font-size: 18px;
    color: #d1d5db;
}

div[data-testid="metric-container"] {
    border: 1px solid #374151;
    padding: 15px;
    border-radius: 15px;
}

</style>

""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------

with st.sidebar:


 st.title("🎯 HireSense AI")

 st.markdown("""
AI Hiring Intelligence Platform

✅ Resume Analysis

✅ ATS Compatibility

✅ Resume Ranking

✅ Skill Gap Detection

 All copy rights reserved @ © 2026

  Developed by Sai Charan
""")

role = st.radio(
    "Select Workspace",
    [
        "Recruiter",
        "Candidate"
    ]
)


# ---------------- HERO ----------------

st.markdown("""

<div class="hero">

<div class="hero-title">
🎯 HireSense AI
</div>

<div class="hero-sub">
AI Hiring Intelligence Platform
</div>

</div>
""", unsafe_allow_html=True)

# ==================================================

# RECRUITER DASHBOARD

# ==================================================

if role == "Recruiter":


  st.markdown("## 👔 Recruiter Workspace")

  recruiter_mode = st.selectbox(
    "Recruiter Tool",
    [
        "Candidate Analysis",
        "Resume Ranking"
    ]
   )

# ==========================================
# CANDIDATE ANALYSIS
# ==========================================

  if recruiter_mode == "Candidate Analysis":

    with st.container(border=True):

        uploaded_file = st.file_uploader(
            "📄 Upload Resume",
            type=["docx"]
        )

        jd_text = st.text_area(
            "📝 Paste Job Description",
            height=200
        )

        analyze = st.button(
            "🔍 Analyze Candidate",
            use_container_width=True
        )

    if analyze:

        if uploaded_file is None:
            st.error("Please upload a resume.")
            st.stop()

        if not jd_text.strip():
            st.error("Please paste a Job Description.")
            st.stop()

        resume_text = extract_resume(uploaded_file)

        score, matched, missing = calculate_match(
            resume_text,
            jd_text
        )

        category_scores = category_analysis(
            matched,
            missing
        )

        ats_score, ats_checks = calculate_ats_score(
            resume_text,
            matched,
            missing
        )
        semantic_score = semantic_match(
           resume_text,
           jd_text
        )


        # Metrics
        col1, col2, col3, col4 = st.columns(4)

        with col1:
           st.metric(
           "Keyword Match",
           f"{score}%"
        )

        with col2:
           st.metric(
            "AI Semantic Match",
             f"{semantic_score}%"
        )

        with col3:
          st.metric(
            "ATS Score",
            f"{ats_score}/100"
        )

        with col4:

          final_score = round(
        (
            score +
            semantic_score +
            ats_score
        ) / 3,
        2
        )

        st.metric(
          "HireSense AI Score",
           f"{final_score}%"
        )
        if semantic_score >= 80:

          st.success(
           "Excellent semantic alignment with the role."
        )

        elif semantic_score >= 60:

         st.warning(
           "Moderate semantic alignment."
        )

        else:

         st.error(
          "Low semantic alignment."
        )

        st.divider()

        # Category Breakdown

        st.subheader("📊 Skill Category Breakdown")

        for category, value in category_scores.items():

            st.write(f"**{category}**")

            st.progress(value / 100)

            st.write(f"{value}%")

        st.divider()

        # ATS Report

        st.subheader("📑 ATS Compatibility Report")

        for item in ats_checks:

            if item.startswith("✅"):
                st.success(item)

            else:
                st.warning(item)

        st.divider()

        # Skills

        left, right = st.columns(2)

        with left:

            st.subheader("💪 Technical Alignment")

            if matched:

                for skill in matched:
                    st.success(skill.title())

            else:
                st.info("No matching skills found.")

        with right:

            st.subheader("⚠ Skill Gaps")

            if missing:

                for skill in missing:
                    st.warning(skill.title())

            else:
                st.success("No major skill gaps.")

        st.divider()

        # Risk Analysis

        st.subheader("🚨 Risk Indicators")

        risk_areas = []

        if "docker" in missing:
            risk_areas.append(
                "Containerization knowledge not evident"
            )

        if "kubernetes" in missing:
            risk_areas.append(
                "Container orchestration experience missing"
            )

        if "aws" in missing:
            risk_areas.append(
                "Cloud deployment experience missing"
            )

        if len(risk_areas) == 0:

            st.success(
                "No major technical risks identified."
            )

        else:

            for risk in risk_areas:
                st.warning(risk)

        st.divider()

        # Hiring Recommendation

        st.subheader("💼 Hiring Recommendation")

        if score >= 80:

            st.success(
                "Proceed to Technical Interview"
            )

        elif score >= 60:

            st.warning(
                "Needs Further Evaluation"
            )

        else:

            st.error(
                "Not a Strong Match For Current Role"
            )

# ==========================================
# RESUME RANKING
# ==========================================

  elif recruiter_mode == "Resume Ranking":

    uploaded_files = st.file_uploader(
        "📄 Upload Resumes",
        type=["docx"],
        accept_multiple_files=True
    )

    jd_text = st.text_area(
        "📝 Paste Job Description",
        height=200
    )

    rank_button = st.button(
        "🏆 Rank Candidates",
        use_container_width=True
    )

    if rank_button:

        if not uploaded_files:
            st.error("Please upload resumes.")
            st.stop()

        if not jd_text.strip():
            st.error("Please paste a Job Description.")
            st.stop()

        rankings = []

        for file in uploaded_files:

            resume_text = extract_resume(file)

            score, matched, missing = calculate_match(
                resume_text,
                jd_text
            )

            rankings.append(
                (
                    file.name,
                    score
                )
            )

        rankings.sort(
            key=lambda x: x[1],
            reverse=True
        )

        st.subheader("🏆 Candidate Rankings")

        for rank, candidate in enumerate(
            rankings,
            start=1
        ):

            st.write(
                f"#{rank} | {candidate[0]} | {candidate[1]}%"
            )


# ==================================================

# CANDIDATE DASHBOARD

# ==================================================

elif role == "Candidate":

    st.markdown("## 🎯 Candidate Workspace")

    uploaded_file = st.file_uploader(
        "📄 Upload Resume",
        type=["docx"]
    )

    target_role = st.selectbox(
        "🎯 Target Role",
        [
            "ML Engineer",
            "Backend Developer",
            "Data Scientist"
        ]
    )

    analyze = st.button(
        "🚀 Analyze My Profile",
        use_container_width=True
    )

    if analyze:

        if uploaded_file is None:
            st.error("Please upload your resume.")
            st.stop()

        resume_text = extract_resume(uploaded_file)

        score, matched, missing = candidate_readiness(
            resume_text,
            target_role
        )

        roadmap = generate_roadmap(missing)

        strength = resume_strength(resume_text)

        # ==================================
        # Career Readiness Score
        # ==================================

        st.divider()

        st.subheader("🎯 Career Readiness Score")

        st.metric(
            "Readiness",
            f"{score}/100"
        )

        # ==================================
        # Career GPS
        # ==================================

        if score < 30:
            level = "Beginner"

        elif score < 60:
            level = "Learner"

        elif score < 80:
            level = "Enthusiast"

        else:
            level = "Job Ready"

        st.divider()

        st.subheader("🧭 Career GPS")

        st.info(
            f"""
Current Level: {level}

Target Role: {target_role}

Progress: {score}%
"""
        )

        st.progress(score / 100)

        # ==================================
        # Skills Analysis
        # ==================================

        st.divider()

        col1, col2 = st.columns(2)

        with col1:

            st.subheader("✅ Matched Skills")

            if matched:

                for skill in matched:
                    st.success(skill.title())

            else:
                st.info("No matching skills found")

        with col2:

            st.subheader("❌ Missing Skills")

            if missing:

                for skill in missing:
                    st.warning(skill.title())

            else:
                st.success("No skill gaps detected")

        # ==================================
        # Personalized Roadmap
        # ==================================

        st.divider()

        st.subheader("🛣 Personalized Roadmap")

        for item in roadmap:
            st.success(item)

        # ==================================
        # Resume Strength Analyzer
        # ==================================

        st.divider()

        st.subheader("📊 Resume Strength Analyzer")

        for section, value in strength.items():

            st.write(
                f"**{section} ({value}/10)**"
            )

            st.progress(value / 10)
        