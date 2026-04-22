from backend.core.config import settings


def keyword_overlap_score(resume_keywords: list[str], job_keywords: list[str]) -> tuple[float, list[str], list[str]]:
    resume_set = {item.lower() for item in resume_keywords}
    job_set = {item.lower() for item in job_keywords}

    matched = sorted(list(resume_set.intersection(job_set)))
    missing = sorted(list(job_set.difference(resume_set)))

    score = 0.0
    if job_set:
        score = len(matched) / len(job_set)
    return score, matched, missing


def final_score(similarity_score: float, overlap_score: float) -> float:
    total = (
        similarity_score * settings.SIMILARITY_WEIGHT
        + overlap_score * settings.KEYWORD_WEIGHT
    )
    return round(max(0.0, min(total, 1.0)) * 100, 2)
