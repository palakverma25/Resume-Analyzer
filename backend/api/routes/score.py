from fastapi import APIRouter, File, Form, UploadFile

from backend.schemas.resume import ScoreBreakdown, ScoreResponse
from backend.services.nlp import nlp_service
from backend.services.parser import extract_text_from_upload
from backend.services.scoring import final_score, keyword_overlap_score

router = APIRouter()


@router.post("/score", response_model=ScoreResponse)
async def score_resume(
    file: UploadFile = File(...),
    job_description: str = Form(..., min_length=1),
) -> ScoreResponse:
    resume_text = await extract_text_from_upload(file)
    normalized_resume = nlp_service.normalize_text(resume_text)
    normalized_jd = nlp_service.normalize_text(job_description)

    resume_keywords = nlp_service.extract_keywords(resume_text)
    job_keywords = nlp_service.extract_keywords(job_description)

    similarity = nlp_service.calculate_similarity(normalized_resume, normalized_jd)
    overlap, matched, missing = keyword_overlap_score(resume_keywords, job_keywords)
    score = final_score(similarity, overlap)

    return ScoreResponse(
        final_score=score,
        breakdown=ScoreBreakdown(
            similarity_score=round(similarity * 100, 2),
            keyword_overlap_score=round(overlap * 100, 2),
            matched_keywords=matched,
            missing_keywords=missing,
        ),
        resume_keywords=resume_keywords,
        job_keywords=job_keywords,
    )
