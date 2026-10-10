
const API_URL = "http://127.0.0.1:8000";
const MAX_FILE_SIZE = 5 * 1024 * 1024;

const matchForm = document.getElementById("matchForm");
const resumeFile = document.getElementById("resumeFile");
const uploadArea = document.getElementById("uploadArea");
const uploadTitle = document.getElementById("uploadTitle");
const uploadHint = document.getElementById("uploadHint");
const jobDescription = document.getElementById("jobDescription");
const charCount = document.getElementById("charCount");
const matchButton = document.getElementById("matchButton");
const buttonText = document.getElementById("buttonText");
const statusMessage = document.getElementById("statusMessage");
const resultsSection = document.getElementById("resultsSection");

function showStatus(message, type = "") {
    statusMessage.textContent = message;
    statusMessage.className = "status-message";

    if (type) {
        statusMessage.classList.add(type);
    }
}

jobDescription.addEventListener("input", function () {
    charCount.textContent =
        jobDescription.value.length.toLocaleString() + " characters";
});

resumeFile.addEventListener("change", function () {
    const file = resumeFile.files[0];
    const error = document.getElementById("fileError");

    error.textContent = "";
    uploadArea.classList.remove("has-file");

    if (!file) {
        uploadTitle.textContent = "Choose your resume";
        uploadHint.textContent = "Click here to browse your files";
        return;
    }

    const extension = file.name.split(".").pop().toLowerCase();

    if (extension !== "pdf" && extension !== "docx") {
        resumeFile.value = "";
        uploadTitle.textContent = "Choose your resume";
        uploadHint.textContent = "Click here to browse your files";
        error.textContent = "Please select a PDF or DOCX file.";
        return;
    }

    if (file.size === 0 || file.size > MAX_FILE_SIZE) {
        resumeFile.value = "";
        uploadTitle.textContent = "Choose your resume";
        uploadHint.textContent = "Click here to browse your files";
        error.textContent = "File must be non-empty and smaller than 5 MB.";
        return;
    }

    uploadTitle.textContent = file.name;
    uploadHint.textContent =
        (file.size / 1024).toFixed(1) + " KB - Ready to analyze";

    uploadArea.classList.add("has-file");
    showStatus("");
});

function renderSkills(containerId, skills, emptyMessage) {
    const container = document.getElementById(containerId);
    container.replaceChildren();

    if (!Array.isArray(skills) || skills.length === 0) {
        const span = document.createElement("span");
        span.className = "empty-skill-message";
        span.textContent = emptyMessage;
        container.appendChild(span);
        return;
    }

    skills.forEach(function (skill) {
        const tag = document.createElement("span");
        tag.className = "skill-tag";
        tag.textContent = String(skill);
        container.appendChild(tag);
    });
}

function displayResults(data, filename) {
    const result = data.result || data;

    const rawScore = Number(result.match_score);

    if (!Number.isFinite(rawScore)) {
        console.error("Unexpected API response:", data);
        throw new Error(
            "Match score is missing. Please check the backend response."
        );
    }

    const score = Math.max(0, Math.min(100, rawScore));

    document.getElementById("resultFilename").textContent =
        "Resume analyzed: " + filename;

    document.getElementById("matchScore").textContent =
        Math.round(score) + "%";

    document.getElementById("scoreCircle").style.setProperty(
        "--score",
        score + "%"
    );

    let title = "Room to improve";
    let description =
        "Review the missing skills and improve your resume.";

    if (score >= 80) {
        title = "Strong match";
        description =
            "Your resume aligns with many job requirements.";
    } else if (score >= 60) {
        title = "Good starting match";
        description =
            "Review the skill gaps to improve your match.";
    } else if (score >= 40) {
        title = "Partial match";
        description =
            "Some relevant skills were found.";
    }

    document.getElementById("scoreTitle").textContent = title;
    document.getElementById("scoreDescription").textContent = description;

    renderSkills(
        "matchedSkills",
        result.matched_skills,
        "No matching skills detected."
    );

    renderSkills(
        "missingSkills",
        result.missing_skills,
        "No missing skills detected."
    );

    const suggestionsList = document.getElementById("suggestionsList");
    suggestionsList.replaceChildren();

    const missing = Array.isArray(result.missing_skills)
        ? result.missing_skills
        : [];

    const suggestions = [];

    if (missing.length > 0) {
        suggestions.push(
            "If you have these skills, highlight them in your resume: " +
            missing.slice(0, 5).join(", ") + "."
        );
    }

    suggestions.push(
        "Tailor your summary to the job description."
    );

    suggestions.push(
        "Include relevant projects and measurable achievements."
    );

    suggestions.push(
        "Only list skills you genuinely possess."
    );

    suggestions.forEach(function (suggestion) {
        const item = document.createElement("li");
        item.textContent = suggestion;
        suggestionsList.appendChild(item);
    });

    resultsSection.hidden = false;

    resultsSection.scrollIntoView({
        behavior: "smooth",
        block: "start"
    });
}

matchForm.addEventListener("submit", async function (event) {
    event.preventDefault();

    const file = resumeFile.files[0];
    const description = jobDescription.value.trim();

    const fileError = document.getElementById("fileError");
    const descriptionError =
        document.getElementById("descriptionError");

    fileError.textContent = "";
    descriptionError.textContent = "";

    if (!file) {
        fileError.textContent = "Please select your resume first.";
        return;
    }

    if (description.length < 30) {
        descriptionError.textContent =
            "Please enter a job description of at least 30 characters.";
        return;
    }

    if (file.size === 0 || file.size > MAX_FILE_SIZE) {
        fileError.textContent =
            "Your resume must be smaller than 5 MB.";
        return;
    }

    const formData = new FormData();

    // IMPORTANT: Backend main.py expects the field name "file".
    formData.append("file", file);
    formData.append("job_description", description);

    matchButton.disabled = true;
    buttonText.textContent = "Analyzing your resume...";
    showStatus("Analyzing your resume. Please wait.");
    resultsSection.hidden = true;

    try {
        const response = await fetch(API_URL + "/match", {
            method: "POST",
            body: formData
        });

        let data;

        try {
            data = await response.json();
        } catch {
            throw new Error(
                "The backend returned an invalid response."
            );
        }

        if (!response.ok) {
            let message = "Request failed: HTTP " + response.status;

            if (typeof data.detail === "string") {
                message = data.detail;
            } else if (Array.isArray(data.detail)) {
                message = data.detail.map(function (item) {
                    return item.loc
                        ? item.loc.join(".") + ": " + item.msg
                        : item.msg || "Invalid input";
                }).join("; ");
            }

            throw new Error(message);
        }

        console.log("API response:", data);

        displayResults(data, file.name);
        showStatus("Analysis completed successfully.", "success");

    } catch (error) {
        console.error("Matching error:", error);

        if (error instanceof TypeError) {
            showStatus(
                "Cannot connect to backend. Check that FastAPI is running on port 8000.",
                "error"
            );
        } else {
            showStatus(error.message, "error");
        }

    } finally {
        matchButton.disabled = false;
        buttonText.textContent = "Analyze My Resume";
    }
});

document.getElementById("resetButton").addEventListener(
    "click",
    function () {
        matchForm.reset();

        uploadTitle.textContent = "Choose your resume";
        uploadHint.textContent = "Click here to browse your files";
        uploadArea.classList.remove("has-file");

        charCount.textContent = "0 characters";

        document.getElementById("fileError").textContent = "";
        document.getElementById("descriptionError").textContent = "";

        resultsSection.hidden = true;
        showStatus("");

        window.scrollTo({
            top: 0,
            behavior: "smooth"
        });
    }
);
