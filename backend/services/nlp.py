from collections import Counter
import math
import re

from backend.core.config import settings


class NLPService:
    STOPWORDS = {
        "a", "an", "and", "are", "as", "at", "be", "by", "for", "from", "has", "he",
        "in", "is", "it", "its", "of", "on", "that", "the", "to", "was", "were",
        "will", "with", "or", "this", "these", "those", "you", "your", "we", "our",
        "us", "i", "me", "my", "they", "them", "their", "if", "but", "not", "can",
    }

    def normalize_text(self, text: str) -> str:
        tokens = self._tokenize(text)
        normalized_tokens = [token for token in tokens if token not in self.STOPWORDS]
        return " ".join(normalized_tokens)

    @staticmethod
    def _tokenize(text: str) -> list[str]:
        cleaned = re.sub(r"[^a-zA-Z0-9\s]", " ", text.lower())
        cleaned = re.sub(r"\s+", " ", cleaned).strip()
        tokens = cleaned.split(" ") if cleaned else []
        return [token for token in tokens if len(token) > 2]

    @staticmethod
    def _vectorize(text: str) -> Counter:
        return Counter(text.split())

    @staticmethod
    def _cosine_from_counters(counter_a: Counter, counter_b: Counter) -> float:
        if not counter_a or not counter_b:
            return 0.0

        common = set(counter_a.keys()).intersection(counter_b.keys())
        numerator = sum(counter_a[token] * counter_b[token] for token in common)

        norm_a = math.sqrt(sum(value * value for value in counter_a.values()))
        norm_b = math.sqrt(sum(value * value for value in counter_b.values()))
        if norm_a == 0 or norm_b == 0:
            return 0.0

        return numerator / (norm_a * norm_b)

    def extract_keywords(self, text: str, top_k: int | None = None) -> list[str]:
        k = top_k or settings.TOP_K_KEYWORDS
        tokens = self.normalize_text(text).split()
        counts = Counter(tokens)
        return [word for word, _ in counts.most_common(k)]

    def calculate_similarity(self, resume_text: str, job_text: str) -> float:
        if not resume_text.strip() or not job_text.strip():
            return 0.0
        normalized_resume = self.normalize_text(resume_text)
        normalized_job = self.normalize_text(job_text)
        resume_vector = self._vectorize(normalized_resume)
        job_vector = self._vectorize(normalized_job)
        score = self._cosine_from_counters(resume_vector, job_vector)
        return float(max(0.0, min(1.0, score)))


nlp_service = NLPService()
