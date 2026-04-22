from fastapi.testclient import TestClient

from backend.main import app

client = TestClient(app)


def test_health_endpoint() -> None:
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_parse_resume_txt() -> None:
    resume_content = b"Python developer with FastAPI and NLP experience."
    files = {"file": ("resume.txt", resume_content, "text/plain")}

    response = client.post("/api/v1/resume/parse", files=files)

    assert response.status_code == 200
    payload = response.json()
    assert payload["filename"] == "resume.txt"
    assert "fastapi" in payload["normalized_text"]


def test_score_resume_txt() -> None:
    resume_content = b"Python FastAPI NLP machine learning API design."
    files = {"file": ("resume.txt", resume_content, "text/plain")}
    data = {
        "job_description": "Looking for Python developer with FastAPI and NLP skills.",
    }

    response = client.post("/api/v1/resume/score", files=files, data=data)

    assert response.status_code == 200
    payload = response.json()
    assert 0 <= payload["final_score"] <= 100
    assert "breakdown" in payload
