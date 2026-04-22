# AI Resume Analyzer

AI Resume Analyzer is a FastAPI-based backend with a minimal frontend dashboard that parses resumes, extracts keywords, and scores resume-job description alignment using NLP.

## Features

- FastAPI REST APIs for health, resume parsing, keyword extraction, and resume scoring
- File parsing support for PDF, DOCX, and TXT resumes
- NLP pipeline using spaCy for normalization and keyword extraction
- TF-IDF + cosine similarity scoring with keyword overlap weighting
- Minimal frontend dashboard to upload resumes and visualize score breakdown

## Project Structure

```text
backend/
  api/routes/         # Route modules
  core/               # App configuration
  schemas/            # Pydantic request/response models
  services/           # Parser, NLP, and scoring services
  main.py             # FastAPI entrypoint
frontend/
  index.html          # Dashboard UI
  app.js              # API integration
  styles.css          # Styling
tests/
  test_api.py         # API tests
requirements.txt
```

## Setup

1. Create and activate a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Download spaCy English model:

```bash
python -m spacy download en_core_web_sm
```

## Run Backend

```bash
uvicorn backend.main:app --reload
```

Backend runs at `http://127.0.0.1:8000`.

## Run Frontend

Serve the `frontend/` directory with any static file server, for example:

```bash
python -m http.server 5500 --directory frontend
```

Then open `http://127.0.0.1:5500`.

## API Endpoints

- `GET /api/v1/health`
- `POST /api/v1/resume/parse` (multipart form-data: `file`)
- `POST /api/v1/resume/keywords` (JSON: `text`, optional `top_k`)
- `POST /api/v1/resume/score` (multipart form-data: `file`, `job_description`)

## Testing

Run tests with:

```bash
pytest
```

## Scoring Logic

- Similarity score from TF-IDF cosine similarity of normalized resume and job description text
- Keyword overlap score from matched resume/job keywords
- Final score:
  - `final = (0.7 * similarity + 0.3 * keyword_overlap) * 100`

## Deploy on Vercel (Frontend + Backend)

This project is set up to run as a single Vercel deployment:
- Frontend is served from `frontend/`
- FastAPI runs as a Python serverless function from `api/index.py`
- Frontend calls `/api/v1` automatically in production

### One-time setup

1. Install the Vercel CLI:
```bash
npm i -g vercel
```
2. Log in:
```bash
vercel login
```

### Deploy

From the project root:
```bash
vercel
```

For a production deployment:
```bash
vercel --prod
```

### Post-deploy check

- Open your app URL (for example: `https://your-app.vercel.app`)
- Check backend health at: `https://your-app.vercel.app/api/v1/health`

If Vercel build/runtime limits become an issue (which can happen with heavier NLP stacks), keep frontend on Vercel and move backend to Render or Railway.
