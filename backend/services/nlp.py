from collections import Counter
import re

import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from backend.core.config import settings


class NLPService:
    def __init__(self) -> None:
        self.nlp = self._load_spacy_model()

    @staticmethod
    def _load_spacy_model():
        try:
            return spacy.load("en_core_web_sm")
        except OSError:
            # Fallback keeps the app runnable even when model download is skipped.
            return spacy.blank("en")

    def normalize_text(self, text: str) -> str:
        cleaned = re.sub(r"\s+", " ", text).strip().lower()
        doc = self.nlp(cleaned)
        tokens: list[str] = []
        for token in doc:
            if token.is_stop or token.is_punct or token.is_space:
                continue
            lemma = token.lemma_.strip() if token.lemma_ else token.text.strip()
            if lemma:
                tokens.append(lemma.lower())
        return " ".join(tokens)

    def extract_keywords(self, text: str, top_k: int | None = None) -> list[str]:
        k = top_k or settings.TOP_K_KEYWORDS
        normalized = self.normalize_text(text)
        doc = self.nlp(normalized)

        candidates: list[str] = []
        if doc.has_annotation("DEP"):
            candidates.extend(chunk.text.lower().strip() for chunk in doc.noun_chunks)

        candidates.extend(
            token.text.lower().strip()
            for token in doc
            if token.is_alpha and len(token.text) > 2 and not token.is_stop
        )

        counts = Counter(term for term in candidates if term)
        return [word for word, _ in counts.most_common(k)]

    @staticmethod
    def calculate_similarity(resume_text: str, job_text: str) -> float:
        if not resume_text.strip() or not job_text.strip():
            return 0.0
        vectorizer = TfidfVectorizer()
        matrix = vectorizer.fit_transform([resume_text, job_text])
        score = cosine_similarity(matrix[0:1], matrix[1:2])[0][0]
        return float(score)


nlp_service = NLPService()
