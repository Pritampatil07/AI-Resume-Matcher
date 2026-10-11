from typing import Optional

from fastapi import FastAPI, File, HTTPException, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from backend.parser import (
    extract_resume_text,
    ResumeParsingError,
    MAX_FILE_SIZE,
)
from backend.matcher import (
    match_resume_to_job,
    rank_jobs,
)


app = FastAPI(
    title="AI Resume–Job Matching Engine",
    description=(
        "Compare resumes with job descriptions, "
        "identify skills gaps, and rank job matches."
    ),
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://ai-resume-matcher-1-he8m.onrender.com",
        "http://127.0.0.1:5500",
        "http://localhost:5500",
        "http://127.0.0.1:5501",
        "http://localhost:5501",
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


class JobDescription(BaseModel):
    id: Optional[str] = None
    title: str = Field(min_length=1, max_length=200)
    description: str = Field(min_length=1, max_length=20000)


class RecommendationRequest(BaseModel):
    resume_text: str = Field(min_length=30, max_length=50000)
    jobs: list[JobDescription] = Field(min_length=1, max_length=50)


@app.get("/")
def home():
    return {
        "message": "AI Resume–Job Matching Engine API",
        "docs": "/docs",
        "health": "/health",
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.post("/match")
async def match_resume(
    file: UploadFile = File(...),
    job_description: str = Form(...),
):
    """Upload a resume and match it to one job description."""

    try:
        # Read at most 1 byte beyond the configured limit.
        file_bytes = await file.read(MAX_FILE_SIZE + 1)

        resume_text = extract_resume_text(
            file.filename or "",
            file_bytes,
        )

        result = match_resume_to_job(
            resume_text,
            job_description,
        )

        return {
            "filename": file.filename,
            "result": result,
        }

    except ResumeParsingError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    finally:
        await file.close()


@app.post("/recommend")
def recommend_jobs(request: RecommendationRequest):
    """Rank multiple jobs against extracted resume text."""

    try:
        jobs = [
            job.model_dump()
            for job in request.jobs
        ]

        results = rank_jobs(
            request.resume_text,
            jobs,
        )

        return {
            "total_jobs": len(results),
            "recommendations": results,
        }

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc
