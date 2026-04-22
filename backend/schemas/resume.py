from pydantic import BaseModel, Field


class ParseResponse(BaseModel):
    filename: str
    extracted_text: str
    normalized_text: str
    char_count: int
    word_count: int


class KeywordRequest(BaseModel):
    text: str = Field(..., min_length=1, description="Input text for keyword extraction.")
    top_k: int = Field(default=15, ge=1, le=50)


class KeywordResponse(BaseModel):
    keywords: list[str]


class ScoreBreakdown(BaseModel):
    similarity_score: float
    keyword_overlap_score: float
    matched_keywords: list[str]
    missing_keywords: list[str]


class ScoreResponse(BaseModel):
    final_score: float
    breakdown: ScoreBreakdown
    resume_keywords: list[str]
    job_keywords: list[str]
