const IS_LOCALHOST = ["localhost", "127.0.0.1"].includes(window.location.hostname);
const API_BASE_URL =
  window.RESUME_ANALYZER_API_BASE_URL || (IS_LOCALHOST ? "http://127.0.0.1:8000/api/v1" : "/api/v1");
const DEFAULT_ERROR_MESSAGE = "Unexpected error occurred.";

const resumeFileInput = document.getElementById("resumeFile");
const jobDescriptionInput = document.getElementById("jobDescription");
const analyzeBtn = document.getElementById("analyzeBtn");
const statusMessage = document.getElementById("statusMessage");

const results = document.getElementById("results");
const finalScore = document.getElementById("finalScore");
const similarityScore = document.getElementById("similarityScore");
const keywordScore = document.getElementById("keywordScore");
const matchedKeywords = document.getElementById("matchedKeywords");
const missingKeywords = document.getElementById("missingKeywords");
const suggestionsList = document.getElementById("suggestionsList");
const finalBar = document.getElementById("finalBar");
const similarityBar = document.getElementById("similarityBar");
const keywordBar = document.getElementById("keywordBar");

function setStatus(message, isError = false) {
  statusMessage.textContent = message;
  statusMessage.style.color = isError ? "#b91c1c" : "#374151";
}

function getErrorMessage(error) {
  return error instanceof Error && error.message ? error.message : DEFAULT_ERROR_MESSAGE;
}

function clampPercent(value) {
  return Math.max(0, Math.min(100, Number(value) || 0));
}

function buildKeywordChips(targetElement, keywords, type) {
  targetElement.innerHTML = "";
  if (!keywords || keywords.length === 0) {
    targetElement.textContent = "None";
    return;
  }

  keywords.forEach((keyword) => {
    const chip = document.createElement("span");
    chip.className = `chip ${type}`;
    chip.textContent = keyword;
    targetElement.appendChild(chip);
  });
}

function buildSuggestions(payload) {
  const suggestions = [];
  const final = clampPercent(payload.final_score);
  const similarity = clampPercent(payload.breakdown.similarity_score);
  const overlap = clampPercent(payload.breakdown.keyword_overlap_score);
  const missing = payload.breakdown.missing_keywords || [];

  if (final < 55) {
    suggestions.push("Your overall match is low. Rewrite the summary section to align directly with this role.");
  } else if (final < 75) {
    suggestions.push("You have a moderate match. Improve role-specific wording and measurable achievements.");
  } else {
    suggestions.push("Strong match. Keep tailoring bullet points to this exact job description before applying.");
  }

  if (similarity < 65) {
    suggestions.push("Use more wording from the job description in your experience bullets and profile summary.");
  }

  if (overlap < 60) {
    suggestions.push("Add or highlight the most important required skills and tools in your resume.");
  }

  if (missing.length > 0) {
    const topMissing = missing.slice(0, 5).join(", ");
    suggestions.push(`Consider including these missing keywords where relevant: ${topMissing}.`);
  }

  suggestions.push("Quantify achievements (impact, metrics, outcomes) to improve ranking in ATS systems.");
  return suggestions;
}

function renderResults(payload) {
  results.classList.remove("hidden");

  const final = clampPercent(payload.final_score);
  const similarity = clampPercent(payload.breakdown.similarity_score);
  const overlap = clampPercent(payload.breakdown.keyword_overlap_score);

  finalScore.textContent = `${final}%`;
  similarityScore.textContent = `${similarity}%`;
  keywordScore.textContent = `${overlap}%`;

  finalBar.style.width = `${final}%`;
  similarityBar.style.width = `${similarity}%`;
  keywordBar.style.width = `${overlap}%`;

  buildKeywordChips(matchedKeywords, payload.breakdown.matched_keywords, "match");
  buildKeywordChips(missingKeywords, payload.breakdown.missing_keywords, "missing");

  suggestionsList.innerHTML = "";
  buildSuggestions(payload).forEach((item) => {
    const li = document.createElement("li");
    li.textContent = item;
    suggestionsList.appendChild(li);
  });
}

analyzeBtn.addEventListener("click", async () => {
  const file = resumeFileInput.files[0];
  const jobDescription = jobDescriptionInput.value.trim();

  if (!file) {
    setStatus("Please upload a resume file.", true);
    return;
  }
  if (!jobDescription) {
    setStatus("Please provide a job description.", true);
    return;
  }

  const formData = new FormData();
  formData.append("file", file);
  formData.append("job_description", jobDescription);

  setStatus("Analyzing resume...");
  analyzeBtn.disabled = true;
  analyzeBtn.textContent = "Analyzing...";

  try {
    const response = await fetch(`${API_BASE_URL}/resume/score`, {
      method: "POST",
      body: formData,
    });

    if (!response.ok) {
      const errorPayload = await response.json().catch(() => ({}));
      const detail = errorPayload.detail || "Failed to analyze resume.";
      throw new Error(detail);
    }

    const payload = await response.json();
    renderResults(payload);
    setStatus("Analysis completed successfully.");
  } catch (error) {
    setStatus(getErrorMessage(error), true);
  } finally {
    analyzeBtn.disabled = false;
    analyzeBtn.textContent = "Analyze Resume";
  }
});
