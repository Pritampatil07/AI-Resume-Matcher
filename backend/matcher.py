
import re
from typing import Any

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# Canonical skill names and their common variations.
SKILL_ALIASES = {
    "python": ["python", "python programming"],
    "sql": ["sql", "structured query language"],
    "machine learning": ["machine learning", "ml"],
    "deep learning": ["deep learning"],
    "artificial intelligence": ["artificial intelligence", "ai"],
    "fastapi": ["fastapi", "fast api"],
    "html": ["html", "html5"],
    "css": ["css", "css3"],
    "javascript": ["javascript", "java script"],
    "typescript": ["typescript"],
    "scikit-learn": ["scikit-learn", "scikit learn", "sklearn"],
    "pandas": ["pandas"],
    "numpy": ["numpy"],
    "power bi": ["power bi", "powerbi", "microsoft power bi"],
    "excel": ["excel", "microsoft excel", "ms excel"],
    "tableau": ["tableau"],
    "tensorflow": ["tensorflow"],
    "pytorch": ["pytorch"],
    "nlp": ["natural language processing", "nlp"],
    "git": ["git", "git version control"],
    "github": ["github"],
    "docker": ["docker", "containerization"],
    "rest api": ["rest api", "restful api"],
    "postgresql": ["postgresql", "postgres"],
    "mysql": ["mysql"],
    "mongodb": ["mongodb", "mongo db"],
    "sqlite": ["sqlite"],
    "database management": ["database management", "dbms"],
    "data analysis": ["data analysis", "data analytics"],
    "data visualization": ["data visualization", "data visualisation"],
    "statistics": ["statistics", "statistical analysis"],
    "matplotlib": ["matplotlib"],
    "seaborn": ["seaborn"],
    "scipy": ["scipy"],
    "power query": ["power query"],
    "dax": ["dax"],
    "pivot tables": ["pivot table", "pivot tables"],
    "vlookup": ["vlookup", "xlookup"],
    "communication": ["communication", "communication skills"],
    "problem solving": ["problem solving", "problem-solving"],
    "teamwork": ["teamwork", "team work"],
    "project management": ["project management"],
    "critical thinking": ["critical thinking"],
    "data cleaning": ["data cleaning", "data cleansing"],
    "etl": ["etl", "extract transform load"],
    "big data": ["big data"],
    "aws": ["aws", "amazon web services"],
    "azure": ["azure", "microsoft azure"],
    "google cloud": ["google cloud", "gcp"],
    "linux": ["linux"],
    "java": ["java"],
    "c++": ["c++"],
    "c#": ["c#"],
    "r programming": ["r programming", "r language"],
    "flask": ["flask"],
    "django": ["django"],
    "fastapi testing": ["pytest", "unit testing"],
}


def normalize_text(text: str) -> str:
    """Normalize whitespace and case."""
    return re.sub(r"\s+", " ", text.lower()).strip()


def contains_alias(text: str, alias: str) -> bool:
    """Find an alias without matching it inside unrelated words."""
    pattern = r"(?<!\w)" + re.escape(alias.lower()) + r"(?!\w)"
    return re.search(pattern, text) is not None


def find_skills(text: str) -> list[str]:
    """Extract skills from text using the configured skill dictionary."""
    normalized = normalize_text(text)
    found = []

    for skill, aliases in SKILL_ALIASES.items():
        for alias in aliases:
            if contains_alias(normalized, alias):
                found.append(skill)
                break

    return sorted(set(found))


def calculate_text_similarity(
    resume_text: str,
    job_description: str,
) -> float:
    """Calculate TF-IDF cosine similarity as a percentage."""
    resume = normalize_text(resume_text)
    job = normalize_text(job_description)

    if not resume or not job:
        return 0.0

    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2),
        sublinear_tf=True,
    )

    try:
        vectors = vectorizer.fit_transform([resume, job])
    except ValueError:
        return 0.0

    similarity = cosine_similarity(
        vectors[0:1],
        vectors[1:2],
    )[0][0]

    return round(float(similarity) * 100, 2)


def match_resume_to_job(
    resume_text: str,
    job_description: str,
) -> dict[str, Any]:
    """Compare resume skills and text against one job description."""
    if not resume_text.strip():
        raise ValueError("Resume text cannot be empty.")

    if not job_description.strip():
        raise ValueError("Job description cannot be empty.")

    resume_skills = set(find_skills(resume_text))
    required_skills = set(find_skills(job_description))

    matched_skills = sorted(resume_skills & required_skills)
    missing_skills = sorted(required_skills - resume_skills)

    if required_skills:
        skill_coverage = (
            len(matched_skills) / len(required_skills)
        ) * 100
    else:
        skill_coverage = 0.0

    text_similarity = calculate_text_similarity(
        resume_text,
        job_description,
    )

    match_score = round(
        (0.60 * text_similarity) + (0.40 * skill_coverage),
        2,
    )

    if match_score >= 75:
        recommendation = "Strong text match"
    elif match_score >= 50:
        recommendation = "Moderate text match"
    else:
        recommendation = "Low text match"

    if matched_skills:
        explanation = (
            "Matching skills found: " + ", ".join(matched_skills) + "."
        )
    else:
        explanation = (
            "No skills from the configured skill dictionary matched. "
            "Consider expanding the dictionary if relevant."
        )

    if missing_skills:
        explanation += (
            " Skills mentioned in the job description but not detected "
            "in the resume: " + ", ".join(missing_skills) + "."
        )
    elif not required_skills:
        explanation += (
            " No recognized skills were found in the job description, "
            "so skill coverage cannot be meaningfully assessed."
        )

    return {
        "match_score": match_score,
        "text_similarity": text_similarity,
        "skill_coverage": round(skill_coverage, 2),
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "resume_skills": sorted(resume_skills),
        "required_skills": sorted(required_skills),
        "recommendation": recommendation,
        "explanation": explanation,
        "scoring_method": (
            "60% TF-IDF text similarity + "
            "40% known-skill coverage"
        ),
    }


def rank_jobs(
    resume_text: str,
    jobs: list[dict[str, str]],
) -> list[dict[str, Any]]:
    """Rank jobs from highest to lowest match score."""
    results = []

    for job in jobs:
        result = match_resume_to_job(
            resume_text,
            job.get("description", ""),
        )

        results.append({
            "job_id": job.get("id"),
            "title": job.get("title", "Untitled job"),
            **result,
        })

    return sorted(
        results,
        key=lambda item: item["match_score"],
        reverse=True,
    )
