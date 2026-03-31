import json
from typing import Any, Dict

from openai import OpenAI

from app.config import settings
from app.core.prompts import KIDNEY_ANALYSIS_SYSTEM_PROMPT


class GPTService:
    def __init__(self) -> None:
        if not settings.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is missing. Please set it in your .env file.")

        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.OPENAI_MODEL

    def analyze_with_gpt(self, prompt: str) -> Dict[str, Any]:
        response = self.client.responses.create(
            model=self.model,
            input=[
                {
                    "role": "system",
                    "content": [
                        {
                            "type": "input_text",
                            "text": KIDNEY_ANALYSIS_SYSTEM_PROMPT,
                        }
                    ],
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "input_text",
                            "text": prompt,
                        }
                    ],
                },
            ],
        )

        text_output = getattr(response, "output_text", None)
        if not text_output:
            raise ValueError("OpenAI returned an empty response.")

        return self._parse_json_result(text_output)

    def _parse_json_result(self, text_output: str) -> Dict[str, Any]:
        cleaned = text_output.strip()

        if cleaned.startswith("```json"):
            cleaned = cleaned.removeprefix("```json").strip()
        if cleaned.startswith("```"):
            cleaned = cleaned.removeprefix("```").strip()
        if cleaned.endswith("```"):
            cleaned = cleaned[:-3].strip()

        try:
            parsed = json.loads(cleaned)
        except json.JSONDecodeError as exc:
            raise ValueError(f"Model output is not valid JSON: {cleaned}") from exc

        return {
            "summary": parsed.get("summary", ""),
            "explanation": parsed.get("explanation", ""),
            "recommendations": parsed.get("recommendations", []),
            "caution": parsed.get(
                "caution",
                "This output is for informational support only and is not a diagnosis.",
            ),
        }