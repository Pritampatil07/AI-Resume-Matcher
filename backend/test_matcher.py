
from backend.matcher import (
    find_skills,
    calculate_text_similarity,
    match_resume_to_job,
    rank_jobs,
)


def test_find_skills():
    text = "I know Python, SQL, Excel and Power BI."
    skills = find_skills(text)

    assert "python" in skills
    assert "sql" in skills
    assert "excel" in skills
    assert "power bi" in skills


def test_find_skills_case_insensitive():
    skills = find_skills("PYTHON and SQL")

    assert "python" in skills
    assert "sql" in skills


def test_text_similarity_returns_percentage():
    score = calculate_text_similarity(
        "Python developer with SQL skills",
        "Python developer with SQL skills",
    )

    assert 0 <= score <= 100
    assert score > 0


def test_match_resume_to_job():
    resume = "Python developer with SQL and Excel experience."
    job = "We need Python, SQL, Excel and Power BI skills."

    result = match_resume_to_job(resume, job)

    assert 0 <= result["match_score"] <= 100
    assert "python" in result["matched_skills"]
    assert "sql" in result["matched_skills"]
    assert "excel" in result["matched_skills"]
    assert "power bi" in result["missing_skills"]


def test_match_rejects_empty_resume():
    try:
        match_resume_to_job("", "Python developer required.")
        assert False, "Expected ValueError"
    except ValueError:
        pass


def test_rank_jobs_highest_score_first():
    resume = "Python developer with SQL and data analysis experience."

    jobs = [
        {
            "id": "1",
            "title": "Graphic Designer",
            "description": "Graphic design and illustration skills required.",
        },
        {
            "id": "2",
            "title": "Python Developer",
            "description": "Python, SQL and data analysis experience required.",
        },
    ]

    results = rank_jobs(resume, jobs)

    assert len(results) == 2
    assert results[0]["match_score"] >= results[1]["match_score"]
    assert results[0]["title"] == "Python Developer"
