from __future__ import annotations

import json

from src.phase4.models.recommendation import LLMRecommendationItem


class LLMResponseParserError(Exception):
    pass


class LLMResponseParser:
    def parse(self, raw_text: str) -> tuple[list[LLMRecommendationItem], str | None]:
        payload = self._extract_json(raw_text)
        recommendations_raw = payload.get("recommendations", [])
        if not isinstance(recommendations_raw, list):
            raise LLMResponseParserError("'recommendations' must be a list.")
        parsed = [LLMRecommendationItem(**item) for item in recommendations_raw]
        summary = payload.get("summary")
        if summary is not None:
            summary = str(summary)
        return parsed, summary

    def _extract_json(self, raw_text: str) -> dict:
        text = raw_text.strip()
        if text.startswith("```"):
            text = text.strip("`")
            if text.startswith("json"):
                text = text[4:].strip()
        try:
            payload = json.loads(text)
        except json.JSONDecodeError as exc:
            raise LLMResponseParserError(f"Failed to parse LLM JSON output: {exc}") from exc
        if not isinstance(payload, dict):
            raise LLMResponseParserError("LLM output JSON must be an object.")
        return payload
