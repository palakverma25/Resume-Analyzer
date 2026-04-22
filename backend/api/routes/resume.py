from fastapi import APIRouter, File, UploadFile

from backend.schemas.resume import KeywordRequest, KeywordResponse, ParseResponse
from backend.services.nlp import nlp_service
from backend.services.parser import extract_text_from_upload

router = APIRouter()


@router.post("/parse", response_model=ParseResponse)
async def parse_resume(file: UploadFile = File(...)) -> ParseResponse:
    extracted_text = await extract_text_from_upload(file)
    normalized_text = nlp_service.normalize_text(extracted_text)

    return ParseResponse(
        filename=file.filename or "unknown",
        extracted_text=extracted_text,
        normalized_text=normalized_text,
        char_count=len(extracted_text),
        word_count=len(extracted_text.split()),
    )


@router.post("/keywords", response_model=KeywordResponse)
def extract_keywords(payload: KeywordRequest) -> KeywordResponse:
    keywords = nlp_service.extract_keywords(payload.text, payload.top_k)
    return KeywordResponse(keywords=keywords)
