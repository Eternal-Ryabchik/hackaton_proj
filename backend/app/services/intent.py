from typing import Dict
from .llm_client import llm_client


async def parse_intent(text: str) -> Dict[str, str]:
    # Use LLM for intent parsing
    try:
        result = await llm_client.parse_intent(text)
        return {"intent": result.get("intent", "unknown"), "text": text, "details": result}
    except Exception:
        # Fallback to simple parsing
        normalized = text.strip().lower()
        intent = "unknown"
        if "etl" in normalized or "пайплайн" in normalized:
            intent = "build_pipeline"
        elif "проанализируй" in normalized or "анализ" in normalized:
            intent = "profile_data"
        return {"intent": intent, "text": text}


