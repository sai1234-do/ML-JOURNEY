from docx import Document
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)
def extract_resume(uploaded_file):

    doc = Document(uploaded_file)

    text = ""

    for para in doc.paragraphs:
        text += para.text + "\n"

    return text


def extract_skills(text):

    master_skills = [

        # Programming
        "python",
        "java",
        "c++",
        "javascript",

        # Full Stack
        "react",
        "node",
        "express",
        "mongodb",

        # Database
        "sql",
        "mysql",
        "postgresql",

        # ML
        "machine learning",
        "tensorflow",
        "pytorch",

        # Cloud
        "aws",
        "azure",

        # DevOps
        "docker",
        "kubernetes",

        # Version Control
        "git",
        "github",

        # Backend
        "spring boot",
        "rest api",

        # CS Fundamentals
        "data structures",
        "algorithms"
    ]

    text = text.lower()

    found = []

    for skill in master_skills:

        if skill in text:
            found.append(skill)

    return found


def calculate_match(resume_text, jd_text):

    resume_skills = extract_skills(resume_text)

    jd_skills = extract_skills(jd_text)

    matched = []
    missing = []

    for skill in jd_skills:

        if skill in resume_skills:
            matched.append(skill)
        else:
            missing.append(skill)

    if len(jd_skills) == 0:
        score = 0
    else:
        score = int(
            (len(matched) / len(jd_skills)) * 100
        )

    return score, matched, missing
def category_analysis(matched, missing):

    categories = {

        "Technical": [
            "python",
            "java",
            "c++",
            "javascript"
        ],

        "Cloud": [
            "aws",
            "azure"
        ],

        "DevOps": [
            "docker",
            "kubernetes"
        ],

        "Database": [
            "sql",
            "mysql",
            "postgresql"
        ]
    }

    results = {}

    all_skills = matched + missing

    for category, skills in categories.items():

        total = 0
        found = 0

        for skill in skills:

            if skill in all_skills:

                total += 1

                if skill in matched:
                    found += 1

        if total == 0:
            results[category] = 0
        else:
            results[category] = int(
                (found / total) * 100
            )

    return results
def calculate_ats_score(resume_text, matched, missing):

    score = 0

    resume_text = resume_text.lower()

    checks = []

    # Skills Section

    if "skills" in resume_text:

        score += 20
        checks.append("✅ Skills Section")

    else:

        checks.append("❌ Skills Section Missing")

    # Projects Section

    if "project" in resume_text:

        score += 20
        checks.append("✅ Projects Section")

    else:

        checks.append("❌ Projects Section Missing")

    # Education Section

    if "education" in resume_text:

        score += 20
        checks.append("✅ Education Section")

    else:

        checks.append("❌ Education Section Missing")

    # JD Skill Coverage

    if len(matched) + len(missing) > 0:

        skill_score = int(
            (len(matched) /
            (len(matched) + len(missing))) * 40
        )

        score += skill_score

    return score, checks
def candidate_readiness(resume_text, target_role):

    roles = {

        "ML Engineer": [
            "python",
            "machine learning",
            "deep learning",
            "sql",
            "aws",
            "docker",
            "mlops"
        ],

        "Backend Developer": [
            "java",
            "spring",
            "sql",
            "rest api",
            "docker"
        ],

        "Data Scientist": [
            "python",
            "statistics",
            "machine learning",
            "pandas",
            "sql"
        ]
    }

    required = roles[target_role]

    resume_text = resume_text.lower()

    matched = []
    missing = []

    for skill in required:

        if skill in resume_text:
            matched.append(skill)
        else:
            missing.append(skill)

    score = int(
        (len(matched) / len(required)) * 100
    )

    return score, matched, missing

def generate_roadmap(missing):

    roadmap = []

    week = 1

    for skill in missing:

        roadmap.append(
            f"Week {week}: Learn {skill.title()} And do projects on each skill to get hands on experience"
        )

        week += 1

    return roadmap
def resume_strength(resume_text):

    resume_text = resume_text.lower()

    scores = {}

    scores["Projects"] = 10 if "project" in resume_text else 4

    scores["Skills"] = 10 if "skills" in resume_text else 1

    scores["Education"] = 10 if "education" in resume_text else 3

    scores["Certifications"] = (
        10 if "certification" in resume_text
        else 3
    )

    scores["Achievements"] = (
        10 if "achievement" in resume_text
        else 3
    )

    return scores
def semantic_match(resume_text, jd_text):

    resume_embedding = model.encode(
        resume_text
    )

    jd_embedding = model.encode(
        jd_text
    )

    similarity = cosine_similarity(
        [resume_embedding],
        [jd_embedding]
    )[0][0]

    return round(similarity * 100, 2)

