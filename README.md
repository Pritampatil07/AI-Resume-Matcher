# AI Resume Matcher

An AI-powered resume--job matching web application that compares an
uploaded resume with a job description, highlights matching and missing
skills, and provides a match score to help users identify areas to
improve.

## Features

-   **Resume upload:** Upload a resume in PDF or DOCX format (maximum
    file size shown in the UI: 5 MB).
-   **Job-description matching:** Compare resume content against a
    pasted job description.
-   **Match score:** View an overall match score and a text-similarity
    score.
-   **Skill coverage:** See the percentage of required skills detected
    in the resume.
-   **Skill gap analysis:** Review matched skills, missing skills,
    resume skills, and required skills.
-   **Explanation and recommendation:** Receive a short explanation of
    the result, including a text-match recommendation.
-   **REST API:** FastAPI endpoints with interactive API documentation.
-   **Automated tests:** Unit tests for matching logic and resume-upload
    validation.

## Screenshots

Add screenshots of your running application to `docs/screenshots/`, then
update the paths below.

### Resume matcher interface

![AI Resume Matcher interface](docs/screenshots/resume-matcher.png)

### API documentation

![FastAPI Swagger documentation](docs/screenshots/api-docs.png)

> Suggested screenshots: the upload/job-description screen, a completed
> match-results screen, and the `/docs` API page. Do not commit resumes
> or screenshots containing personal information.

## Technology stack

-   **Backend:** Python, FastAPI, Uvicorn
-   **Resume parsing:** PyMuPDF (`fitz`) and document-parsing
    dependencies configured in `requirements.txt`
-   **Matching and text similarity:** Python-based skill matching and
    TF-IDF text similarity
-   **Frontend:** HTML, CSS, JavaScript
-   **Testing:** pytest
-   **API documentation:** FastAPI Swagger UI / OpenAPI

Check `requirements.txt` for the exact Python package versions used by
your checkout.

## Project structure

``` text
AI-Resume-Matcher/
├── backend/
│   ├── main.py              # FastAPI application and API endpoints
│   ├── matcher.py           # Resume/job matching logic
│   ├── parser.py            # Resume file parsing and validation
│   ├── models.py            # Request/response models
│   ├── database.py          # Database-related code
│   ├── test_matcher.py      # Matching tests
│   └── test_parser.py       # Parser validation tests
├── frontend/
│   ├── index.html           # User interface
│   ├── style.css            # UI styling
│   └── script.js            # Frontend behavior and API calls
├── tests/                   # Additional tests
├── requirements.txt
└── README.md
```

## Prerequisites

-   Python installed on your system
-   Git (optional, for cloning the repository)
-   A modern web browser

## Installation and setup (Windows PowerShell)

### 1. Clone the repository

``` powershell
git clone https://github.com/Pritampatil07/AI-Resume-Matcher.git
cd AI-Resume-Matcher
```

If you already have the project on your computer, open PowerShell in the
project root instead.

### 2. Create and activate a virtual environment

``` powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, you can run the virtual environment's
Python directly in the commands below, or review your local PowerShell
execution-policy settings.

### 3. Install dependencies

``` powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 4. Start the backend API

Run this command from the project root:

``` powershell
python -m uvicorn backend.main:app --reload
```

The API should be available at `http://127.0.0.1:8000`.

-   Interactive API documentation: `http://127.0.0.1:8000/docs`
-   Health endpoint: `http://127.0.0.1:8000/health`

Keep this terminal open while using the application.

### 5. Start the frontend

Open a **second** PowerShell terminal, navigate to the project root, and
run:

``` powershell
python -m http.server 5501 --directory ".\frontend"
```

Then open `http://127.0.0.1:5501` in your browser.

If the frontend cannot reach the backend, check the API URL configured
in `frontend/script.js` and make sure it points to
`http://127.0.0.1:8000`. If you change the API URL, ensure the backend's
CORS configuration permits the frontend origin.

## Run tests

From the project root, with the virtual environment active:

``` powershell
python -m pytest -v
```

Use the same Python environment where the project dependencies are
installed. If a package import fails during test collection, install the
dependencies into that environment and rerun the tests.

## API overview

The FastAPI application currently exposes these routes:

  -----------------------------------------------------------------------
  Method                  Endpoint                Purpose
  ----------------------- ----------------------- -----------------------
  `GET`                   `/`                     Root/home endpoint

  `GET`                   `/health`               Health check

  `POST`                  `/match`                Upload a resume and
                                                  compare it with a job
                                                  description

  `POST`                  `/recommend`            Job recommendation
                                                  endpoint
  -----------------------------------------------------------------------

For request fields and response schemas, start the backend and visit
[`/docs`](http://127.0.0.1:8000/docs).

### Example matching workflow

1.  Upload a resume through the frontend or the `/match` API.
2.  Paste the target job description.
3.  Submit the request.
4.  Review the overall match score, text similarity, skill coverage,
    matched skills, and missing skills.
5.  Use the missing-skill list as a guide for reviewing your resume.
    Only add skills you genuinely have.

## How matching works

The current API response describes the score as a weighted combination
of:

-   **60% TF-IDF text similarity**
-   **40% known-skill coverage**

The result also includes the detected resume skills, required skills,
matched skills, missing skills, and an explanation. Treat the score as a
comparison aid, not a guarantee of passing an employer's ATS or
receiving an interview.

## Security and privacy notes

-   Use test resumes when demonstrating the project publicly.
-   Do not commit personal resumes, secrets, `.env` files, virtual
    environments, or local databases.
-   Validate file uploads and keep dependencies updated.
-   Before public deployment, configure production CORS origins, request
    limits, logging, and secure storage appropriately.

## Current status

The project includes a working frontend/backend flow and automated
tests. Verify the installation and test suite in a clean environment
before describing a release as production-ready.

## Contributing

1.  Create a feature branch.
2.  Make and test your changes.
3.  Run `python -m pytest -v`.
4.  Open a pull request with a clear description and relevant
    screenshots.

## License

No license is specified here. Add a `LICENSE` file if you want to define
how others may use, modify, and distribute this project.
